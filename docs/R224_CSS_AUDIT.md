# CSS — controllo di manutenibilità

`style.css` ha accumulato molte definizioni sovrapposte e dichiarazioni `!important`. In questa revisione i cambiamenti sono isolati in fondo al file e i vecchi selettori `#pokemart-overlay>div:nth-child(2)` sono stati corretti per puntare a `.mart-shop-card`. Non è stata effettuata una riscrittura delle regole legacy: sarebbe un intervento ad alto rischio.

Restano necessari un confronto visuale completo di tutti gli overlay e una riduzione dei conflitti uno alla volta. Il fatto che un test smoke passi non prova che tutte le combinazioni di stato/layout non abbiano regressioni.
