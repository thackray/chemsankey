import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch
from matplotlib.path import Path
import numpy as np

class ChemSankey(object):
    def __init__(self, ):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1,xticks=[],yticks=[],
                                       ylim=(-1.,1.), xlim=(-1.,1.)
                                       )

    def _add_node(self,loc,color='cyan',label='',
                  **kwargs):
        ell = Ellipse(loc, 0.1, 0.075,
                      facecolor=color,
                      alpha=0.9,
                      edgecolor='k',
                      label=label,
                      **kwargs)
        self.ax.add_artist(ell)

    def _make_connection(self,A,B,bend=1.5,width=3,
                         color='k',
                         **kwargs):
        a1, a2 = A[0],A[1]
        b1, b2 = B[0],B[1]
        path_codes = [Path.MOVETO,
                      Path.CURVE3,
                      Path.CURVE3,
                      ]
        Cont = [a1/abs(bend) + b1/bend, a2/abs(bend) + b2/bend]
        P = Path([A,Cont,B],path_codes)
        PP = PathPatch(P, 
                       fill=False,
                       color=color,
                       linewidth=width,
                       **kwargs)
        self.ax.add_artist(PP)
        

locs = {'A':np.array([0.,.7]),
        'B':np.array([.7,0.]),
        'C':np.array([.7,.7])
        }




CS = ChemSankey()
CS._make_connection(locs['A'],locs['B'])
CS._make_connection(locs['A'],locs['C'],width=4)
CS._add_node(locs['A'])
CS._add_node(locs['B'])
CS._add_node(locs['C'])
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1,xticks=[],yticks=[],title='',
#                     ylim=(-2,2),xlim=(-2,2))

#draw_arrow(locs['A'],locs['B'])
#draw_arrow(locs['A'],locs['C'])

plt.show()

