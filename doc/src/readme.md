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
plus de 50hp). Il doit y toujours y avoir au moins un évènement qui peut être
déclenché. Les évènements sont gérés par `src/game_event.py`

Dans la version actuel du programme rendu, toutes les scènes ne contiennent
qu'un unique évènement, il n'est donc pas nécessaire de leur donner de
conditions particulières.

Un évènement déroule soit une *cinématique*, avec dialogue et choix, soit un
combat. Durant un évènement, des *déclencheurs* (*triggers*) peuvent être
déclenchés. Ils peuvent être soit déclenché par défaut ou peuvent varier en
fonction des choix du joueur, ou bien de la réussite du combat ou non. Ces
triggers peuvent modifier l'état du joueur, des quêtes qu'il a en cours, ou bien
forcer un déplacement sur une nouvelle scène.
