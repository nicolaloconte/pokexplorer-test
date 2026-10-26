> **Nota storica:** il documento descrive la regola precedente (massimo un Raid per dungeon). La R2.23 RC4 sostituisce quel vincolo con un tiro del 10% per ogni strumento raccolto, anche dopo altri Raid conclusi nello stesso dungeon. Vedi `docs/BATCH_BF_MATRIX.md`.

# Pokéxplorer — Backlog di micro-migliorie (25 ottobre 2026)

## Decisioni confermate

- **UI-00 COMPLETATO in R2.21 RC2.1:** togliere il pannello DEV MODE giallo dall'ala sinistra; comandi DEV ricollocati in Opzioni, stesso PIN e stesse meccaniche. Verificato su Chromium 360/390/1440 px.
- **Raid: nessun cambio autorizzato.** L'utente li ha provati e li considera funzionanti; resta il 10% su oggetti raccoglibili e massimo un Raid per dungeon.
- **Incontri selvatici:** Bulbasaur (1), Ivysaur (2), Venusaur (3), Charmander (4), Charmeleon (5), Charizard (6), Squirtle (7), Wartortle (8), Blastoise (9) già esclusi dalla funzione `randomKantoSpecies`; le evoluzioni dei Pokémon posseduti restano possibili. Le squadre avversarie non sono il generatore selvatico.
- **Nessuna altra attività approvata**, nessuna modifica al motore per i task seguenti, niente push/deploy.

## Grafica e interfaccia

| ID | Micro-attività proposta | Criterio di accettazione | Nota |
|---|---|---|---|
| G01 | Rivedere la leggibilità del testo negli HUD delle battaglie | HP, PP, tipo e nomi lunghi leggibili a 360 px | Da valutare sul gioco reale |
| G02 | Verificare il layout Zaino con liste lunghe | Scorrimento senza pulsanti/tagli fuori schermo | QA prima di modificare |
| G03 | Uniformare gli stati focus/hover/pressed | Ogni pulsante mostra uno stato riconoscibile | Miglioria grafica |
| G04 | Migliorare gli indicatori Pokémon attivo/esausto | Stato riconoscibile senza affidarsi soltanto al colore | Miglioria UX |
| G05 | Verificare selettivamente i frame del protagonista femminile | 4 direzioni e lancio coerenti, senza frammenti | Non importare sprite V8.x indiscriminatamente |
| G06 | Controllare l'inquadratura dei ritratti NPC | Nessun ritratto duplicato o tagliato in dialogo | Test cross-browser |
| G07 | Rendere omogenea la durata delle transizioni | Nessuna doppia apertura e testi leggibili | Salvaguardare gameplay |
| G08 | Rifinire i micro-movimenti degli occhi RotomDex | Nessuna oscillazione invadente e rispetto reduced-motion | Solo ritocchi minimali |
| G09 | Verificare tutte le finestre su smartphone reale | Nessun pulsante nascosto da notch/tastiera virtuale | Test dispositivi fisici |
| G10 | Aggiungere riscontro visivo quando un input è bloccato | Breve feedback al comando ignorato | Opzionale |

## Meccaniche e bilanciamento

| ID | Micro-attività proposta | Criterio di accettazione | Nota |
|---|---|---|---|
| M01 | Prova completa dell'esclusione delle 9 specie starter selvatiche | Nessuna delle 9 specie in incontri ordinari o pesca | Test di regressione, NON rimozione dalle palestre |
| M02 | Controllare la distribuzione livelli selvatici per fasce | Avversari coerenti con piano e medaglie | Bilanciamento da misurare |
| M03 | Testare Condividi Esperienza con esausti e level cap | EXP attribuita senza superare il limite | QA + eventuale fix puntuale |
| M04 | Testare permanenza del Pokémon attivo tra lotte | Lo stesso resta attivo salvo KO/sostituzione | QA + eventuale fix puntuale |
| M05 | Testare apprendimento/evoluzioni vicino al level cap | Nessun apprendimento perso o doppio | QA |
| M06 | Verificare Protezione, Magnitudo e PP | Effetti, priorità, PP e messaggi coerenti | Test unitari |
| M07 | Bilanciare incontri e ricompense del Pokémarket | Economia comprensibile durante la run | Proposta opzionale |
| M08 | Testare regali/scambi NPC con zaino pieno | Nessuna perdita o duplicazione di Pokémon/strumenti | QA |
| M09 | Testare pesca e regalo della canna | Niente doppio regalo, pool pesca separato | QA |
| M10 | Verificare cancel/conferma delle palestre | Nessuna sfida consumata per clic involontario | QA |
| M11 | Rivedere avvisi prima di consumare le ultime Poké Ball | Evitare errori senza cambiare il tasso di cattura | UX opzionale |
| M12 | Verificare il Game Over Nuzlocke e ritorno al menu | Nessuno stato della run precedente lasciato attivo | QA |
| M13 | Testare la progressione reale attraverso tutti gli 80 piani | Avventura completabile con PokéAPI reale e senza salti | Collaudo esteso, non certificato |
| M14 | Testare il finale Mewtwo/Grotta Celeste | Sequenza finale e crediti senza blocchi | Collaudo esteso |

## Architettura e qualità

| ID | Micro-attività proposta | Criterio di accettazione | Nota |
|---|---|---|---|
| T01 | Centralizzare le traduzioni IT/EN residue | 100% dei messaggi dinamici principali coperti | Traduzione attualmente parziale |
| T02 | Estrarre un sottosistema battaglia da `engine.js` | Stessi test e nessun cambio comportamento | Refactoring progressivo |
| T03 | Estrarre generazione/raggiungibilità mappe | 500 semi invariati rispetto baseline | Refactoring progressivo |
| T04 | Separare gestione degli overlay UI | Nessun listener duplicato o modale bloccato | Refactoring progressivo |
| T05 | Audit e consolidamento degli override CSS | Screenshot prima/dopo identici salvo fix concordati | CSS con override storici |
| T06 | Standardizzare test e formattazione JS | Format/lint senza cambiare la logica | Tecnico |
| T07 | Creare snapshot grafici desktop/mobile | Screenshot regressione con tolleranza definita | QA visivo |
| T08 | Aggiungere test offline/timeout per PokéAPI | Feedback comprensibile su rete assente | Attuale fallback parziale |
| T09 | Localizzare asset esterni consentiti e documentarne le licenze | Nessuna immagine rotta quando CDN fallisce | Richiede audit licenze |
| T10 | Verificare utilizzo e dimensione delle risorse audio | Nessun file superfluo e transizioni senza silenzio | 6 tracce già ricodificate |
| T11 | Aggiungere un registro di errori riproducibili | Passi, versione, browser e caso di test registrabili | Tool QA, senza cambiare DEV MODE |
| T12 | Definire uno schema per salvataggi locali | Snapshot caricabile e validato in prototipo separato | NUOVA FUNZIONE, non approvata |
| T13 | Valutare l'integrazione Supabase/Discord successiva al salvataggio locale | Nessuna sincronizzazione senza regole di conflitto | NUOVA FUNZIONE, non approvata |
| T14 | Audit legale asset, musica e marchi prima della pubblicazione | Crediti e permessi documentati | Obbligatorio prima di pubblicazione ampia |

## Workflow proposto

Ogni micro-attività va implementata soltanto se approvata, su copia separata della baseline R2.21 RC2.1; un commit logico, test mirati e confronto prima/dopo. Non accorpare grafica e gameplay non correlati. Nessun push o deploy senza autorizzazione.
