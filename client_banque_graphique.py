from tkinter import *
from tkinter.messagebox import *
from client_banque import ClientBanque

class FenetreBanque:
	"""
	Classe chargée de l'affichage graphique des fonctionnalités du client

	initFenetre : Initialisation des éléments en fonction de l'onglet sélectionné(recherche/virement)
	ongletRecherche : Reinitialise l'affichage pour passer à l'onglet recherche
	ongletVirement : Reinitialise l'affichage pour passer à l'onglet virement
	actualiseSoldesEpargne : Actualise tous les soldes des comptes épargne
	rechercheCompteClient : Recherche le compte d'un client
	rechercheCompteCourant : Recherche les comptes courants d'un client
	rechercheCompteEpargne : Recherche les comptes épargne d'un client
	listeDecouverts : Liste tous les comptes courants à découvert
	validerVirement : Valide et conclue le virement
	afficheComptes : Affiche une liste de comptes en fonction des attributs envoyés
	supprimerCompte : Supprime tous les comptes liés à un client, puis supprime le client
	defineAutorisationDecouvert : Inverse l'autorisation de découvert
	"""

	def __init__(self, width=0, height=0):
		self.clientBanque = ClientBanque()
		self.width = width
		self.height = height

		self.fenetre = Tk()
		self.initFenetre()

		self.fenetre.mainloop()

	def initFenetre(self, onglet="recherche"):
		delete_frame(self.fenetre)

		self.mainCanvas = Canvas(width=self.width, height=self.height)
		self.mainCanvas.grid()

		###################Barre de controle

		self.frameActions = Frame(self.fenetre, width=100)
		self.frameActions.grid(row=0, column=3, padx=10, pady=10, sticky="n")
		self.actualiseSoldesEpargneBtn = Button(self.frameActions, text ='Actualiser les soldes d\'épargne', command=self.actualiseSoldesEpargne).grid(row=0, column=0, pady=20, padx=20)
		self.afficheDecouvertsBtn = Button(self.frameActions, text ='Liste découverts', command=self.listeDecouverts).grid(row=1, column=0, pady=20, padx=20)
		

		###################Onglet recherche##############

		self.frameRechercheIdentite = Frame(self.fenetre, borderwidth=2, relief="groove")	#Frame de recherche par nom prenom
		self.frameRechercheIdentite.grid(row=0, column=1, padx=10, pady=10, sticky="n")
		Label(self.frameRechercheIdentite, text="Recherche d'un compte").grid(row=0, column=1, pady=15, padx=20)

		Label(self.frameRechercheIdentite, text="Nom : ").grid(row=1, column=1, pady=15)
		self.nomInput = Entry(self.frameRechercheIdentite, textvariable="Nom", width=10)
		self.nomInput.grid(row=1, column=2)

		Label(self.frameRechercheIdentite, text="Prénom : ").grid(row=2, column=1, pady=15)
		self.prenomInput = Entry(self.frameRechercheIdentite, textvariable="Prenom", width=10)
		self.prenomInput.grid(row=2, column=2, pady=5, padx=10)

        #Entree
		Label(self.frameRechercheIdentite, text="Numéro de compte : ").grid(row=3, column=1, pady=15)
		self.numCompteInput = Entry(self.frameRechercheIdentite, textvariable="Numéro de compte", width=10)
		self.numCompteInput.grid(row=3, column=2, padx=10)

        #Affiche tous les bouttons d'action
		self.recherchecompteClientIdentiteBtn = Button(self.frameRechercheIdentite, command=self.rechercheCompteClient, text ='Compte client')
		self.recherchecompteClientIdentiteBtn.grid(row=4, column=1, pady=10)
		self.rechercheCompteCourantIdentiteBtn = Button(self.frameRechercheIdentite, command=self.rechercheCompteCourant, text ='Compte(s) courant(s)')
		self.rechercheCompteCourantIdentiteBtn.grid(row=4, column=2, pady=10, padx=20)
		self.rechercheCompteEpargneIdentiteBtn = Button(self.frameRechercheIdentite, command=self.rechercheCompteEpargne, text ='Compte(s) épargne')
		self.rechercheCompteEpargneIdentiteBtn.grid(row=4, column=3, pady=10, padx=20)
		self.supprimerCompteBouton = Button(self.frameRechercheIdentite, command=self.supprimerCompte, text ='Supprimer le compte')
		self.supprimerCompteBouton.grid(row=5, column=2, pady=20, padx=20)
		

		###############Onglet virements###############
		self.frameVirement = Frame(self.fenetre, borderwidth=2, relief="groove")
		self.frameVirement.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
		Label(self.frameVirement, text="Effectuer un virement").grid(row=0, column=0, pady=15, padx=20)

		###
		self.frameVirementA = Frame(self.frameVirement, borderwidth=2, relief="groove")
		self.frameVirementA.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
		Label(self.frameVirementA, text="Compte A").grid(row=0, column=1, pady=15, padx=20)
		Label(self.frameVirementA, text="Numéro de compte : ").grid(row=3, column=1, pady=15)
		self.numCompteA = Entry(self.frameVirementA, textvariable="numCompteA", width=10)
		self.numCompteA.grid(row=3, column=2, pady=5, padx=10)
		###
		self.frameVirementB = Frame(self.frameVirement, borderwidth=2, relief="groove")
		self.frameVirementB.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
		Label(self.frameVirementB, text="Compte B").grid(row=0, column=1, pady=15, padx=20)
		Label(self.frameVirementB, text="Numéro de compte : ").grid(row=3, column=1, pady=15)
		self.numCompteB = Entry(self.frameVirementB, textvariable="numCompteB", width=10)
		self.numCompteB.grid(row=1, column=2, pady=5, padx=10)
		###
		self.frameVirementValider = Frame(self.frameVirement, borderwidth=2, relief="groove")
		self.frameVirementValider.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
		Label(self.frameVirementValider, text="Montant : ").grid(row=0, column=0, pady=15)
		self.montantInput = Entry(self.frameVirementValider, textvariable="montant", width=10)
		self.montantInput.grid(row=0, column=1, pady=5, padx=10)
		self.validerVirementBtn = Button(self.frameVirementValider, text ='Valider', width=5, height=2, command=self.validerVirement)
		self.validerVirementBtn.grid(row=1, column=0, padx=20, pady=20, sticky="n")

		#################Modification de découvert###################
		self.frameDecouvert = Frame(self.fenetre, borderwidth=2, relief="groove")
		self.frameDecouvert.grid(row=0, column=2, padx=10, pady=10, sticky="nw")
		Label(self.frameDecouvert, text="Changer l'autorisation de découvert").grid(row=0, column=0, pady=15, padx=20)

		self.frameSelectCompte = Frame(self.frameDecouvert, borderwidth=2, relief="groove")
		self.frameSelectCompte.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

		Label(self.frameSelectCompte, text="Numéro de compte : ").grid(row=0, column=0, pady=15)
		self.numCompte = Entry(self.frameSelectCompte, textvariable="numCompte", width=10)
		self.numCompte.grid(row=0, column=1, pady=5, padx=10)

		Label(self.frameSelectCompte, text="Nouveau découvert : ").grid(row=1, column=0, pady=15)
		self.nouveauDecouvert = Entry(self.frameSelectCompte, textvariable="nouveauDecouvert", width=10)
		self.nouveauDecouvert.grid(row=1, column=1, pady=5, padx=10)
		###
		
		self.validerVirementBtn = Button(self.frameSelectCompte, text ='Valider', width=5, height=2, command=self.changerDecouvert)
		self.validerVirementBtn.grid(row=3, column=0, padx=20, pady=20, sticky="n")
		##########################################

	def changerDecouvert(self):
		idCompte = self.numCompte.get()
		nouveauDecouvert = self.nouveauDecouvert.get()
		self.clientBanque.modifAutorisationDecouvert(idCompte, nouveauDecouvert)

	def actualiseSoldesEpargne(self):
		if askyesno("", 'Êtes-vous sûr de vouloir actualiser tous les soldes d\'épargne ?'):
			self.clientBanque.actualiseComptesEpargne()
			showinfo("", "Les soldes ont bien été actualisés")

	def rechercheCompteClient(self):		#Affiche les infos d'un compte client recherché
		nom = self.nomInput.get()
		prenom = self.prenomInput.get()
		numCompte = self.numCompteInput.get()
		if(nom != "" and prenom != ""):
			clients = self.clientBanque.rechercheClientIdentite(nom, prenom)
		else:
			clients = self.clientBanque.rechercheClientNumCompte(numCompte)

		if(clients != "" and clients != []):
			self.afficheComptes(clients, "client")
		else:
			showerror("Compte", "Veuillez entrer un numéro de compte valide")

	def rechercheCompteCourant(self):	#Affiche les comptes courants d'un client
		nom = self.nomInput.get()
		prenom = self.prenomInput.get()
		numCompte = self.numCompteInput.get()
		if(nom != "" and prenom != ""):
			idCompte = self.clientBanque.rechercheClientIdentite(nom, prenom)[0][0]
		else:
			idCompte = numCompte

		if(idCompte != "" and idCompte != []):
			self.afficheComptes(self.clientBanque.consulteCompteCourant(idCompte), "courant")
		else:
			showerror("Compte", "Veuillez entrer un numéro de compte valide")

	def rechercheCompteEpargne(self):	#Affiche les comptes epargne d'un client
		nom = self.nomInput.get()
		prenom = self.prenomInput.get()
		numCompte = self.numCompteInput.get()
		if(nom != "" and prenom != ""):
			idCompte = self.clientBanque.rechercheClientIdentite(nom, prenom)[0][0]
		else:
			idCompte = numCompte

		if(idCompte != "" and idCompte != []):
			self.afficheComptes(self.clientBanque.consulteCompteEpargne(idCompte), "epargne")
		else:
			showerror("Compte", "Veuillez entrer un numéro de compte valide")

	def listeDecouverts(self):	#Liste les comptes à découvert
		#self.afficheComptes(self.clientBanque.getListeDecouverts(), "decouvert")

		self.frameAfficheur = Frame(self.fenetre, borderwidth=2, relief="groove", width=500, height=200)
		self.frameAfficheur.grid(row=2, padx=10, pady=20, sticky="n")

		self.afficheComptes(self.clientBanque.getListeDecouverts(), "decouvert")

	def validerVirement(self):
		numCompteA = self.numCompteA.get()
		numCompteB = self.numCompteB.get()
		montant = self.montantInput.get()
		if(not montant.isdigit()):
			showerror("Virement", "Veuillez entrer un montant valide")
			return 0
		if askyesno("Virement", 'Confirmez-vous ce virement ?'):
			resultatVirement = self.clientBanque.virement(numCompteA, numCompteB, montant)
			if(resultatVirement != 0):
				showerror("Virement", resultatVirement)	#Affiche l'erreur retournee par la tentative de virement(pas assez d'argent, compte inexistant)
			else:
				showinfo("Virement", "Votre virement à bien été transféré")
		else:
			showwarning('Virement', 'Votre virement à été annulé')

	def supprimerCompte(self):
		nom = self.nomInput.get()
		prenom = self.prenomInput.get()
		numCompte = self.numCompteInput.get()
		if(nom != "" and prenom != ""):       #Si les input nom et prenom sont vides, on utilise le num de compte
			idCompte = self.clientBanque.rechercheClientIdentite(nom, prenom)[0][0]
		else:
			idCompte = numCompte

		if(idCompte == "" or idCompte == []):
			showerror("Compte", "Veuillez entrer un numéro de compte valide")
			return 0

		if askyesno("", 'Êtes-vous sûr de vouloir supprimer ce compte ? '):
			self.clientBanque.supprCompte(idCompte)
			showinfo("Suppression", "Le compte à bien été supprimé")

	def defineAutorisationDecouvert(self):
		nom = self.nomInput.get()
		prenom = self.prenomInput.get()
		idCompte = self.numCompteInput.get()
		if(nom != "" and prenom != ""):
			idCompte = self.clientBanque.rechercheClientIdentite(nom, prenom)[0][0]

		if(self.clientBanque.consulteCompteCourant(idCompte)[0][2]):
			self.clientBanque.modifAutorisationDecouvert(idCompte, 0)
			showinfo("Découvert", "L'autorisation de découvert à été désactivée sur ce compte")
		else:
			self.clientBanque.modifAutorisationDecouvert(idCompte, 1)
			showinfo("Découvert", "L'autorisation de découvert à été activée sur ce compte")

	def afficheComptes(self, comptes, typeCompte):     #Utilise une liste d'attributs et de comptes afin de les afficher sous forme de tableau
		if(typeCompte == "client"):
			attributs = ["Numéro compte", "Nom", "Prénom", "Date d'inscription", "Mail"]
		elif(typeCompte == "courant"):
			attributs = ["Numéro compte courant", "Numéro compte", "Solde", "Découvert"]
		elif(typeCompte == "epargne"):
			attributs = ["Numéro compte épargne", "Numéro compte", "Solde", "Taux"]
		elif(typeCompte == "decouvert"):              #Permet de recuperer l'email
			attributs = ["Numéro compte courant", "Numéro compte", "Nom", "Prénom", "Solde", "Mail"]
		self.initFenetre()

		self.frameAfficheur = Frame(self.fenetre, borderwidth=2, relief="groove", width=500, height=200)
		self.frameAfficheur.grid(row=1, column=1, padx=10, pady=20, sticky="n")

		padx = 20
		for i in range(len(attributs)):   #Parcourt la liste des attributs pour les afficher comme sur un tableau
			Label(self.frameAfficheur, text=attributs[i]).grid(row=0, column=i, pady=15, padx=padx)

		for i in range(len(comptes)):     #Parcourt les resultats envoyes par le client
			for j in range(len(comptes[i])):
				Label(self.frameAfficheur, text=comptes[i][j]).grid(row=i+1, column=j, pady=15, padx=padx)

def delete_frame(frame):		#Permet de vider une frame
    for widget in frame.winfo_children():
        widget.destroy()



FenetreBanque = FenetreBanque()



"""
- Rechercher un client(nom+prenom/numClient)
- Consulter les comptes courants d'un client
- Consulter les comptes epargnes d'un client
- Modifier l'autorisation de decouvert
- Realiser un virement entre deux comptes
- Actualiser tous les soldes des comptes epargne
- Recuperer la liste des personnes a decouvert
- Supprimer un compte ou un utilisateur

"""