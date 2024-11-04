from abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.elerheto = True

    @abstractmethod
    def jarat_informacio(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarat_informacio(self):
        return f"Belföldi járat - Járatszám: {self.jaratszam}, Célállomás: {self.celallomas}, Jegyár: {self.jegyar} Ft"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarat_informacio(self):
        return f"Nemzetközi járat - Járatszám: {self.jaratszam}, Célállomás: {self.celallomas}, Jegyár: {self.jegyar} Ft"


class JegyFoglalas:
    def __init__(self, jarat, foglalas_datum):
        self.jarat = jarat
        self.foglalas_datum = foglalas_datum
        self.jegy_ar = jarat.jegyar

    def foglalas_informacio(self):
        return f"Foglalás - Járat: {self.jarat.jaratszam}, Dátum: {self.foglalas_datum}, Jegyár: {self.jegy_ar} Ft"


class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def jarat_hozzaadasa(self, jarat):
        self.jaratok.append(jarat)

    def jegy_foglalasa(self, jaratszam, foglalas_datum):
        jarat = next((j for j in self.jaratok if j.jaratszam == jaratszam and j.elerheto), None)
        if jarat:
            foglalas = JegyFoglalas(jarat, foglalas_datum)
            self.foglalasok.append(foglalas)
            jarat.elerheto = False
            print(f"{jarat.jaratszam} járat sikeresen lefoglalva {foglalas_datum} dátumra.")
            return foglalas.jegy_ar
        else:
            print("A járat nem elérhető vagy nem létezik.")
            return None

    def foglalas_lemondasa(self, jaratszam):
        foglalas = next((f for f in self.foglalasok if f.jarat.jaratszam == jaratszam), None)
        if foglalas:
            foglalas.jarat.elerheto = True
            self.foglalasok.remove(foglalas)
            print(f"{jaratszam} járat foglalása sikeresen lemondva.")
        else:
            print("Nincs ilyen foglalás.")

    def foglalasok_listazasa(self):
        if self.foglalasok:
            print("Aktuális foglalások:")
            for foglalas in self.foglalasok:
                print(foglalas.foglalas_informacio())
        else:
            print("Nincsenek aktív foglalások.")



tarsasag = LegiTarsasag("Dani Airlines")
jarat1 = BelfoldiJarat("JARAT123", "Budapest", 15000)
jarat2 = BelfoldiJarat("JARAT124", "Debrecen", 12000)
jarat3 = NemzetkoziJarat("JARAT456", "London", 45000)


tarsasag.jarat_hozzaadasa(jarat1)
tarsasag.jarat_hozzaadasa(jarat2)
tarsasag.jarat_hozzaadasa(jarat3)

tarsasag.foglalasok.append(JegyFoglalas(jarat1, datetime(2024, 11, 1).date()))
tarsasag.foglalasok.append(JegyFoglalas(jarat1, datetime(2024, 11, 2).date()))
tarsasag.foglalasok.append(JegyFoglalas(jarat2, datetime(2024, 11, 1).date()))
tarsasag.foglalasok.append(JegyFoglalas(jarat2, datetime(2024, 11, 3).date()))
tarsasag.foglalasok.append(JegyFoglalas(jarat3, datetime(2024, 11, 4).date()))
tarsasag.foglalasok.append(JegyFoglalas(jarat3, datetime(2024, 11, 5).date()))


def menu():
    while True:
        print("\n--- Légitársaság Menü ---")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Válasszon egy lehetőséget: ")

        if valasztas == "1":
            jaratszam = input("Adja meg a járatszámot: ")
            foglalas_datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ.HH.3NN): ")
            try:
                foglalas_datum = datetime.strptime(foglalas_datum, "%Y.%m.%d").date()
                tarsasag.jegy_foglalasa(jaratszam, foglalas_datum)
            except ValueError:
                print("Érvénytelen dátum formátum.")

        elif valasztas == "2":
            jaratszam = input("Adja meg a lemondandó járatszámot: ")
            tarsasag.foglalas_lemondasa(jaratszam)

        elif valasztas == "3":
            tarsasag.foglalasok_listazasa()

        elif valasztas == "4":
            print("Kilépés..")
            break

        else:
            print("Érvénytelen választás, próbálja újra.")


# Menü futtatása
menu()
