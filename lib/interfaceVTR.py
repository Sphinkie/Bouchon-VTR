# coding: UTF-8
# ==================================================================
# INTERFACE VTR
# Cette classe gère les différenst états que peut prendre le VTR
# et réagit aux commandes reçues du GUI ou de la RS
# ------------------------------------------------------------------
# 05/02/2018 | 1.0 | DDL | Version initiale
# ==================================================================

import tkinter
from common.Clock        import Clock
from common.StateMachine import StateMachine
from lib.protocoleVTR    import *

# les status : ejecting, ejected, cueing, cued , playing, stopped

class interfaceVTR:

	# Les variables déclarées ici sont accessibles avant les instanciations
	current_version = "v1.0"
	

	# ------------------------------------------------------------------
	# Constructeur
	# Parametre: handler sur le fichier de log
	# ------------------------------------------------------------------
	def __init__(self, fenetre, COMport):
		self.logger  = logging.getLogger("socket")
		self.mode    = 'remote'
		# on memorise la fenetre associée à ce compteur
		self.fenetre = fenetre
		# initialisation du port COM
		self.vtr = protocoleVTR(COMport)
		# initialisation de la machine à état
		self.state = StateMachine('stopped')
		# initialisation de l'horloge
		self.clock = Clock()
		self.clock.initCounterWithSeconds(0)
		self.logger.info("interfaceVTR {ver}: Starting".format(ver=self.current_version))

	# ------------------------------------------------------------------
	# Renvoie le numero de port utilisé 
	# ------------------------------------------------------------------
	def getCOMport(self):
		return self.vtr.getCOMport()

	# ------------------------------------------------------------------
	# Passe en mode LOCAL
	# ------------------------------------------------------------------
	def setStatusToLocal(self):
		self.mode='local'
		b=self.fenetre.nametowidget('boutonLocal')
		b.configure(state=tkinter.DISABLED, bg="gold")
		b=self.fenetre.nametowidget('boutonRemote')
		b.configure(state=tkinter.NORMAL, bg="lightgrey")
		if (self.state.getStatus()!='ejected'): 
			# On dégrise les boutons PLAY et STOP
			#print (self.fenetre.winfo_children())
			b=self.fenetre.nametowidget('boutonPlay')
			b.configure(state=tkinter.NORMAL)
			b=self.fenetre.nametowidget('boutonStop')
			b.configure(state=tkinter.NORMAL)
			b=self.fenetre.nametowidget('boutonFF')
			b.configure(state=tkinter.NORMAL)
			b=self.fenetre.nametowidget('boutonRW')
			b.configure(state=tkinter.NORMAL)
			

	# ------------------------------------------------------------------
	# Passe en mode REMOTE
	# ------------------------------------------------------------------
	def setStatusToRemote(self):
		self.mode='remote'
		# On grise les boutons PLAY et STOP
		b=self.fenetre.nametowidget('boutonPlay')
		b.configure(state=tkinter.DISABLED)
		b=self.fenetre.nametowidget('boutonStop')
		b.configure(state=tkinter.DISABLED)
		b=self.fenetre.nametowidget('boutonFF')
		b.configure(state=tkinter.DISABLED)
		b=self.fenetre.nametowidget('boutonRW')
		b.configure(state=tkinter.DISABLED)
		b=self.fenetre.nametowidget('boutonLocal')
		b.configure(state=tkinter.NORMAL, bg="lightgrey")
		b=self.fenetre.nametowidget('boutonRemote')
		b.configure(state=tkinter.DISABLED, bg="gold")

	# ------------------------------------------------------------------
	# Passe en PLAY (si local)
	# ------------------------------------------------------------------
	def play(self):
		# le bouton est actif si on est en Local
		# la fonction est active si on est en Stopped ou Cued
		status = self.state.getStatus()
		if ((status=='stopped')or(status=='cued')):
			self.state.setStatus('playing')
			# on initialise le compteur avec la valeur à laquelle on l'avait arrêté
			current_counter = self.clock.getCounterValue()
			self.clock.initCounterWithSeconds(current_counter)
			self.clock.start()
			# On grise les boutons PLAY, FF et RW
			b=self.fenetre.nametowidget('boutonPlay')
			b.configure(state=tkinter.DISABLED, bg="lime")
			b=self.fenetre.nametowidget('boutonFF')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonRW')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonStop')
			b.configure(bg="yellowgreen")

	# ------------------------------------------------------------------
	# Passe en Fast Forward
	# ------------------------------------------------------------------
	def fastForward(self):
		# le bouton est grisé si on est en Local
		# la fonction est active si on est en Stopped ou Cued
		status = self.state.getStatus()
		if ((status=='stopped')or(status=='cued')):
			self.state.setStatus('>>')
			# on initialise le compteur avec la valeur à laquelle on l'avait arrêté
			current_counter = self.clock.getCounterValue()
			self.clock.initCounterWithSeconds(current_counter)
			self.clock.start(10)	# Speed x10
			# On grise les boutons PLAY, FF et RW
			b=self.fenetre.nametowidget('boutonPlay')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonFF')
			b.configure(state=tkinter.DISABLED, bg="lime")
			b=self.fenetre.nametowidget('boutonRW')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonStop')
			b.configure(bg="yellowgreen")

	# ------------------------------------------------------------------
	# Passe en Fast Rewind
	# ------------------------------------------------------------------
	def fastRewind(self):
		# le bouton est grisé si on est en Local
		# la fonction est active si on est en Stopped ou Cued
		status = self.state.getStatus()
		if ((status=='stopped')or(status=='cued')):
			self.state.setStatus('<<')
			# on initialise le compteur avec la valeur à laquelle on l'avait arrêté
			current_counter = self.clock.getCounterValue()
			self.clock.initCounterWithSeconds(current_counter)
			self.clock.start(-10)	# Speed x10
			# On grise les boutons PLAY, FF et RW
			b=self.fenetre.nametowidget('boutonPlay')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonFF')
			b.configure(state=tkinter.DISABLED, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonRW')
			b.configure(state=tkinter.DISABLED, bg="lime")
			b=self.fenetre.nametowidget('boutonStop')
			b.configure(bg="yellowgreen")

	# ------------------------------------------------------------------
	# Passe en STOP 
	# ------------------------------------------------------------------
	def stop(self):
		self.state.setStatus('stopped')
		self.clock.stop()
		# On dégrise les boutons PLAY, FF et RW
		b=self.fenetre.nametowidget('boutonPlay')
		b.configure(state=tkinter.NORMAL, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonFF')
		b.configure(state=tkinter.NORMAL, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonRW')
		b.configure(state=tkinter.NORMAL, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonStop')
		b.configure(bg="lime")


	# ------------------------------------------------------------------
	# Commande PAUSE reçue
	# ------------------------------------------------------------------
	def pause(self):
		self.state.setStatus('cued')
		self.clock.stop()
		
	# ------------------------------------------------------------------
	# Commande CUE reçue  
	# parametre =  TC cible au format FFSSMMHH
	# ------------------------------------------------------------------
	def cue(self, new_tc):
		# On positionne le compteur à la valeur demandée
		self.clock.stop()
		self.clock.resetCounter()
		self.clock.initCounterWithFFSSMMHH(new_tc)
		# On positionne le status
		self.state.setStatus('cueing')
		self.state.setStatusIn('cued',delay=2)
		

	# ------------------------------------------------------------------
	# Ejecte la cassette
	# ------------------------------------------------------------------
	def eject(self):
		self.state.setStatus('ejecting')
		self.state.setStatusIn('ejected', delay=1)	# après dela de 1 seconde
		self.clock.stop()
		self.clock.resetCounter()
		b=self.fenetre.nametowidget('boutonEject')
		b.configure(state=tkinter.DISABLED)
		b=self.fenetre.nametowidget('boutonInsert')
		b.configure(state=tkinter.NORMAL)
		b=self.fenetre.nametowidget('boutonPlay')
		b.configure(state=tkinter.DISABLED, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonFF')
		b.configure(state=tkinter.DISABLED, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonRW')
		b.configure(state=tkinter.DISABLED, bg="yellowgreen")
		b=self.fenetre.nametowidget('boutonStop')
		b.configure(state=tkinter.DISABLED, bg="yellowgreen")

	# ------------------------------------------------------------------
	# Insertion d'une nouvelle cassette
	# par defaut, le TCin de la cassette insérée est 10:00:00
	# ------------------------------------------------------------------
	def insert(self, tcin=36000):
		self.state.setStatus('stopped')
		self.clock.stop()
		self.clock.resetCounter()
		self.clock.initCounterWithSeconds(tcin)
		b=self.fenetre.nametowidget('boutonEject')
		b.configure(state=tkinter.NORMAL)
		b=self.fenetre.nametowidget('boutonInsert')
		b.configure(state=tkinter.DISABLED)
		if (self.mode=='local'): 
			# On dégrise les boutons PLAY et STOP
			b=self.fenetre.nametowidget('boutonPlay')
			b.configure(state=tkinter.NORMAL, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonStop')
			b.configure(state=tkinter.NORMAL, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonFF')
			b.configure(state=tkinter.NORMAL, bg="yellowgreen")
			b=self.fenetre.nametowidget('boutonRW')
			b.configure(state=tkinter.NORMAL, bg="yellowgreen")
		
	# ------------------------------------------------------------------
	# met à jour le status affiché
	# ------------------------------------------------------------------
	def updateDisplay(self, mode_var, status_var, compteur_var):
		# Refresh de l'affichage du mode
		mode_var.set(self.mode)
		# Refresh de l'affichage du status
		status_var.set(self.state.getStatus())
		# Refresh de l'affichage du compteur
		if (self.state.getStatus()=='ejected'):
			compteur_var.set("--:--:--:--")
		elif (self.state.getStatus()=='cueing'):
			compteur_var.set(">>:>>")
		else:
			h,m,s,i = self.clock.getCounterHMSI()
			compteur_var.set("{h:02}:{m:02}:{s:02}:{i:02}".format(h=h%24,m=m,s=s,i=i))	# h modulo 24
		# Lecture des octets reçus, et envoi de la réponse
		message = self.vtr.readCommand()
		if (message):
			self.buildResponse(message)
			self.vtr.sendResponse()
		# Appel périodique (il faut répondre en moins de 10 ms)
		self.fenetre.after(5, self.updateDisplay, mode_var, status_var, compteur_var)

	# ------------------------------------------------------------------
	# Construit le message a renvoyer
	# ------------------------------------------------------------------
	def buildResponse(self, code_reponse):
		if   (code_reponse==None)            : pass
		elif (code_reponse=='TIME_SENSE')    : 
			h,m,s,i = self.clock.getCounterHMSI()
			self.vtr.buildResponseTC(h,m,s,i)
		elif (code_reponse=='STATUS_SENSE')  : self.vtr.buildResponseSTATUS(self.mode, self.state.getStatus())
		elif (code_reponse=='NACK')          : self.vtr.buildResponseNACK()
		elif (code_reponse=='DEVICE_TYPE')	 : self.vtr.buildResponseDEV_TYPE()
		elif (code_reponse=='REW')			 : self.fastRewind()
		elif (code_reponse=='FFWD')			 : self.fastForward()
		elif (code_reponse=='EJECT')		 : self.eject()
		elif (code_reponse=='STOP')		 	 : self.stop()
		elif (code_reponse=='REC')		 	 : pass			# le recording par le VTR n'est pas géré.
		elif (code_reponse=='PLAY')		 	 : self.play()
		elif (code_reponse=='SHTL')		 	 : pass			# SHUTTLE non géré
		elif (code_reponse=='PAUSE')	 	 : self.pause()
		elif (code_reponse=='CUE')		 	 : self.cue(self.vtr.getNewTC())
		else: self.logger.info("Unknown Response: {r}".format(r=code_reponse))
