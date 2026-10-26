# R2.22 RC3 — collaudi manuali indispensabili

I test automatizzati usano dati Pokémon simulati; **nessun playthrough online completo** è stato dichiarato superato.

- [ ] Mobile fisico: aprire zaino con ogni categoria piena, scorrere alla fine e utilizzare un oggetto; ripetere con tastiera a schermo aperta e schermo ruotato
- [ ] Battaglia a 360 px: provare nomi lunghi, 4 mosse, PP a una cifra, HP vicini allo zero, dialogo di conferma e testo inglese
- [ ] Verificare focus visibile usando solo TAB/Invio, senza cambiare modalità o generare pressioni doppie
- [ ] Selezionare allenatrice e camminare in 4 direzioni, pescare e lanciare una Poké Ball in lotta; controllare eventuali frame tagliati
- [ ] Parlare con tutti i tipi di NPC e controllare ritagli, sovrapposizioni e fallback senza connessione
- [ ] Confermare 8 palestre, 80 piani, evoluzioni e finale Mewtwo su connessione reale, senza salto piano e senza DEV MODE
- [ ] Sconfiggere una squadra intera, verificare Game Over Nuzlocke e ritorno al menu, poi avviare nuova run
- [ ] Verificare XP Share su più Pokémon, uno esausto e vicino al cap, con cambio dello starter attivo
- [ ] Verificare scambi NPC con squadra e zaino pieni, disconnessione durante scambio e rifiuto
- [ ] Verificare Pokémarket prezzi/ricompense dall'inizio al finale: test precedenti controllano soltanto atomicità dell'acquisto
- [ ] Cambiare lingua nel menu, durante la lotta e nel finale e registrare tutte le frasi che restano in italiano
- [ ] Ascoltare i passaggi da esplorazione a incontri, palestre, Grotta Celeste e Mewtwo; escludere silenzi e clipping
- [ ] Verificare che i Raid conservino il 10% sugli oggetti, massimo uno attivato per dungeon e tutti e 5 i combattimenti
- [ ] Aprire le Opzioni: DEV MODE e PIN invariati, pannello giallo assente dall'ala sinistra
- [ ] Prima di un eventuale cloud: test multiutente RLS Supabase, token scaduti, conflitti, backup e consenso esplicito; NON COLLEGATO ORA
