import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch, Patch
from matplotlib.path import Path
import numpy as np

def quadratic_bezier(p0,p1,p2,t):
    x0,y0 = p0
    x1,y1 = p1
    x2,y2 = p2
    b = [(1-t)*((1-t)*x0+t*x1)+t*((1-t)*x1+t*x2),
         (1-t)*((1-t)*y0+t*y1)+t*((1-t)*y1+t*y2)]
    return b
     

def split_bezier(p0,p1,p2,n):
    ts = np.linspace(0,1,n)
    return [quadratic_bezier(p0,p1,p2,t) for t in ts]

def get_head_width(width):
    if width < 0.1:
        return 0
    else:
        scale = width*(0.03/5.)
        return max(0.02,min(scale,0.05))

class ChemSankey(object):
    def __init__(self,):
        self.fig = plt.figure(figsize=(18,15))
        self.ax = self.fig.add_subplot(1,1,1,xticks=[],yticks=[],
                                       ylim=(-1.,1.), xlim=(-1.,1.)
                                       )

    def _draw_node(self,loc,color='cyan',label='',size=0.1,
                  **kwargs):
        ell = Ellipse(loc, size, size*0.75,
                      facecolor=color,
                      alpha=1.0,
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
        print width
        self.ax.add_artist(PP)
        segments = split_bezier(np.array(A),np.array(Cont),np.array(B),20)
        x1,y1 = segments[10]
        x2,y2 = segments[11]
        arrow_width = get_head_width(width)
        if arrow_width:
            self.ax.arrow(x1,y1,x2-x1,y2-y1, 
                          head_width=arrow_width,
                          length_includes_head=True,
                          facecolor=color,
                          edgecolor=color,
                          #linewidth=width,
                          )

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
            node_positions = positions
        self.node_positions = node_positions
        return

    def _make_connections(self, ):
        bends = [-.25, .25, 0.]
        conn_counter = {}
        for i,conn in enumerate(self.connections):
            FROM = self.connections[conn]['from']
            TO = self.connections[conn]['to']
            if (FROM in self.omit) or (TO in self.omit):
                pass
            else:
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
            if (node in self.omit):
                pass
            else:
                if self.node_colors:
                    self._draw_node(self.node_positions[node],
                                    size=self.node_sizes[i], 
                                    color=self.node_colors[node])
                else:
                    self._draw_node(self.node_positions[node],
                                    size=self.node_sizes[i])
#                self._draw_node_label(self.node_positions[node],
#                                      node,
#                                      )
        return

    def _setup_colors(self, connections, colors, node_colors=None):
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

        if node_colors:
            assert type(node_colors) == dict, 'node colors must be in dict form'
            self.node_colors = node_colors

        return

    def setup_chem(self, species, reactions, fluxes, concs,
                   omit=[]):
        self.omit=omit
        self.node_labels = species
        self.line_widths = fluxes
        self.node_sizes = 2*concs/max(concs)/len(concs)
        connections = {}
        for i,key in enumerate(reactions):
            connections[i] = {'from':reactions[key]['R'][0],
                              'to':reactions[key]['P'][0],
                              }
            if len(reactions[key]['R']) == 2:
                connections[i]['via'] = reactions[key]['R'][1]
            else:
                connections[i]['via'] = 'None'

        self.connections = connections
        return

    def _make_legend(self,colors):
        for i,key in enumerate(colors):
            self.ax.plot([1.1],[1.1],lw=3,label=key,color=colors[key])
        self.ax.legend(loc='right',prop={'size':40})

    def setup_art(self, colors=None, positions=None, node_colors=None,
                  custom_legend=None):
        self._setup_colors(self.connections,colors,node_colors=node_colors)
        self._set_node_positions(positions=positions)
        self._make_connections()
        self._draw_nodes()

        if custom_legend:
            self._make_legend(custom_legend)
        elif colors is not None:
            self._make_legend(colors)
        return

if __name__=='__main__':
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

