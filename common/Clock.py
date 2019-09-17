# coding: UTF-8
# ==================================================================
# Gestion du temps: objet Timer simple
# ==================================================================
# v3.0	| 08/02/2018 | DDL |	gestion de la vitesse d'avancement
# ==================================================================
# usage:
#		from lib.Clock import *
#   	cpt = Clock()
#       cpt.initCounterWithSeconds(3600)		# 01h00m00
#		cpt.start()
#		...
# 		cpt.getCounterValue()	 	# seconds 
#       cpt.getCounterHMSI()		# hh, mm, ss, ii
#		...
#		cpt.stop()
#		cpt.resetCounter()
# ----------------------------------------------------------------
import time
from common.Common import *


class Clock(object):
# ----------------------------------------------------------------
# le timer: 
#       start() et stop() commandent le timer.
#       getElapsedTime donne le temps écoulé entre les deux
# le counter:
#       initCounter() 		initialise le compteur à une certaine valeur
#       start() 			démarre le counter
#       getCounterValue() 	renvoie sa valeur qui a aumgmenté en fonction du temps écoulé.
# ----------------------------------------------------------------


	# ----------------------------------------------------------------
	# Initialize a new `Clock`, but do not start timing.
	# ----------------------------------------------------------------
	def __init__(self):
		self.start_time    = None
		self.stop_time     = None
		self.start_counter = None
		self.stop_counter  = None
		self.speed         = 1

	# ----------------------------------------------------------------
	# Set Counter initial value.
	# ----------------------------------------------------------------
	def initCounter(self,initial_counter):
		# Le parametre initial_counter est au format 0xFFSSMMHH
		# on le convertit en un nombre de secondes
		start_frames  = fromBCD(toByteArray(initial_counter)[0])
		start_seconds = fromBCD(toByteArray(initial_counter)[1])
		start_minutes = fromBCD(toByteArray(initial_counter)[2])
		start_hours   = fromBCD(toByteArray(initial_counter)[3])
		self.start_counter  = start_frames*0.04 + start_seconds + 60*start_minutes + 3600*start_hours

	# ----------------------------------------------------------------
	# Set Counter initial value. (with seconds)
	# ----------------------------------------------------------------
	def initCounterWithSeconds(self,initial_counter):
		self.start_counter  = initial_counter

	# ----------------------------------------------------------------
	# Set Counter initial value. (with HMSI)
	# ----------------------------------------------------------------
	def initCounterWithHMSI(self,start_hours, start_minutes, start_seconds, start_frames):
		# on le convertit en un nombre de secondes
		self.start_counter  = start_frames*0.04 + start_seconds + 60*start_minutes + 3600*start_hours

	# ----------------------------------------------------------------
	# Set Counter initial value. (with FFSSMMHH)
	# ----------------------------------------------------------------
	def initCounterWithFFSSMMHH(self,initial_counter):
		self.initCounter(initial_counter)

	# ----------------------------------------------------------------
	# Start timing.
	# ----------------------------------------------------------------
	def start(self, speed=1):
		# time() est le nombre de secondes depuis le 01/01/1970
		self.start_time = time.time()
		self.speed      = speed
		self.stop_time  = None

	# ----------------------------------------------------------------
	# Stop timing.
	# ----------------------------------------------------------------
	def stop(self):
		# if the counter is already stopped: do nothing
		if (self.stop_time == None): self.stop_time = time.time()

	# ----------------------------------------------------------------
	# Reset Counter.
	# ----------------------------------------------------------------
	def resetCounter(self):
		self.start_time =None
		self.start_counter=None

	# ----------------------------------------------------------------
	# Return the number of seconds that have elapsed since this 'Clock` started timing.
	# ----------------------------------------------------------------
	def getElapsedTime(self):
		if(self.start_time == None): 
			# Clock timing is not started
			return 0
		elif(self.stop_time == None):  
			# Clock timing is in progress
			return (time.time() - self.start_time)
		else:
			# Clock is stopped
			return self.stop_time - self.start_time

	# ----------------------------------------------------------------
	# Return the value of the Counter (in seconds)
	# ----------------------------------------------------------------
	def getCounterValue(self):
		if (self.start_counter==None):
			return 0
		else:
			return self.start_counter + self.getElapsedTime()*self.speed

	# ----------------------------------------------------------------
	# Return the value of the Counter in HMSI (list of 4 items)
	# ----------------------------------------------------------------
	def getCounterHMSI(self):
		counter_in_sec = self.getCounterValue()
		return secToHMSI(counter_in_sec)

	# ----------------------------------------------------------------
	# Return the number of seconds that elapsed from when this `clock` started to when it ended.
	# ----------------------------------------------------------------
	def getTotalTime(self):
		return self.stop_time - self.start_time

	# ----------------------------------------------------------------
	# Stop timing.
	# ----------------------------------------------------------------
	def __exit__(self, type, value, traceback):
		self.stop()

# ----------------------------------------------------------------------
# Test de la classe
# ----------------------------------------------------------------------
if ( __name__ == "__main__"):

		my_clock = Clock()
		
		print ("Timer:")
		my_clock.start()
		print (my_clock.getElapsedTime())
		print ("waiting...")
		time.sleep(2)          # en secondes
		print (my_clock.getElapsedTime())

		print ("\nCounter:")
		my_clock.initCounter(0x03110610)
		my_clock.start()
		print(" in sec: ",my_clock.getCounterValue())
		print(" (hh, mm, ss, ii):", my_clock.getCounterHMSI())
		print ("waiting...")
		time.sleep(5)          # en secondes
		print(" in sec: ",my_clock.getCounterValue())
		print(" (hh, mm, ss, ii):", my_clock.getCounterHMSI())
