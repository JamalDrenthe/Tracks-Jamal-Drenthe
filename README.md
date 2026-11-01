# Tracks - Jamal Drenthe

Muziektracks van Jamal Drenthe. Alle externe metadata (Suno tags, Suno IDs,
encoder-info, AI/copyright tags) is verwijderd en vervangen door eigen metadata.

## Metadata aanpassen

Alle tags worden centraal beheerd in [`metadata.yaml`](metadata.yaml).
Per track staan deze velden:

| veld | betekenis |
|------|-----------|
| title | titel van de track |
| artist | artiest |
| album_artist | album-artiest |
| album | album / release |
| date | datum (YYYY-MM-DD) |
| genre | genre |
| copyright | copyrightregel |
| comment | commentaar |
| track | tracknummer (bijv. 3/18) |
| lyrics | songtekst |

Pas een waarde aan in `metadata.yaml` en run daarna:

```bash
pip install pyyaml
python3 apply_metadata.py
```

Het script schrijft de velden in de bestanden in `tracks/` met ffmpeg
(`-map_metadata -1 -bitexact`: alle andere tags, inclusief encoder, weg;
`-c copy`: audio wordt niet opnieuw geëncodeerd). Lege velden worden
overgeslagen; nieuwe velden kun je zelf toevoegen.

## Upload naar CloudiAudi.cloud

Deze bestanden zijn bedoeld om later naar CloudiAudi.cloud geüpload te worden.
