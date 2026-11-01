#!/usr/bin/env python3
"""Schrijft metadata uit metadata.yaml in de audiobestanden in tracks/.

Gebruik:
    pip install mutagen pyyaml
    python3 apply_metadata.py

Schrijft volledige ID3v2.4-tags: in .mp3 als ID3v2-header, in .wav als
ingesloten `id3 `-chunk (zelfde velden als mp3). Bestaande tags worden
volledig vervangen; audio zelf blijft bit-identiek. Lege velden in
metadata.yaml worden overgeslagen; elk veld dat je toevoegt wordt
als TXXX (vrij tekstveld) geschreven als het geen bekend frame is.
"""
import os
import sys

import yaml
from mutagen.id3 import (
    APIC, COMM, ID3, TALB, TBPM, TCMP, TCOM, TCON, TCOP, TDOR, TDRC, TDRL,
    TENC, TEXT, TIT1, TIT2, TIT3, TKEY, TLAN, TMED, TMOO, TOPE, TPE1, TPE2,
    TPE3, TPE4, TPOS, TPRO, TPUB, TCON as _TCON, TRCK, TSOC, TSOA, TSOP,
    TSOT, TSRC, TXXX, USLT, WOAR,
)
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

ROOT = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(ROOT, "metadata.yaml")
TRACKS = os.path.join(ROOT, "tracks")

# yaml-veldnaam -> (frameklasse, kwargs)
FRAMES = {
    "grouping":        (TIT1, {}),
    "title":           (TIT2, {}),
    "subtitle":        (TIT3, {}),
    "artist":          (TPE1, {}),
    "album_artist":    (TPE2, {}),
    "conductor":       (TPE3, {}),
    "remixer":         (TPE4, {}),
    "composer":        (TCOM, {}),
    "lyricist":        (TEXT, {}),
    "original_artist": (TOPE, {}),
    "album":           (TALB, {}),
    "track":           (TRCK, {}),
    "disc":            (TPOS, {}),
    "compilation":     (TCMP, {}),
    "date":            (TDRC, {}),
    "originaldate":    (TDOR, {}),
    "releasedate":     (TDRL, {}),
    "genre":           (TCON, {}),
    "bpm":             (TBPM, {}),
    "initialkey":      (TKEY, {}),
    "mood":            (TMOO, {}),
    "title-sort":      (TSOT, {}),
    "artist-sort":     (TSOP, {}),
    "album-sort":      (TSOA, {}),
    "composer-sort":   (TSOC, {}),
    "language":        (TLAN, {}),
    "media_type":      (TMED, {}),
    "isrc":            (TSRC, {}),
    "publisher":       (TPUB, {}),
    "copyright":       (TCOP, {}),
    "producer_rights": (TPRO, {}),
    "encoded_by":      (TENC, {}),
}


def apply(path, fields):
    ext = os.path.splitext(path)[1].lower()
    # eerst álle oude tags strippen (ID3, LIST-INFO, cover-art), audio kopieren
    import subprocess, tempfile
    fd, tmp = tempfile.mkstemp(suffix=ext)
    os.close(fd)
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-i", path,
        "-map", "0:a", "-c", "copy", "-map_metadata", "-1", "-bitexact", tmp])
    audio = MP3(tmp) if ext == ".mp3" else WAVE(tmp)
    if audio.tags is None:
        audio.add_tags()
    audio.tags.clear()

    for key, value in fields.items():
        if value in (None, ""):
            continue
        value = str(value)
        if key == "comment":
            audio.tags.add(COMM(lang="nld", desc="", text=[value]))
        elif key == "lyrics":
            audio.tags.add(USLT(lang="nld", desc="", text=value))
        elif key == "website":
            audio.tags.add(WOAR(url=value))
        elif key == "cover":
            with open(value, "rb") as img:
                audio.tags.add(APIC(mime="image/jpeg", type=3, desc="", data=img.read()))
        elif key in FRAMES:
            cls, kw = FRAMES[key]
            audio.tags.add(cls(encoding=3, text=[value], **kw))
        else:
            audio.tags.add(TXXX(encoding=3, desc=key, text=[value]))

    audio.save()
    os.replace(tmp, path)


def main():
    with open(META, encoding="utf-8") as fh:
        meta = yaml.safe_load(fh)

    for filename, fields in meta.items():
        path = os.path.join(TRACKS, filename)
        if not os.path.exists(path):
            print(f"!! ontbreekt: {filename}")
            continue
        apply(path, fields or {})
        print(f"ok {filename}")


if __name__ == "__main__":
    sys.exit(main())
