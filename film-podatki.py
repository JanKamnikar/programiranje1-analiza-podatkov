import orodja
import time
import os 
import re
import random

def poisci_vec(reg1, reg2, vsebina, locilo=','):
    genres = re.findall(reg1, vsebina, re.DOTALL)
    genres = genres[0].split(locilo)
    genres_seznam = []
    for genre in genres:
        try:
            genres_seznam.append(re.findall(reg2, genre, re.DOTALL)[0])
        except:
            pass
    return genres_seznam

def print_diagnostic(msg):
    print('='*20)
    print(msg)
    print('='*20)
    1/0


seznam_filmov = set()
html_datoteke = './zajeti-podatki/filmi/'
# list all files in the directory and read them
for filename in os.listdir(html_datoteke):
    vsebina = orodja.vsebina_datoteke(html_datoteke + filename)
    print( filename)
    naslov = re.findall(r'<h2 class="movie-title">\s*(.*?)\s*<span', vsebina, re.DOTALL)
    leto = re.findall(r'<span class="release-year">\((.*?)\)<\/span>', vsebina, re.DOTALL)
    reziserji = poisci_vec(r'<h3 class="movie-director".*?<\/h3>', r'<a.*?>(.*?)<\/a>', vsebina, locilo='/')
    print_diagnostic(reziserji)
    reziser = re.findall(r'<h3 class="movie-director".*?<a.*?>(.*?)<\/a>', vsebina, re.DOTALL)
    details = re.findall(r'<div class="details">.*?<\/div>', vsebina, re.DOTALL)
    
    zanri = poisci_vec(r'<span class="header-movie-genres".*?<\/span>', r'<a.*?>(.*?)<\/a>', vsebina)
    drzave = poisci_vec(r'<span.*?Countries.*?(<span.*<\/span>)<span>.*?MPAA', r'<a.*?>(.*?)<\/a>', vsebina)
    run_time = re.findall(r'<span.*?Run Time -.*?(\d*?) min.*?<\/span>', vsebina, re.DOTALL)
    ocene = re.findall(r'<ul class="ratings">.*?<\/ul>', vsebina, re.DOTALL)

    karakteristike = re.findall(r'<section class="characteristics">.*?<\/section>', vsebina, re.DOTALL)
    osnovni_podatki = re.findall(r'<section class="basic-info">.*?<\/section>', vsebina, re.DOTALL)

    raw_podatki_o_filmu = {
        'naslov': naslov[0],
        'leto': leto[0],
    }

    # Reziser 

    print(reziser[0])

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