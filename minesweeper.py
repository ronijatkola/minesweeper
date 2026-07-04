import json
import math
import time
import random
import haravasto

PER_SIVU = 5

tila = {
    "kentta": [],
    "naytto": [],
    "leveys": 0,
    "korkeus": 0,
    "ruutumaara": 0,
    "miinamaara": 0,
    "aloitusaika": 0,
    "klikkaukset": 0,    
    "pelin_kesto": 0,
    "tulos": None,
    "pelattu": None
}

def kysy_leveys():
    """
    Kysyy käyttäjältä kentän leveyden.
    """
    while True:
        try:
            leveys = int(input("Anna kentän leveys (5-35): "))
            if 5 <= leveys <= 35:
                tila["leveys"] = leveys
                ikkuna_leveys = leveys * 40
                return leveys, ikkuna_leveys 
            print("Antamasi leveys ei ole sallituissa rajoissa, yritä uudelleen") 
        except ValueError:
            print("Anna kokonaisluku")

def kysy_korkeus():
    """ 
    Kysyy käyttäjältä kentän korkeuden.
    """
    while True:
        try:
            korkeus = int(input("Anna kentän korkeus (5-20): "))
            if 5 <= korkeus <= 20:
                tila["korkeus"] = korkeus
                ikkuna_korkeus = korkeus * 40
                return korkeus, ikkuna_korkeus
            print("Antamasi korkeus ei ole sallituissa rajoissa, yritä uudelleen") 
        except ValueError:
            print("Anna kokonaisluku")
            
def kysy_miinamaara(ruutumaara):
    """
    Kysyy käyttäjältä miinamäärän.
    """
    while True:
        try:
            miinamaara = int(input(f"Anna miinojen lukumäärä (1 - {ruutumaara - 1}): "))
            if 1 <= miinamaara < ruutumaara:
                tila["miinamaara"] = miinamaara
                return miinamaara
        except ValueError:
            print("Anna kokonaisluku")
        else:
            print("Miinoja täytyy olla enemmän kuin 0 ja vähemmän kuin ruutuja")

def luo_kentta(leveys, korkeus):
    """
    Luo miinoitettavan pelikentän, sekä näytettävän näyttökentän.
    Lisäksi lisää jokaisen ruudun jäljellä listaan miinoitusta varten
    ja palauttaa sen.
    """
    
    pelikentta = []
    nayttokentta = []
    jaljella = []
    for rivi in range(korkeus):
        pelikentta.append([])
        nayttokentta.append([])
        for sarake in range(leveys):
            pelikentta[-1].append("0")
            nayttokentta[-1].append(" ")
            jaljella.append((sarake,rivi))

    tila["kentta"] = pelikentta
    tila["naytto"] = nayttokentta
    return jaljella
        
def miinoita(kentta, vapaat_ruudut, n):
    """
    Asettaa kentälle käyttäjän haluaman määrän miinoja satunnaisiin ruutuihin.
    """
    for _ in range(n):
        ruutu = random.choice(vapaat_ruudut)      
        kentta[ruutu[1]][ruutu[0]] = "x" 
        vapaat_ruudut.remove(ruutu)
        
def laske_miinat(kentta):
    """
    Laskee jokaisen ruudun ympärillä olevien miinojen lukumäärän
    ja syöttää numeron ruutuun.
    """
    for y, rivi in enumerate(kentta):
        for x, ruutu in enumerate(rivi):
            if ruutu == "x":
                continue
               
            miinat = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1), (1,-1),(-1,1),(1,1)]:
                uusi_x, uusi_y = x + dx, y + dy
                if 0<= uusi_x < len(kentta[0]) and 0 <= uusi_y < len(kentta):
                    if kentta[uusi_y][uusi_x] == "x":
                        miinat += 1
            
            kentta[y][x] = str(miinat) if miinat > 0 else "0"

