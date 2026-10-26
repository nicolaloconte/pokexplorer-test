# Pokéxplorer V7.7 — R2.24 RC5 (revisione dei 19 task)

**Build di sviluppo, non release stabile.** Basata sulla R2.23 RC4.1, senza modifiche al repository né al database remoto.

## Novità verificabili
- Pokémarket: catalogo a schede pergamena, prezzi separati, X e pulsante di uscita sempre visibili, ESC su desktop.
- Grotta Celeste riconosciuta come area speciale; sorriso Rotom ripristinato; zaino ampliato e D-pad destro rimosso dal desktop.
- Correzioni responsive alla scala degli sprite, ancora da convalidare su telefono reale.
- Checkpoint locali versionati con copia precedente recuperabile e oggetti Pokémon/Mosse ricostruiti. La run è salvata su confini sicuri, non durante un combattimento.
- Menu **Continua avventura** e **Guarda progressi** collegati ai checkpoint realmente presenti.
- Client OAuth Discord e salvataggio cloud con controllo di revisione implementati ma **non configurati né verificati con un account reale**.
- Rendering sicuro per dati di starter, scheda squadra e inventario; traduzioni del Pokémarket.
- Test supplementari per checkpoint, 80 piani generati e layout mobile/desktop.

## Avvio locale
Estrarre lo ZIP per intero e aprire `index.html`. Questa modalità **locale** è una preview, funziona senza Discord e salva localmente nel browser quando lo storage persistente è disponibile. Se `file://`/modalità privacy ne impedisce l’uso, una memoria temporanea permette il gioco ma NON sopravvive a ricarica/chiusura. Per usare OAuth e cloud è necessario un hosting HTTP(S), `config.js` con soli valori pubblici e configurazione Supabase in un ambiente autorizzato (vedi `docs/R224_OAUTH_SETUP.md`).

## Test
`npm test` · `python tests/browser_r224.py` · `python tests/browser_smoke.py` · `python tests/browser_raid.py` · `python tests/browser_dev_panel.py` · `python tests/asset_audit.py` · `python tests/audio_audit.py`.
I test online e l'intera partita 1–80 con PokéAPI reale **non** sono certificati.

## Limiti e sicurezza
- DEV MODE e probabilità Raid del 10% per ogni raccolta valida non sono cambiati. Le nove specie delle tre linee starter rimangono escluse dagli incontri selvatici ordinari.
- Il client OAuth non sarà operativo senza provider Discord, allowlist redirect, schema/RLS e account di test. **Nessuna configurazione remota è stata modificata.**
- L'autorizzazione sui salvataggi cloud richiede RLS effettivamente testata nel tuo progetto. Non includere chiavi secret/service_role nel frontend.
- Il checkpoint conserva la partita nei momenti sicuri; una chiusura nel mezzo di una battaglia riprende dal checkpoint precedente, non da un turno incompleto.
- Le licenze degli asset non sono tutte documentate: non considerare chiariti i diritti di redistribuzione.

Vedi `docs/R224_TASK_STATUS.md`, `docs/R224_TEST_REPORT.md` e `CHANGELOG.md`.

---

## Cronologia storica

# Pokéxplorer — V7.7 R2.23 RC4.1 (release candidate di review)

Questa build mantiene le regole della **R2.23 RC4** e contiene un restyling *mirato* della scheda Pokémon, il ritorno della posizione nell'ala destra e traduzioni IT/EN aggiuntive. **Non** include un login Discord reale né salvataggi persistenti. Vedi `CHANGELOG.md`, `docs/RC41_FULL_AUDIT.md`, `docs/RC41_TEST_REPORT.md`.

**Avvio:** estrai tutto lo ZIP con la stessa struttura, quindi apri `index.html`. PokéAPI richiede Internet. **Test:** `npm test`, `npm run test:rc41`, `npm run test:batch-bf` e gli altri script esistenti nel `package.json`.

**Vincoli:** Raid 10% indipendente per ogni strumento raccolto, anche se altri Raid sono già partiti nello stesso dungeon; DEV MODE invariata; nove specie delle famiglie starter escluse dagli incontri selvatici ordinari; nessun push o deploy.

---

## Note sulle versioni precedenti (archivio storico)

> **R2.23 RC4.1 — Review UI e traduzioni:** redesign della scheda Pokémon, località di nuovo nel pannello destro, traduzioni mirate per evoluzioni e strumenti. **Non è una release stabile.** Consultare `docs/RC41_FULL_AUDIT.md`.

> **Versione R2.23 RC4 / Batch B–F:** modifiche parziali e fix Raid; consultare `docs/BATCH_BF_MATRIX.md` prima di distribuirla. Discord e salvataggi non sono ancora operativi.

