# coding: UTF-8
# ==================================================================
# PROTOCOLE VTR
# ------------------------------------------------------------------
# selon documentation: BWM to MSW Protocol E2R8.pdf
# Pour tester: On peut utiliser le miniterminal de Python: py -m serial.tools.miniterm (-h pour avoir l'aide)
# ------------------------------------------------------------------
# 05/02/2018 | 1.0 | DDL | Version initiale
# ==================================================================

import logging
import serial
from struct     import *	# pour les unpack_from
from common.Common import *

# les status : ejected, cued , playing, stopped

class protocoleVTR:

	# Les variables déclarées ici sont accessibles avant les instanciations
	current_version = "v1.0"
	# pour avoir la liste des ports visibles: py -m serial.tools.list_ports
	

	# ------------------------------------------------------------------
	# Constructeur
	# Parametre: handler sur le fichier de log
	# ------------------------------------------------------------------
	def __init__(self, COMport):
		self.logger        = logging.getLogger("socket")
		self.COMport       = COMport
		self.new_TC		   = [b'\x00\x00\x00\x10',0]		# 10h00 au format FFSSMMHH
		self.full_message  = bytearray()
		# initialisation du port COM
		self.cnx = serial.Serial(COMport, 9600, timeout=0)  # timeout en secondes. 
	
	# ------------------------------------------------------------------
	# Renvoie le numero de port COM utilisé 
	# ------------------------------------------------------------------
	def getCOMport(self):
		return (self.COMport)

	# ------------------------------------------------------------------
	# Retourne le TC envoyé par le DC, au format FFSSMMHH
	# ------------------------------------------------------------------
	def getNewTC(self):
		return (self.new_TC[0])

	# ------------------------------------------------------------------
	# La fonction retourne la valeur du code de la reponse 
	# Exemple de message reçu:
	# 61.0C   01     6E
	# CMD1    DATA1  CHK   
	# ------------------------------------------------------------------
	def readCommand(self):
		msg_recu = self.cnx.read(10)		# read 10 bits (or timeout)
		if (not msg_recu): return(None)
		
		self.logger.debug(toHex(msg_recu, prefix="<< "))
		# on retourne la commande lue (dans un tuple)
		cmd = unpack_from('>H', msg_recu,0)[0]			 # format 'H' = unsigned int sur 2 bytes > little endian
		# ------------------------------------
		# ANALYSE DES MESSAGES RECUS
		# ------------------------------------
        # GET CURRENT TIME SENSE
		if cmd== 0x610C:
			return ('TIME_SENSE')
        # GET STATUS SENSE
		if cmd== 0x6120:
			return ('STATUS_SENSE')
        # GET EXTENDED STATUS
		if cmd== 0x6121:
			return ('EXT_STATUS')			# ** TODO
        # GET DEVICE TYPE
		if cmd== 0x0011:
			return ('DEVICE_TYPE')
        # FAST REWIND
		if cmd== 0x2020:
			self.buildResponseACK()
			return ('REW')
        # FAST FORWARD
		if cmd== 0x2010:
			self.buildResponseACK()
			return ('FFWD')
        # EJECT
		if cmd== 0x200F:
			self.buildResponseACK()
			return ('EJECT')
        # STOP
		if cmd== 0x2000:
			self.buildResponseACK()
			return ('STOP')
        # REC
		if cmd== 0x2002:
			self.buildResponseACK()
			return ('REC')
        # PLAY
		if cmd== 0x2001:
			self.buildResponseACK()
			return ('PLAY')
        # SHUTTLE FORWARD (souvent utilisé par le DC avec la vitesse 0 pour mettre en pause)
		if cmd== 0x2113:
			self.buildResponseACK()
			if (msg_recu[2]==0x00): return ('PAUSE')
			else: return ('SHTL')
        # CUE UP WITH DATA
		if cmd== 0x2431:
			self.buildResponseACK()
			# on récupère le TC recu
			self.new_TC = unpack_from('>L', msg_recu,2)	# format: 'L' = unsigned long sur 4 bytes | '>' = little endian
			return ('CUE')
		# Sinon
		self.logger.info("{c:04X}: unknown command".format(c=cmd))
		return ('NACK')


	# ------------------------------------------------------------------
	# message CURRENT TIME SENSE
	# ------------------------------------------------------------------
	def buildResponseTC(self,hh,mm,ss,ii):
		response_to_send = bytearray()
		# response code
		response_to_send.append(0x74)
		response_to_send.append(0x04)
		# LTC value (au format FFSSMMHH en BCD)
		response_to_send.append(toBCD(ii))
		response_to_send.append(toBCD(ss))
		response_to_send.append(toBCD(mm))
		response_to_send.append(toBCD(hh))
		self.addHeader(response_to_send)

	# ------------------------------------------------------------------
	# message DEVICE TYPE
	# ------------------------------------------------------------------
	def buildResponseDEV_TYPE(self):
		response_to_send = bytearray()
		# response code
		response_to_send.append(0x12)
		response_to_send.append(0x11)
		response_to_send.append(0x88)
		response_to_send.append(0x88)
		self.addHeader(response_to_send)
		
	# ------------------------------------------------------------------
	# message STATUS SENSE
	# ------------------------------------------------------------------
	def buildResponseSTATUS(self, local,status):
		# DATA0
		LOCAL        = 0x01 * (local=='local')			# la condition vaut 1 si elle est vraie, 0 sinon.
		CASSETTE_OUT = 0x20 * (status=='ejected')
		# DATA1
		STANDBY      = 0x80 * ((status=='cueing')or(status=='cued'))
		STOPPED      = 0x20 * ((status=='stopped')or(status=='cued'))
		EJECTING     = 0x10 * (status=='ejecting')		# état après reception de 20.0F EJECT
		REW		     = 0x08 * (status=='<<')
		FFWD	     = 0x04 * (status=='>>')
		RECORDING    = 0x02 * (status=='recording')
		PLAYING      = 0x01 * (status=='playing')
		# DATA2
		SERVOLOCK    = 0x80 * (status=='playing')
		SHUTTLE      = 0x20 * (status=='shuttle')
		JOG          = 0x10 * (status=='jog')
		VAR          = 0x08 * (status=='var')		    # ***TODO 
		TAPEREW      = 0x04 * (status=='rew')		    # ***TODO 
		STILL        = 0x02 * (status=='still')		    # ***TODO 
		CUE_UP_CPLD  = 0x01 * (status=='cued')		    # ***TODO 
		# DATA4
		CUED_UP      = 0x01 * (status=='cueing')		# ***TODO 
		# DATA8
		REC_INHIB    = 0x01 							# REC INHIBIT (ce bouchon ne gère pas le recording)
		
		
		response_to_send = bytearray()
		# response code
		response_to_send.append(0x79)
		response_to_send.append(0x20)
		# device status: STATUS
		response_to_send.append(CASSETTE_OUT + LOCAL)	    					 # DATA0
		response_to_send.append(STANDBY+STOPPED+RECORDING+PLAYING+EJECTING+REW+FFWD) # DATA1 
		response_to_send.append(SERVOLOCK+SHUTTLE+JOG+VAR+TAPEREW+STILL+CUE_UP_CPLD) # DATA2
		response_to_send.append(0x00)			# DATA3
		response_to_send.append(CUED_UP)		# DATA4
		response_to_send.append(0x00)			# DATA5
		response_to_send.append(0x00)			# DATA6
		response_to_send.append(0x00)			# DATA7
		response_to_send.append(REC_INHIB)		# DATA8
		self.addHeader(response_to_send)

	# ------------------------------------------------------------------
	# message NACK RESPONSE
	# ------------------------------------------------------------------
	def buildResponseNACK(self):
		response_to_send = bytearray()
		# NACK
		response_to_send.append(0x11)
		response_to_send.append(0x12)
		# Code erreur = software overrrun
		response_to_send.append(0x02)
		self.addHeader(response_to_send)
	
	# ------------------------------------------------------------------
	# message ACK RESPONSE
	# ------------------------------------------------------------------
	def buildResponseACK(self):
		response_to_send = bytearray()
		# ACK
		response_to_send.append(0x10)
		response_to_send.append(0x01)
		self.addHeader(response_to_send)
	
	# ------------------------------------------------------------------
	# Contruction du message complet: on ajoute la checksum à la fin
	# ------------------------------------------------------------------
	def addHeader(self, response_to_send):
		checksum = sum(response_to_send)%256
		response_to_send.append(checksum)
		self.full_message = response_to_send
	
	# ------------------------------------------------------------------
	# Envoie le message complet 
	# ------------------------------------------------------------------
	def sendResponse(self):
		self.cnx.write(self.full_message)
		# on ecrit les traces après l'envoi du message pour ne pas ralentir les traitements.
		# On n'a que 10ms pour répondre au DC.
		self.logger.debug (toHex(self.full_message, prefix=">> "))
		
