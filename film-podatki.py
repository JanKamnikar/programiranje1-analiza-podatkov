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

    naslov = re.findall(r'<h2 class="movie-title">.*?<\/h2>', vsebina, re.DOTALL)
    leto = re.findall(r'<span class="release-year">.*?<\/span>', vsebina, re.DOTALL)
    reziser = re.findall(r'<span class="director">.*?<\/span>', vsebina, re.DOTALL)
    podatki = re.findall(r'<div class="details movie">.*?<\/div>', vsebina, re.DOTALL)
    ocene = re.findall(r'<ul class="ratings">.*?<\/ul>', vsebina, re.DOTALL)
    karakteristike = re.findall(r'<section class="characteristics">.*?<\/section>', vsebina, re.DOTALL)
    osnovni_podatki = re.findall(r'<section class="basic-info">.*?<\/section>', vsebina, re.DOTALL)

    raw_podatki_o_filmu = {
        'naslov': naslov[0],
        'leto': leto[0],
    }

    # Reziser 

    print(reziser[0])

    print('-'*20)
    1/0

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