# -*- coding: utf-8 -*-

from dataframes import Dataframes
import requests


class Estimateur:
    """
    dont read this
    """
    def __init__(self, name, reports_list, df_other_marks):
        self.name = name
        self.df = self.create_table(reports_list, df_other_marks)

    def print_all(self):

        note_arr, points_arr, total = self.calc_note(arr=True, opt=True, tot=True)
        note, points = self.calc_note(arr=False, opt=True, tot=False)
        note_opt_arr, points_opt_arr = self.calc_note(arr=True, opt=False, tot=False)
        note_opt, points_opt = self.calc_note(arr=False, opt=False, tot=False)

        text_mention, text_felicitation = self.calc_mention(note_arr)

        text = '{}, votre note est estimée à {:.2f} par arrondissement des moyennes au point supérieur ' \
               '({:.0f}/{:.0f}).\n{} {}\nVotre note serait de {:.2f} sans arrondissements ({:.0f}/{:.0f}).\n' \
               'Et elle serait de {:.2f} avec arrondissements mais sans options ({:.0f}/{:.0f}).\nOu de {:.2f}' \
               ' sans arrondissements ni options ({:.0f}/{:.0f}).'\
            .format(self.name, note_arr, points_arr, total, text_mention, text_felicitation, note, points,
                    total, note_opt_arr, points_opt_arr, total, note_opt, points_opt, total)

        print(text)

        self.gen_pdf(text)

    @staticmethod
    def create_table(reports_list, df_other_marks):
        """
        convert all the reports into one
        """

        ind = ['name', 'average', 'studentClassAverage', 'coefficient']
        av = ['average', 'studentClassAverage']

        df = reports_list[0].loc[:, ind].copy()

        # calc averages
        df.loc[:, av] = (reports_list[0].loc[:, av] + reports_list[1].loc[:, av]) / 2

        # add other grades
        df = df.append(df_other_marks, ignore_index=True)

        # create the full dataframe
        df = Dataframes().create_full_table(df)

        return df

    def calc_note(self, arr=True, opt=True, tot=True):

        rows = self.df.iloc[:-1, :]
        last_row = self.df.iloc[-1, :]

        if arr:
            grade = 'roundedAverage', 'roundedPoints'
        else:
            grade = 'average', 'points'

        if opt:
            points = last_row[grade[1]].sum()
        else:
            points = (rows[grade[0]]*rows['realCoefficient']).sum()

        total_points = last_row['realCoefficient'] * 20

        if total_points == 0:
            note = 20
        else:
            note = 20 * points / total_points

        if tot:
            return note, points, total_points

        else:
            return note, points

    @staticmethod
    def calc_mention(note):

        felicitations = ''
        notes = [12, 14, 16]
        mentions = ['assez bien', 'bien', 'très bien']

        if note >= 10:

            result = 'Vous avez votre bac.'
            felicitations = 'Félicitations !'

            for n, grade in enumerate(notes):
                diff = note - grade
                if diff >= -0.8:
                    if diff >= 0.8:
                        result = 'Il est presque certain que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif diff >= 0.5:
                        result = 'Il est très probable que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif note - grade >= 0:
                        result = 'Il est probable que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif n >= 1:
                        result = 'Il est possible que vous ayez votre bac avec mention {} (à {:.2f} points près) ' \
                                 'sinon vous aurez mention {}.'.format(mentions[n], -1*diff, mentions[n-1])
                    else:
                        result = 'Il est possible que vous ayez votre bac avec mention {}.'.format(mentions[n])

                else:
                    return result, felicitations

        else:
            if 10 - note < 2:
                result = 'Vous avez une note insuffisante pour avoir votre bac, mais la note est assez proche de la ' \
                         'moyenne (à {:.2f} points près) pour être reconsidéré ' \
                         'par un jury ou par un oral de rattrapage.'\
                    .format(10 - note)
            else:
                result = 'Vous avez une note insuffisante pour avoir votre bac.'

        return result, felicitations

    @staticmethod
    def gen_pdf(text):

        url = \
            "https://script.google.com/macros/s/" \
            "AKfycbxl9nFMM8K9hEM3iD1o7cvzencXJd0fvrPitGD54V8LCAyKgzY" \
            "/exec?invoice_id={}"

        invoice_id = text

        response = requests.get(url.format(invoice_id))
        response = requests.get(response.content)

        try:
            with open('output/graphs/pdf/Graph 0.pdf', "wb") as file:
                file.write(response.content)
        except PermissionError:
            print("Erreur dans l'enregistrement de la première page du bilan. Veuillez fermer l'ancien pdf "
                  "(output/graphs/pdf/0.pdf).")
