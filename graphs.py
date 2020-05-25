import matplotlib.pyplot as plt
import numpy as np
from PyPDF2 import PdfFileReader, PdfFileMerger


class Graph:
    """
    draw graphs
    """

    def __init__(self, df, trim_rep):

        self.df = df
        self.dft1, self.dft2 = trim_rep

        self.n = 1

        for name in ('Nuage de points 1', 'Nuage de points 2', 'Histogramme 1', 'Box 1', 'Radar 1'):

            try:

                self.draw(name)
                self.n = self.n + 1

            except:

                print("Erreur, le graphique '{}' n'a pas pu être téléchargé.".format(name))

        self.create_report()

    def draw(self, name):

        # remove TOTAL row
        df = self.df.iloc[:-1, :]

        if name.startswith('Nuage de points'):

            # nice colormaps : 'RdYlBl', 'RdYlGn', 'Spectral'
            colormap = 'RdYlGn'

            if name.endswith('1'):

                ax = df.plot.scatter(x='average', y='name', c='difference', colormap=colormap, s=df['coefficient'] * 50)

                self.dft1.plot.scatter(ax=ax, x='studentClassAverage', y='name', c='grey', s=50, marker='|', alpha=0.4)
                self.dft2.plot.scatter(ax=ax, x='studentClassAverage', y='name', c='grey', s=50, marker='|', alpha=0.4)

                df.plot.scatter(ax=ax, x='studentClassAverage', y='name', c='grey', s=10, marker='s', alpha=0.3)

                self.dft1.plot.scatter(ax=ax, x='average', y='name', color='lightblue', s=50, marker='>', alpha=0.2)
                self.dft2.plot.scatter(ax=ax, x='average', y='name', color='lightblue', s=50, marker='<', alpha=0.2)

                plt.xlabel('Moyennes')
                plt.ylabel('Matières')
                plt.title('Graphique des notes en fonction du coefficient')

                plt.subplots_adjust(left=0.35)

            elif name.endswith('2'):

                ax = df.plot.scatter(x='average', y='studentClassAverage', c='difference', colormap=colormap,
                                     s=df['coefficient'] * 50)

                plt.xlabel('Moyennes personnelles')
                plt.ylabel('Moyennes de classe')
                plt.title('Graphique des notes en fonction de la moyenne de classe')

                tp = df.iloc[:3, :]
                tp = list(tp['average']) + list(tp['studentClassAverage'])

                lim = min(tp) / 1.2, max(tp) * 1.2

                plt.xlim(lim)
                plt.ylim(lim)

        elif name.startswith('Histogramme'):

            if name.endswith('1'):

                df = df.sort_values(by=['maxPoints'])
                ax = df.plot.barh(x='name', y=['maxPoints', 'roundedPoints', 'points', 'studentPoints'], rot=0,
                                  color=['silver', 'darkgreen', 'green', 'teal'])

                plt.xlabel('Points (Note * Coefficient)')
                plt.ylabel('Matières')
                plt.title('Graphique des points reçus')
                ax.legend(['Maximum', 'Points de la note arrondie', 'Points reçus', 'Moyenne de la classe'])

                plt.subplots_adjust(left=0.35)

        elif name.startswith('Box'):

            if name.endswith('1'):

                ax = df.plot.box(y=['average', 'roundedAverage', 'studentClassAverage'], rot=0)

                ax.set_xticklabels(('Moyenne', 'Moyenne arrondie', 'Moyenne de la classe'))
                plt.title('Graphique en boite des moyennes personnelles et de la classe')

        elif name.startswith('Radar'):

            if name.endswith('1'):

                labels = df.loc[:, 'name']

                num_vars = len(labels)
                angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

                angles += angles[:1]

                fig, ax = plt.subplots(subplot_kw=dict(polar=True))

                def add_to_radar(label, color):
                    values = df.loc[:, label].tolist()
                    values = [10 if x != x else x for x in values]
                    values += values[:1]
                    ax.plot(angles, values, color=color, linewidth=1, label=label)

                add_to_radar('average', '#1aaf6c')
                add_to_radar('roundedAverage', 'green')
                add_to_radar('studentClassAverage', 'red')

                ax.set_theta_offset(np.pi / 2)
                ax.set_theta_direction(-1)

                ax.set_thetagrids(np.degrees(angles), labels)

                for label, angle in zip(ax.get_xticklabels(), angles):
                    if angle in (0, np.pi):
                        label.set_horizontalalignment('center')
                    elif 0 < angle < np.pi:
                        label.set_horizontalalignment('left')
                    else:
                        label.set_horizontalalignment('right')

                ax.set_ylim(0, 20)
                ax.set_rgrids([0, 5, 10, 15, 20])

                ax.set_rlabel_position(180 / num_vars)

                ax.tick_params(colors='black')
                ax.tick_params(axis='y', labelsize=8)
                ax.grid(color='lightgrey', alpha=0.4)
                ax.spines['polar'].set_color('grey')
                ax.legend(loc='lower right', bbox_to_anchor=(1.7, -0.4),
                          labels=('Moyenne', 'Moyenne arrondie', 'Moyenne de la classe'))
                ax.set_title("Graphique des notes de l'année en fonction de la moyenne de classe", y=1.2)
                plt.subplots_adjust(left=0.3, right=0.7)

        for file in ('output/graphs/pdf/Graph {}.pdf'.format(self.n), 'output/graphs/{}.png'.format(name)):
            try:
                plt.savefig(file)
            except PermissionError:
                print("Erreur dans l'enregistrement de {}. Veuillez fermer l'ancien document ({})."
                      .format(name.lower(), file))

    def create_report(self):
        """
        merge all graphs into one file
        """

        merged = PdfFileMerger()

        for fileNumber in range(self.n):
            merged.append(PdfFileReader('output\graphs\pdf\Graph {}.pdf'.format(fileNumber), 'rb'))

        try:
            merged.write("output/Bilan.pdf")
        except PermissionError:
            print("Erreur dans l'enregistrement du bilan. Veuillez fermer l'ancien pdf (output/Bilan.pdf).")
