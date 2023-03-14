# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
%matplotlib
import matplotlib.patches as patches
import matplotlib.lines as lines
import geopandas as gpd

def addRectangle(from_ax,to_ax,color='black'):
    """
    Create a rectangle in one axes, representing the boundaries of another axes

    Parameters
    ----------
    from_ax : axes subplot
        The axes of which the boundaries have to be represented.
    to_ax : axes subplot
        The axes in which the boundaries must be drawn as rectangle.
    color : string, optional
        Any valid matplotlib color. This will be the color of the rectangle. The default is 'black'.

    Returns
    -------
    rect : matplotlib patch
        The rectangle that is drawn.

    """
    xmin,xmax = from_ax.get_xlim()
    ymin,ymax = from_ax.get_ylim()
    rect = patches.Rectangle((xmin, ymin),xmax-xmin, ymax-ymin, linewidth=1, linestyle='--', edgecolor=color, facecolor='none')
    to_ax.add_patch(rect)
    return rect

def addLines(figure,from_ax,to_ax,from_side='left',to_side='right',color='black'):
    """
    Create lines from corners of one axes to the rectangle representing that axes in another axes.

    Parameters
    ----------
    figure : matplotlib Figure instance
        The figure in which the axes are
    from_ax : axes subplot
        The ax from which the line goes
    to_ax : axes subplot
        The ax in which from_ax is shown as a rectangle
    from_side : string
        One of 'left', 'right', 'bottom', 'top'. The default is 'left'. The side of which the corners are taken as start points for the lines.
    to_side :  string
        One of 'left', 'right', 'bottom', 'top'. The default is 'right'. The side of the rectangle of which the corners are taken as end points for the lines.

    Returns
    -------
    (l1,l2) : tuple with the two Line2D lines

    """
    ax1 = to_ax
    ax2 = from_ax
    pix_to_fig = figure.transFigure.inverted().transform
    a1_to_pix = ax1.transData.transform
    a2_to_pix = ax2.transData.transform
    
    # Get the start- and endpositions (x1/y1,x2/y2 for lines 1 and 2 (l1, l2)
    if from_side == 'left':
        l1_x2 = l2_x2 = ax2.get_xlim()[0]
        l1_y2,l2_y2 = ax2.get_ylim()
    elif from_side == 'right':
        l1_x2 = l2_x2 = ax2.get_xlim()[1]
        l1_y2,l2_y2 = ax2.get_ylim()
    elif from_side == 'top':
        l1_x2,l2_x2 = ax2.get_xlim() 
        l1_y2 = l2_y2 = ax2.get_ylim()[1]  
    elif from_side == 'bottom':    
        l1_x2,l2_x2 = ax2.get_xlim()    
        l1_y2 = l2_y2 = ax2.get_ylim()[0]       
    
    if to_side == 'left':
        l1_x1 = l2_x1 = ax2.get_xlim()[0]
        l1_y1,l2_y1 = ax2.get_ylim()
    elif to_side == 'right':
        l1_x1 = l2_x1 = ax2.get_xlim()[1]
        l1_y1,l2_y1 = ax2.get_ylim()
    elif to_side == 'top':
        l1_x1,l2_x1 = ax2.get_xlim()  
        l1_y1 = l2_y1 = ax2.get_ylim()[1]  
    elif to_side == 'bottom':    
        l1_x1,l2_x1 = ax2.get_xlim()   
        l1_y1 = l2_y1 = ax2.get_ylim()[0]   
    
    # Turn them into pixels, and then to figure coordinates
    l1_xy1_fig = pix_to_fig(a1_to_pix([l1_x1,l1_y1]))
    l2_xy1_fig = pix_to_fig(a1_to_pix([l2_x1,l2_y1]))
    l1_xy2_fig = pix_to_fig(a2_to_pix([l1_x2,l1_y2]))
    l2_xy2_fig = pix_to_fig(a2_to_pix([l2_x2,l2_y2]))

    # Create the two lines
    l1 = fig.add_artist(lines.Line2D([l1_xy1_fig[0],l1_xy2_fig[0]],[l1_xy1_fig[1],l1_xy2_fig[1]],linewidth=1, linestyle='--', color=color))
    l2 = fig.add_artist(lines.Line2D([l2_xy1_fig[0],l2_xy2_fig[0]],[l2_xy1_fig[1],l2_xy2_fig[1]],linewidth=1, linestyle='--', color=color))
    
    return l1,l2
    
# Importing the shape files, and selecting a region and a zone to plot
ET = gpd.read_file('data/ETadm0.zip')
regions = gpd.read_file('data/ETadm1.zip')
zones = gpd.read_file('data/ETadm2.zip')
SNNPR = zones[zones.admin1Name=='SNNP']
Gamo = zones[zones.admin2Name=='Gamo']

fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2)
ax3.set_visible(False) # I turn ax3 off for now, as it will not be used
regions.plot(ax=ax1,facecolor='none',edgecolor='k')
SNNPR.plot(ax=ax2,facecolor='none',edgecolor='k')
Gamo.plot(ax=ax4,facecolor='none',edgecolor='k')

# Adding rectangles
## Adding rectangles can be done with the above defined function addRectangle()
r1 = addRectangle(ax2,ax1,color='red')
r2 = addRectangle(ax4,ax2,color='purple')
r3 = addRectangle(ax4,ax1,color='purple')

# Adding lines -- only add lines after all else! The line position will shift when sizes of axes and figure changes.
## Adding lines can be done with the above defined function addLines()
l1,l2 = addLines(fig,ax2,ax1,from_side='left',to_side='right',color='r')
l3,l4 = addLines(fig,ax4,ax2,from_side='top',to_side='bottom',color='purple')
l5,l6 = addLines(fig,ax4,ax1,from_side='left',to_side='bottom',color='purple')
