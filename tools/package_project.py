"""Create a clean source archive without local state or interpreter caches."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "mountain_hiking_platform.zip"
EXCLUDED_DIRS = {".git", "venv", ".venv", "__pycache__"}
EXCLUDED_FILES = {".env", "db.sqlite3", ARCHIVE.name}

with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if not path.is_file() or path.name in EXCLUDED_FILES or path.suffix == ".pyc":
            continue
        archive.write(path, relative.as_posix())

print(f"Created {ARCHIVE} ({ARCHIVE.stat().st_size:,} bytes)")
