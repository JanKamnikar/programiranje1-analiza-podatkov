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
            genres_seznam.append(re.findall(reg2, genre, re.DOTALL)[0].strip())
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
    reziserji = poisci_vec(r'<h3 class="movie-director".*?<\/h3>', r'<a.*?>(.*?)<\/a>', vsebina, locilo=' / ')
    opis = re.findall(r'<div class="text">(.*?)<\/div>', vsebina, re.DOTALL)[0].strip()
    zanri = poisci_vec(r'<span class="header-movie-genres".*?<\/span>', r'<a.*?>(.*?)<\/a>', vsebina)
    drzave = poisci_vec(r'<span>.*?Countries(.*?)MPAA', r'<span.*?>(.*?)<\/span>', vsebina)
    run_time = int(re.findall(r'<span.*?Run Time -.*?(\d*?) min.*?<\/span>', vsebina, re.DOTALL)[0].strip())
    ocena_kritikov = int(re.findall(r'<div class="allmovie-rating.*?>(.*?)<\/div>', vsebina, re.DOTALL)[0].strip())
    teme = poisci_vec(r'<div class="themes.*?<div class="charactList.*?<\/div>', r'<a.*?>(.*?)<\/a>', vsebina, '|')
    oznaka = re.findall(r'<div class="mpaa">.*?<div>(.*?)<\/div>', vsebina, re.DOTALL)
    flags = poisci_vec(r'<div class="flags">.*?<div>(.*?)<\/div>', r'<span.*?>(.*?)<', vsebina, '/')
    legacy_id = re.findall(r'<div class="legacy-id">.*?<div>(.*?)<\/div>', vsebina, re.DOTALL)
    html_datoteke_igralci = './zajeti-podatki/filmi-cast/'
    vsebina_igralci = orodja.vsebina_datoteke(html_datoteke_igralci + filename)

    igralci = poisci_vec(r'<div class="description-box">.*?<\/section>', r'<a.*?tooltip.*?>(.*?)<\/a>', vsebina_igralci, 'cast_name')
    print_diagnostic(igralci)
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