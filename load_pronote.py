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
        self.df_other_marks = None

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
                    dico = {'name': [data[0]], 'average': [float(data[1])], 'coefficient': [float(data[2])]}
                    df = pd.DataFrame(dico)
                    if self.df_other_marks is None:
                        self.df_other_marks = df
                    else:
                        self.df_other_marks = self.df_other_marks.append(df, ignore_index=True)
