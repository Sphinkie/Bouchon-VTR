# coding: Latin-1
# ==================================================================
# Diverses fonctions utiles
# ==================================================================

# ------------------------------------------------------------------
# Affiche des octets en hexa sur la console
# ------------------------------------------------------------------
def printHex(valuelist):
	i=0
	while i<len(valuelist):
		print ("%02X" % valuelist[i], end = " ")
		i+=1

# ------------------------------------------------------------------
# Convertit un bytearray en une chaine d'octets lisibles
# ------------------------------------------------------------------
def toHex(value, prefix="", sep=" "):
	hex_chaine=prefix
	if type(value)==str: 
		for c in value: hex_chaine += ("{0}{1}".format(c,sep))
	else:
		for c in value: hex_chaine += ("{0:02X}{1}".format(c,sep))
		#while i<len(value): hex_chaine += ("{0:02X}".format(value[i]))
		
	# hex_chaine += sep
	# i+=1
	return hex_chaine

# ------------------------------------------------------------------
# Convertit un hexa en BCD
#   0x08 (8)	=> 0x08
#   0x09 (9)	=> 0x09
#   0x0A (10)	=> 0x10
#   0x0B (11)	=> 0x11
# ------------------------------------------------------------------
def toBCD(value):
	bcd = int(str(value), 16)
	return bcd

# ------------------------------------------------------------------
# Convertit de BCD en numérique
#   0x08 (8)	=> 8
#   0x09 (9)	=> 9
#   0x10 (16)	=> 10
#   0x11 (17)	=> 11
# ------------------------------------------------------------------
def fromBCD(bcd):
	value = int(hex(bcd)[2:])
	return value

# ------------------------------------------------------------------
# convertit des microsecondes en un tuple HMSI
#  3600000000 => 01,00,00,00
# 36000000000 => 10,00,00,00
# 21300000000 => 05,55,00,00
# 29128000000 => 08,05,28,00
# ------------------------------------------------------------------
def microsecToHMSI(value):
	try:
		hh    = value//3600000000		# hh en heures
		reste = value - (hh*3600000000)	# minutes restantes en microsec
		mm    = reste//60000000			# mm en minutes
		reste = reste - (mm*60000000)   # secondes restantes en microsec
		ss    = reste//1000000			# ss en secondes
		reste = reste - (ss*1000000)    # frames restantes en microsec
		ii    = reste//40000			# ii en frames
		return (hh,mm,ss,ii)
	except TypeError:
		print (F"wrong value = {value}")
		return 0

# ------------------------------------------------------------------
# convertit des microsecondes en une string "hh:mm:ss:ii"
# ------------------------------------------------------------------
def microsecToString(value):
	liste = microsecToHMSI(value)
	string = "{0:02}:{1:02}:{2:02}:{3:02}".format(liste[0],liste[1],liste[2],liste[3])
	return (string)


# ------------------------------------------------------------------
# convertit des FFSSHHMM en HMSI
# ------------------------------------------------------------------
def FFSSMMHHtoHMSI(value):
	ii = fromBCD(toByteArray(value)[0])
	ss = fromBCD(toByteArray(value)[1])
	mm = fromBCD(toByteArray(value)[2])
	hh = fromBCD(toByteArray(value)[3])
	return (hh,mm,ss,ii)

# ------------------------------------------------------------------
# convertit des FFSSHHMM en secondes
# ------------------------------------------------------------------
def FFSSMMHHtoSeconds(value):
	ii = fromBCD(toByteArray(value)[0])
	ss = fromBCD(toByteArray(value)[1])
	mm = fromBCD(toByteArray(value)[2])
	hh = fromBCD(toByteArray(value)[3])
	secondes = hh*3600 + mm*60 + ss + ii*(0.04)
	return (secondes)

