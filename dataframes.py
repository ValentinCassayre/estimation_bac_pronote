# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


class Dataframes:
    """
    class related to the analysis of the grades in dataframes
    """

    @staticmethod
    def create_full_table(df):
        """
        create and manage a dataframes with all the grades and points
        """
        df.loc[:, 'obligatoire'] = df.loc[:, 'coefficient'] >= 2

        # real coeff
        df.loc[:, 'realCoefficient'] = df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire']
        df.loc[:, 'coefficient'] = df.loc[:, 'coefficient'] * 2 - df.loc[:, 'realCoefficient']

        # arrondie au superieur
        df.loc[:, 'roundedAverage'] = df.loc[:, 'average'].apply(np.ceil)

        # calc points
        df.loc[:, 'points'] = \
            df.loc[:, 'average'] * df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire'] + \
            (df.loc[:, 'average'] - 10) * df.loc[:, 'coefficient'] * (df.loc[:, 'obligatoire'] == 0)

        df.loc[:, 'roundedPoints'] = \
            df.loc[:, 'roundedAverage'] * df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire'] + \
            (df.loc[:, 'roundedAverage'] - 10) * df.loc[:, 'coefficient'] * (df.loc[:, 'obligatoire'] == 0)

        df.loc[:, 'studentPoints'] = \
            df.loc[:, 'studentClassAverage'] * df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire'] + \
            (df.loc[:, 'studentClassAverage'] - 10) * df.loc[:, 'coefficient'] * (df.loc[:, 'obligatoire'] == 0)

        df.loc[:, 'maxPoints'] = \
            20 * df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire']

        df.loc[:, 'difference'] = df.loc[:, 'average'] - df.loc[:, 'studentClassAverage']
        df.loc[:, 'roundedDifference'] = df.loc[:, 'roundedPoints'] - df.loc[:, 'points']

        # add total row
        try:
            df.loc['TOTAL']

        except KeyError:
            total = df.sum(axis=0, dtype=None, numeric_only=True)
            total['name'] = 'TOTAL'
            df = df.append(total, ignore_index=True)

        # export dataframe
        df.to_csv('output/Relevé bac.csv', sep=';')

        return df

    @staticmethod
    def from_file(file):
        df = pd.read_csv(file, sep=';')
        print(df)
        Dataframes.create_full_table(df)
        return df
