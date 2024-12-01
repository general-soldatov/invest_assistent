import matplotlib.pyplot as plt
from io import BytesIO
import base64

def graph_bytes():
    x = [1, 2, 3, 4, 5]
    y = [25, 32, 34, 20, 25]

    plt.plot(x, y)
    bio = BytesIO()
    plt.savefig(bio, format="png")

    bio.seek(0)
    return base64.b64encode(bio.read())