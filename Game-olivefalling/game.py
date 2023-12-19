import pygame
import random

# Initialisation de Pygame
pygame.init()

pygame.mixer.init()  # Initialisation du module de mixage Pygame
son_branche = pygame.mixer.Sound("branch_sound.mp3")
# Réglage du volume à 50%
son_branche.set_volume(0.5)
son_hit = pygame.mixer.Sound("hit.mp3")
son_succes = pygame.mixer.Sound("succes.mp3")
son_heal = pygame.mixer.Sound("heal.mp3")
son_picking = pygame.mixer.Sound("picking.mp3")
# Paramètres du jeu
largeur_ecran = 600
hauteur_ecran = 600
fps = 60

# Couleurs
blanc = (255, 255, 255)
hunter_green = (53, 94, 59)
noir =(0,0,0)
yellow = (216,190,83)
red_lose = (232,35,41)

# Initialisation de l'écran
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Ramasse les pommes!")

# Horloge pour contrôler les FPS
horloge = pygame.time.Clock()

# Chargement des images
personnage_image = pygame.image.load("gm.png")
personnage_image = pygame.transform.scale(personnage_image, (50, 100))

pomme_image = pygame.image.load("apple.png")
pomme_image = pygame.transform.scale(pomme_image, (30, 30))

olive_image = pygame.image.load("olive.png")
olive_image = pygame.transform.scale(olive_image, (20, 20))

bandage_image = pygame.image.load("bandage.png")
bandage_image = pygame.transform.scale(bandage_image, (38, 16))

branch_image = pygame.image.load("branch.png")
branch_image = pygame.transform.scale(branch_image, (100, 50))

girl_image = pygame.image.load("little_girl.png")
girl_image = pygame.transform.scale(girl_image, (40, 60))

# Nouvelle image pour la petite fille qui fait face vers la gauche
girl_reverse_image = pygame.image.load("little_girl_reverse.png")
girl_reverse_image = pygame.transform.scale(girl_reverse_image, (40, 60))

fond_image = pygame.image.load("background.png")
fond_image = pygame.transform.scale(fond_image, (largeur_ecran, hauteur_ecran))


# Position initiale du personnage
personnage_x = largeur_ecran // 2
personnage_y = hauteur_ecran - 100
personnage_vitesse = 5

# Liste pour stocker les pommes
pommes = []

# Liste pour stocker les olives
olives = []

# Liste pour stocker les branches
branchs = []

# Liste pour stocker les bandages
bandages = []

# Score
score = 0

#Initialisation du nombre de pomme
quantite_pommes = 0

#Initilisation de la vitesse de chut
vitesse_chute =0

# Initialisation du premier niveau
niveau_actuel = 1

quantite_branches = 0

hp = 5
# Position initiale de la petite fille
girl_x = largeur_ecran // 2
girl_y = hauteur_ecran - 60
girl_vitesse = 1  # Ajustez la vitesse de la petite fille

# Police pour afficher le score
police = pygame.font.Font(None, 36)

# Fonction pour afficher le score
def afficher_score(score):
    texte = police.render(f"Score: {score}/{10+10*niveau_actuel}", True, blanc)
    ecran.blit(texte, (10, 10))
# Fonction pour afficher les hp
def afficher_hp(hp):
    texte = police.render(f"HP: {hp}", True, blanc)
    ecran.blit(texte, (10, 30))
# Fonction pour afficher le score
def afficher_niveau(niveau_actuel):
    texte = police.render(f"Niveau: {niveau_actuel}", True, blanc)
    ecran.blit(texte, (460, 10))
# Fonction pour afficher le personnage
def afficher_personnage(x, y):
    ecran.blit(personnage_image, (x, y))
# Fonction pour afficher le personnage
def afficher_girl(x, y, reverse=False):
    if reverse:
        ecran.blit(girl_reverse_image, (x, y))
    else:
        ecran.blit(girl_image, (x, y))
# Fonction pour afficher les pommes
def afficher_pommes():
    for pomme in pommes:
        ecran.blit(pomme_image, (pomme[0], pomme[1]))
# Fonction pour afficher les olives
def afficher_olives():
    for olive in olives:
        ecran.blit(olive_image, (olive[0], olive[1]))
# Fonction pour afficher les branchs
def afficher_branches():
    for branch in branchs:
        ecran.blit(branch_image, (branch[0], branch[1]))

# Fonction pour afficher les branchs
def afficher_bandages():
    for bandage in bandages:
        ecran.blit(bandage_image, (bandage[0], bandage[1]))
