# Test RC4.1

**Eseguiti offline:** 37 test Node, test browser avvio/gameplay/Raid/DEV/Batch A/Batch B–F/offline/RC4.1, snapshot visivi, audit immagini e sei MP3. I browser test usano dati Pokémon simulati e non sostituiscono la prova live.

**Risultato principale:** 37/37 Node PASS; RC4.1 4/4 viewport PASS; audit grafico 214 file senza problemi. Il menu visivo standard e l'avventura hanno baseline aggiornate solo nella copia RC4.1.

Screenshot: `docs/visual/rc41-390-info.png`, `docs/visual/rc41-1440-info.png`. Lo sprite illustrato nei test è un *segnaposto locale*, poiché le richieste esterne vengono bloccate volutamente; il gioco usa il vero sprite da PokéAPI quando disponibile.

**Richiesto per release stabile:** test manuali reali su 80 piani con API, tutti i messaggi IT/EN durante battaglia/evoluzione/NPC, misure smartphone reale, foto e scelta abilità su sprite reali. Nessuna verifica Discord/cloud.
