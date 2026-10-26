# V7.7 R2.24 RC5 — 26 ottobre 2026

**Copia separata della RC4.1. Nessun push/deploy/SQL remoto.**

- N01: X, ESC e pulsante uscita fisso nel Pokémarket; stato di movimento ripristinato.
- N02: catalogo pergamena, prezzi e icone separati, commesso conservato, spazio scroll solo sui prodotti.
- N03: Grotta Celeste / Cerulean Cave prevale su Villaggio.
- N04: ripristinato sorriso Rotom mantenendo gli occhi animati.
- N05: maggiore altezza zaino lato destro, con scrolling solo dell'inventario.
- N06: controlli movimento dell'ala destra nascosti su desktop e D-pad sovrapposto limitato a piccoli schermi.
- N07: ridotta la scala di alcuni sprite su smartphone; serve confronto con sprite reali sul dispositivo.
- F01: nuovo checkpoint v2 con backup, validazione, isolamento per ID utente, ripristino istanze Pokémon e mosse; hook su starter, fine battaglia, passaggi, negozio e NPC.
- F02: modulo auth Discord con public config e salvataggio cloud a revisione ottimistica; **non collaudato con account o database reale**.
- F03: Continue e statistiche da checkpoint locale; versione cloud dipende da F02.
- F04/F05: catalogo del Pokémarket bilingue e alcuni stati nuovi tradotti; rimangono stringhe legacy da centralizzare.
- F06/F07: CSS scoped e moduli checkpoint/auth separati; refactoring complessivo non completato.
- F08: dati non fidati di starter, squadra e inventario costruiti tramite textContent invece di HTML interpolato.
- F09: test offline ripetuti e client PokéAPI a retry/timeout già esistente mantenuto.
- F10: test strutturali su 80 piani **simulati**, non una campagna reale completa.
- F11: cinque viewport (360/390/412/768/1440), salvataggio, UI negozio, lingua/località e browser regression.
- F12: inventario delle dipendenze e dei rischi di licenza; diritti degli asset ancora da accertare.

# R2.23 RC4.1 — Revisione scheda Pokémon, posizione e traduzioni (25 ottobre 2026)

**Fonte:** copia locale della R2.23 RC4. Nessun push, deploy, credenziale o intervento a database e servizi remoti.

- **Scheda Pokémon:** nuovo layout GBA con intestazione blu notte, pedana sprite, badge per tipi, barra grafica per ognuna delle 6 statistiche, mosse con accenti per tipo e descrizioni espandibili. Ridotta l'altezza del pannello per mostrare tutte e quattro le mosse nel layout desktop testato; fallback immagine locale. I valori delle statistiche, abilità, IV/EV, PP e natura non cambiano.
- **Posizione:** testo località rimosso dal frontale Rotom; occhi e animazioni conservati, senza ripristinare il sorriso. Nuovo riquadro POSIZIONE / LOCATION nell'ala destra, sotto il profilo Allenatore. Città, villaggi e percorsi 1–80; nessun cambiamento a mappe e collisioni.
- **IT/EN:** stati dinamici prima/dopo evoluzione e pulsanti; nomi di rimedi/strumenti e messaggi di selezione/uso su Pokémon; nomi delle mosse nel selettore lotta e nelle info. Altri testi sono ancora parzialmente hardcoded: verificare `docs/RC41_FULL_AUDIT.md`.
- **Test:** mantenuti 37 test Node e gli smoke browser; aggiunto `tests/browser_rc41.py` per 360, 390, 768, 1440 px e due lingue. Aggiornati i controlli posizione nel vecchio browser test e gli snapshot intenzionalmente modificati, verificati senza errori.
- **Non cambiato:** Raid al 10% su ogni raccolta (anche più Raid nello stesso dungeon), DEV MODE, esclusione di nove specie starter dagli incontri selvatici, sistema di battaglia, progressione, mappe, salvataggi e account Discord.

**Limiti:** prova browser con dati API simulati; nessuna certificazione di partita online completa o su telefono fisico. Login Discord, 'Continua' e salvataggi cloud non funzionanti in questa build.

