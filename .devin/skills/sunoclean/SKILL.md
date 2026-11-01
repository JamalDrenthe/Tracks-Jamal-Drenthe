---
name: sunoclean
description: Suno/AI-tags uit audio verwijderen en vervangen door eigen metadata via een centraal metadata.yaml (Suno/AI tags, encoder, IDs) volledig vervangen door eigen metadata via een centraal metadata.yaml. Gebruik bij het opschonen van gedownloade tracks (Suno, AI-muziek, downloads) of als tags/lyrics/copyright van audiobestanden aangepast moeten worden.
---

# Audio metadata opschonen en beheren

Werkflow om alle externe metadata uit audiobestanden (mp3, wav) te verwijderen
en te vervangen door eigen, volledig beheerde tags.

## Werkwijze

1. **Inventariseer** eerst wat er op elk bestand staat — nooit blind strippen:

   ```bash
   ffprobe -v quiet -show_entries format_tags -of json bestand.mp3
   ```

   Typische Suno-tags: `comment` = "made with suno; created=<datum>; id=<uuid>",
   `encoder` = "Lavf...", `title`, `artist`, `lyrics-eng`.

2. **metadata.yaml** — één bestand in de repo-root, per bestandsnaam alle
   invulbare velden (title, artist, album_artist, album, date, genre,
   copyright, comment, track, lyrics). Dit is de enige bron van waarheid;
   de gebruiker vult hier zelf elke waarde.

3. **Toepassen** met `apply_metadata.py` uit deze repo:

   ```bash
   pip install pyyaml
   python3 apply_metadata.py
   ```

   Per bestand draait het:
   `ffmpeg -i in -map 0:a -c copy -map_metadata -1 -bitexact -metadata k=v ... out`
   - `-map 0:a`: alleen audiostreams (geen embedded cover-art)
   - `-c copy`: audio wordt niet opnieuw geëncodeerd
   - `-map_metadata -1 -bitexact`: verwijdert álle oude tags inclusief encoder
   - lege velden in metadata.yaml worden overgeslagen (tag komt er niet in)

## Regels

- Lyrics (`lyrics`/`lyrics-eng`) **behouden** tenzij de gebruiker anders zegt.
- Werkt op zowel mp3 (ID3v2) als wav (RIFF LIST-INFO); dezelfde veldnamen
  mappen automatisch goed.
- Verifieer na het schrijven altijd met ffprobe dat er geen vreemde tags
  over zijn en dat elk gewenst veld gevuld is.
