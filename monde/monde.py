import pygame
import sys

############################
####   LES FONCTIONS   #####
############################

def lire_fichier(nom):
  carte =[]
  with open(nom,'r',encoding='utf-8') as mon_fichier:
    contenu = mon_fichier.read()
    lignes = contenu.split(chr(10))
    for ligne in lignes :
        carte.append(ligne.split(';'))
  print(carte)
  return carte

def dessinerMonde(carte):
    r=0
    for ligne in range(debutcarte[1],fincarte[1]):
      c=0
      for colonne in range(debutcarte[0],fincarte[0]):
        if debutcarte[1] <= ligne < fincarte[1] and debutcarte[0] <= colonne < fincarte[0]:

          
          positionX = dimCase[0]*(colonne-debutcarte[0])+debutCadre[0]

          positionY=dimCase[1]*(ligne-debutcarte[1])+debutCadre[1]
          c+=1
          r+=1
          if positionX==debutCadre[0]+perso["colonne"]*dimCase[0] and positionY==debutCadre[1]+perso["ligne"]*dimCase[1]:
            perso["eau"]=False
            if carte[ligne][colonne]=='1':
              perso["eau"]=True
          if r==fincarte[1]-debutcarte[1]:
            r=0
          if carte[ligne][colonne]=='1':      
            screen.blit(imMer, (positionX,positionY))
          elif carte[ligne][colonne]=='2':
            screen.blit(imPrairie, (positionX,positionY))
          elif carte[ligne][colonne]=='3':
            screen.blit(imChamp, (positionX,positionY))
          elif carte[ligne][colonne]=='4':
            screen.blit(imForet, (positionX,positionY))
          elif carte[ligne][colonne]=='5':
            screen.blit(imMontagne, (positionX,positionY))

def creerPerso():
  perso={}
  perso["ligne"]=5
  perso["colonne"]=6
  perso["image"]=pygame.image.load('images/bonhomme.png').convert_alpha()
  perso["image"]= pygame.transform.scale(perso["image"], dimCase)
  perso["sens"]="stop"
  perso["bateau"]=pygame.image.load('images/bateau.png').convert_alpha()
  perso["bateau"]= pygame.transform.scale(perso["bateau"], dimCase)
  return perso

def dessinerperso(perso):
        positionX = debutCadre[0]+perso["colonne"]*dimCase[0]
        positionY = debutCadre[1]+perso["ligne"]*dimCase[1] 
        if perso["eau"]==True:
          screen.blit(perso["bateau"], (positionX,positionY))
        else:
          screen.blit(perso["image"], (positionX,positionY))

def deplacerPerso(perso):
  global debutcarte, fincarte
  if perso["sens"] == "bas" and fincarte[1] < len(carte[0]):
      debutcarte[1] += 1
      fincarte[1] += 1
  elif perso["sens"] == "haut" and debutcarte[1] > 0:
      debutcarte[1] -= 1
      fincarte[1] -= 1
  elif perso["sens"] == "droite" and fincarte[0] < len(carte):
      debutcarte[0] += 1
      fincarte[0] += 1
  elif perso["sens"] == "gauche" and debutcarte[0] > 0:
      debutcarte[0] -= 1
      fincarte[0] -= 1

  perso["sens"]="stop"
#####################################    
####   PROGRAMME PRINCIPAL   ########
#####################################

pygame.init()
screen = pygame.display.set_mode((820,640))
pygame.display.set_caption("îles")

### Les variables globales  ###
dimCase = (60,60)
debutCadre = (20,20)
debutcarte=[14,49]
fincarte=[27,59]
perso=creerPerso()

### Chargement des fichiers ###
imMer = pygame.image.load('images/mer.jpg').convert_alpha()
imMer = pygame.transform.scale(imMer, dimCase)

imPrairie = pygame.image.load('images/prairie.jpg').convert_alpha()
imPrairie = pygame.transform.scale(imPrairie, dimCase)

imChamp = pygame.image.load('images/champ.jpg').convert_alpha()
imChamp = pygame.transform.scale(imChamp, dimCase)

imForet = pygame.image.load('images/foret.jpg').convert_alpha()
imForet = pygame.transform.scale(imForet, dimCase)

imMontagne = pygame.image.load('images/montagne.jpg').convert_alpha()
imMontagne = pygame.transform.scale(imMontagne, dimCase)

carte = lire_fichier("carte_mini.csv")
print(carte)

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


    pygame.display.flip()
            
                      
sys.exit() # pour fermer correctement