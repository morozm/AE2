import matplotlib.pyplot as plt
import numpy as np
import math
import random

xmapy = 10
ymapy = 10
wielkosc_populacji = 50
liczba_generacji = 200
szansa_krzyzowania = 1
szansa_mutowania = 0.01

miasta = [[0, 0], [9, 9], [2, 1], [4, 2], [6, 2], [8, 3], [0, 9], [5, 6], [7, 6], [2, 5]]
liczba_miast = len(miasta) # wieksza rowna 2

# miasta = [[2, 2], [8, 9], [6, 6], [8, 1], [7, 3], [7, 5], [3, 4], [5, 10], [4, 7], [1, 8], [3, 0], [2, 4], [9, 7], [6, 2], [4, 9], [5, 3], [7, 8], [9, 1], [4, 5], [0, 0], [9, 8], [4, 3], [1, 7], [5, 2], [1, 8], [7, 6], [4, 5]]
# miasta = [[2, 2], [9, 8], [6, 6], [1, 8], [3, 7], [5, 7], [4, 3], [10, 5], [7, 4], [8, 1]]
# miasta = [[1, 3], [5, 5], [9, 4], [0, 0], [2, 1], [2, 4], [7, 2], [9, 1], [7, 0], [8, 4]]
# miasta = [[2, 1], [9, 7], [6, 5], [1, 7], [3, 6], [5, 6], [4, 2], [10, 4], [7, 3], [8, 10]]
# miasta = [[2, 1], [9, 7], [6, 5], [1, 7], [3, 6], [5, 6], [4, 2], [10, 4], [7, 3], [8, 10], [1, 3], [5, 5], [9, 4], [0, 0], [2, 1], [2, 4], [7, 2], [9, 1], [7, 0], [8, 4]]
# miasta = [[1, 1], [2, 1], [2, 2]]

najkrotsza_droga_calosc = [None, 0]
najdluzsza_droga_calosc = [None, math.inf]

populacja = []
przystosowanie_avg = []
przystosowanie_min = []
przystosowanie_max = []
aktualne_przystosowania = []

def generuj_populacje():
    global populacja
    for i in range (wielkosc_populacji):
        osobnik = []
        losowa_kolejnosc = random.sample(range(0, liczba_miast), liczba_miast)
        osobnik.extend(losowa_kolejnosc)
        populacja.append(osobnik)
        
def statystyki():
    global przystosowanie_avg
    global przystosowanie_min
    global przystosowanie_max
    global aktualne_przystosowania
    global najkrotsza_droga_calosc
    global najdluzsza_droga_calosc
    aktualne_przystosowania = policz_przystosowania()
    przystosowanie_min.append(min(aktualne_przystosowania))
    przystosowanie_max.append(max(aktualne_przystosowania))
    przystosowanie_avg.append(sum(aktualne_przystosowania)/wielkosc_populacji)
    if max(aktualne_przystosowania) > najkrotsza_droga_calosc[1]:
        najkrotsza_droga_calosc[0] = populacja[aktualne_przystosowania.index(max(aktualne_przystosowania))].copy()
        najkrotsza_droga_calosc[1] = max(aktualne_przystosowania)
    if min(aktualne_przystosowania) < najdluzsza_droga_calosc[1]:
        najdluzsza_droga_calosc[0] = populacja[aktualne_przystosowania.index(min(aktualne_przystosowania))].copy()
        najdluzsza_droga_calosc[1] = min(aktualne_przystosowania)
        
def policz_przystosowania():
    przystosowania = []
    for i in range (wielkosc_populacji):
        suma = 0
        for j in range (liczba_miast):
            AX = miasta[populacja[i][j]][0]
            AY = miasta[populacja[i][j]][1]
            BX = miasta[populacja[i][(j+1)%liczba_miast]][0]
            BY = miasta[populacja[i][(j+1)%liczba_miast]][1]
            suma += (math.sqrt((AX-BX)**2+(AY-BY)**2))
        przystosowania.append((1/suma)**1)
    return przystosowania

