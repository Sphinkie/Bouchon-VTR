# coding: UTF-8
# ==================================================================
# Machine a état, permettant de simuler un device physique
# ==================================================================
import time

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class StateMachine(object):


	# ----------------------------------------------------------------
	# initialisation
	# ----------------------------------------------------------------
	def __init__(self, default_status=0):
		self.status_queue = list()
		self.default_status = default_status

	# ----------------------------------------------------------------
	# Définit le prochain status de la machine à états 
	# time = heure d'activation de ce status (en nombre de secondes depuis minuit)
	# ----------------------------------------------------------------
	def setStatus(self, status, time=None):
		self.status_queue.append((status,time))
		#if (time): print (time)

	# ----------------------------------------------------------------
	# Définit le prochain status de la machine à états 
	# delay = délai avant l'activation de ce status (en nombre de secondes)
	# ----------------------------------------------------------------
	def setStatusIn(self, status, delay=0):
		# on récupère le datetime courant
		tm = time.localtime()
		# on calcule l'heure ourante (en nb de secondes) depuis minuit
		today_seconds = tm.tm_hour * 3600 + tm.tm_min * 60 + tm.tm_sec
		# on ajoute le délai demandé
		new_time = today_seconds+delay
		self.status_queue.append((status,new_time))


	# ----------------------------------------------------------------
	# Ajoute une séquence de statuts à la machine à états
	# ----------------------------------------------------------------
	def addSequence(self, *status_list):
		for status in status_list:
			self.status_queue.append((status,None))


	# ----------------------------------------------------------------
	# on renvoie le status en cours, et on l'enleve de la queue si nécessaire
	# ----------------------------------------------------------------
	def getStatus(self):
		# S'il n'y a aucun element dans la queue: on retourne le status par défaut
		if len(self.status_queue)==0:
			return self.default_status
		# S'il y a 1 seul element dans la queue: on retourne son status
		if len(self.status_queue)==1:
			first_item=self.status_queue[0]
			return first_item[0]
		# On récupère l'heure du 2nd élement
		item_timing = self.status_queue[1][1]
		# On récupère l'heure courante
		tm = time.localtime()
		current_seconds = tm.tm_hour * 3600 + tm.tm_min * 60 + tm.tm_sec
		# Sinon, si le 2nd élement n'est pas horodaté (immédiat): on pop et on retourne le 1er status
		if (item_timing==None):
			first_item=self.status_queue.pop(0)
			return first_item[0]
		# Sinon, si l'horodatage du 2nd item est passé: on pop le 1er item, et on retourne le 2eme status
		if (item_timing<current_seconds):
			#print ("timer reached");
			self.status_queue.pop(0)
			next_item=self.status_queue[0]
			return next_item[0]
		# Sinon (horodatage du 2nd item pas encore atteint), on retourne le 1er status
		else:
			#print ("timer not reached");
			#if (current_seconds): print (current_seconds)
			first_item=self.status_queue[0]
			return first_item[0]


# ----------------------------------------------------------------------
# Test de la classe
# ----------------------------------------------------------------------
if ( __name__ == "__main__"):

	my_machine = StateMachine('empty')

	print ("initial state: attendu 0-0-0")
	print (my_machine.status_queue)
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())

	print ("Constant state: attendu 1-1-1-1-1")
	my_machine.setStatus(1)
	print (my_machine.status_queue)
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
		
	print ("Sequence: attendu 1-2-3-3-3")
	my_machine.addSequence(2,3)
	print (my_machine.status_queue)
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())

	print ("Sequence: attendu 3-4-5-6-6")
	my_machine.addSequence(4,5,6)
	print (my_machine.status_queue)
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())
	print (my_machine.getStatus())

	print ("timestamped status: attendu 6-6...7-7-7")
	tm = time.localtime()
	current_seconds = tm.tm_hour * 3600 + tm.tm_min * 60 + tm.tm_sec
	my_machine.setStatus(7,current_seconds+2)
	print (my_machine.status_queue)
	print (my_machine.getStatus())
	time.sleep(1)
	print (my_machine.getStatus())
	time.sleep(1)
	print (my_machine.getStatus())
	time.sleep(1)
	print (my_machine.getStatus())
	time.sleep(1)
	print (my_machine.getStatus())


