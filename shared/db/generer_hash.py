import bcrypt

# Génération des hash bcrypt pour les comptes de test
comptes = {
    "admin@yok.com": "AdminPassword123",
    "vendeur1@yok.com": "VendeurPass123",
    "vendeur2@yok.com": "VendeurPass456"
}

print("-- Hash bcrypt générés pour PostgreSQL\n")

for email, password in comptes.items():
    hash_bcrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    print(f"-- {email} : {password}")
    print(f"-- Hash: {hash_bcrypt.decode('utf-8')}\n")
