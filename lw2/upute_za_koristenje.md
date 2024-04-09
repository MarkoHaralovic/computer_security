# README  za upravitelja zaporkama

## Opis sustava

Ovaj sustav uključuje dva alata: skriptu za upravljanje korisnicima (`usergmt.py`) i skriptu za prijavu (`login.py`). Oba alata zajedno rade na upravljanju i autentifikaciji korisničkih vjerodajnica. Skripta za upravljanje korisnicima omogućuje dodavanje, mijenjanje i brisanje korisničkih vjerodajnica, dok skripta za prijavu rukuje autentifikacijom korisnika.

### Skripta za upravljanje korisnicima (usergmt.py)

- **Dodaj korisnika**: Dodaje novog korisnika s korisničkim imenom i lozinkom.
- **Promjena lozinke**: Mijenja lozinku postojećeg korisnika.
- **Prisilna promjena lozinke**: Označava korisnika za promjenu lozinke pri sljedećoj prijavi.
- **Brisanje korisnika**: Uklanja korisnika iz sustava.

### Skripta za prijavu (login.py)

- Rukuje autentifikacijom korisnika.
- Dopušta tri pokušaja za unos ispravne lozinke.
- Ako je potrebno promijeniti lozinku (`Force_Pass`), skripta traži od korisnika da to učini.
- Otvora naredbeni redak nakon uspješne autentifikacije.

## Značajke sigurnosti

- Lozinke se heširaju s SHA-512 algoritmom i solju koristeći `get_random_bytes` iz Crypto knjižnice.
- Sol je 16-bajtna nasumično generirana vrijednost, koja poboljšava sigurnost.
- Ne daje se naznaka je li korisničko ime netočno ili ukoliko lozinka ne odgovara, u svrhu sigurnosti.
- Dopušteno je maksimalno tri pokušaja za autentifikaciju korisnika.

## Naredbe za korištenje

### Upravljanje korisnicima

1. **Dodavanje novog korisnika**:
   ```bash
   python usergmt.py add [korisničko ime]

2. **Promjena lozinke korisnika**:
   ```bash
   python usergmt.py passwd [korisničko ime]
   
3. **Prisilna promjena lozinke korisnika pri sljedećoj prijavi**:
   ```bash
   python usergmt.py forcepass [korisničko ime]

4. **Brisanje korisnika**:
   ```bash
   python usergmt.py del [korisničko ime]

### Prijava korisnika
**Za prijavu korisnika pokrenite**: 
   ```bash
   python login.py [korisničko ime]
