import matplotlib.pyplot as plt
import numpy as np

class ChemSankey(object):
    def __init__(self, ):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1,xticks=[],yticks=[],
                                       ylim=(-1.,1.), xlim=(-1.,1.)
                                       )

    def _add_node(self,loc,**kwargs):
        

    def _make_connection(self,A,B,width=0.01,**kwargs):
        a1, a2 = A[0],A[1]
        b1, b2 = B[0],B[1]
        plt.arrow(a1,a2,b1-a1,b2-a2,
                  length_includes_head=True, 
                  head_length=width,
                  head_width=width*2,
                  width=width,
                  **kwargs)
        

locs = {'A':np.array([0.,.7]),
        'B':np.array([.7,0.]),
        'C':np.array([.7,.7])
        }

CS = ChemSankey()
CS._make_connection(locs['A'],locs['B'])
CS._make_connection(locs['A'],locs['C'],width=0.04)
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1,xticks=[],yticks=[],title='',
#                     ylim=(-2,2),xlim=(-2,2))

#draw_arrow(locs['A'],locs['B'])
#draw_arrow(locs['A'],locs['C'])

plt.show()

