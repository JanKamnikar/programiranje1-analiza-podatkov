import orodja
import time
import os 
import re
import random
import pandas as pd

def poisci_vec(reg1, reg2, vsebina, locilo=','):
    genres = re.findall(reg1, vsebina, re.DOTALL)
    if not genres:
        return []
    genres = genres[0].split(locilo)
    genres_seznam = []
    for genre in genres:
        try:
            genres_seznam.append(re.findall(reg2, genre, re.DOTALL)[0].strip())
        except:
            pass
    return genres_seznam

def poisci_vec_drzav(reg1, reg2, vsebina, locilo=','):
    genres = re.findall(reg1, vsebina, re.DOTALL)
    if not genres:
        return []
    genres = genres[0]
    return re.findall(reg2, genres, re.DOTALL)

def print_diagnostic(msg):
    print('='*20)
    print(msg)
    print('='*20)
    1/0

mn_ljudi = set()
mn_zanrov = set()
mn_drzav = set()
mn_tem = set()
mn_oznak = set()

podatki = []


seznam_filmov = set()
html_datoteke = './zajeti-podatki/filmi/'
# list all files in the directory and read them
for i,filename in enumerate(os.listdir(html_datoteke)):
    #print(i+1, 'od', '~1017:', filename)
    try:

        vsebina = orodja.vsebina_datoteke(html_datoteke + filename)
        naslov = re.findall(r'<h2 class="movie-title">\s*(.*?)\s*<span', vsebina, re.DOTALL)
        leto = re.findall(r'<span class="release-year">\((.*?)\)<\/span>', vsebina, re.DOTALL)
        oznaka = re.findall(r'<div class="mpaa">.*?<div>(.*?)<\/div>', vsebina, re.DOTALL)
        if oznaka:
            oznaka = oznaka[0].strip()
        opis = re.findall(r'<div class="text">(.*?)<\/div>', vsebina, re.DOTALL)
        if opis:
            opis = opis[0].strip()
        run_time = re.findall(r'<span.*?Run Time -.*?(\d*?) min.*?<\/span>', vsebina, re.DOTALL)
        if run_time:
            run_time = int(run_time[0].strip())
        ocena_kritikov = re.findall(r'<div class="allmovie-rating.*?>(.*?)<\/div>', vsebina, re.DOTALL)
        if ocena_kritikov:
            ocena_kritikov = int(ocena_kritikov[0].strip())

        html_datoteke_igralci = './zajeti-podatki/filmi-cast/'
        vsebina_igralci = orodja.vsebina_datoteke(html_datoteke_igralci + filename)

        igralci = poisci_vec(r'<div class="description-box">(.*?)<\/section>', r'<div class="cast_name.*?<a.*?tooltip.*?>(.*?)<\/a>', vsebina_igralci, 'cast_container')
        reziserji = poisci_vec(r'<h3 class="movie-director"(.*?)<\/h3>', r'<a.*?>(.*?)<\/a>', vsebina, locilo=' / ')
        zanri = poisci_vec(r'<span class="header-movie-genres".*?<\/span>', r'<a.*?>(.*?)<\/a>', vsebina)
        drzave = poisci_vec_drzav(r'<span>.*?Countries(.*?)MPAA', r'<span.*?>(.*?)<\/span>', vsebina)
        if drzave:
            drzave = drzave[0].split(', ')
        teme = poisci_vec(r'<div class="themes.*?<div class="charactList.*?<\/div>', r'<a.*?>(.*?)<\/a>', vsebina, '|')
        flags = poisci_vec(r'<div class="flags">.*?<div>(.*?)<\/div>', r'<span.*?>(.*?)<', vsebina, '/')
        mn_ljudi.update(igralci)
        mn_ljudi.update(reziserji)
        mn_zanrov.update(zanri)
        mn_drzav.update(drzave)
        mn_tem.update(teme)
        mn_oznak.update(flags)

        raw_podatki_o_filmu = {
            'naslov': naslov[0],
            'leto': int(leto[0]),
            'opis': opis,
            'trajanje': run_time,
            'ocena_kritikov': ocena_kritikov,
            'oznaka': oznaka,

            'igralci': igralci,
            'reziserji': reziserji,
            'zanri': zanri,
            'drzave': drzave,
            'teme': teme,
            'oznake': flags
        }
        podatki.append(raw_podatki_o_filmu)
    except Exception as e:
        print('Napaka pri branju podatkov o filmu:', i+1)
        raise e

seznam_ljudi = list(mn_ljudi)
seznam_zanrov = list(mn_zanrov)
seznam_drzav = list(mn_drzav)
seznam_tem = list(mn_tem)
seznam_oznak = list(mn_oznak)

orodja.zapisi_json(podatki, './obdelani-podatki/filmi.json')

ljudje_filmi = []
drzave_filmi = []
teme_filmi = []
oznake_filmi = []
zanri_filmi = []

for i,podatek in enumerate(podatki):
    #print(i+1, 'od', len(podatki))
    ljudje_filmi.extend([ [i, str(seznam_ljudi.index(igralec)), 'Igralec'] for igralec in podatek['igralci']])
    ljudje_filmi.extend([[i, str(seznam_ljudi.index(reziser)), 'Reziser'] for reziser in podatek['reziserji']])
    drzave_filmi.extend([[i, drzava] for drzava in podatek['drzave']])
    teme_filmi.extend([[i, tema] for tema in podatek['teme']])
    oznake_filmi.extend([[i, zastava] for zastava in podatek['oznake']])
    zanri_filmi.extend([[i, zanr] for zanr in podatek['zanri']])

imena = ['filmi', 'ljudje_indeks', 'ljudje_filmi', 'drzave_filmi', 'teme_filmi', 'oznake_filmi', 'zanri_filmi']
column_name = [[], ['ime'], ['film','clovek', 'vloga'], ['film','drzava'], ['film','tema'], ['film','oznaka'], ['film','zanr']]
for i,seznam in enumerate([podatki, seznam_ljudi, ljudje_filmi, drzave_filmi, teme_filmi, oznake_filmi, zanri_filmi]):
    print(i+1, 'od', len(imena))
    df = pd.DataFrame(seznam)
    print(df)
    if i == 0:
        df.index.name = 'film'
        df.to_csv('./obdelani-podatki/' + imena[i] + '.csv', index=True, header=True)
    elif i == 1:
        df.index.name = 'clovek'
        df.columns = ['ime']
        df.to_csv('./obdelani-podatki/' + imena[i] + '.csv', index=True, header=True)
    else:
        df.columns = column_name[i]
        df.to_csv('./obdelani-podatki/' + imena[i] + '.csv', index=False, header=True)

