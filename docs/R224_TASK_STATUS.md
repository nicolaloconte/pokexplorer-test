# R2.24 RC5 — Registro dei 19 task

**Criterio dei risultati:** “Implementato e testato” indica soltanto il perimetro descritto; “Parziale” significa che il requisito originale non è completamente soddisfatto. Il lavoro remoto non è autorizzato.

| ID | Stato verificato | Lavoro e limiti |
|---|---|---|
| F01 | **Parziale avanzato** | Checkpoint locali v2, validazione, backup, isolamento per account, ripristino di Pokémon/mosse/mappe/inventario; niente ripresa a metà lotta e manca un end-to-end reale su tutti gli eventi. |
| F02 | **Parziale — attivazione bloccata** | OAuth Discord e client Supabase predisposti; nessuna configurazione provider, test RLS o login con un account vero. |
| F03 | **Funziona localmente; cloud parziale** | Continua e Guarda progressi mostrano dati locali salvati; sincronizzazione fra dispositivi non verificata. |
| F04 | **Parziale** | Catalogo Pokémarket IT/EN e messaggi nuovi localizzati; testi storici hardcoded possono restare. |
| F05 | **Parziale** | Logica precedente di descrizioni, ability e fallback conservata; audit linguistico totale e dati mancanti IT non risolti. |
| F06 | **Parziale** | Override nuovi confinati e selettori negozio corretti; CSS legacy mantiene centinaia di !important. |
| F07 | **Parziale** | Nuovi moduli checkpoint/auth, nessuna riscrittura rischiosa di engine.js, ancora monolitico. |
| F08 | **Parziale** | Sostituiti tre template dinamici con DOM/textContent; restano alcune interpolazioni statiche e altri punti da verificare. |
| F09 | **Verificato in test offline** | Client PokéAPI con retry/timeout e fallback esistenti; tutti gli errori della campagna reale non certificati. |
| F10 | **Simulato, non collaudato realmente** | 80 piani generati, uscite e raggiungibilità controllate; non giocata completa con PokéAPI reale. |
| F11 | **Parziale** | Chromium 360,390,412,768,1440 e screenshot; telefono fisico, screen reader e zoom 200% da provare. |
| F12 | **Inventario eseguito, licenze aperte** | Fonti e dipendenze elencate, asset localmente integri; diritti e licenze non verificati da titolari. |
| N01 | **Implementato e testato** | Uscita Pokémarket con X/ESC/pulsante, nessun blocco nei viewport di prova. |
| N02 | **Implementato e testato** | Catalogo visivamente riprogettato; screenshot desktop e mobile in docs/visual. |
| N03 | **Implementato e testato** | Luogo speciale Grotta Celeste / Cerulean Cave. |
| N04 | **Implementato e testato** | Sorriso Rotom restituito con occhi conservati. |
| N05 | **Implementato, verifica visiva** | Più altezza per l'inventario, scorrimento interno degli oggetti mantenuto. |
| N06 | **Implementato e testato** | D-pad dell'ala destra non mostrato su PC; D-pad nel viewport mobile conservato. |
| N07 | **Parziale** | Ridimensionamento di sprite su viewport mobile; una prova con sprite e dispositivi reali resta necessaria. |

## Decisioni da non aggirare
Nessuna modifica ai Raid 10% indipendenti per ogni strumento, DEV MODE o esclusione delle 9 specie starter. Non chiamare “completato” ciò che richiede credenziali e test remoti.
