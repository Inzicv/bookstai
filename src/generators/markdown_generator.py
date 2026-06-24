"""Utilities for Markdown book files."""

from __future__ import annotations

import os
import re
from pathlib import Path


BOOK_TEMPLATE = """# {title}

### 1. Personnages (Nom, Prénom & Description physique)

* À compléter

---

### 2. Tropes Littéraires

* À compléter

---

### 3. Résumé du Tome

À compléter

---

### 4. Citations Clés

> À compléter

---

### 5. Timeline des Événements

```text
À compléter
```

---

### 6. Scènes Importantes

À compléter
"""


def clean_filename(title: str) -> str:
    """Sanitize a string for use as a filename."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", title)
    cleaned = cleaned.strip().replace(" ", "_")
    return cleaned if cleaned else "unknown_book"


def create_empty_book_template(title: str, output_dir: str = "memory/books") -> str:
    """Create an empty Markdown template matching the existing book format."""
    os.makedirs(output_dir, exist_ok=True)
    file_path = Path(output_dir) / f"{clean_filename(title)}.md"
    file_path.write_text(BOOK_TEMPLATE.format(title=title or "Titre à compléter"), encoding="utf-8")
    return str(file_path.resolve())
