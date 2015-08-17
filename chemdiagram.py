import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch
from matplotlib.path import Path
import numpy as np

class ChemSankey(object):
    def __init__(self,):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1,xticks=[],yticks=[],
                                       ylim=(-1.,1.), xlim=(-1.,1.)
                                       )

    def _draw_node(self,loc,color='cyan',label='',size=0.1,
                  **kwargs):
        ell = Ellipse(loc, size, size*0.75,
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
        d1 = b1-a1
        d2 = b2-a2
        b = abs(bend)
        path_codes = [Path.MOVETO,
                      Path.CURVE3,
                      Path.CURVE3,
                      ]
        if bend < -0.1:
            Cont = [b1, a2]
        elif bend > 0.1:
            Cont = [a1, b2]
        else:
            Cont = [a1/2. + b1/2., a2/2. + b2/2.]
        if (abs(d1) < 0.01) and (bend > 0.1):
            Cont = [a1 + d2/2*b , a2 + d2/2*b]
        elif (abs(d1) < 0.01) and (bend < -0.1):
            Cont = [a1 - d2/2*b , a2 + d2/2*b]
        elif (abs(d2) < 0.01) and (bend > 0.1):
            Cont = [a1 + d1/2*b , a2 + d1/2*b]
        elif (abs(d2) < 0.01) and (bend < -0.1):
            Cont = [a1 + d1/2*b , a2 - d1/2*b]
        #    Cont = [a1/abs(bend) + b1/bend, a2/abs(bend) + b2/bend]
        P = Path([A,Cont,B],path_codes)
        PP = PathPatch(P, 
                       fill=False,
                       color=color,
                       linewidth=width,
                       **kwargs)
        self.ax.add_artist(PP)
        
    def _set_node_positions(self, positions=None):
        if positions == None:
            node_positions = {}
            for i,node in enumerate(self.node_labels):
                xy = [0.5,0.9-2*i/float(len(self.node_labels))]
                if i%2:
                    xy[0] *= -1
                node_positions[node] = xy
        else:
            assert type(positions) == dict, 'given node positions must be dict'
            for node in self.node_labels:
                assert node in positions.keys(), '%s not in position dict'%node
        self.node_positions = node_positions
        return

    def _make_connections(self, ):
        bends = [-.25, .25]
        conn_counter = {}
        for i,conn in enumerate(self.connections):
            FROM = self.connections[conn]['from']
            TO = self.connections[conn]['to']
            conn_name = '_'.join(sorted([FROM, TO]))
            if not (conn_name in conn_counter):
                conn_counter[conn_name] = 0
            self._make_connection(self.node_positions[FROM],
                                  self.node_positions[TO],
                                  bend=bends[conn_counter[conn_name]],
                                  width=self.line_widths[i],
                                  color=self.colors[self.connections \
                                                        [conn]['via']],
                                  )

            conn_counter[conn_name] += 1

    def _draw_node_label(self, loc, label):
        self.ax.text(loc[0],loc[1],label,
                     verticalalignment='center',
                     horizontalalignment='center')
        return

    def _draw_nodes(self, ):
        for i,node in enumerate(self.node_labels):
            self._draw_node(self.node_positions[node],
                            size=self.node_sizes[i])
            self._draw_node_label(self.node_positions[node],
                                  node,
                                  )
        return

    def _setup_colors(self, connections, colors):
        diff_conn = []
        for conn in connections:
            if not (connections[conn]['via'] in diff_conn):
                diff_conn.append(connections[conn]['via'])
        if colors == None:
            colors_dict = {}
            for dc in diff_conn:
                colors_dict[dc] = 'k'
        elif type(colors) == list:
            assert len(colors) == len(diff_conn), ('must give one color for',
                                                   'each',
                                                   'different connection type')
            colors_dict = {}
            for i,dc in enumerate(colors):
                colors_dict[dc]=colors[i]
        elif type(colors) == dict:
            for dc in diff_conn:
                assert dc in colors.keys(), 'connection %s not in colors'%dc
            colors_dict = colors
        else:
            raise IOError, 'unknown type for connection colors definition'
        self.colors = colors_dict
        return

    def setup_chem(self, species, reactions, fluxes, concs,
                   ):
        self.node_labels = species
        self.line_widths = fluxes
        self.node_sizes = 2*concs/max(concs)/len(concs)
        connections = {}
        for i,key in enumerate(reactions):
            connections[i] = {'from':reactions[key]['R'][0],
                              'to':reactions[key]['P'][0],
                              'via':reactions[key]['R'][1],
                              }
        self.connections = connections
        return

    def setup_art(self, colors=None, positions=None):
        self._setup_colors(self.connections,colors)
        self._set_node_positions(positions=positions)
        self._make_connections()
        self._draw_nodes()
        return


species = ['A','B','C','D','E']
conspecies = ['OH','NO']
reactions = {0:{'R':['A','OH'],'P':['B']},
             1:{'R':['B','NO'],'P':['C']},
             2:{'R':['C','OH'],'P':['D']},
             3:{'R':['C','NO'],'P':['D']},
             4:{'R':['C','NO'],'P':['E']},
             5:{'R':['A','NO'],'P':['C']},
             }
fluxes = np.array([8.,8.,5.,4.,1.,2.])
concs = np.array([2.,5.,3.,1.1,2.,1.5])

CS = ChemSankey()
CS.setup_chem(species,reactions,fluxes,concs)
CS.setup_art(colors={'OH':'r','NO':'b'})

#locs = {'A':np.array([0.,.7]),
#        'B':np.array([.7,0.]),
#        'C':np.array([.7,.7])
#        }

#CS._make_connection(locs['A'],locs['B'])
#CS._make_connection(locs['A'],locs['C'],width=4)
#CS._add_node(locs['A'])
#CS._add_node(locs['B'])
#CS._add_node(locs['C'])
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1,xticks=[],yticks=[],title='',
#                     ylim=(-2,2),xlim=(-2,2))

#draw_arrow(locs['A'],locs['B'])
#draw_arrow(locs['A'],locs['C'])

plt.show()

