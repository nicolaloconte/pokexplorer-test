> **Nota storica:** il documento descrive la regola precedente (massimo un Raid per dungeon). La R2.23 RC4 sostituisce quel vincolo con un tiro del 10% per ogni strumento raccolto, anche dopo altri Raid conclusi nello stesso dungeon. Vedi `docs/BATCH_BF_MATRIX.md`.

# Pokéxplorer R2.22 RC3 — stato verificabile dei 38 task

**Legenda:** ✅ I = modifica/test del perimetro specifico completato; 🔎 V = comportamento verificato con test, senza cambiare gameplay; ◐ P = intervento parziale / test non esaustivi. **Nessun task parziale deve essere marcato come concluso.**

| ID | Task approvato | Stato | Risultato / limite |
|---|---|---|---|
| G01 | Rivedere la leggibilità del testo negli HUD delle battaglie | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| G02 | Verificare il layout Zaino con liste lunghe | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| G03 | Uniformare gli stati focus/hover/pressed | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| G04 | Migliorare gli indicatori Pokémon attivo/esausto | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| G05 | Verificare selettivamente i frame del protagonista femminile | ◐ P | PNG 4 direzioni verificati; camminata e lancio su dispositivo reale da provare |
| G06 | Controllare l'inquadratura dei ritratti NPC | ◐ P | Fallback già presenti, proporzioni NPC da ispezionare manualmente |
| G07 | Rendere omogenea la durata delle transizioni | ◐ P | Riduzione animazioni attiva; transizioni di tutti i dialoghi non collaudate |
| G08 | Rifinire i micro-movimenti degli occhi RotomDex | ◐ P | Comportamento occhi preservato; nessun restyling invasivo |
| G09 | Verificare tutte le finestre su smartphone reale | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| G10 | Aggiungere riscontro visivo quando un input è bloccato | ◐ P | Esistono messaggi per molte azioni bloccate, non copertura universale |
| M01 | Prova completa dell'esclusione delle 9 specie starter selvatiche | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| M02 | Controllare la distribuzione livelli selvatici per fasce | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M03 | Testare Condividi Esperienza con esausti e level cap | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M04 | Testare permanenza del Pokémon attivo tra lotte | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M05 | Testare apprendimento/evoluzioni vicino al level cap | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M06 | Verificare Protezione, Magnitudo e PP | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M07 | Bilanciare incontri e ricompense del Pokémarket | ◐ P | Acquisti atomici testati; prezzi e ricompense non ribilanciati senza criteri |
| M08 | Testare regali/scambi NPC con zaino pieno | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M09 | Testare pesca e regalo della canna | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M10 | Verificare cancel/conferma delle palestre | 🔎 V | Test di regressione aggiunto; nessuna modifica delle regole originali |
| M11 | Rivedere avvisi prima di consumare le ultime Poké Ball | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| M12 | Verificare il Game Over Nuzlocke e ritorno al menu | ◐ P | Reset dal menu verificato, Game Over Nuzlocke reale non provato |
| M13 | Testare la progressione reale attraverso tutti gli 80 piani | ◐ P | Badge/floor gate simulati; 80 piani online non completati |
| M14 | Testare il finale Mewtwo/Grotta Celeste | ◐ P | Condizioni finale verificate; sequenza Mewtwo end-to-end non provata |
| T01 | Centralizzare le traduzioni IT/EN residue | ◐ P | Avviso ultima Poké Ball localizzato; molte stringhe dinamiche residue |
| T02 | Estrarre un sottosistema battaglia da `engine.js` | ◐ P | Estratti 6 helper di battaglia; turni, IA, XP rimangono nel motore |
| T03 | Estrarre generazione/raggiungibilità mappe | ◐ P | Estratti 3 helper mappa; generatore principale resta nel motore |
| T04 | Separare gestione degli overlay UI | ◐ P | Estratti 3 helper Opzioni; non tutte le finestre centralizzate |
| T05 | Audit e consolidamento degli override CSS | ◐ P | CSS append conservativo; nessuna rimozione massiva degli override |
| T06 | Standardizzare test e formattazione JS | ◐ P | node --check, .editorconfig e static audit; non ancora ESLint completo |
| T07 | Creare snapshot grafici desktop/mobile | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| T08 | Aggiungere test offline/timeout per PokéAPI | ◐ P | Retry starter offline verificato; non copre tutti i flussi di rete |
| T09 | Localizzare asset esterni consentiti e documentarne le licenze | ◐ P | Fallback Pokémon migliorato; asset remoti ancora richiesti |
| T10 | Verificare utilizzo e dimensione delle risorse audio | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| T11 | Aggiungere un registro di errori riproducibili | ✅ I | Patch UI/test mirato effettuato, vedi changelog |
| T12 | Definire uno schema per salvataggi locali | ◐ P | Prototipo isolato con validator e test; salvataggi non integrati |
| T13 | Valutare l'integrazione Supabase/Discord successiva al salvataggio locale | ◐ P | Adapter cloud testato con mock; OAuth, RLS e cloud reale non configurati |
| T14 | Audit legale asset, musica e marchi prima della pubblicazione | ◐ P | Inventario fonti; diritti di redistribuzione non verificati |

## Vincoli espliciti preservati

- **DEV MODE:** comandi, bonus e PIN rimangono identici a RC2.1; niente pannello giallo nella barra sinistra.
- **Raid:** probabilità 10% quando si raccoglie un oggetto; massimo un Raid attivato per dungeon; cinque lotte.
- **Starter:** Bulbasaur, Ivysaur, Venusaur, Charmander, Charmeleon, Charizard, Squirtle, Wartortle, Blastoise esclusi dai pool selvatici ordinari.
- Nessun push GitHub, nessun deploy, nessuna modifica al database Supabase.
- Lo ZIP originale RC2.1 è preservato.

## Test realmente eseguiti

- 37 test Node (situazione al momento della stesura); 500 mappe nell’audit browser esistente.
- Browser smoke, Raid, DEV MODE, gameplay locale, offline PokéAPI e snapshot visivi a 390/1440 px.
- 213 asset locali integri, 6 MP3 decodificabili.
- Gli screenshot di riferimento sono basati sulla RC3, non sulla versione precedente, e impiegano dati simulati.

## Da evitare

- Non trattare i prototipi T12/T13 come salvataggi utilizzabili in gioco.
- Non dichiarare completati gli 80 piani o la Grotta Celeste senza collaudo reale.
