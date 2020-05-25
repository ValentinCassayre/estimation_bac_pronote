# -*- coding: utf-8 -*-

from load_pronote import Pronote
from note_mention import Estimateur
from graphs import Graph
import urllib

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

        pronote = Pronote(user_id=(username, password, link, ac), offline=True)

        try:
            print("Connection réussie à Pronote {}".format(pronote.result['name']))
            return pronote

        except KeyError:

            print("Erreur lors de la connection à pronote : {}".format(pronote.result['error']))

            try:
                return offline_connection()
            except:
                os.system('pause')

    except urllib.error.URLError:

        print("Erreur lors de la connection à l'API de pronote. Veuillez la lancer.")

        try:
            return offline_connection()
        except FileNotFoundError:
            print('Pas de sauvegarde de connection trouvé.')
            os.system('pause')


def offline_connection():

    pronote = Pronote(None, offline=True)
    return pronote


def make_dir():

    for path in ['output', 'output/graphs', 'output/graphs/pdf']:

        try:
            os.mkdir(path=path)

        except FileExistsError:
            pass


def main():

    make_dir()

    pronote = connection()

    bulletins = pronote.reports()

    pronote.load_notes_bac()

    df = Estimateur().print_all(pronote.result['name'], pronote.reports_list, pronote.df_other_marks)

    Graph(df, bulletins)

    print('Les graphiques ont été téléchargé dans output/graphs ou dans le fichier output/bilan')

    os.system("pause")


if __name__ == '__main__':
    main()
