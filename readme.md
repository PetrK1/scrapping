Election scrapper

Popis projektu: Projekt slouží k extrakci výsledků parlamentních voleb z roku 2017, viz odkaz:
https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Knihovny:

Jejich seznam je uveden v souboru requirements.txt
Instalace knihoven: V rámci nově vytvořeného virtuálního prostředí lze provést ve složce
File/Settings/PythonInterpreter. V nově otevřeném okně kliknout na tlačítko "+" (vlevo dole) a poté
vyhledat a nainstalovat potřebné knihovny.

Spuštění projektu scrapping.py:

Provádí se pomocí příkazového řádku a musí obsahovat 2 argumenty:
py scrapping.py <odkaz_uzemniho_celku><vysledny_soubor>
Výsledky se uloží do souboru s příponou .csv

Ukázka projektu:

Výsledky hlasování pro okres České Budějovice
1. argument: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101"
2. argument: "budejovice.csv"

Spuštění programu:
py scrapping.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" "budejovice.csv"

Průběh zpracování:
EXTRAHUJI DATA Z ODKAZU https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101

ZPRACOVAVAM

UKLADAM VYSLEDKY DO SOUBORU budejovice.csv

HOTOVO

Částečný výstup:

číslo obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana,....
535826,Adamov,682,474,472,91,0,2,37,0,36,40,4,3,13,0,1,43,0,23,126,0,0,12,0,3,1,0,36,1,-
536156,Bečice,82,63,63,3,0,0,1,0,5,3,0,1,1,0,0,8,0,5,17,0,0,10,0,0,0,0,9,0,-
