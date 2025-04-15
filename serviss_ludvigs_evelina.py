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
        self.deriguma_termins = datetime.datetime.now() + datetime.timedelta(years = 5) #izveido derīguma termiņu, izmantojot laiku, kad šķidrums tiek pasūtīts
        self.cena = cena

class Klients():  #satur datus par katra klienta pierakstu
    def __init__(self, nepieciesamas_detalas, marka, modelis):
        self.nepieciesamas_detalas = nepieciesamas_detalas
        self.pieraksta_laiks = datetime.datetime.now() #ņem aktuālās dienas laiku
        self.marka = marka
        self.modelis = modelis

    def remontet(self, stundu_skaits, fails): 
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
        skaits = int(input("Ievadiet detaļu skaitu: "))
        
        datums = datetime.datetime.now() + datetime.timedelta(days=piegadatajs.laiks)
        kopeja_cena = detala.detalas_cena * skaits + piegadatajs.cena_par_piegadi
        
        print(f"Kopējā detaļu cena: {kopeja_cena}")
        faila_detala = {
            "nosaukums" : detala.nosaukums,
            "marka" : detala.marka,
            "modelis" : detala.modelis,
            "cena" : detala.detalas_cena,
            "skaits" : skaits,
            "piegādes diena" : datums.strftime("%D")
        }
        
        with open('pasutijumi.json', 'a', encoding="utf8") as f:
            json.dump(faila_detala, f, ensure_ascii=False, indent=4)
        
        if input("Vai vēlaties pievienot vēl detaļas (j/n)? ") == "n":
            break

def pieraksts(pasutitajs):
    detalu_saraksts = pasutitajs.nepieciesamas_detalas
    date = datetime.datetime.now()
    klients = {
        "pieraksta laiks" : date.strftime("%D/%H/%M"),
        "mašīnas marka" : pasutitajs.marka,
        "mašīnas modelis" : pasutitajs.modelis,
        "nepieciešamās detaļas" : detalu_saraksts.split(", ")
    }
    
    with open('pieraksti.json', 'a', encoding="utf8") as f:
        json.dump(klients, f, ensure_ascii=False, indent=4)

def noliktava():
    with open('pasutijumi.json', 'r') as file:
        pasutijumi = [json.loads(line) for line in file]

    for i in pasutijumi:
        laiks = i.get('piegādes diena')
        piegades_diena = datetime.strptime(laiks, '%D')
        if piegades_diena < datetime.now():
            with open('noliktava.json', 'a', encoding="utf8") as f:
                json.dump(i, f, ensure_ascii=False, indent=4)
            
            pasutijumi.remove(i)

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
            piegadatajs = 0
            for i in piegadataji:
                print(f"Piegādātājs {piegadataji.index(i) + 1} - pasūtījuma cena: {i.cena_par_piegadi}€, pasūtījuma laiks: {i.laiks} dienas, minimālais pasūtījuma daudzums: {i.min_apjoms}, maksimālais pasūtījuma daudzums: {i.max_apjoms}")
            while True:
                piegadatajs = int(input(f"Kādu piegādātāju jūs vēlaties (1 - {len(piegadataji)}): "))
                if piegadatajs < 1 or piegadatajs > len(piegadataji):
                    print("Nepareizi ievadīts skaitlis!")
                else:
                    break

            pasutijums(piegadataji[int(piegadatajs)], Detala(None, None, None, None))
        if izvele == "4":
            print("Visu labu!")
            break

izvelne()