"""A simplified matplot api
Copyright 2019 Yang Kaiyu yku12cn@gmail.com
"""

import matplotlib.pyplot as plt
import numpy as np


def draw(y=None, ran=None, res=10000, sudozero=0.00000001):
    """Draw a function in the given range
    Usage:
        draw(lambda x: (np.sin(x)/x), [0, 2*np.pi])
        draw(y=, ran=, res=, sudozero=0.00000001)
    """
    if not y:
        print(draw.__doc__)
        return False
    if not ran:
        xc = np.linspace(sudozero, sudozero + 1, res + 1)
    else:
        ran[0] = ran[0] + sudozero
        ran[1] = ran[1] + sudozero
        xc = np.linspace(ran[0], ran[1], res + 1)
    xc = xc[0:res]
    yc = y(xc)

    plt.plot(xc, yc, color="black")
    plt.grid(True, which='both', linestyle='--')

    plt.axhline(y=0, color='k', linestyle='--')
    plt.axvline(x=0, color='k', linestyle='--')

    plt.show()
    return True


# demo:
if __name__ == "__main__":
    draw(lambda x: (np.sin(x)/x), [0, 2*np.pi])
