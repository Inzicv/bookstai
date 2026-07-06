"""Tests for StyleMemoryAgent."""

from pathlib import Path

from bookstai.agents.style_memory import StyleMemoryAgent


def test_loads_reviews_memory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    reviews_file = memory_root / "reviews" / "reviews.md"
    reviews_file.parent.mkdir(parents=True)
    reviews_file.write_text("# Tone\nDirect and warm", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context["reviews"] == {"Tone": "Direct and warm"}


def test_loads_humor_memory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    humor_file = memory_root / "humor" / "references.md"
    humor_file.parent.mkdir(parents=True)
    humor_file.write_text("# Jokes\nPlayful and sharp", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context["humor"] == {"Jokes": "Playful and sharp"}


def test_loads_review_pitchs_memory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    pitchs_file = memory_root / "pitchs" / "output" / "pitchs.md"
    pitchs_file.parent.mkdir(parents=True)
    pitchs_file.write_text(
        "# CASTEL BOY de Eny heli\nLe pitch d'ouverture\n\n# AUTRE PITCH\nDu style",
        encoding="utf-8",
    )

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert "review_pitchs" in context
    assert context["review_pitchs"] == {
        "CASTEL BOY de Eny heli": "Le pitch d'ouverture",
        "AUTRE PITCH": "Du style",
    }


def test_loads_multiple_songs(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    songs_root = memory_root / "songs"
    songs_root.mkdir(parents=True)
    (songs_root / "alpha.md").write_text("# Song\nFirst", encoding="utf-8")
    (songs_root / "beta.md").write_text("# Song\nSecond", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context["songs"] == {
        "alpha": {"Song": "First"},
        "beta": {"Song": "Second"},
    }


def test_ignores_empty_songs_directory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    (memory_root / "songs").mkdir(parents=True)

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context == {}


def test_ignores_missing_reviews_directory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    humor_file = memory_root / "humor" / "references.md"
    humor_file.parent.mkdir(parents=True)
    humor_file.write_text("# Humor\nOnly humor", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert "reviews" not in context
    assert context["humor"] == {"Humor": "Only humor"}


def test_ignores_missing_humor_directory(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    reviews_file = memory_root / "reviews" / "reviews.md"
    reviews_file.parent.mkdir(parents=True)
    reviews_file.write_text("# Reviews\nOnly reviews", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context["reviews"] == {"Reviews": "Only reviews"}
    assert "humor" not in context


def test_ignores_missing_review_pitchs_file(tmp_path: Path) -> None:
    memory_root = tmp_path / "memory"
    reviews_file = memory_root / "reviews" / "reviews.md"
    reviews_file.parent.mkdir(parents=True)
    reviews_file.write_text("# Reviews\nOnly reviews", encoding="utf-8")

    agent = StyleMemoryAgent(memory_root=memory_root)

    context = agent.build()

    assert context["reviews"] == {"Reviews": "Only reviews"}
    assert "review_pitchs" not in context


def test_returns_empty_dict_when_no_memory_exists(tmp_path: Path) -> None:
    agent = StyleMemoryAgent(memory_root=tmp_path / "memory")

    assert agent.build() == {}
