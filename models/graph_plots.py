import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import base64
# from mail_parse import MainPage

class ByteGraph:
    def __init__(self):
        self.plot: plt = plt

    def graph_1(self, data: dict):
        absciss = []
        ordinate = []
        ordinate_cumul = []
        cash = 0
        for x, y in sorted(data.items(), key=lambda x: x[0]):
            absciss.append(x)
            ordinate.append(y)
            cash += y
            ordinate_cumul.append(cash)
        self.plot.figure(figsize=(7, 4), layout="constrained")
        self.plot.plot(absciss, ordinate)
        self.plot.plot(absciss, ordinate_cumul)

    def graph_cash(self, usd, eur, diff_usd, diff_eur):
        def lineFunc(x, y, reversed=False, hight=0.2):
            color='green'
            diff = (0, hight)
            if reversed:
                y += hight
                diff = map(lambda x: -1 * x, diff)
                color='red'
            line = mpatches.Arrow(x, y, *diff, width=0.15)
            line.set(color=color)
            return line

        axs = self.plot.figure(figsize=(7, 4), layout="constrained")
        axs.add_artist(lineFunc(0.85, 0.1, reversed = diff_eur < 0))
        axs.text(0.58, 0.2, eur, size=50, rotation=0.,
                ha="center", va="center",
                bbox=dict(boxstyle="square",
                        ec='#FFEFD5',
                        fc='#FFF5EE',
                        )
                )
        axs.add_artist(lineFunc(0.85, 0.4, reversed = diff_usd < 0))
        axs.text(0.58, 0.5, usd, size=50, rotation=0.,
                ha="center", va="center",
                bbox=dict(facecolor='#FFF5EE', edgecolor='#FFEFD5', boxstyle="square",
                        # ec=(1., 0.5, 0.5),
                        # fc=(1., 0.8, 0.8),
                        )
                )
        axs.text(0.03, 0.8, f"КУРСЫ ВАЛЮТ ЦБ", size=50, rotation=0.,
                ha="left", va="center",
                color='white',
                bbox=dict(boxstyle="square", facecolor='black', edgecolor='black')
                )
        axs.text(0.03, 0.5, "USD $", size=50, rotation=0.,
                ha="left", va="center",
                color='black',
                bbox=dict(boxstyle="square", facecolor='#D3D3D3', edgecolor='#A9A9A9')
                )
        axs.text(0.03, 0.2, "EUR €", size=50, rotation=0.,
                ha="left", va="center",
                color='black',
                bbox=dict(boxstyle="square", facecolor='#D3D3D3', edgecolor='#A9A9A9')
                )
        self.plot.axis('off')

    def graph_bytes(self):
        bio = BytesIO()
        self.plot.savefig(bio, format="png")
        bio.seek(0)
        return base64.b64encode(bio.read()).decode('utf-8')

if __name__ == "__main__":
    data = ByteGraph()
    # data.graph_1(MainPage().get_cash())
    data.graph_cash(123.0, 4.5, -1, -1)
    # data.graph_bytes()
    data.plot.show()