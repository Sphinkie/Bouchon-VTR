# ==================================================================
# GENERATION DU FICHIER EXE
# ------------------------------------------------------------------
# Usage : 
#		py setup.py build
# ==================================================================


from cx_Freeze import setup, Executable


setup(
    name = "BouchonVTR",
    version = "1.0",
    description = "Bouchon pour devices VTR",
    executables = [Executable("..\BouchonVTR.py")],
    )