def reprodukuj_populacje():
    global populacja
    nowa_populacja = []
    suma = sum(aktualne_przystosowania)
    for i in range (wielkosc_populacji):
        akumulator = 0
        losowa_wartosc = random.uniform(0, suma)
        for index, osobnik in enumerate(populacja):
            akumulator += aktualne_przystosowania[index]
            if akumulator > losowa_wartosc:
                nowa_populacja.append(populacja[index])
                break
    populacja = nowa_populacja.copy()

def krzyzuj_populacje_CX():
    global populacja
    nowa_populacja = []
    for i in range(math.floor(wielkosc_populacji/2)):
        indexa = random.randrange(len(populacja))
        a = populacja[indexa]
        del populacja[indexa]
        indexb = random.randrange(len(populacja))
        b = populacja[indexb]
        del populacja[indexb]
        losowa_wartosc = random.uniform(0, 1)
        if losowa_wartosc < szansa_krzyzowania:
            start_cyklu = random.randint(0, liczba_miast-1)
            dziecko1 = [-1] * liczba_miast
            dziecko2 = [-1] * liczba_miast
            while -1 in dziecko1:
                aktualny_index = start_cyklu
                while dziecko1[aktualny_index] == -1:
                    dziecko1[aktualny_index] = b[aktualny_index]
                    aktualny_index = a.index(b[aktualny_index])
                for j in range (liczba_miast):
                    if dziecko1[j] == -1:
                        dziecko1[j] = a[j]
            while -1 in dziecko2:
                aktualny_index = start_cyklu
                while dziecko2[aktualny_index] == -1:
                    dziecko2[aktualny_index] = a[aktualny_index]
                    aktualny_index = b.index(a[aktualny_index])
                for j in range (liczba_miast):
                    if dziecko2[j] == -1:
                        dziecko2[j] = b[j]
            nowa_populacja.append(dziecko1)
            nowa_populacja.append(dziecko2)
        else:
            nowa_populacja.append(a)
            nowa_populacja.append(b)
    if wielkosc_populacji % 2 == 1:
        nowa_populacja.append(populacja[-1])
    populacja = nowa_populacja.copy()

def krzyzuj_populacje_OX():
    global populacja
    nowa_populacja = []
    for i in range(math.floor(wielkosc_populacji/2)):
        indexa = random.randrange(len(populacja))
        a = populacja[indexa]
        del populacja[indexa]
        indexb = random.randrange(len(populacja))
        b = populacja[indexb]
        del populacja[indexb]
        losowa_wartosc = random.uniform(0, 1)
        if losowa_wartosc < szansa_krzyzowania:
            punkt_krzyzowania1, punkt_krzyzowania2 = sorted(random.sample(range(liczba_miast+1), 2))
            dziecko1 = [-1] * liczba_miast
            dziecko2 = [-1] * liczba_miast
            dziecko1[punkt_krzyzowania1:punkt_krzyzowania2] = a[punkt_krzyzowania1:punkt_krzyzowania2]
            dziecko2[punkt_krzyzowania1:punkt_krzyzowania2] = b[punkt_krzyzowania1:punkt_krzyzowania2]
            index1 = punkt_krzyzowania2
            for i in range(punkt_krzyzowania2, liczba_miast + punkt_krzyzowania2):
                if b[i % liczba_miast] not in dziecko1:
                    dziecko1[index1 % liczba_miast] = b[i % liczba_miast]
                    index1 += 1
            index2 = punkt_krzyzowania2
            for i in range(punkt_krzyzowania2, liczba_miast + punkt_krzyzowania2):
                if a[i % liczba_miast] not in dziecko2:
                    dziecko2[index2 % liczba_miast] = a[i % liczba_miast]
                    index2 += 1
            nowa_populacja.append(dziecko1)
            nowa_populacja.append(dziecko2)
        else:
            nowa_populacja.append(a)
            nowa_populacja.append(b)
    if wielkosc_populacji % 2 == 1:
        nowa_populacja.append(populacja[-1])
    populacja = nowa_populacja.copy()

