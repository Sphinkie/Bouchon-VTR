# coding: "Latin-1"
# ==================================================================
# Gestion des logs
# ==================================================================

import logging
from logging.handlers import RotatingFileHandler

class LogFile:

	# ----------------------------------------------------------------------
	# Constructeur
	# ----------------------------------------------------------------------
	# Initialise le systeme de Logs, comportant :
	#  - Un affichage sur la console (niveau = INFO et au dessus)
	# ----------------------------------------------------------------------
	def __init__(self, filename, default_log_level=logging.DEBUG, log_size=2):
		# création de l'objet logger qui va nous servir à écrire dans les logs
		self.logger = logging.getLogger("socket")
		# on met le niveau du logger à DEBUG, comme ça il reçoit tout. Le filtre se faisant au niveau du fichier.
		self.logger.setLevel(logging.DEBUG)
		# ------------------------------------------------------------------
		# création d'un handler qui va rediriger chaque écriture de log sur la console
		self.stream_handler = logging.StreamHandler()
		self.stream_handler.setLevel(logging.INFO)
		self.logger.addHandler(self.stream_handler)
		# création d'un handler qui va rediriger chaque écriture dans un fichier
		self.file_handler=self.addLogFile(filename, default_log_level, log_size)
		# Initialisations des variables
		self.current_level = default_log_level

	# ----------------------------------------------------------------------
	#  - Un fichier de Logs (niveau paramétrable)
	# Parametres:
	#   - nom du fichier de log
	#   - log level initial pour le fichier de log
	#   - Taille Max du fichier de log (en MB)
	# ----------------------------------------------------------------------
	def addLogFile(self,filename, default_log_level, log_size):
		# ------------------------------------------------------------------
		# création d'un formateur qui ajoute l'heure et le niveau de log
		formatter = logging.Formatter('%(asctime)s	%(name)s	%(levelname)s : %(message)s')
		# ------------------------------------------------------------------
		# création d'un handler qui va rediriger les log vers un fichier en mode 'append', de 2 MB, avec 0 backup
		fh = RotatingFileHandler(filename, 'a', log_size*1000000, 0)
		# Fichier log: on regle le niveau de logs
		fh.setLevel(default_log_level)
		# Fichier log: utiliser le formateur créé précédement
		fh.setFormatter(formatter)
		# On ajoute ce handler au logger
		self.logger.addHandler(fh)
		# ------------------------------------------------------------------
		# Affichage du niveau de log courant
		self.current_level = default_log_level
		self.logger.info("LogFile: verbose log is {0}" .format(self.current_level==logging.DEBUG))
		return(fh)

	# ----------------------------------------------------------------------
	# On regle le niveau de logs du Fichier LOG
	# ----------------------------------------------------------------------
	def setLogLevel(self,log_level):
		self.current_level=log_level
		self.file_handler.setLevel(log_level)
		# self.logger.info("LogFile: verbose log is now {0}" .format(self.current_level==logging.DEBUG))

	def toggleLogLevel(self):
		# Fichier log: on regle le niveau de logs
		if self.current_level == logging.INFO:
			self.current_level=logging.DEBUG
		else:
			self.current_level=logging.INFO
		self.file_handler.setLevel(self.current_level)
		#self.logger.info("LogFile: verbose log is now {0}" .format(self.current_level==logging.DEBUG))

	def isVerbose(self):
		return (self.current_level==logging.DEBUG)
		
# ----------------------------------------------------------------------
# Test de la classe
# ----------------------------------------------------------------------
if ( __name__ == "__main__"):
   
   # Instancie un objet de test
   logs    = LogFile("LogFile.log")
   # demander un handler
   logger  = logs.getLogger()
   # Tester le handler
   logger.info("Test starting")
   # Tester le log level
   logs.setLogLevel(logging.INFO)
   logger.info("Niveau info (visible)")
   logger.debug("Niveau Debug (non visible)")
   logs.toggleLogLevel()
   logger.info("Niveau info (visible)")
   logger.debug("Niveau Debug (visible)")
   logs.toggleLogLevel()
   logger.info("Niveau info (visible)")
   logger.debug("Niveau Debug (non visible)")
   # Fin
   logger.info("End")




