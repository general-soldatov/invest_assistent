import matplotlib.pyplot as plt
from io import BytesIO
import base64
from mail_parse import MainPage

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

        self.plot.plot(absciss, ordinate)
        self.plot.plot(absciss, ordinate_cumul)

    def graph_bytes(self):
        # self.plot.show()
        bio = BytesIO()
        self.plot.savefig(bio, format="png")
        bio.seek(0)
        return base64.b64encode(bio.read()).decode('utf-8')

if __name__ == "__main__":
    data = ByteGraph()
    data.graph_1(MainPage().get_cash())
    data.graph_bytes()