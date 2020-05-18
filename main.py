from load_pronote import Pronote
import os


def get_id():

    print("Connection à Pronote...")

    id = []
    complete = True

    with open("infos/connection_data.txt", 'r') as file:

        for line in file:
            line = line.replace(' ', '').replace('\n', '')
            if line.startswith('#'):
                pass
            else:
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
            os.system('break')
            exit()

    except Exception:

        print("Erreur lors de la connection à l'API de pronote. Veuillez la lancer.")
        os.system("break")
        exit()


def main():

    pronote = connection()

    pronote.reports()

    finale_grade = pronote.est_bac()

    mention = pronote.est_mention()

    print('Votre note est estimée à {:.2f}'.format(finale_grade))

    print(mention)


if __name__ == '__main__':
    main()
