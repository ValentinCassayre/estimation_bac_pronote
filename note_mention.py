# -*- coding: utf-8 -*-

from dataframes import Dataframes
import requests


class Estimateur:

    @staticmethod
    def print_all(reports_list, df_other_marks):

        df, note, points, total_points = Estimateur().calc_note(reports_list, df_other_marks)

        text_note = Estimateur().print_note(note, points, total_points)

        text_mention, text_felicitation = Estimateur().print_mention(note)

        text = '{}\n{}\n{}'.format(text_note, text_mention, text_felicitation)

        Estimateur.gen_pdf(text)

        return df

    @staticmethod
    def print_note(note, points, total_points):

        text = 'Votre note est estimée à {:.2f}, soit {:.2f}/{:.2f}'.format(note, points, total_points)
        print(text)

        return text

    @staticmethod
    def print_special_note(text, note, points, total_points):

        text = '{} Votre note serait de {:.2f}, soit {:.2f}/{:.2f}'.format(text, note, points, total_points)
        print(text)

        return text

    @staticmethod
    def print_mention(note):

        result, felicitations = Estimateur().calc_mention(note)
        print(result)
        print(felicitations)
        return result, felicitations

    @staticmethod
    def calc_note(reports_list, df_other_marks):
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

        # calc
        last_row = df.iloc[-1, :]
        points = last_row['roundedPoints']
        total_points =last_row['realCoefficient']*20

        note = 20 * points / total_points

        return df, note, points, total_points

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
                if diff >= -0.3:
                    if diff >= 0.8:
                        result = 'Il est presque certain que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif diff >= 0.3:
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

        url = "https://script.google.com/macros/s/AKfycbxl9nFMM8K9hEM3iD1o7cvzencXJd0fvrPitGD54V8LCAyKgzY/exec?invoice_id={}"

        invoice_id = text

        response = requests.get(url.format(invoice_id))
        response = requests.get(response.content)
        with open('output\Estimation.pdf', "wb") as file:
            file.write(response.content)
