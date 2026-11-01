# Tracks - Jamal Drenthe

Muziektracks van Jamal Drenthe, opgeschoond van externe metadata (Suno tags, encoder info, AI/copyright tags).

## Metadata beleid

Elke track bevat alleen:
- `title` = bestandsnaam (zonder extensie)
- `artist` = Jamal Drenthe

Geen comments, lyrics tags, tool/encoder tags of Suno IDs.

## Schoonmaak commando

```bash
ffmpeg -y -i input.ext -map 0:a -c copy -map_metadata -1 -bitexact \
  -metadata title="<titel>" -metadata artist="Jamal Drenthe" output.ext
```

`-map 0:a` houdt alleen audio (geen cover-art streams), `-c copy` re-encodeert niet, `-map_metadata -1 -bitexact` verwijdert alle overige tags inclusief encoder.

## Upload naar CloudiAudi.cloud

Deze bestanden zijn bedoeld om later naar CloudiAudi.cloud geüpload te worden.
