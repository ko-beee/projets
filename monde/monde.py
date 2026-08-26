import pygame
import sys
from pathlib import Path

DOSSIER = Path(__file__).parent

############################
####   LES FONCTIONS   #####
############################

def lire_fichier(nom):
  carte =[]
  with open(nom,'r',encoding='utf-8') as mon_fichier:
    contenu = mon_fichier.read()
    lignes = contenu.splitlines()
    for ligne in lignes :
        if ligne.strip(): # on ne prend pas en compte les lignes vides
          carte.append(ligne.split(';'))
  return carte

def dessinerMonde(carte):
  for ligne in range(debutcarte[0],fincarte[0]):
    for colonne in range(debutcarte[1],fincarte[1]):
        numeroColonne =colonne-debutcarte[1]
        numeroLigne=ligne-debutcarte[0]
        if numeroColonne==perso["colonne"] and numeroLigne==perso["ligne"]:
          perso["eau"]=False
          perso["montagne"]=False
          if carte[ligne][colonne]=='1':
            perso["eau"]=True
          elif carte[ligne][colonne]=='5':
            perso["montagne"]=True
          if persobloquer()==True:
            return
        numeroColonne = dimCase[0]*numeroColonne+debutCadre[0]
        numeroLigne = dimCase[1]*numeroLigne+debutCadre[1]
        if carte[ligne][colonne]=='1':      
          screen.blit(imMer, (numeroColonne,numeroLigne))
        elif carte[ligne][colonne]=='2':
          screen.blit(imPrairie, (numeroColonne,numeroLigne))
        elif carte[ligne][colonne]=='3':
          screen.blit(imChamp, (numeroColonne,numeroLigne))
        elif carte[ligne][colonne]=='4':
          screen.blit(imForet, (numeroColonne,numeroLigne))
        elif carte[ligne][colonne]=='5':
          screen.blit(imMontagne, (numeroColonne,numeroLigne))
  
def creerPerso():
  perso={}
  perso["ligne"]=4
  perso["colonne"]=6
  perso["image"]=pygame.image.load(DOSSIER / 'images/personnage/bonhomme.png').convert_alpha()
  perso["image"]= pygame.transform.scale(perso["image"], dimCase)
  perso["sens"]="stop"
  perso["épée"]=pygame.transform.scale(pygame.image.load(DOSSIER /'images/personnage/personnage_epee.png').convert_alpha(), dimCase)
  perso["chaussure"]=pygame.transform.scale(pygame.image.load(DOSSIER / 'images/objet/chaussure.png').convert_alpha(), dimCase)
  perso["bateau"]= pygame.transform.scale(pygame.image.load(DOSSIER / 'images/objet/bateau.png').convert_alpha(), dimCase)
  perso["eau"]=False
  perso["montagne"]=False

  return perso


def creerObjets():
  objet={}
  objet["bateau"]={"colonne":17,"ligne":53,"image":pygame.transform.scale(pygame.image.load(DOSSIER / 'images/objet/bateau.png').convert_alpha(), dimCase),"perso":False}
  objet["épée"]={"colonne":14,"ligne":50,"image":pygame.transform.scale(pygame.image.load(DOSSIER / 'images/objet/epee.png').convert_alpha(), dimCase),"perso":False}
  objet["chaussure"]={"colonne":10,"ligne":52,"image":pygame.transform.scale(pygame.image.load(DOSSIER / 'images/objet/chaussure.png').convert_alpha(), dimCase),"perso":False}
  return objet

def dessinerObjets(objets):
  for (objet, chose) in objets.items():
      if debutcarte[0]<=chose["ligne"]<fincarte[0] and debutcarte[1]<=chose["colonne"]<fincarte[1]:
        coordonneColonne = dimCase[1]*(chose["colonne"]-debutcarte[1])+debutCadre[1]
        coordonneLigne = dimCase[0]*(chose["ligne"]-debutcarte[0])+debutCadre[0]
        if chose["perso"]==False:
          screen.blit(chose["image"], (coordonneColonne,coordonneLigne))
        if coordonneColonne==debutCadre[0]+perso["colonne"]*dimCase[0] and coordonneLigne==debutCadre[1]+perso["ligne"]*dimCase[1]:
          chose["perso"]=True

