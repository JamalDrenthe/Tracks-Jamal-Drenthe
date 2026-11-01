# Tracks - Jamal Drenthe

Muziektracks van Jamal Drenthe. Alle externe metadata (Suno tags, Suno IDs,
encoder-info, AI/copyright tags) is verwijderd en vervangen door eigen metadata.

## Metadata aanpassen

Alle tags worden centraal beheerd in [`metadata.yaml`](metadata.yaml).
Pas een waarde aan en run daarna:

```bash
pip install mutagen pyyaml
python3 apply_metadata.py
```

Het script verwijdert eerst álle bestaande tags (ffmpeg `-map_metadata -1
-bitexact`, alleen audiostreams, geen re-encode) en schrijft daarna volledige
ID3v2.4-tags met mutagen: bij `.mp3` als ID3v2-header, bij `.wav` als
ingesloten `id3 `-chunk — dus wav krijgt exact dezelfde velden als mp3.
Lege velden worden overgeslagen; extra velden die je toevoegt worden als
vrij tekstveld (TXXX) geschreven.

### Velden per track (metadata.yaml)

| groep | velden |
|-------|--------|
| Titels | `grouping` (TIT1), `title` (TIT2), `subtitle` (TIT3) |
| Uitvoerenden | `artist` (TPE1), `album_artist` (TPE2), `conductor` (TPE3), `remixer` (TPE4) |
| Auteurs | `composer` (TCOM), `lyricist` (TEXT), `original_artist` (TOPE) |
| Album & set | `album` (TALB), `track` (TRCK), `disc` (TPOS), `compilation` (TCMP) |
| Datums | `date` (TDRC), `originaldate` (TDOR), `releasedate` (TDRL) |
| Muzikaal | `genre` (TCON), `bpm` (TBPM), `initialkey` (TKEY), `mood` (TMOO) |
| Sortering | `title-sort` (TSOT), `artist-sort` (TSOP), `album-sort` (TSOA), `composer-sort` (TSOC) |
| Taal & medium | `language` (TLAN, ISO-639-2), `media_type` (TMED) |
| IDs & rechten | `isrc` (TSRC), `publisher` (TPUB), `copyright` (TCOP), `producer_rights` (TPRO), `encoded_by` (TENC) |
| Tekst & media | `comment` (COMM), `lyrics` (USLT), `website` (WOAR), `cover` (APIC, pad naar jpg/png) |

## Upload naar CloudiAudi.cloud

Deze bestanden zijn bedoeld om later naar CloudiAudi.cloud geüpload te worden.
