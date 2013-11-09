# ==============================================================================
# VISUAL NOVEL PROJECT : Protoype version - For University Bordeaux Segalen
# ==============================================================================
"""Role Playing Game with combat, choice and stuff system"""
__author__  = "Paul Ecoffet and Elias Rhouzlane"
__version__ = "0.1"
__date__    = "2013-10-25"
__usage__   = """Essais"""
# ==============================================================================
from managertool_window import *

def interface():
    """main program of the screen printing module"""
    #Initialisation de la fenêtre de jeu à taille fixe
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    C1 = Checkbutton(root, text = "Réference", variable = CheckVar1, \
                     onvalue = 1, offvalue = 0, height=0, \
                     width = 50)
    C2 = Checkbutton(root, text = "Condition", variable = CheckVar2, \
                     onvalue = 1, offvalue = 0, height=0, \
                     width = 50, command=test(CheckVar2))
    
    C1.pack()
    C2.pack()
    root.mainloop()
def test(CheckVar2):
    print("variable is", CheckVar2.get())
