---
name: sunoclean
description: Suno/AI-tags uit audio verwijderen en vervangen door eigen metadata via een centraal metadata.yaml. Gebruik bij het opschonen van gedownloade tracks (Suno, AI-muziek, downloads) of als tags/lyrics/copyright van audiobestanden (mp3, wav) aangepast moeten worden.
---

# sunoclean

Werkflow om alle externe metadata uit audiobestanden (mp3, wav) te verwijderen
en te vervangen door eigen, volledig beheerde ID3v2.4-tags.

## Werkwijze

1. **Inventariseer** eerst wat er op elk bestand staat — nooit blind strippen:

   ```bash
   ffprobe -v quiet -show_entries format_tags -of json bestand.mp3
   ```

   Typische Suno-tags: `comment` = "made with suno; created=<datum>; id=<uuid>",
   `encoder` = "Lavf...", `title`, `artist`, `lyrics-eng`.

2. **metadata.yaml** — één bestand in de repo-root, per bestandsnaam alle
   invulbare velden. Dit is de enige bron van waarheid; de gebruiker vult
   hier zelf elke waarde. Standaardvelden:

   - titels: `grouping`, `title`, `subtitle`
   - uitvoerenden: `artist`, `album_artist`, `conductor`, `remixer`
   - auteurs: `composer`, `lyricist`, `original_artist`
   - album/set: `album`, `track`, `disc`, `compilation`
   - datums: `date`, `originaldate`, `releasedate`
   - muzikaal: `genre`, `bpm`, `initialkey`, `mood`
   - sortering: `title-sort`, `artist-sort`, `album-sort`, `composer-sort`
   - taal/medium: `language` (ISO-639-2, bijv. nld), `media_type`
   - ids/rechten: `isrc`, `publisher`, `copyright`, `producer_rights`, `encoded_by`
   - tekst/media: `comment`, `lyrics` (USLT), `website` (WOAR), `cover` (APIC)

3. **Toepassen** met `apply_metadata.py`:

   ```bash
   pip install mutagen pyyaml
   python3 apply_metadata.py
   ```

   Per bestand: eerst ffmpeg `-map 0:a -c copy -map_metadata -1 -bitexact`
   (alle oude tags inclusief encoder en cover-art weg, geen re-encode),
   daarna mutagen ID3v2.4 — bij `.mp3` als ID3v2-header, bij `.wav` als
   ingesloten `id3 `-chunk zodat wav exact dezelfde velden krijgt.
   Lege velden worden overgeslagen; onbekende extra velden worden TXXX.

## Regels

- Lyrics (`lyrics`/`lyrics-eng`) **behouden** tenzij de gebruiker anders zegt.
- Elk veld dat bestaat wordt ook gevuld — geen lege plekken, behalve velden
  die de gebruiker expliciet leeg wil.
- Verifieer na het schrijven altijd met ffprobe dat er geen vreemde tags
  over zijn en dat elk gewenst veld gevuld is.
