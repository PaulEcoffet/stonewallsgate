Dunwall's Gate
==============

Le jeu se lance en exécutant le fichier `src/dunwallsgate.py`

Fonctionnement IHM
------------------

Le jeu lance une `Window`. la `window` charge un screen, qui est soit
un `HomeScreen`, l'écran d'accueil, un `StoryScreen`, l'écran "histoire"
ou "cinématique" ou bien un `BattleScreen` l'écran de combat.

Le screen dessine sur la surface de `window` des sprites, soit directement
soit à l'aide de classes personnalisées héritées de `pygame.Sprite`, situé
dans `src/customsprite.py` et `src/button.py`.

Les évènements pygame (les entrées utilisateurs) sont géré par un `EventManager`
situé dans `src/event_manager.py`. Il enregistre l'ensemble des actions
possibles et appelle des *callbacks* quand un évènement est vérifié. Il est
possible de verrouiller ces *callbacks* afin de bloquer leur déclenchement.

Fonctionnement Gameplay
-----------------------

Lorsque l'utilisateur clique sur *NEW GAME*, un nouvel objet `Game` est crée. Il
déclenche un `StoryScreen` qui va déclencher un évènement situé dans la scène
`intro`.

Le déroulement du programme se fait par un système d'*évènement de jeu* et de
*scène*. Pour chaque scène, une liste d'évènements est disponible. Cette liste
se situe dans `data/scenes/<nom_scene>/events.json`. Un évènement ne peut être
déclenché que s'il respecte que toutes ses conditions (par exemple, le héros a
plus de 50hp). Il doit toujours y avoir au moins un évènement qui peut être
déclenché. Les évènements sont gérés par `src/game_event.py`

Dans la version du programme rendu, toutes les scènes ne contiennent
qu'un unique évènement, il n'est donc pas nécessaire de leur donner de
conditions particulières.

Un évènement déroule soit une *cinématique*, avec dialogue et choix, soit un
combat. Durant un évènement, des *déclencheurs* (*triggers*) peuvent être
déclenchés. Ils peuvent être soit déclenché par défaut ou peuvent varier en
fonction des choix du joueur, ou bien de la réussite du combat ou non. Ces
triggers peuvent modifier l'état du joueur, des quêtes qu'il a en cours, ou bien
forcer un déplacement sur une nouvelle scène.

Lorsque l'evenement est un combat, le joueur doit affronter au maximum 4
adversaires avec l'aide d'au maximum 3 compagnons. Dans le cas des compagnons,
le programme se base sur la liste de personnage `hero_compagnon`, cette liste
peut être modifié au cours du jeu grâce à d'autres évenements.  Dans l'autre
cas, les adversaires sont déterminés dans la déclaration du battle.  Les
capacités initiales d'un personnage au combat sont introduites dans le fichier
`characters.json`. En fonction de ce fichier, les personnages auront des
statistiques différentes, ces statistiques peuvent être fixé arbitrairement ou
selon une loi de probabilité.

Le combat se déroule en 4 phases dont 2 potentiellement discrètes.  Le programme
tache de trouver l'arme de base et de la mettre dans la "main" du joueur. Si
cette arme nécessite des munitions mais qu'aucune munition n'est trouvé alors le
joueur doit changer d'arme avant d'attaquer.  Il doit pour ce faire cliquer sur
le boutton `WEAPONS` qui lui permettra forcemment de trouver une arme convenable
(avec ou sans munitions).  Le joueur peut dans tout les cas utiliser ses mains
s'il se retrouve sans munition.  Cette étape de faite, le joueur doit maintenant
attaquer. Pour ce faire il faut cliquer sur `ATTACK`puis choisir l'adversaire
qui recevra le coup en cliquant sur un des portraits.  Le joueur ne peut pas
choisir un adversaire mort. Une attaque peut potentiellement faire baisser la
vie du receveur, cela depend de sa défense et de la puissance de l'arme adverse.
De plus si l'attaque a nécessité une munition, cette munition est dégradée.

Une IA minimaliste se charge de produire un comportement similaire au joueur, en
l'attaquant lui ou ses compagnons selon les même critères.  L'IA cherche
néanmoins à utiliser l'arme la plus puissante du joueur qu'elle contrôle.

Le combat se termine si l'une des deux équipes se retrouve sans aucun joueur
vivant.  Le joueur peut aussi décider de terminer le combat en s'échappant. Ce
faisant, il perd le combat.  L'IA  ne peut pas s'échapper. A la fin du combat,
les triggers adéquats sont déclanchés en fonction de quelle équipe a gagné, ces
triggers sont définis en même temps que la déclaration du battle.
