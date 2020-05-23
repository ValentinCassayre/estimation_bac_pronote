# -*- coding: utf-8 -*-

import numpy as np


class Dataframes:
    """
    class related to the analysis of the grades in dataframes
    """
    @staticmethod
    def create_full_table(df):
        """
        create other columns in the table
        """
        # arrondi au superieur
        df.loc[:, 'roundedAverage'] = df.loc[:, 'average'].apply(np.ceil)

        # option
        df.loc[:, 'obligatoire'] = df.loc[:, 'coefficient'] >= 2

        # calc points
        df.loc[:, 'points'] = df.loc[:, 'average'] * df.loc[:, 'coefficient']
        df.loc[:, 'roundedPoints'] = df.loc[:, 'roundedAverage'] * df.loc[:, 'coefficient']
        df.loc[:, 'studentPoints'] = df.loc[:, 'studentClassAverage'] * df.loc[:, 'coefficient']
        df.loc[:, 'maxPoints'] = 20 * df.loc[:, 'coefficient']

        # real coeff
        df.loc[:, 'realCoefficient'] = df.loc[:, 'coefficient'] * df.loc[:, 'obligatoire']
        df.loc[:, 'coefficient'] = df.loc[:, 'coefficient'] * 2 - df.loc[:, 'realCoefficient']

        df.loc[:, 'difference'] = df.loc[:, 'average'] - df.loc[:, 'studentClassAverage']
        df.loc[:, 'roundedDifference'] = df.loc[:, 'roundedPoints'] - df.loc[:, 'points']

        # add total row
        total = df.sum(axis=0, dtype=None, numeric_only=True)
        total['name'] = 'TOTAL'
        df = df.append(total, ignore_index=True)

        # export dataframe
        df.to_csv('output/Relevé bac.csv', sep=';')

        return df
