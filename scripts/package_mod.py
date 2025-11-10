import shutil
import zipfile
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
MOD_DIR = ROOT / "GX_Cosmic_Spectrum"
DIST_DIR = ROOT / "dist"
EXPORT_ARCHIVE = ROOT / "GX_Cosmic_Spectrum.zip"
GENERATOR = ROOT / "scripts" / "generate_assets.py"


def collect_files(base: Path):
    for path in base.rglob("*"):
        if path.is_file():
            yield path


def package_mod() -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    archive_path = DIST_DIR / "GX_Cosmic_Spectrum.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in collect_files(MOD_DIR):
            relative = file_path.relative_to(MOD_DIR)
            zf.write(file_path, arcname=str(relative))
    return archive_path


def main() -> None:
    if not MOD_DIR.exists():
        raise SystemExit("GX_Cosmic_Spectrum directory not found")
    if GENERATOR.exists():
        subprocess.run([sys.executable, str(GENERATOR)], check=True)
    archive = package_mod()
    # Copy the archive beside the repo root so it can be shared directly.
    shutil.copy2(archive, EXPORT_ARCHIVE)
    print(f"Created {archive}")
    print(f"Exported {EXPORT_ARCHIVE}")


if __name__ == "__main__":
    main()
