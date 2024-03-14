#jednostavan i siguran prototip alata za pohranu zaporki (password manager) koristeći simetričnu kriptografiju

#  Alat mora omogućavati korisniku sljedeće:
# 1. Inicijalizacija alata odnosno stvaranje prazne baze zaporki.
# 2. Pohrana para adresa, zaporka. Ako je već pohranjena zaporka pod istom adresom onda ju je potrebno zamijeniti sa zadanom.
# 3. Dohvaćanje pohranjene zaporke za zadanu adresu.

#  potrebno je osigurati sljedeć sigurnosne zahtjeve:
# 1. Povjerljivost zaporki: napadač ne može odrediti nikakve informacije o zaporkama, čak niti njihovu
# duljinu, čak ni jesu li zaporke za dvije adrese jednake, čak ni je li nova zaporka jednaka staroj kada
# se promijeni.
# 2. Povjerljivost adresa: napadač ne može odrediti nikakve informacije o adresama, osim da zna
# koliko se različitih adresa nalazi u bazi.
# 3. Integritet adresa i zaporki: nije moguće da korisnik dobije od alata zaporku za određenu adresu,
# ako prethodno nije unio točno tu zaporku za točno tu adresu. Obratite pažnju na napad zamijene:
# napadač ne smije moći zamijeniti zaporku određene adrese zaporkom neke druge adrese.

#The Crypto.Cipher package contains algorithms for protecting the confidentiality of data.
# Symmetric ciphers: all parties use the same key, for both decrypting and encrypting data. 
# Symmetric ciphers are typically very fast and can process very large amount of data.

