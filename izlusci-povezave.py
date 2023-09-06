import orodja
import time
import os 
import re
import random

seznam_filmov = set()
html_datoteke = './zajeti-podatki/seznami-filmov/'
# list all files in the directory and read them
for filename in os.listdir(html_datoteke):
    vsebina = orodja.vsebina_datoteke(html_datoteke + filename)

    vzorec = r'<div class="movie .*?">.*?<\/div>'
    kartice = re.findall(vzorec, vsebina, re.DOTALL)
    for div in kartice:
        vzorec2 = r'<a class="img-link" href="(.*?)"'
        link = re.findall(vzorec2, div, re.DOTALL)
        seznam_filmov.add(link[0])

for film in seznam_filmov:
    ime_datoteke = 'zajeti-podatki/filmi/stran' + film.replace('/', '-') + '.html'
    spletna_stran = f'https://www.allmovie.com{film}'
    orodja.shrani_spletno_stran(spletna_stran, ime_datoteke)
    time.sleep(1 + 4 * random.random())