def krzyzuj_populacje_PMX():
    global populacja
    nowa_populacja = []
    for i in range(math.floor(wielkosc_populacji/2)):
        indexa = random.randrange(len(populacja))
        a = populacja[indexa]
        del populacja[indexa]
        indexb = random.randrange(len(populacja))
        b = populacja[indexb]
        del populacja[indexb]
        losowa_wartosc = random.uniform(0, 1)
        if losowa_wartosc < szansa_krzyzowania:
            punkt_krzyzowania1, punkt_krzyzowania2 = sorted(random.sample(range(liczba_miast+1), 2))
            rodzic1_srodek = a[punkt_krzyzowania1:punkt_krzyzowania2]
            rodzic2_srodek = b[punkt_krzyzowania1:punkt_krzyzowania2]
            temp_dziecko1 = a[:punkt_krzyzowania1] + rodzic2_srodek + a[punkt_krzyzowania2:]
            temp_dziecko2 = b[:punkt_krzyzowania1] + rodzic1_srodek + b[punkt_krzyzowania2:]
            global relacje
            relacje = []
            for i in range(len(rodzic1_srodek)):
                relacje.append([rodzic2_srodek[i], rodzic1_srodek[i]])  
            dziecko1 = rekursja1(temp_dziecko1, punkt_krzyzowania1, punkt_krzyzowania2, rodzic1_srodek, rodzic2_srodek)
            dziecko2 = rekursja2(temp_dziecko1, punkt_krzyzowania1, punkt_krzyzowania2, rodzic1_srodek, rodzic2_srodek)
            nowa_populacja.append(dziecko1)
            nowa_populacja.append(dziecko2)
        else:
            nowa_populacja.append(a)
            nowa_populacja.append(b)
    if wielkosc_populacji % 2 == 1:
        nowa_populacja.append(populacja[-1])
    populacja = nowa_populacja.copy()
    
def rekursja1(temp_dziecko, punkt_krzyzowania1, punkt_krzyzowania2, rodzic1_srodek, rodzic2_srodek):
    dziecko = [-1] * liczba_miast
    for i,j in enumerate(temp_dziecko[:punkt_krzyzowania1]):
        c=0
        for x in relacje:
            if j == x[0]:
                dziecko[i]=x[1]
                c=1
                break
        if c==0:
            dziecko[i]=j
    j=0
    for i in range(punkt_krzyzowania1,punkt_krzyzowania2):
        dziecko[i]=rodzic2_srodek[j]
        j+=1

    for i,j in enumerate(temp_dziecko[punkt_krzyzowania2:]):
        c=0
        for x in relacje:
            if j == x[0]:
                dziecko[i+punkt_krzyzowania2]=x[1]
                c=1
                break
        if c==0:
            dziecko[i+punkt_krzyzowania2]=j
    dziecko_unikat=np.unique(dziecko)
    if len(dziecko)>len(dziecko_unikat):
        dziecko=rekursja1(dziecko,punkt_krzyzowania1,punkt_krzyzowania2,rodzic1_srodek,rodzic2_srodek)
    return(dziecko)
    
def rekursja2(temp_dziecko, punkt_krzyzowania1, punkt_krzyzowania2, rodzic1_srodek, rodzic2_srodek):
    dziecko = [-1] * liczba_miast
    for i,j in enumerate(temp_dziecko[:punkt_krzyzowania1]):
        c=0
        for x in relacje:
            if j == x[1]:
                dziecko[i]=x[0]
                c=1
                break
        if c==0:
            dziecko[i]=j
    j=0
    for i in range(punkt_krzyzowania1,punkt_krzyzowania2):
        dziecko[i]=rodzic1_srodek[j]
        j+=1

    for i,j in enumerate(temp_dziecko[punkt_krzyzowania2:]):
        c=0
        for x in relacje:
            if j == x[1]:
                dziecko[i+punkt_krzyzowania2]=x[0]
                c=1
                break
        if c==0:
            dziecko[i+punkt_krzyzowania2]=j
    dziecko_unikat=np.unique(dziecko)
    if len(dziecko)>len(dziecko_unikat):
        dziecko=rekursja2(dziecko,punkt_krzyzowania1,punkt_krzyzowania2,rodzic1_srodek,rodzic2_srodek)
    return(dziecko)

