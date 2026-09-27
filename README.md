# keycloak-customization-mcp

MCP server local (stdio) con la documentación de personalización de UI de Keycloak
(<https://www.keycloak.org/guides#ui-customization>, versión Nightly 26.7.4). Las guías están en
`src/keycloak_customization_mcp/docs/*.md`; agregar o editar un `.md` (con front-matter `title`, `source`,
`summary`) alcanza para que el server lo exponga.

## Tools

| Tool | Uso |
|---|---|
| `list_guides` | Slugs, títulos y resúmenes de las 8 guías |
| `get_guide(slug, section?)` | Guía completa o una sección `##` |
| `list_sections(slug)` | Encabezados de una guía |
| `search_docs(query, limit?)` | Busca en todas las guías y devuelve las secciones más relevantes |

Resource: `keycloak://guides/{slug}`.

## Uso

```bash
uv sync
uv run pytest
```

Registrar en Claude Code:

```bash
claude mcp add keycloak-customization -- uv run --directory /Users/christiannicolasyazky/Documents/projects/mcp-keycloak-customization keycloak-customization-mcp
```

Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "keycloak-customization": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/christiannicolasyazky/Documents/projects/mcp-keycloak-customization", "keycloak-customization-mcp"]
    }
  }
}
```

## Notas

- Se fija `mcp<2` porque la 2.x renombró `FastMCP` a `MCPServer`.
- El contenido se extrajo con un resumidor intermedio; verificar snippets críticos contra la fuente.
