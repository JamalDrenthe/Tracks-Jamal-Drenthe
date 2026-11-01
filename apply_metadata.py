#!/usr/bin/env python3
"""Schrijft metadata uit metadata.yaml in de audiobestanden in tracks/.

Gebruik:
    pip install pyyaml
    python3 apply_metadata.py            # schrijft tags in tracks/

Pas waarden aan in metadata.yaml en run dit script opnieuw.
Elk veld in metadata.yaml wordt als tag geschreven; leeg veld wordt overgeslagen.
Velden: title, artist, album_artist, album, date, genre, copyright,
        comment, track, lyrics  (extra velden mag je toevoegen)
"""
import os
import subprocess
import sys
import tempfile

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(ROOT, "metadata.yaml")
TRACKS = os.path.join(ROOT, "tracks")


def main():
    with open(META, encoding="utf-8") as fh:
        meta = yaml.safe_load(fh)

    for filename, fields in meta.items():
        src = os.path.join(TRACKS, filename)
        if not os.path.exists(src):
            print(f"!! ontbreekt: {filename}")
            continue
        fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(filename)[1])
        os.close(fd)
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-i", src,
            "-map", "0:a", "-c", "copy",
            "-map_metadata", "-1", "-bitexact",
        ]
        for key, value in fields.items():
            if value:
                cmd += ["-metadata", f"{key}={value}"]
        cmd.append(tmp)
        subprocess.check_call(cmd)
        os.replace(tmp, src)
        print(f"ok {filename}")


if __name__ == "__main__":
    sys.exit(main())
