# Discord Login — QA report (RC5.1)

## Verifiche locali effettuate

| Controllo | Esito |
|---|---|
| 51 test Node, di cui 9 nuovi sul login | PASS |
| Config assente: gioco in preview locale | PASS |
| Config valida: visitatore anonimo vede il gate e `GameEngine` non viene creato | PASS, mock |
| Config valida: sessione autenticata avvia gioco e imposta ID owner | PASS, mock |
| Client ID Discord non trattato come Bot Token | PASS, controllo codice |
| OAuth provider `discord`, scope `identify`, redirect all'URL esatto | PASS, mock |
| Redirect file:// bloccato; localhost ammesso | PASS, mock |
| Avatar con host HTTPS Discord consentito, fallback per altri URL | PASS, mock |
| Logout eseguito tramite SDK | PASS, mock |
| Errore remoto: gioco rimane chiuso e compare Riprova | PASS, mock |
| Browser smoke 5 viewport e 500 mappe | PASS, dati simulati |
| Browser R2.24 regressione UI, salvataggi locali e Raid | PASS, dati simulati |
| Asset audit 214 file | PASS |

## Non certificato / condizioni esterne

- Supabase project `tynhqehheteynviyqkaf` risulta `INACTIVE` alla lettura: il database non è raggiungibile.
- Discord provider, OAuth2 Client ID/Secret e Redirect URLs non sono configurati da questo pacchetto.
- Nessun flusso OAuth reale, refresh token, re-login su secondo dispositivo o logout remoto è stato verificato.
- Nessun schema SQL o policy RLS remota è stato applicato. Non attestata la sicurezza dei dati cloud senza test multi-account.
- Non sono state apportate modifiche a GitHub né eseguiti deploy.

**Conclusione:** codice client e gate localmente testati; attendere riattivazione progetto, configurazione OAuth autorizzata e collaudo su HTTPS prima di pubblicare come login obbligatorio.
