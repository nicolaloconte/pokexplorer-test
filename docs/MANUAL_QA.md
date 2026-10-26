# Collaudo manuale prima del rilascio pubblico

Spuntare i controlli dopo averli svolti **sulla release candidate reale, con rete attiva e nel browser effettivo**. I test automatizzati non sono una prova completa del gioco.

## Avvio e collegamenti
- [ ] Avviare dalla root estratta e dal server statico, in Firefox/Chrome/Edge.
- [ ] Verificare PokéAPI raggiungibile e l'errore di rete con tasto **RIPROVA**.
- [ ] Simulare assenza sprite su CDN e verificare placeholder locale.
- [ ] Verificare tutti i collegamenti, font e licenze del progetto.

## Partita completa (F05 — da certificare)
- [ ] Scelta starter 1/4/7 con dati reali e caricamento mosse.
- [ ] Visitare 80 piani **senza teleport/DEV MODE**, documentando uscita e collisioni.
- [ ] Battere i tre allenatori e il capopalestra in tutte le 8 città.
- [ ] Sbloccare in ordine tutte le 8 medaglie; verificare i cap e gli slot di squadra.
- [ ] Verificare esperienza, evoluzioni, apprendimento, PP, status, Nuzlocke e cattura.
- [ ] Testare pesca, scambi NPC, Centro Pokémon, Pokémarket, inventario pieno.
- [ ] Testare Raid su pickup (10% su oggetti, massimo uno per dungeon): vedi `docs/RAID_QA.md`.
- [ ] Completare la Grotta Celeste, Mewtwo e il finale (ove previsti dal flusso).
- [ ] Ripetere una sconfitta e ricominciare: nessuna memoria di stato residua nella run.

## Display, suono e lingua
- [ ] Mouse, tastiera, touch e pressione D-pad continua senza input bloccati.
- [ ] Screen reali: 360, 390, 768, 1024, 1440 px; controllare ogni overlay.
- [ ] Verificare tasti di scelta starter e pannelli su mobile, senza overlay fuori schermo.
- [ ] Verificare animazioni `prefers-reduced-motion`.
- [ ] Verificare ciascuno dei 6 brani audio, transizioni e qualità dopo ricodifica.
- [ ] Esaminare tutte le stringhe dinamiche in inglese (traduzione parziale nota).

## GitHub / release
- [ ] Confrontare `BASELINE_SHA256.txt` con ZIP originale e verificare `SHA256SUMS.txt`.
- [ ] Ottenere autorizzazione prima di fare push o deploy.
- [ ] Risolvere il rischio DEV MODE/piano nella distribuzione pubblica (F07 non approvato).
- [ ] Verificare provenienza e diritti degli asset prima della diffusione.
