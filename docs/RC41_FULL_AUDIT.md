# Pokéxplorer — Audit completo dei sorgenti · R2.23 RC4.1

**Data:** 25 ottobre 2026  
**Base immutata:** `Pokexplorer_V7.7_R2.23_RC4_BatchBF_Raid10.zip`  
**Ambito:** HTML, CSS, 10 file principali JS, prototipi isolati, test Node/Chromium, asset grafici e audio. Nessun codice o credenziale eseguiti su servizi remoti. Il controllo statico non equivale a certificazione di 80 piani.

## Risultato immediato

| Segnalazione | Stato | Evidenza |
| --- | --- | --- |
| Scheda Pokémon visivamente troppo simile alla precedente | **Corretto in RC4.1** | `index.html` `#pokemon-info-overlay`, `style.css` blocco `R2.23 RC4.1`, `engine.js` `openPokemonInfo()`; screenshot `docs/visual/rc41-1440-info.png` |
| Località fra gli occhi indesiderata | **Corretto in RC4.1** | `#route-location-panel` nell'ala destra; `.rotom-face` conserva soltanto occhi e glint |
| Evoluzione sempre in italiano | **Corretto in RC4.1** | `evolutionText()`, attributi `data-i18n` e aggiornamento lingua a overlay aperto |
| Alcuni rimedi/zaino e feedback in italiano con EN | **Corretto per rimedi e scelta/uso oggetti** | `renderSidebar()`, `beginItemTargetSelection()`, `giveItemToPokemon()` |
| Nomi delle mosse italiani nel selettore lotta con EN | **Corretto nella presentazione** | `displayMoveName()` usato nel selettore e nella scheda Pokémon. Il motore continua a usare gli ID delle mosse. |

## Audit delle aree e lavoro ancora aperto

| Priorità | Componente | Riscontro | Intervento raccomandato (non applicato) |
| --- | --- | --- | --- |
| P0 | Salvataggi/Login Discord | `js/prototypes/checkpoint.js` e `cloud-sync.js` non fanno parte del gioco operativo; `Continua avventura` resta disabilitato e il profilo è ospite. | Definire round-trip affidabile stato partita e recupero; poi OAuth Discord, Supabase RLS e test account multipli, prima di abilitarlo. |
| P1 | Localizzazione globale | `localize()` in `engine.js` usa dizionari parziali e regex. Dialoghi, messaggi battaglia, NPC, finale, accessibilità, testi di debug e tooltip contengono ancora stringhe fisse IT. | Catalogo IT/EN per chiavi univoche; test lingua cambiata con overlay e battaglie attive. Evitare traduzioni a sostituzione testuale euristica. |
| P1 | Localizzazione delle descrizioni | `getPokedexDescription()` ripiega sui testi inglesi quando mancano quelli italiani: alcune descrizioni in IT restano in EN. | Indicare esplicitamente lingua del fallback o gestire testo assente in IT; evitare schede miste non segnalate. |
| P1 | API esterne | Pokémon, mosse, evoluzioni e diversi sprite richiedono servizi esterni. Il retry degli starter e dei Raid è presente ma la rete può interrompere eventi più complessi. | Simulare network failure ad ogni fase di una partita completa; usare cache asset lecita e idempotenza degli eventi. |
| P1 | Motore monolitico | `js/engine.js` comprende ancora ~3.700 righe: input, UI, lotte, stati della partita. | Estrarre un singolo sottosistema alla volta, dopo test E2E; conservare contratti e API del motore. |
| P1 | CSS fragile | `style.css` contiene molte regole ripetute e oltre 1.300 `!important`, con override cronologici. | Normalizzare per componenti, media query e variabili; confronti visivi su layout desktop/mobile per ogni fase. |
| P1 | `innerHTML` con dati esterni | Alcuni nomi Pokémon/mosse (ad es. render slot e starter) vengono interpolati in HTML; non c'è una policy chiara di sanitizzazione dei dati remoti. | Costruire i nodi con `textContent` e inserire immagini via DOM, senza interpolare stringhe non controllate. |
| P1 | Verifica progressione | Test Node e Chromium simulano Pokémon; non certificano 80 piani, tutte le evoluzioni, il finale, sconfitta/raid durante errori di rete. | Eseguire un percorso reale riproducibile in browser con PokéAPI, con punti di controllo e telemetria QA. |
| P2 | Coerenza testi nel menu | L'interfaccia di login è un documento di anteprima, non un accesso reale; menu e pannello Allenatore sono incompleti rispetto al target. | Non rendere obbligatorio il login prima di avere una sessione OAuth e dati persistenti validi. |
| P2 | Asset/licenze | Sprite esterni e materiali Pokémon vanno verificati prima di una distribuzione pubblica. | Audit licenze e attribuzioni; evitare di supporre che ogni asset GitHub/PokéAPI sia liberamente redistribuibile. |
| P2 | Accessibilità e qualità visiva | Molti font pixel sono piccoli; in alcuni overlay il contenuto richiede scroll. Test visivi simulati non sostituiscono device fisici. | Test con zoom 200%, keyboard-only, VoiceOver/TalkBack, schermi bassi e touch. |
| P2 | Test visuali | Baseline screenshot ricreata per le modifiche intenzionali RC4.1; il nuovo flusso info è coperto da screenshot ma manca un confronto automatico approvato dedicato alla modale in tutte le lingue. | Integrare screenshot diff per scheda Pokémon IT/EN con 4 mosse e descrizioni estese. |

## Esiti verificati in ambiente locale

- `npm test`: **37/37 PASS**.
- `tests/browser_rc41.py`: **PASS** su 360×780, 390×844, 768×900, 1440×900; scheda Pokémon a 4 mosse, barre statistiche, località in ala destra e traduzioni di evoluzioni, mosse/strumenti IT/EN.
- `tests/browser_batch_bf.py`: **PASS** con test adattati alla nuova collocazione del riquadro posizione.
- `tests/browser_smoke.py`, `browser_gameplay_qa.py`, `browser_raid.py`, `browser_dev_panel.py`, `browser_batch_a.py`, `browser_offline.py`: **PASS** in controlli separati.
- `tests/browser_visual.py`: **PASS** con nuove baseline desktop/mobile approvate dalla modifica; screenshot menu/gioco confrontati.
- `tests/asset_audit.py`: **214** file controllati senza anomalie.
- `tests/audio_audit.py`: **PASS** su sei tracce locali (verifica tecnica; non ascolto percettivo).
- Nessun test di login Discord reale, persistenza permanente, full-run PokéAPI o smartphone fisico effettuato.

## Vincoli preservati

- Raid: tiro **10% su ogni raccolta valida**, anche dopo altri Raid nello stesso dungeon; non si avviano due Raid simultanei.
- DEV MODE e comandi invariati.
- Nove specie delle tre linee evolutive starter escluse dagli incontri selvatici ordinari.
- Nessun push Git, deploy GitHub Pages, modifica Supabase, password o token aggiunti.
