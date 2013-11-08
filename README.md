dunwallsgate
============

Voici le projet dunwallsgate qui correspond au projet "Fiction interactive". Il
est réalisé par Elias RHOUZLANE et Paul ECOFFET.

Lancer le projet
----------------
Le projet peut être lancé en éxecutant le fichier
dunwallsgate/src/dunwallsgate.py avec Python3 et le module pygame d'installer.

08/11/13
--------
### Tâches effectuées

#### IHM
Nous souhaitons réaliser ce projet avec une interface graphique. Nous avons donc
décider d'utiliser le module `pygame`. Comme architecture, nous avons penser à
décomposer notre projet en plusieurs écrans, tel que l'écran d'accueil, l'écran
de scène, l'écran de combat ou l'écran de carte. Pour cela, chacun de ces écrans
est défini dans un objet python. Ils se situent tous dans le dossier `screens`.
À chaque tour de boucle, l'objet `Window` appelle la méthode `draw` de l'écran.

Pour l'instant, seul l'écran "HomeScreen" est implémenté. Il permettra de
commencer une nouvelle partie, d'en charger une, ou bien de quitter le jeu. Les
images utilisées sont pour l'instant issues de jeux, que nous avons ensuite
modifié. La musique, elle, est composée par Clément Maliet, exprès pour le jeu.
Elle contient déjà les principaux thèmes musicaux qui seront déclinés en
fonction des écrans.

Afin de gérer les évènements, nous avons coder un gestionnaire d'évènement,
un objet `EventManager`. Il permet de simplifier l'enregistrement de callbacks
déclenchés pour un évènement donné.

#### Mécaniques de jeu et structures de données
Nous avons commencé à réfléchir sur nos attentes au niveau du gameplay. Nous
souhaitons intégrer un système de quêtes, d'évènements aléatoires, de
déplacements guidés sur une carte, de gestion de ressources. Nous avons, de
plus, commencer à travailler sur un scénario.

Pour structurer toutes nos données, nous pensons faire appelle au JSON. Ce
format est très simple à utiliser, très flexible, et lisible facilement par un
humain. Ce format de fichier nous permettra de décrire nos quêtes, dialogues,
évènements, personnages, … Nous avons commencé à réfléchir à la manière de
structurer ces données. Nous souhaitons décrire le plus précisément possible la
structure de ces fichiers afin de pouvoir implémenter leur lecture sans la
moindre ambiguïté possible. Nous avons des brouillons de ceci dans le dossier
doc du projet.

### Travail à faire

#### IHM
Nous souhaiterions implémenter un système de "pop up", de fenêtres qui
viendraient apporter des informations au joueur (tutoriel) ou bien lui poser des
questions (Confirmation avant de quitter, etc.).

De plus, l'`EventManager` n'est pas totalement fini. Le code est peu lisible. Il
est nécessaire d'améliorer ceci ainsi que d'implémenter d'autres évènements qui
ne sont pas encore gérés.

Enfin, nous souhaiterions trouver des sprites pour notre jeu. Nous allons
essayer de trouver des personnes à E-art sup pouvant nous les faire, puisque
nous avons des connaissances là-bas. Sinon, nous prendrons des Sprites trouvés
sur internet.

#### Mécaniques de jeu et structures de données
Nous devons continuer de clarifier la structure de nos données. Nous avons pour
objectif de finir la description des évènements et des dialogues ainsi que la
lecture en python de celles-ci pour le prochain rendu.
