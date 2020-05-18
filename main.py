# -*- coding: utf-8 -*-

from load_pronote import Pronote
import os


def get_id():

    print("Connection à Pronote...")

    id = []
    complete = True

    with open("infos/connection_data.txt", 'r', encoding='utf-8') as file:

        for line in file:
            line = line.replace(' ', '').replace('\n', '')
            if not line.startswith('#'):
                data = line.split('=')
                if data[1] == '':
                    if complete:
                        print("Veuillez remplir les champs manquants :")
                        complete = False
                    id.append(input('{} : '.format(data[0].replace('_', ' '))))
                else:
                    id.append(data[1])

    return id


def connection():

    link, ac, username, password = get_id()

    try:

        pronote = Pronote(username=username, password=password, url=link, ac=ac)

        try:
            print("Connection réussie à Pronote {}".format(pronote.result['name']))
            return pronote

        except KeyError:
            print("Erreur lors de la connection à pronote : {}".format(pronote.result['error']))
            os.system('pause')

    except:

        print("Erreur lors de la connection à l'API de pronote. Veuillez la lancer.")
        os.system("pause")


def main():

    try:
        os.mkdir('output')

    except FileExistsError:
        pass

    pronote = connection()

    pronote.reports()

    finale_grade = pronote.est_bac()

    mention, felicitation = pronote.est_mention()

    print('Votre note est estimée à {:.2f}'.format(finale_grade))

    print(mention)

    print(felicitation)

    os.system("pause")


if __name__ == '__main__':
    main()
