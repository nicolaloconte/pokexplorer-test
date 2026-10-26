> **Nota storica:** il documento descrive la regola precedente (massimo un Raid per dungeon). La R2.23 RC4 sostituisce quel vincolo con un tiro del 10% per ogni strumento raccolto, anche dopo altri Raid conclusi nello stesso dungeon. Vedi `docs/BATCH_BF_MATRIX.md`.

# Pokéxplorer — Checklist QA Raid R2.21 RC2

**Regola confermata dall'utente:** su un percorso non cittadino, dopo aver raccolto un oggetto ammissibile, c'è il **10% di probabilità** che quell'oggetto si trasformi in una sfida Raid. Il premio oggetto in quel caso non viene assegnato. In ogni dungeon può verificarsi **al massimo un Raid**, non necessariamente uno. In città/villaggi nessun Raid. Non esistono posizioni Raid segrete nell'erba.

## Verifiche automatizzate (eseguite)
- [x] `npm test`: 18/18 test superati, compresi 9 test Raid.
- [x] `python tests/browser_raid.py`: 500 generazioni riproducibili con seed `0x1647babe` senza anomalie.
- [x] Oggetti 1–3, allenatori 1–4 su percorsi, uscite ed entità accessibili; città/villaggi senza spawn itineranti.
- [x] Dopo primo Raid, pickup successivi non lo riattivano.
- [x] Cinque vittorie avanzano esattamente una alla volta; eventi duplicati sono ignorati.
- [x] Caricamento iniziale fallito: viene ripristinato l'oggetto corretto (non un'altra cella), senza un secondo tiro casuale.
- [x] Caricamento fallito dopo vittorie: il numero di avversari rimanenti viene conservato e la UI propone un retry.
- [x] Sconfitta dell'intera squadra: Raid disattivato e schermata game over disponibile.

## Collaudo manuale ancora indispensabile (NON eseguito)
- [ ] Giocare con PokéAPI reale: verificare fino al quinto avversario, EXP, PP, cure e danni persistenti.
- [ ] Forzare l'errore PokéAPI prima del primo avversario. Raccogliere nuovamente lo stesso oggetto: il Raid riparte senza consumare un nuovo tiro.
- [ ] Disconnettere la rete dopo la 2ª o 3ª vittoria, verificare la schermata **RIPROVA IL CARICAMENTO**, poi ricollegare: nessun premio duplicato e ripresa dal prossimo nemico.
- [ ] Provare pulsanti di cattura e fuga durante un Raid: azioni vietate, anche con connessione lenta.
- [ ] Provare input veloce/touch e pressione prolungata sulle caselle di oggetti: una sola attivazione.
- [ ] Sconfiggere tutti i Pokémon durante il Raid: game over come per le battaglie ordinarie, senza softlock.
- [ ] Passare al dungeon seguente: il flag Raid del vecchio piano non deve persistere.
- [ ] Ripetere su PC e smartphone reale, con rete instabile.

## Limiti
- I test automatici impiegano stubs API, non costituiscono una prova online completa.
- La schermata di errore in mezzo a un Raid consente di riprovare il caricamento; non introduce un nuovo pulsante per fuggire dalla sfida.
- Le azioni di debug restano quelle precedenti: **non sono oggetto di questo rilascio**.
- La probabilità del 10% è rispettata nella scelta del trigger, non è una promessa di almeno un Raid ogni dieci raccolte.
