# Upute za korištenje.

## Opis sustava

Alat je smišljen ako rješenja za zaštićeno spemanje korisničkih zaporki.

Pomoću glavne zaporke (master password), koja se derivira PBKDF2  funkcijom za deriviranje ključa,
u bazu se spremaju parovi adresa i lozinka.
Za dekripciju ključa koristi se i salt, odnosno nasumično generirana vrijednost od 16 bajtova,kako bi se osnažila zaporka.
Salt se generira funkcijom get_random_bytes biblioteke Crypto.

Baza je binarna datoteka, inicijalizira se na željenoj lokaciji, u slučaju postojanja istoimene datoteke na toj lokaciji,
ta se prebriše i nova baza se postavlja na istu lokaciju, o čemu je korisnik pravodobno obaviješten.
Na početku se u bazu sprema salt, inicijalizacoijski vektor te prazan rječnik.

Za svaku je adresu moguće spremiti samo jednu zaporku. Ukoliko korisnik pošalje zaporku za adresu za koju već
postoji zaporka, prethodna se briše te se posljednja zaporka sprema u bazu podataka.

Za spremanje je potrebno poslati glavnu zaporku, koja se derivira, a zatim se tim
deriviranim ključem podaci kriptiraju te serijaliziraju i spremaju u binarnu datoteku, 
zajedno s 16 bajtnim slatom i inicijalizacijskim vektorom. Koristio se AES, odnosno simetrični algoritam u kojemu se isti ključ koristi i za dekripciju i enkripciju.

Dohvaćanje podataka je slično, pošalje se glavna zaporka pomoću koje se dohvati
deserijaliziran binarni zapis zaporki te se za određenu adresu dobije zaporka.

Rušenje pvpg sustava moće je jedino brute-force napadom, nigdje se ne evidentira 
duljina glavne zaporke niti se provjerava njen oblik. Binarni podaci su nevažni 
te ih se ne može dekriptirati bze glavne zaporke. Nemoguće je da se s krivom zaporkom 
dekriptiraju podaci, kako se dobije greška "MAC check failed" prilikom korištenja
decrypt_and_verify funkcije iz biblioteke Crypto.

## Korištenje sustava
Moguće je pokrenuti manager naredbom

''bash
python lab1.py 

Ispisati će se opis alat. Moguće naredbe su:
Inicijalizacija baze podataka lozinki:

### Inicijalizacija Baze Podataka Lozinki
- **Naredba:** `init`
- **Svrha:** Inicijalizira bazu podataka lozinki.
- **Primjer upotrebe:** `python password_manager.py init "VašaGlavnaLozinka"`

### Pohrana Nove Lozinke
- **Naredba:** `put`
- **Svrha:** Pohranjuje novu lozinku za određenu adresu.
- **Primjer upotrebe:** `python password_manager.py put "VašaGlavnaLozinka" "example.com" "VašaLozinka"`

### Dohvaćanje Pohranjene Lozinke
- **Naredba:** `get`
- **Svrha:** Dohvaća pohranjenu lozinku za određenu adresu.
- **Primjer upotrebe:** `python password_manager.py get "VašaGlavnaLozinka" "example.com"`