def dessinerperso(perso):
        coordonnepersocolonne = debutCadre[0]+perso["colonne"]*dimCase[0]
        coordonnepersoligne = debutCadre[1]+perso["ligne"]*dimCase[1] 
        if perso["eau"]==True and objets["bateau"]["perso"]==True:
          screen.blit(perso["bateau"], (coordonnepersocolonne,coordonnepersoligne))
        else:
          if objets["épée"]["perso"]==True: 
            screen.blit(perso["épée"], (coordonnepersocolonne,coordonnepersoligne))
          else:
            screen.blit(perso["image"], (coordonnepersocolonne,coordonnepersoligne))
          if objets["chaussure"]["perso"]==True:
            screen.blit(perso["chaussure"], (coordonnepersocolonne,coordonnepersoligne))

def deplacerPerso(perso):
  global debutcarte, fincarte
  if perso["sens"] == "bas" and fincarte[0] < len(carte):#len(carte) pour le nombre de lignes
      debutcarte[0] += 1
      fincarte[0] += 1
  elif perso["sens"] == "haut" and debutcarte[0] > 0:
      debutcarte[0] -= 1
      fincarte[0] -= 1
  elif perso["sens"] == "droite" and fincarte[1] < len(carte[0]):#len(carte[0]) pour le nombre de colonnes
      debutcarte[1] += 1
      fincarte[1] += 1
  elif perso["sens"] == "gauche" and debutcarte[1] > 0:
      debutcarte[1] -= 1
      fincarte[1] -= 1
  

  perso["sens"]="stop"

def persobloquer():
  global debutcarte, fincarte
  if (perso["eau"]==True and objets["bateau"]["perso"]==False) or (perso["montagne"]==True and objets["chaussure"]["perso"]==False):
     debutcarte=[coordonnéesinitiales[0], coordonnéesinitiales[1]]
     fincarte=[coordonnéesinitiales[2], coordonnéesinitiales[3]]
     return True
  return False
    
#####################################    
####   PROGRAMME PRINCIPAL   ########
#####################################
coordonnéesinitiales=(45, 8,54,21) #ligne début, colonne début, ligne fin, colonne fin
dimCase = (60,60)
debutCadre = (20,20)
pygame.init()
taille_fenetre = ((coordonnéesinitiales[3]-coordonnéesinitiales[1])*dimCase[1]+debutCadre[1]*2, (coordonnéesinitiales[2]-coordonnéesinitiales[0])*dimCase[0]+debutCadre[0]*2)
screen = pygame.display.set_mode((taille_fenetre))
pygame.display.set_caption("îles")

### Les variables globales  ###


debutcarte=[coordonnéesinitiales[0], coordonnéesinitiales[1]]
fincarte=[coordonnéesinitiales[2], coordonnéesinitiales[3]]
#ligne-->debutcarte[0] fincarte[0]
#colonne-->debutcarte[1] fincarte[1]
perso=creerPerso()
objets=creerObjets()
### Chargement des fichiers ###
imMer = pygame.image.load(DOSSIER / 'images/carte/mer.jpg').convert_alpha()
imMer = pygame.transform.scale(imMer, dimCase)

imPrairie = pygame.image.load(DOSSIER / 'images/carte/prairie.jpg').convert_alpha()
imPrairie = pygame.transform.scale(imPrairie, dimCase)

imChamp = pygame.image.load(DOSSIER / 'images/carte/champ.jpg').convert_alpha()
imChamp = pygame.transform.scale(imChamp, dimCase)

imForet = pygame.image.load(DOSSIER / 'images/carte/foret.jpg').convert_alpha()
imForet = pygame.transform.scale(imForet, dimCase)

imMontagne = pygame.image.load(DOSSIER / 'images/carte/montagne.jpg').convert_alpha()
imMontagne = pygame.transform.scale(imMontagne, dimCase)

carte = lire_fichier(DOSSIER / "carte_mini.csv")


continuer = True # variable pour laisser la fenêtre ouverte

while continuer : ### BOUCLE DE JEU  ###

    ### GESTION DES EVENEMENTS  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            continuer = False
        if event.type==pygame.KEYDOWN:
          if event.key==pygame.K_RIGHT:
            perso["sens"]="droite"
          elif event.key==pygame.K_LEFT:
            perso["sens"]="gauche"
          elif event.key==pygame.K_UP:
            perso["sens"]="haut"
          elif event.key==pygame.K_DOWN:
            perso["sens"]="bas"
            
    ### ANIMATIONS   ###
    deplacerPerso(perso)        
            
    ### DESSINS      ###
    dessinerMonde(carte)
    dessinerperso(perso)
    dessinerObjets(objets)

    pygame.display.flip()
            
                      
sys.exit() # pour fermer correctement