---

# R2.23 RC4 — Batch B–F e ripristino Raid (25 ottobre 2026)

- **Raid:** tiro indipendente del 10% per ogni strumento raccolto. Rimosso il vincolo «massimo un Raid per dungeon» su nuova richiesta; mantiene protezioni contro doppi avvii e ripresa errori API.
- **B:** pannello Oggetti chiave leggibile con due voci fisse; display Rotom dinamico (1–80), occhi preservati.
- **C:** scheda Pokémon più compatta, descrizioni mosse espandibili; mappe lasciate inalterate dopo valutazione.
- **D:** traduzione selettiva della scheda Pokémon, dei nomi di natura, tipi e abilità. L'audit generale IT/EN non è ancora completo.
- **E:** pannello Allenatore con segnaposto locale; login Discord solo concept HTML indipendente, senza account né endpoint. Salvataggi non attivi.
- **F:** quattro pulsanti menu, conferma prima di aprire l'invito Discord; Continua disabilitato e Progressi esplicita assenza del checkpoint.
- **Test:** aggiornati test Node Raid e aggiunto controllo Chromium offline Batch B–F.

**Stato:** RC di sviluppo. Vedere `docs/BATCH_BF_MATRIX.md` per risultati, limiti e attività da completare. Nessun push, deploy o DB modificato.

---

# Changelog — Pokéxplorer V7.7 R2.22 RC3.1 · Batch A (25 ottobre 2026)

**Origine immutata:** `Pokexplorer_V7.7_R2.22_RC3_Microfix_QA.zip`, SHA-256 registrato in `SOURCE_RC3_SHA256.txt`. Nuova copia di sviluppo, **non release stabile**, nessun push né deploy.

## Modifiche autorizzate: T01 + T02 soltanto

- **T01 — Squadra senza etichetta ATTIVO/LEAD:** rimosso il badge visivo generato da `data-status`/CSS pseudoelemento; mantenuto l'originale bordo dorato `.active` e il comportamento del Pokémon attivo. Stato attivo/esausto ora comunicato nell'`aria-label` dello slot senza modificare selezione, ordine o combattimenti.
- **T02 — Ala sinistra compatta:** elenco di 6 slot verticali leggermente più basso, immagini e gap adeguati; pulsante Radar Scan ridotto, con contatore visibile; Portamedaglie sempre presente. Su viewport mobili/tablet, scorre la pagina e non l'interno dell'ala; su desktop normalmente alti l'ala non richiede scroll interno. Su schermi desktop molto bassi resta scorrimento interno per garantire accessibilità ai controlli.
- Nessun intervento su HTML, pannello destro, mappe, DEV MODE, Raid, starter selvatici, lingue o login. I file modificati per l'app sono esclusivamente `style.css` e `js/engine.js`.
- Test nuovo `tests/browser_batch_a.py` verifica sette viewport, sei slot non sovrapposti, assenza dell'etichetta grafica, semantica assistiva IT/EN, Radar e Portamedaglie; sono stati aggiornati gli snapshot grafici del test visivo per i cambiamenti autorizzati e creati confronti prima/dopo in `docs/visual/`.

## Collaudo effettuato

- `npm test`: **37/37 PASS**.
- `python tests/browser_batch_a.py`: **7/7 configurazioni PASS** (360×780, 390×844, 768×900, 1024×900, 1440×900, 1440×760, 1440×650).
- `python tests/browser_smoke.py`, `browser_dev_panel.py`, `browser_raid.py`, `browser_gameplay_qa.py`, `browser_offline.py`: **PASS**.
- `python tests/browser_visual.py`: **PASS** dopo aggiornamento baseline per la modifica UI approvata.
- Le prove in browser usano simulazioni e una pagina caricata in memoria: non certificano l'intera partita online o un dispositivo mobile reale.

## Limiti accettati

