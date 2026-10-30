# Pokéxplorer Beta

## Avvio

1. Estrai lo ZIP interamente (non eseguire i file dall'anteprima dello ZIP).
2. Apri `Pokéxplorer Beta/index.html` in un browser aggiornato.
3. In locale è disponibile la modalità **UTENTE**, senza salvataggio dei progressi. Per il login Discord occorre la pubblicazione su origine web autorizzata e la configurazione OAuth.

## Centro Pokémon — modalità classica ripristinata

Nei villaggi e nelle città, **davanti alla porta sul lato sud del Centro Pokémon**, premi **SU**: appare immediatamente il dialogo dell'infermiera Joy. Non si entra in un dungeon interno. Dopo 2 secondi Joy cura tutti i Pokémon della squadra e riproduce il motivetto `pokeheal.mp3` sovrapposto alla musica, con volume controllato dal cursore MUSICA (0% = silenzio). Il giocatore resta nello stesso villaggio/città e sulla stessa casella.

## Movimento

Corretta l'animazione verso **destra** del protagonista maschile: tre frame realmente orientati a destra, specchiati dalla normale camminata verso sinistra. La scena di lancio della Poké Ball, i frame pesca e i movimenti femminili non sono stati modificati.

## File principali

- `index.html` / `style.css`: schermata di gioco e interfaccia.
- `js/`: logiche, battaglie, salvataggi e interazioni.
- `assets/`: grafica, suoni e sprite in uso.
- `config.js`: configurazione runtime; modificare soltanto se necessario.
- `docs/`: privacy, attribuzioni e relazione tecnica dei fix.

## Test e note

Vedi `docs/RIPRISTINO_CENTRO_POKEMON.md`. Non sono stati eseguiti push, deploy o modifiche a Supabase. Le prove automatizzate non sostituiscono un test completo su dispositivo fisico e con login Discord reale.

## Nuovo: Pokédex Hybrid 1.0 (30 ottobre 2026)

Il gioco include ora il Pokédex di Kanto accessibile dal menu principale e dall'ala sinistra del RotomDex: lista 151 specie, ricerca/filtri, schede, varianti maschio/femmina/shiny **completamente segrete fino alla scoperta**, habitat e diario. I Pokémon nuovi mantengono sesso e brillantezza in squadra, battaglia, evoluzione e checkpoint v2. Le scoperte sopravvivono al Game Over e alla creazione di una nuova run.

**Per sincronizzare realmente la collezione tramite Discord occorre attivare le tabelle e RPC Supabase incluse in `sql/`.** Leggere **`docs/POKEDEX_HYBRID_INSTALLAZIONE.md`** prima di pubblicare; contiene ordine di migrazione, requisiti, limitazioni e test. Per il dettaglio delle differenze tra questa e la beta originale: `docs/POKEDEX_HYBRID_MODIFICHE.md`.

Il codice e i test locali sono inclusi; **non** sono state effettuate migrazioni del database online, test OAuth reali né deploy.
