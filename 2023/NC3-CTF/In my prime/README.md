Du bliver givet et primtal N og skal inden for 3 sekunder udføre følgende tre beregninger og svare med summen af resultaterne:

For hvert 2. primtal fra N ned til 0: Udregn summen af det mest betydende og mindst betydende ciffer. Læg resultaterne sammen.
For hvert 3. primtal fra N ned til 0: Udregn tværsummen af primtallet i base 7. Læg resultaterne sammen.
For hvert 5. primtal fra N ned til 0: Lad p1 være dette primtal og p2 det nærmeste mindre primtal. Udregn (p1 * p2) mod 31337 og tæl antallet af ulige cifre. Læg resultaterne sammen.
Eksempel:

```
Givet N = 23:

primtal = [2,  3,  5,  7, 11, 13, 17, 19, 23]

1) [23, 17, 11, 5, 2]   - Hvert 2. primtal
2) [23, 13, 5]          - Hvert 3. primtal
3) [23, 7]              - Hvert 5. primtal


1) 2+3 + 1+7 + 1+1 + 5+5 + 2+2 = 29

2) base_7(23) = 32 -> 3 + 2  =  5
   base_7(13) = 16 -> 1 + 6  =  7
   base_7(5)  =  5 -> 5      =  5
                             -----
                               17

3) 23*19 mod 31337 = 437 -> 2
     7*5 mod 31337 =  35 -> 2
                     --------
                            4

Svaret er derfor: 29 + 17 + 4 = 50


      N |   Svar
--------+-------
     23 |     50
     97 |    178
    997 |   1434
 549979 | 509053
 
```

Opgaven er tilgængelig via Haaukins:

https://ncctf.haaukins.dk