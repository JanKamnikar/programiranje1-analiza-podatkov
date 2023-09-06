import orodja
import time
import random
# Zajem podatkov
zanri = ['/genre/action-va5788',
         '/genre/comedy-drama-va5771',
         '/genre/comedy-va2681',
         '/genre/horror-va2771',
         '/genre/thriller-va5793',
         '/genre/drama-va2715',
         '/genre/science-fiction-va5777',
         '/genre/romance-va2880',
         '/genre/adventure-va5782',
         '/genre/fantasy-va2729',
         '/genre/childrens-family-d660',
         '/genre/crime-va2697',
         '/genre/western-va2955',
]
for zanr in zanri:
    for i in range(1, 12):
        spletna_stran = f'https://www.allmovie.com{zanr}/alltime-desc/{i}'
        ime_datoteke = 'zajeti-podatki/seznami-filmov/stran-' + zanr.replace('/', '-') + str(i) + '.html'
        orodja.shrani_spletno_stran(spletna_stran, ime_datoteke)
        time.sleep(1 + 4 * random.random())
