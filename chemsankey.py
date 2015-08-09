from matplotlib.sankey import Sankey
import matplotlib.pyplot as plt

import numpy as np

# Example 1 -- Mostly defaults
# This demonstrates how to create a simple diagram by implicitly calling the
# Sankey.add() method and by appending finish() to the call to the class.
#Sankey(flows=[0.25, 0.15, 0.60, -0.20, -0.15, -0.05, -0.50, -0.10],
#       labels=['', '', '', 'First', 'Second', 'Third', 'Fourth', 'Fifth'],
#       orientations=[-1, 1, 0, 1, 1, 1, 0, -1]).finish()
#plt.title("The default settings produce a diagram like this.")
# Notice:
#   1. Axes weren't provided when Sankey() was instantiated, so they were
#      created automatically.
#   2. The scale argument wasn't necessary since the data was already
#      normalized.
#   3. By default, the lengths of the paths are justified.

# Example 2
# This demonstrates:
#   1. Setting one path longer than the others
#   2. Placing a label in the middle of the diagram
#   3. Using the the scale argument to normalize the flows
#   4. Implicitly passing keyword arguments to PathPatch()
#   5. Changing the angle of the arrow heads
#   6. Changing the offset between the tips of the paths and their labels
#   7. Formatting the numbers in the path labels and the associated unit
#   8. Changing the appearance of the patch and the labels after the figure is
#      created
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
                     title="Flow Diagram of a Widget")


sankey = Sankey(ax=ax, scale=1./25., offset=0.05, head_angle=150,
                format='%.0f', unit='%')
sankey.add(flows=[25, -20, -5],
           labels = ['one', 'two', 'three'],
           orientations=[0,-1,1],
           pathlengths = [0.25, 0.25, 0.25],
           patchlabel="Widget\nA",
           rotation=-90,
           alpha=0.2, lw=2.0) # Arguments to matplotlib.patches.PathPatch()
sankey.add(flows=[20, -10, -10],
           labels = ['', 'four', 'five'],
           orientations=[0,1,1],
           pathlengths = [0.25, 0.25, 0.25],
           patchlabel="Widget\nA",
           rotation=-90,
           prior=0, connect=(1,0),
           alpha=0.2, lw=2.0) # Arguments to matplotlib.patches.PathPatch()
sankey.add(flows=[5, -2.5, -2.5],
           labels = ['', 'six', 'seven'],
           orientations=[0,-1,-1],
           pathlengths = [0.25, 0.25, 0.25],
           patchlabel="Widget\nA",
           rotation=-90,
           prior=0, connect=(2,0),
           alpha=0.2, lw=2.0) # Arguments to matplotlib.patches.PathPatch()
sankey.add(flows=[10, -5, -5],
           labels = ['', '', ''],
           orientations=[0,1,0],
           pathlengths = [0.25, 0.25, 0.25],
           patchlabel="Widget\nA",
           rotation=-90,
           prior=1, connect=(1,0),
           alpha=0.2, lw=2.0) # Arguments to matplotlib.patches.PathPatch()
sankey.add(flows=[10, -7, -3],
           labels = ['', '', ''],
           orientations=[0,-1,0],
           pathlengths = [0.25, 0.25, 0.25],
           patchlabel="Widget\nA",
           rotation=-90,
           prior=1, connect=(2,0),
           alpha=0.2, lw=2.0) # Arguments to matplotlib.patches.PathPatch()

diagrams = sankey.finish()
diagrams[0].patch.set_facecolor('#37c959')
diagrams[0].texts[-1].set_color('r')
diagrams[0].text.set_fontweight('bold')


num_nodes = 7
nodes = ['node'+str(i) for i in range(num_nodes)]
node_sizes = [float(i) for i in range(len(nodes))]

#flows: [into system, out of system, node0, node1, etc., nodeN] 

num_vertices = 20
vertices = {0:{'from':None,'to':[1,2],'values':    [1,0,0,-1,-1,0,0,0,0]},
            1:{'from':0,'to':[3,4,5], 'values':[0,0,1,0,0,-1,-1,-1,0]},
            2:{'from':0,'to':[6],'values'  :   [0,0,1,0,0,0,0,0,-1]},
            3:{'from':1,'to':[],'values':      [0,-1,0,1,0,0,0,0,0]},
            4:{'from':1,'to':[],'values':      [0,-1,0,1,0,0,0,0,0]},
            5:{'from':1,'to':[],'values':      [0,-1,0,1,0,0,0,0,0]},
            6:{'from':2,'to':[],'values':      [0,-1,0,0,1,0,0,0,0]},
            }


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
                     title="Flow Diagram of a Widget")

sankey = Sankey(ax=ax, scale=1./4., offset=0.001, head_angle=150,
                format='%.0f', unit='',tolerance=1e6)

sankey.add(flows=vertices[0]['values'],
               pathlengths=[0.005]*len(vertices[0]['values']),
               patchlabel=nodes[0],
               rotation=-90,
               orientations=[0,0,0,0,0,0,0,0,0],
               )

for i,node in enumerate(nodes):
    if i > 0:
        print i, node
        sankey.add(flows=vertices[i]['values'],
                   pathlengths=[0.005]*len(vertices[i]['values']),
                   labels=None,
                   patchlabel=node,
                   rotation=-90,
                   orientations=[0,0,0,0,0,0,0,0,0],
                   prior=vertices[i]['from'],
                   connect=(i+2,vertices[i]['from']+2)
                   )

sankey.finish()
# Notice:
#   1. Since the sum of the flows is nonzero, the width of the trunk isn't
#      uniform.  If verbose.level is helpful (in matplotlibrc), a message is
#      given in the terminal window.
#   2. The second flow doesn't appear because its value is zero.  Again, if
#      verbose.level is helpful, a message is given in the terminal window.


plt.show()