- Altezza desktop molto ridotta (es. 1440×650): scorrimento di sicurezza, intenzionale.
- Confronti visuali browser con sprite fittizio e rendering offline; il confronto pixel va interpretato come collaudo del layout, non dei servizi grafici remoti.
- Nessun push, deploy o cambiamento di account/database.

---

# Changelog — Pokéxplorer V7.7 R2.22 RC3

**Base intatta:** `Pokexplorer_V7.7_R2.21_RC2.1_DevPanel_UI.zip` (SHA-256 in `UPSTREAM_ZIP_SHA256.txt`).

### Modifiche applicate a questa copia

- **G01/G02/G03/G04/G09:** leggibilità HUD e nome Pokémon, zaino scrollabile in viewport stretti, focus/pressed visibili, tag testuali ATTIVO/ESAUSTO, accorgimenti safe area mobile.
- **M11:** conferma esplicita per l'ultima Poké Ball; il tasso di cattura e la logica degli oggetti non cambiano.
- **T02/T03/T04 (parziali):** estratti i metodi autonomi su HUD/animazioni, mappe/Radar e opzioni in tre moduli; restano ampie sezioni da modularizzare.
- **T01 (parziale):** conferme Poké Ball localizzate; traduzioni dinamiche complessive non finite.
- **T09 (parziale):** fallback Pokémon aggiornato per l'immagine di battaglia fallita; asset trainer/NPC continuano a usare i loro fallback già presenti.
- **T06:** `.editorconfig`, controlli sintattici JS e verifica di ID HTML univoci.
- **T07:** quattro screenshot-golden per Chromium in memoria a 390/1440 px e test di differenza pixel (tolleranza 2%).
- **T08:** test browser per riprova starter a PokéAPI offline.
- **T10:** audit FFprobe: 6 file MP3, ~32,34 MB, tutti con utilizzo in `js/music.js`.
- **T11:** modello incident report e checklist manuale.
- **T12/T13 (solo prototipi):** snapshot allowlisted con validazione e archiviazione locale per test; client Supabase con revisione ottimistica e schema RLS di sola revisione. **NON attivi nel gioco, nessun database modificato**.
- **M01–M10, M12–M14:** ampliati i test sulle regole, senza dichiarare verificati tutti i flussi reali; consulta la matrice task.

### Test e limiti

- `npm test`: 37/37 unit test attesi (da ricontrollare alla chiusura pacchetto).
- Browser smoke/raid/DEV, gameplay locale, rete offline, snapshot visivi; 500 mappe nel test browser; audit 213 asset.
- Restano da provare: run online integrale 80 piani, gioco mobile fisico, sequenza completa Mewtwo, evoluzioni e scambi con API reale, tutte le localizzazioni.

### Regole intoccate

- DEV MODE, bonus e PIN: invariati.
- Raid al 10% sugli strumenti raccolti, massimo un Raid attivato per dungeon e 5 lotte: invariati.
- Nove specie delle famiglie starter escluse dagli incontri selvatici: invariato.
- Nessun push, deploy o attivazione Supabase/Discord.

---

# Changelog — V7.7 · R2.21 RC2.1 (25 ottobre 2026)

**Base:** R2.21 RC2 RaidFix. **Ambito:** solo interfaccia DEV MODE, senza modificare la logica di gioco. Nessun push né deploy.

- Spostato `#developer-panel` dall'ala sinistra al menu Opzioni. La cornice gialla tratteggiata non compare più.
- Conservati gli stessi tre pulsanti e ID JavaScript: `dev-radar`, `dev-capture`, `dev-skip-encounter`; sono disponibili nel menu Opzioni dopo l'attivazione DEV.
- Il menu Opzioni diventa scrollabile su schermi bassi. Nessuna modifica alla probabilità Raid (10%), al filtro specie selvatiche, al PIN o alla progressione.
- Aggiunto test browser per layout e raggiungibilità dei comandi DEV.
- Tutte le ulteriori proposte sono registrate in `docs/BACKLOG_MICROFIX.md` ma NON implementate.

---

# Changelog — V7.7 · R2.21 RC2 (25 ottobre 2026)

