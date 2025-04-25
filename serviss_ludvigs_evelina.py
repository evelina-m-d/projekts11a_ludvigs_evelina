import datetime
import json

class Detala():  #satur tikai datus par detaļām, bez metodēm
    def __init__(self, nosaukums, marka, modelis, detalas_cena):
        self.nosaukums = nosaukums   
        self.marka = marka
        self.modelis = modelis
        self.detalas_cena = detalas_cena

class Piegadatajs(): #satur datus par piegadatajiem
    def __init__(self, laiks, min_apjoms, max_apjoms, cena_par_piegadi):
        self.laiks = laiks
        self.min_apjoms = min_apjoms
        self.max_apjoms = max_apjoms
        self.cena_par_piegadi = cena_par_piegadi

piegadataji = [      #visi pieejamie piegādātāji un to dati, izmantojot OOP principus
    Piegadatajs(2, 1, 100, 10),
    Piegadatajs(3, 1, 2, 3),
    Piegadatajs(4, 1, 120, 12)
]

def pasutijums(piegadatajs, detala): #ļauj pasūtīt detaļas un ievieto datus par tām failā
    while True:
        detala.nosaukums = input("Ievadiet, kādu detaļu jums vajag pasūtīt: ")
        detala.marka = input("Ievadiet, kādas mašīnas markas detaļa vajadzīga: ")
        detala.modelis = input("Ievadiet, kāds ir mašīnas modelis: ")
        while True:
            try:
                detala.detalas_cena = float(input("Ievadiet, kāda ir šīs detaļas cena: "))
                break
            except ValueError:
                print("Ievadiet cenu kā skaitli!") #pārbauda datu tipu

        while True:
            try:
                skaits = int(input("Ievadiet detaļu skaitu: "))
                if skaits < piegadatajs.min_apjoms or skaits > piegadatajs.max_apjoms: #izmanto katra piegādātāja individuālos datus, lai kontrolētu pasūtījumus
                    print("Ievadiet piegādātājam atbilstošu detaļu skaitu!")
                else:
                    break
            except ValueError:
                print("Ievadiet skaitu kā skaitli!") #pārbauda datu tipu
            
            
        
        datums = datetime.datetime.now() + datetime.timedelta(days=piegadatajs.laiks) #izveido piegādes datumu no esošās dienas datuma un katra piegādātāja piegādes laiku
        kopeja_cena = detala.detalas_cena * skaits + piegadatajs.cena_par_piegadi #izrēķina kopējo cenu
        print(f"Kopējā detaļu cena: {kopeja_cena}")
        try:
            with open('pasutijumi.json', 'r', encoding='utf8') as file: #ielasa pasūtijumu faila saturu
                pasutijumi = json.load(file) 
            
            faila_detala = {
                "nosaukums" : detala.nosaukums,
                "marka" : detala.marka,
                "modelis" : detala.modelis,
                "cena" : detala.detalas_cena,
                "skaits" : skaits,
                "piegādes diena" : datums.isoformat()
            }
 
            pasutijumi.append(faila_detala)               #ielasītajiem datiem pievieno jaunos
            with open('pasutijumi.json', 'w', encoding="utf8") as f:
                json.dump(pasutijumi, f, ensure_ascii=False) #pārraksta bijušos datus ar updated jauniem datiem
        except FileNotFoundError:
            print("Vēl nav veikti pasūtījumi!")
        
        if input("Vai vēlaties pievienot vēl detaļas (j/n)? ") == "n":
            break

def pieraksts(vards, uzvards, detala, marka, modelis): #ļauj pierakstīt klientus un ievieto datus par tiem failā, fails ir tikai kā blociņš servisa menedžmentam
    datums = datetime.datetime.now()

    with open('pieraksti.txt', 'a', encoding="utf8") as f:
        f.write(f"\n***\nKlienta vārds: {vards.capitalize()} {uzvards.capitalize()}\nPieraksta veikšanas datums: {datums.strftime('%d/%m/%Y')}\nMašīnas marka: {marka.capitalize()}\nMašīnas modelis: {modelis}\nNepieciešamās detaļas: {detala}")

def noliktava():
    while True:
        try:
            with open('pasutijumi.json', 'r', encoding='utf8') as file: #ielasa pasūtijumu faila saturu
                pasutijumi = json.load(file)

            with open('noliktava.json', 'r', encoding='utf8') as file: #ielasa noliktavas faila saturu
                noliktava = json.load(file)

            for pasutijums in pasutijumi[:]:
                laiks = pasutijums['piegādes diena']
                piegades_diena = datetime.datetime.fromisoformat(laiks)  #salīdzina piegādes dienu failā ar esošo datumu, ja piegādes diena sakrīt vai ir vecāka par esošo datumu, pasūtījums automātiski tiek pievienots noliktavai

                if piegades_diena <= datetime.datetime.now():
                    pasutijums.pop("piegādes diena")  #izņem no detaļas dict piegādes dienu un pievieno noliktavas datiem
                    noliktava.append(pasutijums)
                    pasutijumi.remove(pasutijums) #izņem pasūtījumu no pasūtījumu datiem
                else:
                    pass
            
            with open('pasutijumi.json', 'w', encoding='utf8') as file:   #visus updated datus ieliek abos atbilstošajos failos
                json.dump(pasutijumi, file)
            with open('noliktava.json', 'w', encoding='utf8') as file:
                json.dump(noliktava, file)

        except FileNotFoundError:
            pass
        
        try:
            with open('noliktava.json', 'r') as file:  #noliktavas skatīšanai
                preces = json.load(file)

            print("Preces, kas atrodas noliktavā:")
            for i in preces:
                print(i, '\n')
        except FileNotFoundError:
            print("Noliktava ir tukša!")
        
        break

def izvelne():
    print("Servisa noliktavas un pierakstu uzskaites programma.")
    while True:
        izvele = input("****************************************************\n1-Apskatīt noliktavu\n2-Veikt klienta pierakstu\n3-Veikt pasūtījumu\n4-Iziet no programmas\nIzvēle: ")

        if izvele == "1": 
            noliktava()   #izsauc funkciju
        if izvele == "2":
            vards = input("Kāds ir klienta vārds?:")
            uzvards = input("Kāds ir klienta uzvārds?:")
            marka = input("Kāda ir klienta mašīnas marka?: ")
            detala = input("Kādas detaļas klientam ir vajadzīgas? (atdalīt ar ', '): ")
            modelis = input("Kāds ir klienta mašīnas modelis?: ")
            pieraksts(vards, uzvards, detala, marka, modelis) #izsauc funkciju
        if izvele == "3":
            piegadatajs = 0
            for i in piegadataji:
                print(f"Piegādātājs {piegadataji.index(i) +1} - pasūtījuma cena: {i.cena_par_piegadi}€, pasūtījuma laiks: {i.laiks} dienas, minimālais pasūtījuma daudzums: {i.min_apjoms}, maksimālais pasūtījuma daudzums: {i.max_apjoms}")
            while True:
                piegadatajs = int(input(f"Kādu piegādātāju jūs vēlaties (1 - {len(piegadataji)}): ")) #izsauc funkciju
                if piegadatajs < 1 or piegadatajs > len(piegadataji) +1:
                    print("Nepareizi ievadīts skaitlis!")
                else:
                    break
            
            pasutijums(piegadataji[int(piegadatajs)-1], Detala(None, None, None, None)) #izsauc funkciju
        if izvele == "4":  #noslēdz programmu
            print("Visu labu!") 
            break

izvelne()  #palaiž visu programmu