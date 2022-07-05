import sqlite3

class ClientBanque:
	"""
	Classe chargée des manipulations et de récupérer les infos. sur la base de données

	rechercheClientIdentite
	rechercheClientNumCompte
	consulteCompteCourant
	consulteCompteEpargne
	modifAutorisationDecouvert
	virement
	actualiseComptesEpargne
	getListeDecouverts
	supprCompte
	"""

	def __init__(self, nomBDD='banque.db'):
		self.conn = sqlite3.connect("banque.db")
		self.cursor = self.conn.cursor()

	def rechercheClientIdentite(self, nom, prenom):
		return self.cursor.execute("SELECT * FROM clients WHERE LOWER(nom)=\"" + nom.lower() + "\" AND LOWER(prenom)=\"" + prenom.lower() + "\";").fetchall()

	def rechercheClientNumCompte(self, numCompte):
		try:
			return self.cursor.execute("SELECT * FROM clients WHERE id=\"" + str(numCompte) + "\";").fetchall()
		except:
			return []

	def consulteCompteCourant(self, idCompte):
		try:
			return self.cursor.execute("SELECT comptes_courants.id, id_client, solde, decouvert FROM comptes_courants JOIN clients ON clients.id=comptes_courants.id_client WHERE id_client=" + str(idCompte)).fetchall()
		except:
			return []

	def consulteCompteEpargne(self, idCompte):
		return self.cursor.execute("SELECT comptes_epargne.id, id_client, solde, taux FROM comptes_epargne JOIN clients ON clients.id=comptes_epargne.id_client WHERE id_client=" + str(idCompte)).fetchall()

	def modifAutorisationDecouvert(self, idCompte, autorisation):#Autorisation est un float
		numCompteClient = idCompte.split('-')[0]
		numCompteCourant = idCompte.split('-')[1]
		self.cursor.execute("UPDATE comptes_courants SET decouvert=" +str(autorisation) + " WHERE id_client=\"" + str(numCompteClient) + "\" AND comptes_courants.id=\"" + str(numCompteCourant) + "\"")

	def virement(self, numCompteA, numCompteB, montant):
		montant = int(montant)
		numCompteClientA = numCompteA.split('-')[0]
		numCompteActifA = numCompteA.split('-')[1]
		numCompteClientB = numCompteB.split('-')[0]
		numCompteActifB = numCompteB.split('-')[1]

		soldeOrigineA = float(self.consulteCompteCourant(numCompteClientA)[0][2])
		soldeOrigineB = float(self.consulteCompteCourant(numCompteClientB)[0][2])
		print(self.consulteCompteCourant(numCompteClientA))
		if(numCompteActifA[0] == 'A'):
			if(soldeOrigineA-montant < self.consulteCompteCourant(numCompteClientA)[0][3]):
				return "Le solde n'est pas suffisant pour faire ce virement"

		if(numCompteActifB[0] == 'B'):
			if(soldeOrigineB+montant < self.consulteCompteCourant(numCompteClientB)[0][3]):
				return "Le solde n'est pas suffisant pour faire ce virement"

		print(soldeOrigineA-montant)
		print(soldeOrigineB+montant)
		if(self.consulteCompteCourant(numCompteClientA) != [] or self.consulteCompteCourant(numCompteClientB) != []): #On vérifie que le compte existe
			if(numCompteActifA[0] == 'A'):
				print(numCompteClientA)
				self.cursor.execute("UPDATE comptes_courants SET solde=" +str(soldeOrigineA-montant) + " WHERE id=\"" + str(numCompteActifA) + "\" AND exists(select id from clients where id=\"" + str(numCompteClientA) + "\")")
			else:
				self.cursor.execute("UPDATE comptes_epargne SET solde=" +str(soldeOrigineA-montant) + " WHERE id=\"" + str(numCompteActifA) + "\" AND exists(select id from clients where id=\"" + str(numCompteClientA) + "\")")
				if(numCompteActifB[0] == 'A'):
					print(numCompteActifB)
					self.cursor.execute("UPDATE comptes_courants SET solde=" +str(soldeOrigineB+montant) + " WHERE id=\"" + str(numCompteActifB) + "\" AND exists(select id from clients where id=\"" + str(numCompteClientB) + "\")")
				else:
					self.cursor.execute("UPDATE comptes_courants SET solde=" +str(soldeOrigineB+montant) + " WHERE id=\"" + str(numCompteActifB) + "\" AND exists(select id from clients where id=\"" + str(numCompteClientB) + "\")")
				return 0
		else:
			return "Le compte que vous recherchez n'existe pas"

	def actualiseComptesEpargne(self):
		comptesEpargne = self.cursor.execute("SELECT * FROM comptes_epargne").fetchall()
		for compte in comptesEpargne:
			nouveauSolde = compte[2]*compte[3]
			self.cursor.execute("UPDATE comptes_epargne SET solde=" +str(nouveauSolde) + " WHERE id_client=\"" + str(compte[1]) + "\" AND id=\"" + str(compte[0]) + "\"")

	def getListeDecouverts(self):
		return self.cursor.execute("SELECT comptes_courants.id, clients.id, nom, prenom, solde, mail FROM comptes_courants JOIN clients ON comptes_courants.id_client=clients.id WHERE solde < 0").fetchall()

	def supprCompte(self, idCompte):
		try:
			self.cursor.execute("DELETE FROM comptes_courants WHERE id_client=" + str(idCompte))
			self.cursor.execute("DELETE FROM comptes_epargne WHERE id_client=" + str(idCompte))
			self.cursor.execute("DELETE FROM clients WHERE id=" + str(idCompte))
		except:
			pass

	def __del__(self):
		self.conn.commit()

"""
tables :
comptes_courants(#id_client, solde, decouvert BOOL)
comptes_epargne(#id_client, solde, taux)
clients(id, nom, prenom, date_inscription, mail)
"""