**Base:** `Pokexplorer_V7.7_R2.20_RC1.zip`, SHA-256 `f7e331084c52fc533f8bfb673277e3cfbd2f3f8fd2ac51ec9da2e59b7ca03c05`. R2.20 RC1 originale conservata. **Nessun push o deploy.**

## Solo micro-fix autorizzati

| Micro-fix | Risultato | Verifica |
|---|---|---|
| **R05** | Il Raid rimane una possibilità **10% quando si raccoglie un oggetto**, ma una volta attivato non può attivarsi di nuovo nello stesso dungeon; il piano successivo azzera il vincolo. Nessun Raid garantito. | Test probabilità, doppio oggetto e reset nei 500 dungeon. |
| **R09** | Avvio idempotente, protezione dalle conferme asincrone obsolete, pulizia dei listener d'attesa al cambio run/piano. | Test avvio doppio e callback tardive. |
| **R10** | Cinque vittorie esatte; protezione del conteggio contro completamenti asincroni doppi. Resta vietata la cattura/fuga. | Test unitario per 5 vittorie, 4 passaggi e un completamento. |
| **R11** | Errore prima del primo avversario: ripristino dell'oggetto **sulla sua cella originale** e retry senza rilanciare la probabilità. Errore dopo almeno una vittoria: avanzamento conservato e interfaccia RIPROVA CARICAMENTO. | Test reti simulate assenti, retry e overlay browser. |
| **R12** | Al termine del Raid pulizia stato temporaneo; sconfitta completa della squadra interrompe il Raid e mostra game over senza nuove attivazioni dello stesso piano. | Test unitario game over/cleanup. |
| **R13** | 500 mappe con PRNG deterministico (`0x1647babe`), tutte 10×10. | `python tests/browser_raid.py`: 500/500, zero violazioni. |
| **R14** | Testati per ogni mappa: uscita raggiungibile, tutti gli item/trainer raggiungibili, da 1 a 3 item e da 1 a 4 trainer sui percorsi, niente item/trainer nelle città/villaggi. | Controlli browser con stessa sequenza PRNG. |

### Risultato controlli
- **18/18** test Node superati, 9 precedenti + 9 nuovi per il Raid.
- Smoke browser (5 viewport): superato con dati Pokémon simulati.
- **500/500** mappe deterministiche valide, zero violazioni ai criteri R13/R14.
- Browser: flusso di retry Raid, protezione da clic duplicati e stato overlay verificati.
- Asset: **213/213** file controllati, nessuna anomalia.
- Controllo sintattico JavaScript e integrità del pacchetto eseguiti prima della consegna.

### Comportamenti lasciati invariati
- Il tiro **10%** rimane associato agli oggetti raccoglibili, senza Raid garantiti e senza Raid nell'erba.
- Regola F03 sullo zaino pieno preservata.
- Nessun cambiamento alla DEV MODE (F07) o ai salvataggi (F16).
- Nessun restyling, nessuna modifica alle geometrie del dungeon 10×10 o alle tabelle Pokémon.

### Limiti residui
I test dell'intero ciclo Raid usano oggetti o risposte API **simulate**. Non è stata completata una partita online manuale con cinque battaglie reali consecutive, disconnessioni effettive su hardware o browser mobili. Consultare `docs/RAID_QA.md` prima di classificare la versione come stabile.

---

# Changelog — V7.7 · R2.20 RC1 (25 ottobre 2026)

**Base:** `pokexplorer.zip` V7.7 R2.19 TEST. Modifiche applicate a copia separata; archivio originale immutato. **Nessun push e nessun deploy.**