# Fonction pour afficher la hitbox du personnage
def afficher_hitbox_personnage(x, y):
    pygame.draw.rect(ecran, blanc, [x, y, 50, 100], 2)
# Fonction pour initialiser un nouveau niveau
def initialiser_niveau(niveau):
    global pommes, score, vitesse_chute, quantite_pommes, quantite_branches, olives,branchs,girl_vitesse, bandages
    pommes = []
    branchs = []
    olives = []
    bandages = []
    girl_vitesse+=0.5
    score = 0
    vitesse_chute = 1 + niveau * 0.5  # Ajustez la vitesse en fonction du niveau
    quantite_pommes = 5 + niveau   # Ajustez la quantité en fonction du niveau
    quantite_branches = 2 + niveau
# Fonction pour afficher le menu entre les niveaux
def afficher_menu(score, niveau):
    menu_affiche = True
    while menu_affiche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        

        # Affichage du fond du jeu (pour voir le jeu derrière le menu)
        afficher_personnage(personnage_x, personnage_y)
        afficher_pommes()
        afficher_olives()
        afficher_branches()
        afficher_bandages()
        afficher_girl(girl_x, girl_y, reverse=not vers_la_droite)

        # Affichage du menu au centre de l'écran
        largeur_menu = largeur_ecran // 2
        hauteur_menu = hauteur_ecran // 3
        menu_rect = pygame.Rect(largeur_ecran // 2 - largeur_menu // 2, hauteur_ecran // 2 - hauteur_menu // 2, largeur_menu, hauteur_menu)
        pygame.draw.rect(ecran, yellow, menu_rect)

        # Affichage du score et du niveau atteint
        texte_score = police.render(f"Score: {score}", True, blanc)
        texte_niveau = police.render(f"Niveau {niveau-1} terminé", True, blanc)
        texte_score_rect = texte_score.get_rect(center=(menu_rect.centerx, menu_rect.centery - 50))
        texte_niveau_rect = texte_niveau.get_rect(center=(menu_rect.centerx, menu_rect.centery - 70))
        ecran.blit(texte_score, texte_score_rect)
        ecran.blit(texte_niveau, texte_niveau_rect)

        # Affichage du bouton "Continuer"
        bouton_rect = pygame.Rect(largeur_ecran // 2 - 75, hauteur_ecran // 2 + 50, 150, 50)
        pygame.draw.rect(ecran, blanc, bouton_rect)
        texte_continuer = police.render("Continuer", True, hunter_green)
        texte_continuer_rect = texte_continuer.get_rect(center=bouton_rect.center)
        ecran.blit(texte_continuer, texte_continuer_rect)

        # Actualisation de l'écran
        pygame.display.flip()

        # Vérification de l'appui sur le bouton "Continuer"
        touches = pygame.key.get_pressed()
        if touches[pygame.K_RETURN]:
            menu_affiche = False

        # Contrôle des FPS
        horloge.tick(fps)
def afficher_menu_perdu():
    menu_affiche = True
    while menu_affiche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        

        # Affichage du fond du jeu (pour voir le jeu derrière le menu)
        afficher_personnage(personnage_x, personnage_y)
        afficher_pommes()
        afficher_olives()
        afficher_branches()
        afficher_bandages()
        afficher_girl(girl_x, girl_y, reverse=not vers_la_droite)

        # Affichage du menu au centre de l'écran
        largeur_menu = largeur_ecran // 2
        hauteur_menu = hauteur_ecran // 3
        menu_rect = pygame.Rect(largeur_ecran // 2 - largeur_menu // 2, hauteur_ecran // 2 - hauteur_menu // 2, largeur_menu, hauteur_menu)
        pygame.draw.rect(ecran, red_lose, menu_rect)

        # Affichage du score et du niveau atteint
        texte_score = police.render(f"Tu as perdu", True, blanc)
        texte_score_rect = texte_score.get_rect(center=(menu_rect.centerx, menu_rect.centery - 50))
        ecran.blit(texte_score, texte_score_rect)

        # Affichage du bouton "Continuer"
        bouton_rect = pygame.Rect(largeur_ecran // 2 - 75, hauteur_ecran // 2 + 50, 150, 50)
        pygame.draw.rect(ecran, blanc, bouton_rect)
        texte_continuer = police.render("Continuer", True, hunter_green)
        texte_continuer_rect = texte_continuer.get_rect(center=bouton_rect.center)
        ecran.blit(texte_continuer, texte_continuer_rect)

        # Actualisation de l'écran
        pygame.display.flip()

        # Vérification de l'appui sur le bouton "Continuer"
        touches = pygame.key.get_pressed()
        if touches[pygame.K_RETURN]:
            menu_affiche = False

        # Contrôle des FPS
        horloge.tick(fps)
# Boucle principale du jeu
running = True
initialiser_niveau(niveau_actuel)
vers_la_droite = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Déplacement du personnage avec les touches gauche et droite
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT] and personnage_x > 0:
        personnage_x -= personnage_vitesse
    if touches[pygame.K_RIGHT] and personnage_x < largeur_ecran - 50:
        personnage_x += personnage_vitesse

    # Mouvement de la petite fille de droite à gauche
    if vers_la_droite:
        girl_x += girl_vitesse
        if girl_x > largeur_ecran - 40:
            vers_la_droite = False
    else:
        girl_x -= girl_vitesse
        if girl_x < 0:
            vers_la_droite = True

    if score >= 10+(10*niveau_actuel):
        niveau_actuel+=1
        print("Niveau ",niveau_actuel," atteint.")
        son_succes.play()
        afficher_menu(score, niveau_actuel)
        initialiser_niveau(niveau_actuel)

    if hp <= 0:
        afficher_menu_perdu()


    # Génération aléatoire de nouvelles olives
    if random.randint(0, 500) < quantite_pommes:
        olives.append([random.randint(0, largeur_ecran - 30), 0])

    # Génération aléatoire de nouvelles branches
    if random.randint(0, 1000) < quantite_branches:
        branchs.append([random.randint(0, largeur_ecran - 30), 0])
        son_branche.play()
    # Génération aléatoire de nouvelles bandage
    if random.randint(0, 1200) < 1:
        bandages.append([random.randint(0, largeur_ecran - 30), 0])

    # Déplacement des olives vers le bas
    for olive in olives:
        olive[1] += vitesse_chute+1
        # Vérification de la collision avec le personnage
        if (
            personnage_x < olive[0] < personnage_x + 50 and
            personnage_y < olive[1] < personnage_y + 120
        ) or (
            personnage_x < olive[0] + 30 < personnage_x + 50 and
            personnage_y < olive[1] + 30 < personnage_y + 120
        ):
            olives.remove(olive)
            score += 1
            son_picking.play()
    # Déplacement des branches vers le bas
    for branch in branchs:
        branch[1] += vitesse_chute + 1
        # Vérification de la collision avec le personnage ou la petite fille
        if (
            (personnage_x < branch[0] + 100 and personnage_x + 50 > branch[0] and personnage_y < branch[1] + 50 and personnage_y + 80 > branch[1]) or 
            (girl_x < branch[0] + 100 and girl_x + 40 > branch[0] and girl_y < branch[1] + 50 and girl_y + 60 > branch[1])
        ):
            branchs.remove(branch)
            son_hit.play()
            hp -= 1
    # Déplacement des branches vers le bas
    for bandage in bandages:
        bandage[1] += vitesse_chute + 1
        # Vérification de la collision avec le personnage ou la petite fille
        if (
            (personnage_x < bandage[0] + 100 and personnage_x + 50 > bandage[0] and personnage_y < bandage[1] + 50 and personnage_y + 80 > bandage[1]) or 
            (girl_x < bandage[0] + 100 and girl_x + 40 > bandage[0] and girl_y < bandage[1] + 50 and girl_y + 60 > bandage[1])
        ):
            bandages.remove(bandage)
            son_heal.play()
            hp += 1
    # Suppression des pommes qui ont atteint le bas de l'écran
    pommes = [pomme for pomme in pommes if pomme[1] < hauteur_ecran]
    # Suppression des branchs qui ont atteint le bas de l'écran
    branchs = [branch for branch in branchs if branch[1] < hauteur_ecran]
    # Suppression des olives qui ont atteint le bas de l'écran
    olives = [olive for olive in olives if olive[1] < hauteur_ecran]
    # Suppression des bandages qui ont atteint le bas de l'écran
    bandages = [bandage for bandage in bandages if bandage[1] < hauteur_ecran]    
    # Effacement de l'écran
    ecran.blit(fond_image, (0, 0))

    # Affichage du personnage, des pommes et du score
    afficher_personnage(personnage_x, personnage_y)
    afficher_olives()
    afficher_branches()
    afficher_bandages()
    afficher_score(score)
    afficher_niveau(niveau_actuel)
    afficher_girl(girl_x, girl_y, reverse=not vers_la_droite)
    afficher_hp(hp)
    ##afficher_hitbox_personnage(personnage_x, personnage_y)
    

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Contrôle des FPS
    horloge.tick(fps)

# Quitter Pygame
pygame.quit()
