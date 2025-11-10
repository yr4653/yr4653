import math
import os
import wave
from dataclasses import dataclass
from typing import Iterable, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "GX_Cosmic_Spectrum", "assets")
AUDIO_DIR = os.path.join(ASSET_DIR, "audio")

@dataclass
class GalaxyPalette:
    core: Tuple[int, int, int]
    mid: Tuple[int, int, int]
    outer: Tuple[int, int, int]
    star: Tuple[int, int, int]


PALETTE = GalaxyPalette(
    core=(230, 214, 255),
    mid=(170, 90, 255),
    outer=(32, 6, 66),
    star=(245, 228, 255),
)


def ensure_asset_dir() -> None:
    os.makedirs(ASSET_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)


def radial_blend(width: int, height: int, palette: GalaxyPalette, swirl: float = 0.0,
                 rotation: float = 0.0) -> Image.Image:
    cx, cy = width / 2, height / 2
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    xv, yv = np.meshgrid(x, y)
    # Convert to polar coordinates
    radius = np.sqrt(xv ** 2 + yv ** 2)
    angle = np.arctan2(yv, xv)

    # Apply swirl effect that decays with radius
    swirl_strength = swirl * np.exp(-radius * 2.5)
    angle = angle + swirl_strength + rotation

    # Blend palette based on radius and swirl angle
    t = np.clip(radius, 0, 1)[..., None]
    outer = np.array(palette.outer, dtype=np.float32)[None, None, :]
    mid = np.array(palette.mid, dtype=np.float32)[None, None, :]
    core = np.array(palette.core, dtype=np.float32)[None, None, :]

    # Interpolate between outer and mid
    mid_mix = outer * (1 - t) + mid * t
    # Boost mid tones near the spiral arms
    arm_mask = np.sin(angle * 3) * np.exp(-radius * 3)
    arm_mask = (arm_mask + 1) / 2  # normalize 0-1
    arm_enhanced = mid_mix * (0.7 + 0.6 * arm_mask[..., None])

    # Blend towards the bright core near the center
    core_weight = np.exp(-(radius ** 2) * 4)[..., None]
    rgb = arm_enhanced * (1 - core_weight) + core * core_weight

    # Clip to byte range
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    img = Image.fromarray(rgb, mode="RGB")
    return img


def add_stars(image: Image.Image, count: int = 1500, palette: GalaxyPalette = PALETTE) -> Image.Image:
    rng = np.random.default_rng(seed=42)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    for _ in range(count):
        x = rng.integers(0, width)
        y = rng.integers(0, height)
        brightness = rng.random() ** 2  # bias towards smaller stars
        radius = 1 + int(brightness * 2)
        color = tuple(int(c * (0.7 + 0.3 * brightness)) for c in palette.star)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    return image


def vignette(image: Image.Image, strength: float = 0.9) -> Image.Image:
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((-width * 0.2, -height * 0.2, width * 1.2, height * 1.2), fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(width, height) * 0.1))
    vignette_layer = Image.new("RGB", (width, height), color=PALETTE.outer)
    return Image.composite(image, vignette_layer, mask)


def create_wallpaper(width: int, height: int, rotation: float = 0.0) -> Image.Image:
    base = radial_blend(width, height, PALETTE, swirl=1.25, rotation=rotation)
    base = add_stars(base, count=int(width * height / 1600))
    base = vignette(base, strength=0.85)
    return base


def create_logo(size: int = 512) -> Image.Image:
    img = create_wallpaper(size, size, rotation=0.3)
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((size * 0.08, size * 0.08, size * 0.92, size * 0.92), outline=(255, 255, 255, 200), width=int(size * 0.02))
    draw.ellipse((size * 0.18, size * 0.24, size * 0.82, size * 0.88), outline=(255, 255, 255, 180), width=int(size * 0.018))

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = int(size * 0.14)
    font = ImageFont.truetype(font_path, font_size)
    title = "COSMIC"
    subtitle = "SPECTRUM"
    def _text_size(text: str) -> Tuple[int, int]:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    tw, th = _text_size(title)
    draw.text(((size - tw) / 2, size * 0.36), title, font=font, fill=(255, 242, 255, 255))
    sw, sh = _text_size(subtitle)
    draw.text(((size - sw) / 2, size * 0.52), subtitle, font=font, fill=(223, 200, 255, 255))

    combined = Image.alpha_composite(img.convert("RGBA"), overlay)
    return combined


