import sqlite3
import random

def arrondi(n, decimales=0): #Récupéré sur internet...
    multiplier = 10**decimales
    return int(n* multiplier)/multiplier

conn = sqlite3.connect('banque.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS comptes_courants")
cursor.execute("DROP TABLE IF EXISTS comptes_epargne")
cursor.execute("DROP TABLE IF EXISTS clients")

cursor.execute("CREATE TABLE comptes_courants(id TEXT PRIMARY KEY UNIQUE, id_client INTEGER, solde FLOAT, decouvert FLOAT, FOREIGN KEY(id_client) REFERENCES clients(id) )")
cursor.execute("CREATE TABLE comptes_epargne(id TEXT PRIMARY KEY UNIQUE, id_client INTEGER, solde FLOAT, taux INT, FOREIGN KEY(id_client) REFERENCES clients(id) )")
cursor.execute("CREATE TABLE clients(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, prenom TEXT, date_inscription DATE, mail TEXT)")

noms = ["Danilevski", "Khomiakov", "Astafiev", "Bogdanov", "Bakounine", "De Robertis", "Lourkevitch", "Soloviev", "Rozanov", "Florensky", "Setchenov"]
prenoms = ["Mikhaïl", "Alexandre", "Helena", "Georges", "Piotr", "Vissarion", "Nikolaï", "Vladimir", "Ivan", "Lénine", "Evald", "Dimitri", "Paul", "Eugène"]

for i in range(10):
	date_inscription = str(random.randint(1, 12)) + "/" + str(random.randint(1, 30)) + "/" + str(random.randint(1990, 2019))
	nom = random.choice(noms)
	prenom = random.choice(prenoms)
	mail = prenom.lower() + "." + nom.lower() + "@gmail.com"

	cursor.execute("INSERT INTO clients(nom,prenom,date_inscription,mail) VALUES(\"" + nom + "\", \"" + prenom + "\", \"" + date_inscription + "\", \"" + mail + "\")") #Creation des entrees clients

	decouvert = str(random.randint(0,1))
	if(decouvert):
		solde = str(arrondi(random.randint(-500, 2000), 2))
	else:
		solde = str(arrondi(random.randint(0, 2000), 2))
	cursor.execute("INSERT INTO comptes_courants(id, id_client,solde,decouvert) VALUES(\"A" + str(random.randint(1, 9999)) + "\", " + str(i) + ", " + solde + ", " + decouvert + ")") #creation des entrees comptes courants
	if(0.25 > random.random()):	#25% de chances d'avoir un deuxieme compte courant
		if(decouvert):
			solde = str(arrondi(random.randint(-500, 2000)*0.75, 2))
		else:
			solde = str(arrondi(random.randint(0, 2000), 2))
		solde = str(arrondi(random.randint(0, 2000), 2))
		cursor.execute("INSERT INTO comptes_courants(id, id_client,solde,decouvert) VALUES(\"A" + str(random.randint(1, 9999)) + "\", " + str(i) + ", " + solde + ", " + decouvert + ")")

	solde = str(arrondi(random.uniform(0, 5000), 2))
	taux = str(arrondi(random.uniform(1, 2), 2))
	cursor.execute("INSERT INTO comptes_epargne(id, id_client,solde,taux) VALUES(\"B" + str(random.randint(1, 9999)) + "\", " + str(i) + ", " + solde + ", " + taux + ")") #creation des entrees comptes epargne
	if(0.20 > random.random()):	#20% de chances d'avoir un deuxieme compte epargne
		solde = str(arrondi(random.uniform(0, 5000)*0.75, 2))
		taux = str(arrondi(random.uniform(1, 2), 2))
		cursor.execute("INSERT INTO comptes_epargne(id, id_client,solde,taux) VALUES(\"B" + str(random.randint(1, 9999)) + "\", " + str(i) + ", " + solde + ", " + taux + ")")

#Affiche la bdd

print("-------------Comptes client : -------------")
result = cursor.execute("SELECT * FROM clients")	
for row in result:
	print(row)
print("-------------Comptes courants : -------------")
result = cursor.execute("SELECT * FROM comptes_courants")	
for row in result:
	print(row)
print("-------------Comptes epargne : -------------")
result = cursor.execute("SELECT * FROM comptes_epargne")	
for row in result:
	print(row)
conn.commit()

"""
clients :
-nom
-prenom
-date_inscription
-mail

tables :
comptes_courants(#id_client, solde, decouvert BOOL)
comptes_epargne(#id_client, solde, taux)
clients(id, nom, prenom, date_inscription, mail)
"""