def ajastin(loppuaika):
    """
    Pelin loputtua ottaa lopetusajan talteen.
    """
    kesto = (loppuaika - tila["aloitusaika"]) / 60
    tila["pelin_kesto"] = kesto

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """Käsittelee hiiren painallukset. Vasemmalla avataan ruutu,
    oikealla liputetaan.
    """
    kentta_x = int(x // 40)
    kentta_y = int(y // 40)
    
    if nappi == haravasto.HIIRI_VASEN:           
        if tila["kentta"][kentta_y][kentta_x] == "x":
            lopeta_miinaan()            
        else:
            lisaa_klikkaus(kentta_x, kentta_y)
            tulvataytto(tila["kentta"], tila["naytto"], kentta_x, kentta_y)
            tarkista_voitto()
            
    elif nappi == haravasto.HIIRI_OIKEA:
        if tila["naytto"][kentta_y][kentta_x] == " ":
            tila["naytto"][kentta_y][kentta_x] = "f"
        elif tila["naytto"][kentta_y][kentta_x] == "f":
            tila["naytto"][kentta_y][kentta_x] = " "
            
def piirra_kentta():
    """
    Piirtää ruudukon ja paljastetut ruudut kentälle.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    
    for y, rivi in enumerate(tila["naytto"]):
        for x, ruutu in enumerate(rivi):
            if ruutu != " ":
                haravasto.lisaa_piirrettava_ruutu(ruutu, x * 40, y * 40)
            else:
                haravasto.lisaa_piirrettava_ruutu(" ", x * 40, y * 40)
    
    haravasto.piirra_ruudut()            

def pelaa_peli():
    """
    Ajaa tarvittavat funktiot ja aloittaa pelin. 
    Ottaa myös aloitusajan muistiin.
    """
    leveys, ikkuna_leveys = kysy_leveys()
    korkeus, ikkuna_korkeus = kysy_korkeus()
    tila["ruutumaara"] = leveys * korkeus
    miinamaara = kysy_miinamaara(tila["ruutumaara"])
    jaljella = luo_kentta(leveys, korkeus)
    miinoita(tila["kentta"], jaljella, miinamaara)
    laske_miinat(tila["kentta"])
     
    alkuaika = time.time()
    tila["aloitusaika"] = alkuaika
 
    haravasto.lataa_kuvat("icons")
    haravasto.luo_ikkuna(ikkuna_leveys, ikkuna_korkeus)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()
        
def aloitus(): 
    """
    Toimii alkuvalikkona.
    """
    print("Tervetuloa pelaamaan miinantallaajaa!")
    while True:
        valinta = (
            input("Valitse seuraavista vaihtoehdoista: (A)loita, (L)opeta, (T)ilastot: ")
            .strip()
            .lower()
    )

        if valinta == "a":
            pelaa_peli()
            
        elif valinta == "l":
            print("Kiitos pelaamisesta!")
            break
        
        elif valinta == "t":              
            tilastot = lataa_tilastot("miinaharavatiedosto.json")
            if tila["pelattu"]:
                tulosta(tilastot)
            else: 
                print("Ei vielä pelejä tilastoitavaksi")
        else:
            print("Virheellinen valinta, yritä uudelleen")
            
def tulvataytto(kentta, naytto, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi ja paljastaa ne 
    näyttökentässä siten, että täyttö aloitetaan annetusta x, y -pisteestä.
    """
    if kentta[y][x] == "x":
        return

    taytettavat = [(x, y)]
    while taytettavat:
        nykyinen_x, nykyinen_y = taytettavat.pop(0)

        if naytto[nykyinen_y][nykyinen_x] != " ":
            continue 

        miinat = 0       
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            uusi_x, uusi_y = nykyinen_x + dx, nykyinen_y + dy     
            if 0 <= uusi_x < len(kentta[0]) and 0 <= uusi_y < len(kentta):
                if kentta[uusi_y][uusi_x] == "x":
                    miinat += 1

        if miinat > 0:
            naytto[nykyinen_y][nykyinen_x] = str(miinat)
        else:
            naytto[nykyinen_y][nykyinen_x] = "0"
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                uusi_x, uusi_y = nykyinen_x + dx, nykyinen_y + dy
                if 0 <= uusi_x < len(kentta[0]) and 0 <= uusi_y < len(kentta):
                    if naytto[uusi_y][uusi_x] == " ":
                        taytettavat.append((uusi_x, uusi_y))
 
def lisaa_klikkaus(x, y):
    """
    Pitää yllä klikkausten määrää tilastointia varten.
    """
    if tila["naytto"][y][x] == " ":
        tila["klikkaukset"] += 1
            
def tarkista_voitto():
    """
    Tarkistaa joka ruudun avautuessa, onko kaikki tyhjät ruudut avattu.
    """
    vapaat_ruudut = 0
    
    for rivi in tila["naytto"]:
        for ruutu in rivi:
            if ruutu not in (" ", "f"):
                vapaat_ruudut += 1
                
    if vapaat_ruudut == tila["ruutumaara"] - tila["miinamaara"]:        
        lopetusaika = time.time()
        ajastin(lopetusaika) 
                        
        print("Onneksi olkoon, voitit pelin.")
        tila["tulos"] = "Voitto"       
        time.sleep(2)
        haravasto.lopeta()
        tallenna_peli("miinaharavatiedosto.json")
            
def lopeta_miinaan():
    """
    Jos käyttäjä klikkaa miinaa, lopettaa pelin.
    """
    lopetusaika = time.time()
    ajastin(lopetusaika)
    tila["klikkaukset"] += 1
    
    print("Osuit miinaan! Peli päättyi häviöön.")
    tila["tulos"] = "Häviö"
    time.sleep(2)
    haravasto.lopeta()
    tallenna_peli("miinaharavatiedosto.json")
    
def tallenna_peli(tiedosto):
    """
    Funktio hakee arvot tila sanakirjasta, tallentaa ne tekstitiedostoon
    ja lopuksi nollaa klikkaukset
    """
    
    paivamaara = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    
    tulokset = {
        "Päivämäärä": paivamaara,
        "Tulos": tila["tulos"],
        "Kesto minuuteissa": f"{tila['pelin_kesto']:.1f}",
        "Klikkauksien määrä": f"{tila['klikkaukset']}",
        "Kentän koko": f"{tila['leveys']} x {tila['korkeus']}",
        "Miinamäärä": f"{tila['miinamaara']}"
    }
 
    try:
        try:
            with open(tiedosto, "r", encoding='utf-8') as kohde:
                tilastot = json.load(kohde)  
        except (IOError, json.JSONDecodeError):  
            tilastot = []  

        tilastot.append(tulokset)

        with open(tiedosto, "w", encoding='utf-8', newline="") as kohde:
            json.dump(tilastot, kohde, ensure_ascii=False, indent=4)

        print("Pelin tiedot tallennettu")
    
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")
    
    tila["klikkaukset"] = 0
 
def lataa_tilastot(tiedosto):
    """
    Tarkistaa löytyykö tilasto tiedostoa jo etukäteen,
    ja muuttaa pelattu muuttujan statusta sen mukaan.
    """
    try:
        with open(tiedosto, 'r', encoding='utf-8') as lahde:
            tilastot = json.load(lahde)
            tila["pelattu"] = True
            return tilastot
            
    except (IOError, json.JSONDecodeError):
        tila["pelattu"] = False 
        return []
        
def muotoile_sivu(rivit, sivu):
    """
    Muotoilee sivut tulostusta varten.
    """
    for _, tilastot in enumerate(rivit, sivu * PER_SIVU + 1):
        print(
            f"{tilastot['Päivämäärä']} - {tilastot['Tulos']} - "
            f"{tilastot['Kesto minuuteissa']} min - {tilastot['Klikkauksien määrä']} klikkausta - "
            f"Kentän koko: {tilastot['Kentän koko']} - Miinat: {tilastot['Miinamäärä']}"
        )

def tulosta(tilastot):
    """
    Tulostaa sivut.
    """
    tulostuksia = math.ceil(len(tilastot) / PER_SIVU)
    for i in range(tulostuksia):
        alku = i * PER_SIVU
        loppu = (i + 1) * PER_SIVU
        muotoile_sivu(tilastot[alku:loppu], i)
        if i < tulostuksia - 1:
            input("   -- paina enter jatkaaksesi tulostusta --")
       
if __name__ == "__main__":
    aloitus()