def save_frames(frames: Iterable[Image.Image], path: str, duration: int = 100) -> None:
    frames = list(frames)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=duration,
        loop=0,
    )


def create_animated_wallpaper(width: int, height: int, frame_count: int = 24) -> None:
    frames = []
    for i in range(frame_count):
        rotation = (i / frame_count) * math.pi * 2
        frame = create_wallpaper(width, height, rotation=rotation * 0.08)
        frames.append(frame)
    save_frames(frames, os.path.join(ASSET_DIR, "wallpaper_animated.gif"), duration=120)


def write_wave(path: str, samples: np.ndarray, sample_rate: int = 44100) -> None:
    if samples.ndim == 1:
        samples = np.stack([samples, samples], axis=1)
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype("<i2")

    with wave.open(path, "wb") as wf:
        wf.setnchannels(pcm.shape[1])
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())


def create_ambient_pad(duration: float = 36.0, sample_rate: int = 44100) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    low = np.sin(2 * math.pi * 55 * t) * 0.28
    mid = np.sin(2 * math.pi * 110 * t + math.pi / 6) * 0.32
    shimmer_freq = 440 + 38 * np.sin(2 * math.pi * 0.05 * t)
    shimmer = np.sin(2 * math.pi * shimmer_freq * t) * 0.18
    pulse = np.sin(2 * math.pi * 0.18 * t) * 0.12

    envelope = 0.65 + 0.35 * np.sin(2 * math.pi * 0.06 * t + math.pi / 3)
    fade = np.minimum(1.0, t / 2) * np.exp(-t / (duration * 1.6))

    left = (low + mid + shimmer + pulse) * envelope * fade
    right = (low + mid + shimmer + np.sin(2 * math.pi * 0.18 * t - math.pi / 4) * 0.12) * envelope * fade
    stereo = np.stack([left, right], axis=1)
    return stereo


def create_focus_sfx(duration: float = 0.45, sample_rate: int = 44100) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freq = np.linspace(660, 1320, t.size)
    base = np.sin(2 * math.pi * freq * t)
    overtone = np.sin(2 * math.pi * freq * 2 * t) * 0.35
    envelope = np.exp(-t * 6.5) * (1 - np.exp(-t * 18))
    sparkles = np.sin(2 * math.pi * 8 * t) * 0.2
    tone = (base + overtone) * envelope + sparkles * envelope
    return tone * 0.8


def create_notification_sfx(duration: float = 0.6, sample_rate: int = 44100) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freq = 880 + 180 * np.sin(2 * math.pi * 2.2 * t)
    chime = np.sin(2 * math.pi * freq * t)
    sweep = np.sin(2 * math.pi * (freq * 1.5) * t) * 0.25
    envelope = np.exp(-t * 5) * (1 - np.exp(-t * 12))
    stereo_variation = np.sin(2 * math.pi * 0.7 * t)
    left = (chime + sweep) * envelope * (0.8 + 0.2 * stereo_variation)
    right = (chime + sweep) * envelope * (0.8 - 0.2 * stereo_variation)
    return np.stack([left, right], axis=1) * 0.9


def main() -> None:
    ensure_asset_dir()

    wallpaper = create_wallpaper(1920, 1080)
    wallpaper.save(os.path.join(ASSET_DIR, "wallpaper_4k.jpg"), quality=95)

    preview = wallpaper.resize((1920 // 4, 1080 // 4), Image.LANCZOS)
    preview.save(os.path.join(ASSET_DIR, "wallpaper_preview.jpg"), quality=95)

    square_wallpaper = create_wallpaper(1024, 1024)
    square_wallpaper.save(os.path.join(ASSET_DIR, "wallpaper_square.jpg"), quality=95)

    logo = create_logo(512)
    logo.save(os.path.join(ASSET_DIR, "logo.png"))

    create_animated_wallpaper(1280, 720)

    write_wave(
        os.path.join(AUDIO_DIR, "background_music.wav"),
        create_ambient_pad(),
    )

    write_wave(
        os.path.join(AUDIO_DIR, "sfx_focus.wav"),
        create_focus_sfx(),
    )

    write_wave(
        os.path.join(AUDIO_DIR, "sfx_notification.wav"),
        create_notification_sfx(),
    )


if __name__ == "__main__":
    main()
