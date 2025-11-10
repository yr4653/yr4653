# Cosmic Spectrum Opera GX Mod

Cosmic Spectrum is a fully customized Opera GX theme that wraps the browser in luminous purple nebulae. The mod ships with procedurally generated art assets and a curated color palette that matches the "Cosmic Spectrum" identity.

## Features

- **Dynamic cosmic wallpapers** – static 4K image plus a looping animated GIF inspired by interstellar swirls.
- **Hand-tuned color palette** – accent, sidebar, GX Corner, and highlight colors harmonize around rich violets and pastel highlights.
- **Square logo** – ready for Opera GX mod listings and the GX Corner card.
- **Immersive audio profile** – procedurally generated background music and paired sound effects that carry the ethereal purple vibe.
- **Extensible config** – tweak colors quickly by editing `config/theme_tokens.json` and re-exporting the mod package.

## Getting started

1. Ensure Python 3.11+ is available.
2. Install dependencies once: `pip install pillow numpy`.
3. Rebuild art assets (required on a fresh checkout because generated files are not tracked):
   ```bash
   python scripts/generate_assets.py
   ```
4. Package the mod into a `.zip` archive:
   ```bash
   python scripts/package_mod.py
   ```
   The packaging script first regenerates the artwork and audio, then creates `dist/GX_Cosmic_Spectrum.zip`. Import it in Opera GX via **GX Control → Mods → Developer → Load unpacked**.

## Customization tips

- Update colors in `manifest.json` and `config/theme_tokens.json` to fine-tune component tints.
- Replace or edit the generated assets inside `GX_Cosmic_Spectrum/assets/` after running the generator to inject your own artwork.
- Opera GX accepts animated wallpapers as `.gif`, `.webm`, or `.mp4`. The included GIF keeps the project dependency-free, but you can drop in a higher quality video clip and update the manifest path.
- Tweak audio by replacing the files in `GX_Cosmic_Spectrum/assets/audio/`. Regenerate them with `scripts/generate_assets.py` for fresh procedural pads, or swap in your own `.wav`/`.ogg` tracks and update the manifest volume levels to taste.

## Attribution

All visuals were generated procedurally by `scripts/generate_assets.py`. Feel free to iterate on the script to align with your personal branding.
