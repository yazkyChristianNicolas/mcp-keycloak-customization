"""MCP server (stdio) con la documentación de personalización de UI de Keycloak."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DOCS_DIR = Path(__file__).parent / "docs"

mcp = FastMCP("keycloak-customization")


@dataclass(frozen=True)
class Section:
    heading: str
    body: str


@dataclass(frozen=True)
class Guide:
    slug: str
    title: str
    source: str
    summary: str
    content: str
    sections: tuple[Section, ...]


def _parse_front_matter(raw: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not match:
        return {}, raw
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, match.group(2).strip()


def _split_sections(content: str) -> tuple[Section, ...]:
    """Divide por encabezados `##` (ignora los que están dentro de bloques de código)."""
    sections: list[Section] = []
    heading, lines, in_code = "(intro)", [], False
    for line in content.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            sections.append(Section(heading, "\n".join(lines).strip()))
            heading, lines = line[3:].strip(), []
        else:
            lines.append(line)
    sections.append(Section(heading, "\n".join(lines).strip()))
    return tuple(s for s in sections if s.body)


@lru_cache(maxsize=1)
def load_guides() -> dict[str, Guide]:
    guides: dict[str, Guide] = {}
    for path in sorted(DOCS_DIR.glob("*.md")):
        meta, content = _parse_front_matter(path.read_text(encoding="utf-8"))
        guides[path.stem] = Guide(
            slug=path.stem,
            title=meta.get("title", path.stem),
            source=meta.get("source", ""),
            summary=meta.get("summary", ""),
            content=content,
            sections=_split_sections(content),
        )
    return guides


def _get(slug: str) -> Guide:
    guides = load_guides()
    if slug not in guides:
        raise ValueError(f"Guía '{slug}' no existe. Disponibles: {', '.join(guides)}")
    return guides[slug]


@mcp.tool()
def list_guides() -> str:
    """Lista las guías de personalización de UI de Keycloak (slug, título, resumen y URL oficial).

    Usar primero para descubrir qué slug pasar a `get_guide`.
    """
    return "\n".join(
        f"- `{g.slug}`: {g.title} — {g.summary} ({g.source})" for g in load_guides().values()
    )


@mcp.tool()
def get_guide(slug: str, section: str | None = None) -> str:
    """Devuelve una guía completa, o solo una sección.

    Args:
        slug: identificador de la guía (ver `list_guides`), p. ej. "themes" o "localization".
        section: texto (parcial, sin distinguir mayúsculas) del encabezado `##` a devolver.
            Si se omite, devuelve la guía entera. Ver `list_sections` para los encabezados.
    """
    guide = _get(slug)
    if section is None:
        return f"# {guide.title}\nFuente: {guide.source}\n\n{guide.content}"
    needle = section.lower()
    matches = [s for s in guide.sections if needle in s.heading.lower()]
    if not matches:
        raise ValueError(
            f"Sección '{section}' no encontrada en '{slug}'. "
            f"Secciones: {', '.join(s.heading for s in guide.sections)}"
        )
    return "\n\n".join(f"## {s.heading}\n{s.body}" for s in matches)


@mcp.tool()
def list_sections(slug: str) -> str:
    """Lista los encabezados de nivel `##` de una guía, para usar con `get_guide(section=...)`."""
    guide = _get(slug)
    return "\n".join(f"- {s.heading}" for s in guide.sections)


@mcp.tool()
def search_docs(query: str, limit: int = 5) -> str:
    """Busca en todas las guías y devuelve las secciones más relevantes con su contenido.

    Args:
        query: palabras clave, p. ej. "dark mode", "kcLogoIdP", "footer.ftl", "locales".
        limit: máximo de secciones a devolver (1-20).
    """
    terms = [t for t in re.split(r"\W+", query.lower()) if t]
    if not terms:
        raise ValueError("La consulta está vacía.")
    limit = max(1, min(limit, 20))

    scored: list[tuple[int, Guide, Section]] = []
    for guide in load_guides().values():
        for section in guide.sections:
            heading = f"{guide.slug} {guide.title} {section.heading}".lower()
            body = section.body.lower()
            # Frecuencia acotada para que las secciones largas no ganen solo por tamaño.
            score = sum(min(body.count(t), 3) + 5 * (t in heading) for t in terms)
            if score:
                scored.append((score, guide, section))
    if not scored:
        return f"Sin resultados para '{query}'."

    scored.sort(key=lambda item: item[0], reverse=True)
    return "\n\n---\n\n".join(
        f"### [{g.slug}] {g.title} › {s.heading}\n\n{s.body}" for _, g, s in scored[:limit]
    )


@mcp.resource("keycloak://guides/{slug}")
def guide_resource(slug: str) -> str:
    """Contenido completo de una guía como resource."""
    return _get(slug).content


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
