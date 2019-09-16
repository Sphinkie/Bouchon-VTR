# coding: UTF-8
# ==================================================================
# PROGRAMME BOUCHON POUR SIMULER UN DEVICE SERIE
# ------------------------------------------------------------------
# 05/02/2018 | 1.0 | DDL | Version initiale
# ==================================================================
import logging		# pour les logs
from tkinter     import *
import sys
sys.path.append("..")
from common.Common  import *
from common.LogFile import *
from lib.interfaceVTR import *


# ----------------------------------------------------
# Main function
# ----------------------------------------------------

def main():
	# ----------------------------------------------------
    # Initialisation des logs
	# ----------------------------------------------------
    logs    = LogFile("logs/BouchonVTR.log",logging.INFO)
    logger  = logging.getLogger("socket")
    logger.info(" ******* STARTING BouchonVTR")
    # Pour les tests on peut activer le mode Verbose dès le debut
    # logs.toggleLogLevel()

	# ----------------------------------------------------
    # Initialisation de l'affichage
	# ----------------------------------------------------
    fenetre  = Tk()
    # Initialisation du VTR
    COMport = 'COM4'
    vtr = interfaceVTR(fenetre, COMport)

	# ----------------------------------------------------
    # on declare les champs variables de la fenetre
	# ----------------------------------------------------
    verboselog_var=IntVar()
    compteur_var=StringVar()
    status_var=StringVar()
    mode_var=StringVar()

    compteur_var.set(" ")
    status_var.set("stopped")
    mode_var.set("remote")

	# ----------------------------------------------------
	# Elements de la fenêtre principale:
	# ----------------------------------------------------
    fenetre.resizable(width=False, height=False)
    fenetre.title('BouchonVTR')
    
    # Label 
    label_1 = Label(fenetre, text="VTR: com0com -> "+COMport)
    label_1.pack()
    # Vue du compteur
    label_cpt = Label(fenetre, textvariable=compteur_var, height=1, width=12, background="#0c2b19", foreground="green", font=("verdana", 32))
    label_cpt.pack(side=TOP, padx=5, pady=0)
    # Vue du status
    label_status = Label(fenetre, textvariable=status_var, height=1, width=25, background="#0c2b19", foreground="green", font=("verdana", 16))
    label_status.pack(side=TOP, padx=5, pady=0)
    # Vue du mode
    label_status = Label(fenetre, textvariable=mode_var, height=1, width=25, background="#0c2b19", foreground="green", font=("verdana", 16))
    label_status.pack(side=TOP, padx=5, pady=0)
    
    # Bouton LOCAL
    bouton=Button(fenetre, name = "boutonLocal", text="LOCAL", bg="lightgrey", command=vtr.setStatusToLocal)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton REMOTE
    bouton=Button(fenetre, name = "boutonRemote", text="REMOTE", bg="gold", state=DISABLED, command=vtr.setStatusToRemote)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton RW
    bouton=Button(fenetre, name="boutonRW", text="RW", bg="yellowgreen", state=DISABLED, command=vtr.fastRewind)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton PLAY
    bouton=Button(fenetre, name="boutonPlay", text="PLAY", bg="yellowgreen", state=DISABLED, command=vtr.play)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton FF
    bouton=Button(fenetre, name="boutonFF", text="FF", bg="yellowgreen", state=DISABLED, command=vtr.fastForward)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton STOP
    bouton=Button(fenetre, name="boutonStop", text="STOP", bg="yellowgreen", state=DISABLED, command=vtr.stop)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton EJECT
    bouton=Button(fenetre, name="boutonEject", text="EJECT", command=vtr.eject)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Bouton INSERT K7
    bouton=Button(fenetre, name="boutonInsert", text="INSERT K7", state=DISABLED, command=vtr.insert)
    bouton.pack(side=LEFT, padx=5, pady=5)
    # Case à cocher pour les logs Verbose
    bouton=Checkbutton(fenetre, text="verbose log", variable=verboselog_var, command=logs.toggleLogLevel) #setVerbose(verboselog_var==1))
    bouton.pack(side=BOTTOM, padx=5, pady=5)
    # bouton QUIT
    bouton=Button(fenetre, text="QUIT", bg="darkgrey", command=fenetre.quit)
    bouton.pack(side=BOTTOM, padx=5, pady=5)

    # On insère une cassette dans le VTR
    vtr.insert(36000)
    # On déclenche le refresh automatique
    fenetre.after(1000, vtr.updateDisplay, mode_var, status_var, compteur_var)
	# ----------------------------------------------------
	# On passe la main à l'affichage!
	# ----------------------------------------------------
    fenetre.mainloop()



# -------------------------------------------------------------------------
# Execute main program
# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()