# Pokéxplorer — V7.7 R2.22 RC3.1 · Batch A (T01/T02)

Build di sviluppo **non definitiva**, derivata senza sovrascrivere la RC3. Rimossi ATTIVO/LEAD visivi nella squadra; compattati Radar, sei slot e Portamedaglie. La meccanica del Pokémon attivo non cambia. Vedi `CHANGELOG.md` e `docs/BATCH_A_QA.md`.

Esegui `npm test` (37 test Node) e `npm run test:batch-a` (sette viewport Chromium; richiede Playwright e Chromium). Per confronti prima/dopo consulta `docs/visual/`.

DEV MODE, Raid 10% su ogni oggetto, 5 lotte Raid, esclusione delle nove specie starter e tutte le altre regole: invariati. Nessun push, deploy o integrazione di login/cloud.

---

# Pokéxplorer — V7.7 · R2.22 RC3 (release candidate, non finale)

Questa è una **copia di sviluppo incrementale** basata su R2.21 RC2.1, non una partita online completamente certificata. Per lo stato puntuale dei 38 task selezionati: **`docs/R222_TASK_MATRIX.md`**.

## Cosa cambia

- Rifiniture G01–G04/G09: HUD mobile e nomi lunghi, scorrimento zaino, focus tastiera, indicatore testuale ATTIVO/ESAUSTO nel party e safe-area smartphone.
- M11: conferma distinta quando si sta per lanciare l'ultima Poké Ball, localizzata IT/EN.
- T02/T03/T04: estratti piccoli gruppi di metodi autonomi in `js/battle-helpers.js`, `js/map-helpers.js`, `js/ui-helpers.js`. `engine.js` mantiene ancora l'orchestrazione e molte regole.
- T08/T09: test browser di rete offline e retry, fallback sprite Pokémon locale più appropriato (non più Poké Ball al posto del Pokémon).
- T07/T10/T11: snapshot visuali, audit di sei tracce audio, modello standard per bug riproducibili.
- T12/T13: **solo prototipi isolati**, in `js/prototypes/`, **non caricati dal gioco**. Nessun account Discord, DB Supabase, autenticazione o salvataggio di partita attivato.

## Avvio

Estrai lo ZIP; apri `index.html` oppure usa un server statico locale. Tutto l'HTML/CSS/JS è nella root dell'archivio. Per i Pokémon reali è richiesta PokéAPI: offline il gioco segnala errori e offre il retry per la scelta starter, non un Pokédex locale completo.

## Test eseguibili

- `npm test` — test Node **37 casi** attesi (con dati offline/mock).
- `npm run assets` — integrità risorse.
- `npm run test:audio` — MP3 e mappatura scene (richiede `ffprobe`).
- `npm run test:browser`, `npm run test:raid-browser`, `npm run test:dev-panel`, `npm run test:gameplay-browser`, `npm run test:offline` — Chromium con Playwright Python.
- `npm run test:visual` — snapshot confrontati con `tests/visual-baseline/` (Pillow e Playwright richiesti). Per approvare intenzionalmente un nuovo aspetto: `python tests/browser_visual.py --update-baseline`.

Il browser del collaudo simula dati Pokémon e in alcuni test la pagina è caricata in memoria perché un server HTTP locale è bloccato in questo ambiente. Le immagini di confronto **non dimostrano la resa completa degli asset remoti**.

## Garanzie e limiti

- DEV MODE e relativo PIN invariati; il pannello giallo rimane assente dalla barra sinistra, ma i comandi stanno nel menu Opzioni.
- Raid invariati rispetto alla RC4: **10% indipendente su ogni oggetto raccolto, anche dopo Raid precedenti dello stesso dungeon**; sequenza di cinque battaglie.
- Le **nove specie** delle famiglie evolutive dei tre starter non compaiono nei pool selvatici ordinari; evoluzioni e incontri di palestra sono sistemi distinti.
- `js/prototypes/checkpoint.js` salva **solo un sottoinsieme** dello stato, non mappe/eventi/abilitazioni; è un prototipo per QA, non per partite reali. Lo SQL di Supabase è **REVIEW ONLY** e non è stato eseguito.
- Non sono state verificate una run reale di 80 piani, tutte le animazioni femminili, tutte le traduzioni, tutte le transizioni o le licenze di redistribuzione degli asset.
- Nessun push/deploy, nessuna chiamata di modifica a servizi esterni.

Per i passi manuali: `docs/R222_MANUAL_CHECKLIST.md`. Per i problemi: `docs/QA_INCIDENT_TEMPLATE.md`. Per le attribuzioni: `docs/ATTRIBUZIONI_E_ASSET.md`.

#   p o k e x p l o r e r - t e s t  
 