def mutuj_populacje():
    global populacja
    for osobnik in populacja:
        losowa_wartosc = random.uniform(0, 1)
        if losowa_wartosc < szansa_mutowania:
            indeks1, indeks2 = random.sample(range(0, liczba_miast), 2)
            osobnik[indeks1], osobnik[indeks2] = osobnik[indeks2], osobnik[indeks1]
            
def wykresy():
    plt.figure(num="Przystosowania i trasy", figsize=(8, 8))
    plt.subplot(2, 2, 1)
    ypoints = np.array(przystosowanie_min)
    plt.plot(ypoints, label="Przystosowanie min", color="red")
    ypoints = np.array(przystosowanie_max)
    plt.plot(ypoints, label="Przystosowanie max", color="green")
    ypoints = np.array(przystosowanie_avg)
    plt.plot(ypoints, label="Przystosowanie avg", color="blue")
    plt.legend()

def mapy():
    # najkrotsza_droga = populacja[aktualne_przystosowania.index(max(aktualne_przystosowania))]
    # najdluzsza_droga = populacja[aktualne_przystosowania.index(min(aktualne_przystosowania))]
    najkrotsza_droga = najkrotsza_droga_calosc[0]
    najdluzsza_droga = najdluzsza_droga_calosc[0]
    x = [punkt[0] for punkt in miasta]
    y = [punkt[1] for punkt in miasta]
    
    plt.subplot(2, 2, 3)
    plt.scatter(x, y, color='blue', label='Miasta')
    
    for i in range(len(najkrotsza_droga)):
        punkt1 = miasta[najkrotsza_droga[i]]
        punkt2 = miasta[najkrotsza_droga[(i+1)%len(najkrotsza_droga)]]
        plt.plot([punkt1[0], punkt2[0]], [punkt1[1], punkt2[1]], color='green', linestyle='-')
        
    plt.xlabel('Wspolrzedna X')
    plt.ylabel('Wspolrzedna Y')
    plt.title('Najkrotsza Trasa')
    plt.grid()
    plt.legend()
    plt.xlim(-0.5, xmapy+0.5)
    plt.ylim(-0.5, ymapy+0.5)
    
    plt.subplot(2, 2, 4)
    plt.scatter(x, y, color='blue', label='Miasta')
        
    for i in range(len(najdluzsza_droga)):
        punkt1 = miasta[najdluzsza_droga[i]]
        punkt2 = miasta[najdluzsza_droga[(i+1)%len(najdluzsza_droga)]]
        plt.plot([punkt1[0], punkt2[0]], [punkt1[1], punkt2[1]], color='red', linestyle='-')
    
    plt.xlabel('Wspolrzedna X')
    plt.ylabel('Wspolrzedna Y')
    plt.title('Najdluzsza Trasa')
    plt.grid()
    plt.legend()
    plt.xlim(-0.5, xmapy+0.5)
    plt.ylim(-0.5, ymapy+0.5)
    
    plt.tight_layout()
    plt.show()

def cykl():
    reprodukuj_populacje()
    krzyzuj_populacje_CX() # CX, OX, PMX
    mutuj_populacje()
    statystyki()
    
generuj_populacje()
statystyki()

for i in range(liczba_generacji):
    cykl()

# print(najdluzsza_droga_calosc[0], 1/najdluzsza_droga_calosc[1], najkrotsza_droga_calosc[0], 1/najkrotsza_droga_calosc[1])
wykresy()
mapy()