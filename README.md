# Estimateur de note de bac 2020

Ce script python permet d'évaluer et d'estimer une note ainsi qu'une mention pour le bac de 2020 qui sera en contrôle continue. Pour ça il
utilise l'api pronote de Litarvan https://github.com/Litarvan/pronote-api.

## Avantage du script

* Automatisé au maximum
* Base du script utilisable pour créer d'autres scripts Pythons, par exemple pour récupérer des devoirs ou faire des
moyennes de notes
* Sors une base de bulletin en format de tableur (*Trimestre n.csv*)
* Sors un détail de toutes les notes (*Relevé notes.csv*)
* Plus classe que de calculer à la main

## Limites du script

* L'installation peut être longue
* Certains coefficients peuvent être erronés sur pronote (par exemple les langues vivantes peuvent être les deux coeff. 3)
* Il peut y arriver que le script ne se lance pas et affiche une erreur au niveau de l'académie
* Il faut avoir pronote pour utiliser le script
* Ce n'est qu'une estimation, la note finale sera surement un peu différente, la méthode de calcul que j'utilise pour
calculer la note n’est qu’une hypothèse. Je fais une moyenne des notes de chaque matières dans les deux premiers trimestres et je la
coefficients avec les coefficients du bac. Je fais ensuite une moyenne de toutes ces notes. Et pour les options je prends
les points au dessus de 10 et ils sont ajoutés à la note finale.

# Comment l'utiliser ?

D'abord [téléchargez et décompressez le script](https://github.com/V-def/estimation_bac_pronote) et
[téléchargez et décompressez l'api](https://github.com/Litarvan/pronote-api).
Ensuite allez dans le dossier du script puis dans le dossier 'infos'. Il y a **deux fichiers à remplir** :
1. Le fichier *connection_data.txt* doit contenir les 4 informations suivantes :
   1. *Lien_pronote* s'obtient en se connectant à pronote, il sera de la forme
   *00000000.index-education.net/pronote/eleve/...* mais retirez la partie qui se trouve après
   pronote/ pour obtenir un lien de la forme *00000000.index-education.net/pronote*.
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
## Sous linux
### Lancer l'api
Dans le terminal si ce n'est pas déjà fait installez npm et node\
`$ sudo apt-get install nodejs npm`\
Une fois que c'est fait vous pouvez vous rendre dans le dossier de l'api que vous avez téléchargé\
`$ cd usr/.../pronote-api-master`\
Puis lancez l'api\
`$ node index.js`\
Le terminal devrait afficher🍞\
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