| ID | Stato | Modifica/verifica |
|---|---|---|
| F01 | ✅ Eseguito | Suite Node senza dipendenze esterne, browser smoke e audit asset; impronta SHA-256 della baseline. |
| F03 | ✅ Eseguito | Zaino pieno: nessuna rimozione di item, nessuna attivazione Raid per consumo oggetto; pickup verificato. |
| F04 | 🟡 Parziale | Client PokéAPI comune con retry (1), timeout (8 s), 404 senza retry, recupero dopo errore; pulsante RIPROVA starter. Offline completo non implementato. |
| F05 | 🟡 Parziale | Test su 8 medaglie, level cap, slot squadra, condizioni per il finale; 500 mappe e avvio browser simulati. **Partita reale fino a Giovanni non effettuata.** |
| F06 | ✅ Eseguito | Le famiglie degli starter non compaiono nei pool casuali selvatici; 4.500 estrazioni verificate. |
| F08 | ✅ Eseguito | ZIP con `index.html` alla root, `package.json` e CI di test senza deployment. Nessuna pubblicazione. |
| F09 | 🟡 Parziale | Placeholder Pokémon SVG locale per immagini principali, fallback NPC e allenatori già presenti conservati; font e sprite esterni ancora richiesti. Licenze da verificare. |
| F10 | 🟡 Parziale | Dati/algoritmi statici in `game-data.js`, servizi dati in `game-services.js`, client API isolato. `engine.js` conserva rendering/battaglie. |
| F11 | 🟡 Parziale | Rimosso un blocco CSS **identico**; nessun collasso indiscriminato di selettori con cascata intenzionale. |
| F12 | 🟡 Parziale | Eliminato pulsante non collegato `party-lead-action`, metodo non chiamato `setActivePartyPokemon`, scritture di `hiddenRaidPosition` mai lette. Non è un audit completo di tutte le funzioni morte. |
| F13 | 🟡 Parziale | Test mobile/desktop 5 viewport, switch IT/EN e fallback sprite; status navigazione con `aria-live`, retry IT/EN. Traduzioni complete pendenti. |
| F14 | ✅ Eseguito | README, changelog, checklist manuale, note asset, test e manifest. UI mostra versione RC1. |
| F15 | ✅ Eseguito | Cinque brani originariamente MP3 320 kbps ricodificati a 128 kbps; brano già 128 kbps conservato. Integrità decodifica verificata. |

### Test eseguiti

- **9/9** test Node superati.
- Browser Chromium simulato: **5/5** viewport senza overflow, nessuna eccezione JS osservata, starter selezionato e cambio lingua funzionante.
- **500/500** mappe senza problemi osservati di dimensione/raggiungibilità uscita/oggetti/allenatori.
- **213** asset locali verificati con 0 anomalie nell'audit del pacchetto di rilascio (conteggio prima della documentazione).
- Audio: 58.532.309 byte originari → 32.337.341 byte, **−44,8%**; controllo di decodifica FFprobe.

### Esclusi per scelta esplicita

- **F02**: nessuna conversione del Raid in casella d'erba.
- **F07**: nessuna modifica ai comandi DEV MODE / salto piano.
- **F16**: nessun sistema di salvataggio / Discord Cloud / Supabase.

Questa è una **release candidate di test**, non una release definitiva certificata. Vedi `docs/MANUAL_QA.md` per i test umani indispensabili prima di considerare la build stabile.

## R2.24 RC5.1 — Preparazione autenticazione Discord (26 ottobre 2026)
- Nessuna modifica a RAID, DEV MODE, generatore, gameplay o asset di gioco.
- Quando Supabase è configurato, il motore parte solo **dopo** la verifica della sessione Discord (non viene creato per i visitatori non autenticati).
- Aggiunti logout nell'area Opzioni e fallback per avatar Discord non autorizzati.
- Redirect OAuth vincolato a HTTPS o localhost, con pagina di ritorno precisa e niente `file://`.
- Isolato il caso di servizio OAuth non raggiungibile: accesso bloccato e comando Riprova.
- Il bootstrap senza config pubblica resta un'anteprima locale, non una falsa sessione Discord.
- Nove test Node nuovi per le condizioni di login, logout, profilo e caricamento gioco.
- Aggiunta guida `docs/DISCORD_LOGIN_SETUP.md` per app bot esistente e distinzione release/test.
- **Non eseguiti**: riattivazione Supabase, provider Discord, SQL, RLS, push Git, deploy, login con credenziali reali.
