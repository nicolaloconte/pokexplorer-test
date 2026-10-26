# R2.24 RC5 — Report prove

## Automatizzate
- Node: `npm test`: 42 su 42 (37 storici, 5 nuovi test salvataggi).
- Chromium nuovo: `python tests/browser_r224.py`: 360×800, 390×844, 412×915, 768×900, 1440×900. Uscita Pokémarket, salvataggio locale e ripristino con classi vere, località della Grotta, sorriso, controlli desktop e overflow: PASS.
- Generazione 80 piani nella prova browser: 80 mappe 10×10, tutte con uscita raggiungibile: PASS, con **progressione simulata**.
- Test precedenti Chromium smoke, Raid, DEV MODE, RC4.1: PASS; offline PokéAPI: PASS.
- Audit asset: 214 file, nessuna anomalia; audit audio: sei tracce decodificabili.

## Non certificati
- Partita reale completa dal piano 1 a 80 (comprese 8 palestre, tutti i combattimenti, Grotta Celeste e Mewtwo).
- Autenticazione Discord OAuth con account reale, RLS e sincronizzazione effettiva fra dispositivi.
- Test su smartphone fisici, screen reader, zoom 200% e tutti i testi legacy inglesi.
- Licenze/diritti di pubblicazione degli asset.

**Nota:** il browser usato nei test non può aprire `file://` nell'ambiente di esecuzione. Per questo è stata caricata una pagina di prova in memoria con PokéAPI simulata e asset esterni non certificati. Non presentare le immagini di test come screenshot reali del browser dell'utente.
