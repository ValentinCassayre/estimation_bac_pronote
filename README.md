# Estimateur de note de bac 2020

Ce script python permet d'évaluer et d'estimer une note ainsi qu'une mention pour le bac de 2020 qui sera en contrôle continue. 
Pour ça j'utilise la superbe api pronote de Litarvan (https://github.com/Litarvan/pronote-api).

## Méthode de calcul

La note est estimé d'après les notes des bulletins des deux premiers trimestres publiés sur pronote et des notes ajoutés dans le fichier 
(voir la rubrique *utilisation*) ainsi que leurs coefficients. Les deux bulletins sont d'abord fusionnées en gardant la moyenne
et les coefficients de chaque matière. Chacune de ces moyennes, arrondies au supérieur (d'après le décret le plus récent) 
correspondent à la note de l'épreuve. Le total de points de l'élève est calculé en multipliant
chacune de ces notes par le coefficient de la matière. Le total des points est donc 20*le total des coefficients. \
Maintenant vient également les notes des options qui comptent comme bonus. Chaque point au dessus de la moyenne est multiplié
par son coefficient (d'après les coefficients officiels du bac) ou par le double de son coefficient 
(en prennant le coeff. pronote qui est la moitié du coeff officiel). Ces points bonus une fois additionnées sont ajoutés
au total des points de l'élève sans que le total des points maximum ne change.\
Si vous avez des remarques à faire n'hésitez pas à [m'en faire part](http://valentin.cassayre.me/contact).

## Avantage du script

* Automatisé au maximum
* Base du script utilisable pour créer d'autres scripts Pythons, par exemple pour récupérer des devoirs ou faire des
moyennes de notes
* Sors une base de bulletin en format de tableur (*output/Trimestre n.csv*)
* Sors un détail de toutes les notes (*output/Relevé notes.csv*)
* Plus classe que de calculer à la main

## Limites du script

* L'installation peut être longue
* La connection n'est pas forcément sécurisée
* Certains coefficients peuvent être erronés sur pronote (par exemple les langues vivantes peuvent être les deux coeff. 3)
* Il peut y arriver que le script ne se lance pas et affiche une erreur au niveau de l'académie. Cela s'explique par une 
saturation du serveur de pronote (voir message d'erreur de l'api)
* Il faut avoir pronote pour utiliser le script
* Ce n'est qu'une estimation, la note finale sera surement un peu différente, la méthode de calcul est loin d'être parfaite
et n'est qu'une supposition. D'autres facteurs comme les appréciations et le livret scolaire vont également compter pour ce bac assez spécial.

# Comment l'utiliser ?

D'abord [téléchargez et décompressez le script](https://github.com/V-def/estimation_bac_pronote) et
[téléchargez et décompressez l'api](https://github.com/Litarvan/pronote-api).
Ensuite allez dans le dossier du script puis dans le dossier 'infos'. Il y a **deux fichiers à remplir** :
1. Le fichier *connection_data.txt* doit contenir les 4 informations suivantes :
   1. *Lien_pronote* s'obtient en se connectant à pronote, il sera de la forme
   *00000000.index-education.net/pronote/eleve/...* mais retirez la partie qui se trouve après
   pronote/ pour obtenir un lien de la forme *00000000.index-education.net/pronote/*.
   2. *Académie* est le nom de l'académie, par exemple *ac-strasbourg* ou *ac-lyon*.
   3. *Utilisateur* est l'identifiant de votre ENT.
   4. *Mot_de_passe* est le mot de passe de votre ENT. 
   Pour une protection des données il est conseillé de ne pas le
   remplir dans le fichier le mot de passe, il vous sera demandé par le script.

2. Le fichier *marks_data* sert à ajouter des notes qui ne sont pas présentes sur pronote. Dans la majorité des cas
il s'agit des épreuves anticipées, mais il peut également s'agir d'une matière qui n'est pas noté sur pronote. 
Pour ajouter la note, sautez une ligne dans le fichier texte et écrivez le nom de la matière en majuscules,
puis un séparateur ';' suivit de la note en question, d'un autre séparateur ';', et enfin du coefficient de la matière. 
Si la matière est une option, indiquer la moitié du coefficient, par exemple le TPE de coefficient 2 devient de coefficient 1.

Une fois ces informations rentrées vous pouvez lancer le script et l'api.

## Sous windows

### Lancer l'api

[Télécharger node et suivre toutes les instructions](https://nodejs.org/dist/v12.16.3/node-v12.16.3-x64.msi)
Lancer l'invite de commandes en tappant cmd dans la barre de recherche windows, et récupérer le chemin d'accès vers l'api
téléchargé précedemment (chemin d'accès = C:\Users\...\pronote-api-master), puis tapper 'cd ' suivi du chemin d'accès :\
`cd C:\Users\...\pronote-api-master`\
Ensuite tappez\
`npm i`\
`node index.js`\
L'api est lancée et la console devrait afficher :\
`Starting...
---> Pronote API HTTP Server working on 127.0.0.1:21727`

### Lancer le script

Il y a deux possibilités pour lancer le script, la première méthode est plus simple et ne nécessite plus rien, mais 
n'est peut être pas mis à jour.

#### Par l'executable

Retourner dans le dossier *estimation_bac_pronote-master* et lancer l'executable

#### En utilisant python

Récupérer le chemin d'accès vers le dossier du script (C:\...\estimation_bac_pronote-master) et rentrer dans une 
autre fenêtre de la console (cd + le chemin d'accès) :\
`cd C:\...\estimation_bac_pronote-master`\
Puis installez les modules python :\
`pip install -r requirements.txt`\
Et lancez le script en double cliquant sur main.py ou en rentrant dans la console\
 `main.py`

## Sous linux

### Lancer l'api

Dans le terminal si ce n'est pas déjà fait installez npm et node\
`$ sudo apt-get install nodejs npm`\
Une fois que c'est fait vous pouvez vous rendre dans le dossier de l'api que vous avez téléchargé\
`$ cd usr/.../pronote-api-master`\
Puis lancez l'api\
`$ npm i`\
`$ node index.js`\
Le terminal devrait afficher\
`Starting...
---> Pronote API HTTP Server working on 127.0.0.1:21727`

### Lancer le script

Rendez vous dans le dossier du script téléchargé et remplit précédemment\
`$ cd usr/.../estimation_bac_pronote-master`\
Pour installer les librairies installez pip si ce n'est pas fait\
`$ sudo apt install python3-pip`\
Puis installez les\
`$ pip3 install -r requirements.txt`\
Maintenant vous pouvez lancer le script\
`$ python3 main.py`\
La note est affichée à l'écran avec la mention

##Les graphiques

Le script crée automatiquement un certain nombre de graphiques, ils sont tous rangés dans le dossier *output/graphs*.
Voici des explications plus claires que leur titre et leur mini légende :\

### Les nuages de points

1. Ce premier nuage de points a comme ordonnée les matières et en abscisses les notes. Les points colorés représentent la moyenne
de chaque matière. La taille des points correspond au coefficient donc au poids de la moyenne dans la note finale. La 
couleur de ces points représente l'écart à la moyenne de la classe, plus la couleur est dans le haut de la colormap plus
la note est bonne par rapport à la moyenne de la classe. Les triangles représentent les moyennes des trimestres 
(T1 > et T2 <) et par la même occasion les barres verticales représentent les moyennes de classe dans les trimestres correspondants (|).
Le carré gris représente la moyenne de classe des deux trimestres.

2. Ce deuxième nuage de points est une représentation plus simple du dernier. La note de l'élève est tracé par un rond coloré ayant des
coordonnées relatives à elle même en abscisse et à la moyenne de la classe en ordonnée. Comme le précédent la couleur
représente la différence par rapport à la moyenne de classe.

### Les histogrammes

1. Le premier histogramme est une représentation simple des points. Les points correspondent au produit entre la note d'une
matière et son coefficient. En ordonnée les matières et en abscisse les points. Plusieurs barres sont présentes, d'abord il y
a la moyenne de classe, puis la moyenne de tes points, ensuite la moyenne de tes points avec les notes arrondies au supérieur
et enfin le maximum de points possibles pour cette matière.

### Les graphiques en boite

1. Le graphique en boite représente des informations sur chaque données comme la moyenne en vert au milieu, ou les quartiles
qui représentent ou se trouve la majorité des notes. Les extrémités des valeurs sont aussi données.

### Le radar

1. Le radar est une représentation d'un graphique avec des lignes dans un repère polaire. Il représente les notes de l'élève,
ainsi que les notes arrondies de l'élèves et sont comparées à la moyenne de classe dans chaque matière.

#### Des problèmes ? [Contactez moi](http://valentin.cassayre.me/contact)
