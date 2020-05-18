# -*- coding: utf-8 -*-

from urllib import request
import json
import pandas as pd


class Pronote:
    """
    class that load the data from Pronote
    """

    def __init__(self, username, password, url, ac):

        self.reports_list = []
        self.other_marks = []
        self.finale_grade = 0

        self.body = {"type": "fetch", "username": username, "password": password, "url": url, "cas": ac}

        self.jsondata = json.dumps(self.body).encode("utf8")

        req = request.Request("http://127.0.0.1:21727/")
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        res = request.urlopen(req, self.jsondata).read()
        page = res.decode("utf8")

        self.result = json.loads(page)

        with open('output/pronote.txt', 'w', encoding='utf-8') as txt:
            txt.write(str(self.result))

    def reports(self):
        """
        return the reports
        """
        for trimester in range(3):
            report = self.result['reports'][trimester]
            try:
                df = pd.DataFrame(report['subjects'])
                self.reports_list.append(df)
                df.to_csv('output/Bulletin Trimestre {}.csv'.format(trimester + 1), sep=';')

            except KeyError:
                pass

        return self.reports_list

    def load_notes_bac(self):
        """
        load the additional notes from the première (Français/TPE/Sciences...)
        """

        with open('infos/marks_data.txt', 'r', encoding='utf-8') as txt:
            for line in txt:
                line = line.replace('\n', '')
                if line.startswith('#'):
                    pass
                else:
                    data = line.split(';')
                    dico = {'name': data[0], 'average': float(data[1]), 'coefficient': float(data[2])}
                    self.other_marks.append(dico)

    def est_bac(self):
        """
        convert all the reports into one
        """

        dico1 = self.reports_list[0].to_dict(orient='records')
        dico2 = self.reports_list[1].to_dict(orient='records')

        output = []

        self.load_notes_bac()

        for n, _ in enumerate(dico1):

            temp = {}
            temp.update({'name': dico1[n]['name']})
            temp.update({'average': (dico1[n]['average']+dico2[n]['average'])/2})
            temp.update({'coefficient': dico1[n]['coefficient']})

            output.append(temp)

        for data in self.other_marks:
            output.append(data)

        df = pd.DataFrame(output)

        df.to_csv('output/Relevé bac.csv', sep=';')

        points = 0
        total_points = 0

        for index, row in df.iterrows():
            if row['coefficient'] >= 2:
                points = points + row['average']*row['coefficient']
                total_points = total_points + 20 * row['coefficient']

            elif row['average'] > 10.0:
                points = points + (row['average']-10) * row['coefficient'] * 2

        self.finale_grade = 20*points/total_points

        return self.finale_grade

    def est_mention(self):

        felicitations = ''
        mentions = ['assez bien', 'bien', 'très bien']

        if self.finale_grade >= 10:

            result = 'Vous avez votre bac.'
            felicitations = 'Félicitations !'

            for n, grade in enumerate([12, 14, 16]):
                diff = self.finale_grade - grade
                if diff >= -0.3:
                    if diff >= 0.8:
                        result = 'Il est presque certain que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif diff >= 0.3:
                        result = 'Il est très probable que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif self.finale_grade - grade >= 0:
                        result = 'Il est probable que vous ayez votre bac avec mention {}.'.format(mentions[n])
                    elif n >= 1:
                        result = 'Il est possible que vous ayez votre bac avec mention {} (à {:.2f} points près) ' \
                                 'sinon vous aurez mention {}.'.format(mentions[n], -1*diff, mentions[n-1])
                    else:
                        result = 'Il est possible que vous ayez votre bac avec mention {}.'.format(mentions[n])

                else:
                    return result

        else:
            if 10 - self.finale_grade < 2:
                result = 'Vous avez une note insuffisante pour avoir votre bac, mais la note est assez proche de la ' \
                         'moyenne (à {:.2f} points près) pour être reconsidéré ' \
                         'par un jury ou par un oral de rattrapage.'\
                    .format(10 - self.finale_grade)
            else:
                result = 'Vous avez une note insuffisante pour avoir votre bac.'

        return result, felicitations
