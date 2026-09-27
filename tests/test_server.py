import pytest

from keycloak_customization_mcp import server

EXPECTED = {
    "introduction", "themes", "quick-theme", "localization",
    "avatars", "welcome-theme", "creating-your-own-console", "themes-react",
}


def test_loads_all_guides():
    assert set(server.load_guides()) == EXPECTED


def test_list_guides_mentions_every_slug():
    out = server.list_guides()
    assert all(f"`{slug}`" in out for slug in EXPECTED)


def test_get_guide_full_and_section():
    assert "keycloak-themes.json" in server.get_guide("themes")
    assert "kcLogoIdP" in server.get_guide("themes", section="Íconos")


def test_code_block_hashes_do_not_split_sections():
    headings = [s.heading for s in server.load_guides()["themes"].sections]
    assert not any(h.startswith("#") for h in headings)


def test_unknown_guide_and_section():
    with pytest.raises(ValueError):
        server.get_guide("nope")
    with pytest.raises(ValueError):
        server.get_guide("themes", section="zzz")


def test_search_ranks_relevant_section_first():
    out = server.search_docs("welcome-theme spi", limit=1)
    assert "welcome" in out.lower()
    assert "Sin resultados" in server.search_docs("qwertyuiop")
