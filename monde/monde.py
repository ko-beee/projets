import pygame
import sys

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
          positionColonne = dimCase[0]*(colonne-debutcarte[1])+debutCadre[1]
          positionLigne=dimCase[1]*(ligne-debutcarte[0])+debutCadre[0]
          if positionColonne==debutCadre[0]+perso["colonne"]*dimCase[0] and positionLigne==debutCadre[1]+perso["ligne"]*dimCase[1]:
            perso["eau"]=False
            perso["montagne"]=False
            if carte[ligne][colonne]=='1':
              perso["eau"]=True
            else:
                if objets["épée"]["perso"]==True:
                  perso["objet"]["épée"]=True
                if carte[ligne][colonne]=='5':
                  perso["montagne"]=True
          if carte[ligne][colonne]=='1':      
            screen.blit(imMer, (positionColonne,positionLigne))
          elif carte[ligne][colonne]=='2':
            screen.blit(imPrairie, (positionColonne,positionLigne))
          elif carte[ligne][colonne]=='3':
            screen.blit(imChamp, (positionColonne,positionLigne))
          elif carte[ligne][colonne]=='4':
            screen.blit(imForet, (positionColonne,positionLigne))
          elif carte[ligne][colonne]=='5':
            screen.blit(imMontagne, (positionColonne,positionLigne))

def creerPerso():
  perso={}
  perso["ligne"]=4
  perso["colonne"]=6
  perso["image"]=pygame.image.load('images/personnage/bonhomme.png').convert_alpha()
  perso["image"]= pygame.transform.scale(perso["image"], dimCase)
  perso["sens"]="stop"
  perso["épée"]=pygame.transform.scale(pygame.image.load('images/personnage/personnage_epee.png').convert_alpha(), dimCase)
  perso["chaussure"]=pygame.transform.scale(pygame.image.load('images/objet/chaussure.png').convert_alpha(), dimCase)
  perso["bateau"]= pygame.transform.scale(pygame.image.load('images/objet/bateau.png').convert_alpha(), dimCase)
  perso["objet"]={"bateau":False,"épée":False,"chaussure":False}
  perso["eau"]=False
  perso["montagne"]=False

  return perso


def creerObjets():
  objet={}
  objet["bateau"]={"coordonnéX":17,"coordonnéY":53,"image":pygame.transform.scale(pygame.image.load('images/objet/bateau.png').convert_alpha(), dimCase),"perso":False}
  objet["épée"]={"coordonnéX":14,"coordonnéY":50,"image":pygame.transform.scale(pygame.image.load('images/objet/epee.png').convert_alpha(), dimCase),"perso":False}
  objet["chaussure"]={"coordonnéX":10,"coordonnéY":52,"image":pygame.transform.scale(pygame.image.load('images/objet/chaussure.png').convert_alpha(), dimCase),"perso":False}
  return objet

def dessinerObjets(objets):
  for (objet, chose) in objets.items():
      positionColonne = dimCase[0]*(chose["coordonnéX"]-debutcarte[1])+debutCadre[0]
      positionLigne=dimCase[1]*(chose["coordonnéY"]-debutcarte[0])+debutCadre[1]
      if debutCadre[0]<=positionColonne<taille_fenetre[0] and debutCadre[1]<=positionLigne<taille_fenetre[1]:
        if chose["perso"]==False:
          screen.blit(chose["image"], (positionColonne,positionLigne))
        if positionColonne==debutCadre[0]+perso["colonne"]*dimCase[0] and positionLigne==debutCadre[1]+perso["ligne"]*dimCase[1]:
          chose["perso"]=True
          perso["objet"][objet]=True

def dessinerperso(perso):
        positionColonne = debutCadre[0]+perso["colonne"]*dimCase[0]
        positionLigne = debutCadre[1]+perso["ligne"]*dimCase[1] 
        if perso["eau"]==True and perso["objet"]["bateau"]==True:
          screen.blit(perso["bateau"], (positionColonne,positionLigne))
        else:
          if perso["objet"]["épée"]==True:
            screen.blit(perso["épée"], (positionColonne,positionLigne))
          else:
            screen.blit(perso["image"], (positionColonne,positionLigne))
          if perso["objet"]["chaussure"]==True:
            screen.blit(perso["chaussure"], (positionColonne,positionLigne))

def deplacerPerso(perso):
  global debutcarte, fincarte
  persobloquer()
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
  if (perso["eau"]==True and perso["objet"]["bateau"]==False) or (perso["montagne"]==True and perso["objet"]["chaussure"]==False):
     debutcarte=[coordonnéesinitiales[0], coordonnéesinitiales[1]]
     fincarte=[coordonnéesinitiales[2], coordonnéesinitiales[3]]

    
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
imMer = pygame.image.load('images/carte/mer.jpg').convert_alpha()
imMer = pygame.transform.scale(imMer, dimCase)

imPrairie = pygame.image.load('images/carte/prairie.jpg').convert_alpha()
imPrairie = pygame.transform.scale(imPrairie, dimCase)

imChamp = pygame.image.load('images/carte/champ.jpg').convert_alpha()
imChamp = pygame.transform.scale(imChamp, dimCase)

imForet = pygame.image.load('images/carte/foret.jpg').convert_alpha()
imForet = pygame.transform.scale(imForet, dimCase)

imMontagne = pygame.image.load('images/carte/montagne.jpg').convert_alpha()
imMontagne = pygame.transform.scale(imMontagne, dimCase)

carte = lire_fichier("carte_mini.csv")


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