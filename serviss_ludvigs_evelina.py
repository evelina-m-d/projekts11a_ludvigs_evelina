import datetime
import json

class Detala():  #satur tikai datus par detaļām, bez metodēm
    def __init__(self, nosaukums, marka, modelis, detalas_cena):
        self.nosaukums = nosaukums   
        self.marka = marka
        self.modelis = modelis
        self.detalas_cena = detalas_cena

class Skidrumi():  #satur tikai datus par šķidrumiem, bez metodēm
    def __init__(self, nosaukums, cena):
        self.nosaukums = nosaukums
        self.deriguma_termins = datetime.now() + datetime.timedelta(years = 5) #izveido derīguma termiņu, izmantojot laiku, kad šķidrums tiek pasūtīts
        self.cena = cena

class Klients():  #satur datus par katra klienta pierakstu
    def __init__(self, nepieciesamas_detalas, marka, modelis):
        self.nepieciesamas_detalas = nepieciesamas_detalas
        self.pieraksta_laiks = datetime.now() #ņem aktuālās dienas laiku
        self.marka = marka
        self.modelis = modelis

    def remontet(self, stundu_skaits): 
        stundas_likme = 50 #eiro
        cena = (stundu_skaits * stundas_likme) + self.nepieciesamas_detalas.detalas_cena #aprēķina izmaksas klientam
        return cena

        #butu janonem no noliktavas detala bet to izdomas kad bus kopa salikts

class Piegadatajs():
    def __init__(self, laiks, min_apjoms, max_apjoms, cena_par_piegadi):
        self.laiks = laiks
        self.min_apjoms = min_apjoms
        self.max_apjoms = max_apjoms
        self.cena_par_piegadi = cena_par_piegadi

piegadataji = [
    Piegadatajs(2, 1, 100, 10),
    Piegadatajs(3, 1, 2, 3),
    Piegadatajs(4, 1, 120, 12)
]

def pasutijums(piegadatajs, detala):
    while True:
        #detala = Detala(None, None, None, None)

        detala.nosaukums = input("Ievadiet, kādu detaļu jums vajag pasūtīt: ")
        detala.marka = input("Ievadiet, kādas mašīnas markas detaļa vajadzīga: ")
        detala.modelis = input("Ievadiet, kāds ir mašīnas modelis: ")
        detala.detalas_cena = float(input("Ievadiet, kāda ir šīs detaļas cena: "))
        skaits = float(input("Ievadiet detaļu skaitu: "))
        
        kopeja_cena = detala.detalas_cena * skaits + piegadatajs.cena_par_piegadi
        
        print(f"Kopējā detaļu cena: {kopeja_cena}")
        faila_detala = {
            "nosaukums" : detala.nosaukums,
            "marka" : detala.marka,
            "modelis" : detala.modelis,
            "cena" : detala.detalas_cena,
            "skaits" : skaits,
            "piegades diena" : datetime.now() + datetime.timedelta(days= piegadatajs.laiks) #izveido produkta piegādes laiku no pasūtījuma brīža un katra piegādātāja piegādes laika
        } 
        
        with open('pasutijumi.json', 'a') as f:
            json.dump(faila_detala, f)
        
        if input("Vai vēlaties pievienot vēl detaļas (j/n)? ") == "n":
            break

def pieraksts(pasutitajs=Klients()):
    detalu_saraksts = pasutitajs.nepieciesamas_detalas

    klients = {
        "pieraksta laiks" : datetime.now(),
        "mašīnas marka" : pasutitajs.marka,
        "mašīnas modelis" : pasutitajs.modelis,
        "nepieciešamās detaļas" : [detalu_saraksts.split(", ")]
    }
    
    with open('pieraksti.json', 'a') as f:
            json.dump(klients, f)

def noliktava():
    pass

def izvelne():
    print("Servisa noliktavas un pierakstu uzskaites programma.")
    while True:
        izvele = input("****************************************************\n1-Apskatīt noliktavu\n2-Veikt pierakstu\n3-Veikt pasūtījumu\n4-Iziet no programmas\nIzvēle: ")

        if izvele == "1":
            noliktava()
        if izvele == "2":
            detala = input("Kādas detaļas jums ir vajadzīgas (atdalīt ar ', '): ")
            marka = input("Kāda ir jūsu mašīnas marka: ")
            modelis = input("Kāds ir jūsu mašīnas modelis: ")
            pieraksts(Klients(detala, marka, modelis))
        if izvele == "3":
            for i in piegadataji:
                print(f"Piegādātājs {piegadataji.index(i) + 1} - pasūtījuma cena: {i.cena_par_piegadi}, pasūtījuma laiks: {i.laiks}, minimālais pasūtījuma daudzums: {i.min_apjoms}, maksimālais pasūtījuma daudzums: {i.max_apjoms}")
            piegadatajs = input(f"Kādu piegādātāju jūs vēlaties: ")
            pasutijums(piegadataji[0], Detala(None, None, None, None))
        if izvele == "4":
            print("Visu labu!")
            break

izvelne()