# ------------------------------------------------------------------
# convertit des FFSSHHMM en une string "hh:mm:ss:ii"
# ------------------------------------------------------------------
def FFSSMMHHtoString(value):
	liste = FFSSMMHHtoHMSI(value)
	string = "{0:02}:{1:02}:{2:02}:{3:02}".format(liste[0],liste[1],liste[2],liste[3])
	return (string)
	
# ------------------------------------------------------------------
# convertit des secondes en HMSI
#   3600 => 01,00,00,00	(1 heure)
#  36000 => 10,00,00,00	(10 heures)
#  21300 => 05,55,00,00	(5h55min)
#  29128 => 08,05,28,00	(8h05m28sec)
# ------------------------------------------------------------------
def secToHMSI(value):
	hh    = int(value/3600)			# hh en heures
	reste = value - (hh*3600)		# minutes restantes en microsec
	mm    = int(reste/60)			# mm en minutes
	reste = reste - (mm*60)   		# secondes restantes en microsec
	ss    = int(reste)			# ss en secondes
	reste = reste - ss			# frames restantes en microsec
	ii    = int(reste*25)			# ii en frames
	return (hh,mm,ss,ii)
	
# ------------------------------------------------------------------
# convertit des microsecondes en frames 
# 2336800000 => 58420 (00:38:56:20)
# 1847840000 => 46196 (00:30:47:21)
# ------------------------------------------------------------------
def toFrames(value):
	ff = value//40000
	return (ff)
	
# ------------------------------------------------------------------
# convertit un int en un array de 4 octets
# 270   => 00 00 01 0E
# 58420 => 00 00 E4 34
# ------------------------------------------------------------------
def toByteArray(value):
	return (value.to_bytes(4, byteorder = 'big'))

# ------------------------------------------------------------------
# convertit un int en une liste de 4 octets
# ------------------------------------------------------------------
def toByteList(value, byteorder = 'big'):
	hexa = value.to_bytes(4, byteorder = byteorder)
	return [hexa[0],hexa[1],hexa[2],hexa[3]]

# ------------------------------------------------------------------
# convertit une liste H,M,S,I en une string hh:mm:ss:ii
# ------------------------------------------------------------------
def convertListToHMSI(value):
	string = "{0}:{1}:{2}:{3}".format(value[0],value[1],value[2],value[3])
	return (string)

# ------------------------------------------------------------------
# Convertit une string "hh:mm:ss:ii" en micro-secondes
# ------------------------------------------------------------------
def stringToMicrosec(value):
	liste = value.split(":")
	result  = int(liste[0])*60*60*1000000	# heures -> us
	result += int(liste[1])*60*1000000		# minutes -> us
	result += int(liste[2])*1000000			# secondes -> us
	result += int(liste[3])*40*1000			# frames -> us
	return result

	
# ------------------------------------------------------------------
# Additionne deux string "hh:mm:ss:ii"
# ------------------------------------------------------------------
def HMSIadd(value1, value2):
	v1 = stringToMicrosec(value1) 	# conversion en micro-secondes
	v2 = stringToMicrosec(value2) 	# conversion en micro-secondes
	result = microsecToString(v1+v2)
	return result
	
# ----------------------------------------------------------------------
# Test des fonctions
# ----------------------------------------------------------------------
if ( __name__ == "__main__"):

	import os

	print (printHex(b'\1\2\3\4'))
	print (toHex(b'\1\x7f\x31\x30', prefix="=> ", sep=" "))
	print (toBCD(18))			        # 24 (=0x18)
	print (FFSSMMHHtoString(0x23595909))            # 09:59:59:23
	print (microsecToHMSI(29128000000))		# (8,5,28,0)
	print (toFrames(2336800000))	                # 58.420 frames
	print (toByteList(58495))		        # 0x00 0x00 0xe4 0x7f
	print (toHex(toByteList(2159975)))		# 00 20 F5 67
	print (microsecToHMSI(36246014184))             # 
	print (microsecToString(2143200000))             

        


	# os.system("pause")
