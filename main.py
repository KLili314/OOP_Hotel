from abc import ABC, abstractmethod
from datetime import datetime, timedelta

#Szoba absztrakt osztaly
class Szoba(ABC):
    def __init__(self, ar, szobaSzam):
        self.ar = ar
        self.szobaSzam = szobaSzam

        def get_szoba_info(self):
            pass

#EgyagyasSzoba osztaly
class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobasSzam,vanFurdo):
        super().__init__(ar,szobasSzam)
        self.vanFurdo = vanFurdo

    def get_szoba_info(self):
        return f"Egyágyas Szoba - Szám: {self.szobaSzam}, Ár: {self.ar} FT/éjszaka, Fürdőszoba: {self.vanFurdo}"

# KétágyasSzoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaSzam, vanKonyha):
        super().__init__(ar, szobaSzam)
        self.vanKonyha = vanKonyha

    def get_szoba_info(self):
        return f"Kétágyas Szoba - Szám: {self.szobaSzam}, Ár: {self.ar} Ft/éjszaka, Konyha: {self.vanKonyha}"

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):
        self.foglalasok.append(foglalas)

    def get_szalloda_info(self):
        return f"Szálloda: {self.nev}, Szobák száma: {len(self.szobak)}"

# Foglalás osztály
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def get_foglalas_info(self):
        return f"Foglalás - Szoba: {self.szoba.szobaSzam}, Dátum: {self.datum}, Ár: {self.szoba.ar} Ft"

# Segédfüggvények
def foglalas_letrehozasa(szalloda, szobaSzam, datum):
    for szoba in szalloda.szobak:
        if szoba.szobaSzam == szobaSzam:
            if not any(f.datum == datum and f.szoba.szobaSzam == szobaSzam for f in szalloda.foglalasok):
                foglalas = Foglalas(szoba, datum)
                szalloda.add_foglalas(foglalas)
                return foglalas
    return None

def foglalas_lemondasa(szalloda, szobaSzam, datum):
    for foglalas in szalloda.foglalasok:
        if foglalas.szoba.szobaSzam == szobaSzam and foglalas.datum == datum:
            szalloda.foglalasok.remove(foglalas)
            return True
    return False

def listaz_foglalasok(szalloda):
    return [f.get_foglalas_info() for f in szalloda.foglalasok]



def datum_ellenorzese(datum):
    return datum > datetime.now().date()

szalloda = Szalloda("Hungary Hotel")
szalloda.add_szoba(EgyagyasSzoba(10000,101,"Van"))
szalloda.add_szoba(EgyagyasSzoba(8000,102,"Nincs"))
szalloda.add_szoba(KetagyasSzoba(18000,201,"Van"))
szalloda.add_szoba(KetagyasSzoba(15000,202,"Nincs"))


def listaz_szalloda(szalloda):
    return [sz.get_szoba_info() for sz in szalloda.szobak]


for i in range(0, 3):
    foglalas_letrehozasa(szalloda, 101, datetime.now().date() + timedelta(days=i))
    foglalas_letrehozasa(szalloda, 201, datetime.now().date() + timedelta(days=i))
# Felhasználói interfész
def felhasznaloi_interfesz():
    while True:
        print("\n--- Szállodai Foglalási Rendszer ---")
        print("1. Szobák listázása")
        print("2. Szoba foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")

        valasztas = input("Válasszon egy opciót: ")

        if valasztas == "1":
            szobak = listaz_szalloda(szalloda)
            print("\n--- Szobák ---")
            for szoba in szobak:
                print(szoba)

        elif valasztas == "2":
            szobaSzam = int(input("Adja meg a szobaszámot: "))
            datum_str = input("Adja meg a dátumot (YYYY-MM-DD): ")
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()

            if datum_ellenorzese(datum):
                foglalas = foglalas_letrehozasa(szalloda, szobaSzam, datum)
                if foglalas:
                    print(f"Sikeres foglalás! {foglalas.get_foglalas_info()}")
                else:
                    print("A szoba már foglalt erre a dátumra vagy nem létezik.")
            else:
                print("Érvénytelen dátum. Kérjük, jövőbeli dátumot adjon meg.")

        elif valasztas == "3":
            szobaSzam = int(input("Adja meg a szobaszámot: "))
            datum_str = input("Adja meg a dátumot (YYYY-MM-DD): ")
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()

            if foglalas_lemondasa(szalloda, szobaSzam, datum):
                print("Foglalás sikeresen lemondva.")
            else:
                print("Nem található ilyen foglalás.")

        elif valasztas == "4":
            foglalasok = listaz_foglalasok(szalloda)
            print("\n--- Foglalások ---")
            for foglalas in foglalasok:
                print(foglalas)

        elif valasztas == "5":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen opció, kérjük válasszon újra.")

# Program futtatása
if __name__ == "__main__":
    felhasznaloi_interfesz()