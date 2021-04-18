import requests
import bs4
import csv
import sys



def extrahuj_tabulky(url):
# najde se celkova tabulka s obcema extrakci ze vsech tabulek na strance
    print('EXTRAHUJI DATA Z ODKAZU',url)
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    tabulky = soup.find_all('table')
    vysledek = []
    for tabulka in tabulky:
            radky = tabulka.find_all('tr')[2:]
            vysledek.extend(radky)
    return vysledek

def vrat_url(vysledek):
#vraci kompletni list URL z celkove tabulky
    vysl_seznam = []
    for radek in vysledek:

        odkaz = radek.find_all('a')
        vysl_seznam.append(odkaz)
    return vysl_seznam

def vycisti(vysl_seznam):
#vycisti kompletni list URl, pokud na konci jsou prazdne podlisty
    for polozka in vysl_seznam[::-1]:
        if polozka == [] or polozka == ['-', '-']:
            vysl_seznam.pop()
    return vysl_seznam
def separuj(vysl_seznam):
#vrati casti URL, ktere se potom pouziji v odkazu na jednotlive obce v okrese
    list_url = []
    for polozka in vysl_seznam:
        odkaz = polozka[0]
        vlozeny_odkaz = odkaz['href']
        list_url.append(vlozeny_odkaz)
    return(list_url)
def cisla_nazvy(vysledek):
#vraci nazvy obci a jejich cisel
    vysl_seznam=[]
    for radek in vysledek:
        seznam=[]
        cislo = radek.find_all('td')[0].text
        obec = radek.find_all('td')[1].text
        [seznam.append(cislo), seznam.append(obec)]
        vysl_seznam.append(seznam)
    return vysl_seznam
#odtud zacinaji funkce pro extrakci dat pro jednotlive obce

def extrahuj_tabulky1(url):
#pro danou obec vraci celkovou tabulku politickych a hlasu ze vsech tabulek na strance

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    tabulky = soup.find_all('table')
    vysledek = []
    for tabulka in tabulky[1:]:
        radky = tabulka.find_all('tr')[2:]
        vysledek.extend(radky)
    return vysledek

def vyrob_hlavicku(vysledek):
#vyrobi hlavicku pro csv soubor
    hlavicka=['číslo obce','název obce','voliči v seznamu', 'vydané obálky', 'platné hlasy']
    for radek in vysledek:
        strana=radek.find_all('td')[1]
        hlavicka.append(strana.text)
    return hlavicka
def vyrob_zaznamy(vysledek):
#vyrobeni listu poctu hlasu pro jednotlive strany v obcich
    zaznamy=[]
    for radek in vysledek:
        strana=radek.find_all('td')[2]
        zaznamy.append(strana.text)
    return zaznamy
def vyrob_list_udaju(url):

    #vyrobi list udaju pro obce z prvni tabulky(volici v seznamu, vydane obalky...)
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    tabulky = soup.find_all('table')
    tabulka1=tabulky[0]
    list_udaju=[]
    list_udaju1=[]
    for udaj in tabulka1.find_all('td'):
        list_udaju.append(udaj.text)
    list_udaju1.append(list_udaju[3])
    list_udaju1.append(list_udaju[4])
    list_udaju1.append(list_udaju[-2])
    return(list_udaju1)


def main():
    #nacitani argumentu a osetreni chyb
    try:
        url = sys.argv[1]
        jmeno_souboru=sys.argv[2]
    except IndexError:
        print('nezadal jsi url nebo vystupni soubor')
    else:
#url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5301"
#url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xnumnuts=3105"
        try:
            vysledek = extrahuj_tabulky(url)
        except requests.exceptions.MissingSchema:
               print('neplatne URL-zrejme jsi prohodil argumenty')
        except requests.exceptions.ConnectionError:
               print('neexistujici nebo neplatne URL')
        else:
            seznam_url=vrat_url(vysledek)
            vysl_seznam=vycisti(seznam_url)
            cast_url=separuj(vysl_seznam)
            cn=cisla_nazvy(vysledek)
            obce=vycisti(cn)

            #tady zacina zpracovani udaju pro jednotlive obce v ramci okresu
            vysledny_zaznam=[]
            print('ZPRACOVAVAM')
            if cast_url==[]:
                print('Zadna data ke zpracovani - chyba v URL')
                exit()
            else:
                #zpracovani URL probehlo v poradku
                for i in range(len(cast_url)):
                    ocas = cast_url[i]
                    zacatek ='https://volby.cz/pls/ps2017nss/'
                    #dojde ke spojeni pocatku URL a a casti odkazujici na jednotlive obce
                    url1 = zacatek+ocas
                    #extrakce vysledku pro jednotlivou obec
                    vysledek=extrahuj_tabulky1(url1)

                    if i==0:
                        #na zacatku se vytvori hlavicka
                        hlavicka=vyrob_hlavicku(vysledek)

                    #zaznamy hlasu pro jednotlive strany
                    zaznamy = vyrob_zaznamy(vysledek)
                    #udaje pro obce tykajici se obalek a platnych hlasu
                    udaje=vyrob_list_udaju(url1)
                    #spojeni zaznamu a udaju
                    udaje.extend(zaznamy)
                    #list se jmeny a cisly obci
                    obec=obce[i]
                    obec.extend(udaje)
                    #vytvoreni kompletniho zaznamu pro csv soubor
                    vysledny_zaznam.append(obec)



            #zapis do souboru
            f=open(jmeno_souboru,'w')
            print('UKLADAM VYSLEDKY DO SOUBORU {}'.format(jmeno_souboru))
            writer=csv.writer(f)
            writer.writerow(hlavicka)
            writer.writerows(vysledny_zaznam)
            f.close
            print("HOTOVO")

main()