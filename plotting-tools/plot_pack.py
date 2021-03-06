import math as ma
import numpy as np
import scipy as sc
import scipy.special as ss
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
sq2 = ma.sqrt(2.0)


""" ---------------------- Custom Color Dictionaries ------------------------ """

# Custom grey scale
cdict1 = {'red':  ((0.0, 1.0, 1.0),
                   (0.25, 0.75, 0.75),
                   (0.5, 0.5, 0.5),
                   (0.75, 0.25, 0.25),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 1.0, 1.0),
                   (0.25, 0.75, 0.75),
                   (0.5, 0.5, 0.5),
                   (0.75, 0.25, 0.25),
                   (1.0, 0.0, 0.0)),
         'blue':  ((0.0, 1.0, 1.0),
                   (0.25, 0.75, 0.75),
                   (0.5, 0.5, 0.5),
                   (0.75, 0.25, 0.25),
                   (1.0, 0.0, 0.0))        }
white_black = LinearSegmentedColormap('grey', cdict1)
# Custom central-void (white) color map
cdict2 = {'red':  ((0.0, 0.0, 0.0),
                   (0.125, 1.0, 1.0),
                   (0.25, 0.0, 0.0),
                   (0.4, 0.5, 0.5),
                   (0.5, 1.0, 1.0),
                   (0.6, 0.0, 0.0),
                   (0.7, 1.0, 1.0),
                   (0.875, 0.75, 0.75),
                   (1.0, 0.5, 0.5)),
         'green': ((0.0, 0.0, 0.0),
                   (0.125, 0.0, 0.0),
                   (0.25, 0.0, 0.0),
                   (0.4, 0.5, 0.5),
                   (0.5, 1.0, 1.0),
                   (0.6, 1.0, 1.0),
                   (0.7, 1.0, 1.0),
                   (0.875, 0.0, 0.0),
                   (1.0, 0.2, 0.2)),
         'blue':  ((0.0, 0.0, 0.0),
                   (0.125, 1.0, 1.0),
                   (0.25, 1.0, 1.0),
                   (0.4, 1.0, 1.0),
                   (0.5, 1.0, 1.0),
                   (0.6, 0.0, 0.0),
                   (0.7, 0.0, 0.0),
                   (0.825, 0.0, 0.0),
                   (1.0, 0.2, 0.2))        }
spec_center = LinearSegmentedColormap('spec_c', cdict2)

# IN PROGRESS
cdict3 = {'red':  ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),
         'green': ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (1.0, 0.0, 0.0)),
         'blue':  ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (1.0, 0.0, 0.0))        }
#spec_center = LinearSegmentedColormap('spec_c', cdict3)
#Custom heatmap
spectral_colors = np.loadtxt('../utilities/spectral_cm.txt')
spectral_wb = ListedColormap(spectral_colors[:,:3], name="spectral_wb", N=256)
#Custom heatmap
#spectral_colors = np.loadtxt('../utilities/spectral_center.txt')
#spectral_c = ListedColormap(spectral_colors[:,:3], name="spectral_c", N=256)

""" ---------------------- 2D Hist Methods ---------------------------------- """
""" 2-dimensional histogram, creates histogram ready for imshow, and factors for
    converting between matrix elements and real-world values.
     - Read & Bin Data
     - Print data to file
     - Read data from file
     - plot data
     -- raw bins
     -- Smoothed bins
     -- Error Blurred bins
    """

class HistMaker:
    def __init__(self, xdata, ydata, xsize=None, ysize=None, xarea=None, yarea=None):
        self.xbins, self.xmin, self.xmax, self.xsize = GetArea(xdata, xsize, xarea)
        self.ybins, self.ymin, self.ymax, self.ysize = GetArea(ydata, ysize, yarea)
        self.H = BlockHist(xdata, ydata, self)
        self.cmap = 'color'      # Sets colormap
        self.varea = (0.0,None)  # Sets contrast range for pixels
        self.scale = None        # Special scaling, such as 'sqrt' or 'log'
        self.labels = [None, None]  # Labels for x,y axes
        self.ticks = [None, None]  # Tick Locations for x,y axes
        self.ticklabels = [None, None]  # Tick Labels for x,y axes  NOT IMPLEMENTED
        self.xflip, self.yflip = 0, 0   # Set=1 to flip respective axis
    def savehist(self, outfile, fmt='%.2f'):
        np.savetxt(outfile, self.H, delimiter=",", fmt=fmt) #, header=" pyplot image output, in y,x. "+\
        #  "x is {0} from {1} to {2}, in steps of {3}; "+\
        #  "y is {4} from {5} to {6}, in steps of {7}".format(self.labels[0], self.xmin,
        #    self.xmax, self.xsize, self.labels[1], self.ymin, self.ymax, self.ysize)  )
    def xyToBins(self, x=None, y=None):
        """ Take x,y, coordinates and convert them to bin coordinates"""
        if x != None:  xx = (x - self.xarea[0]) / self.xsize
        else:  xx = None
        if y != None:  yy = (y - self.yarea[0]) / self.ysize
        else:  yy = None
        return xx, yy
    def gblur(self, blur=1):
        self.H = GaussBlurHist(self.H, blur)
    def plot(self):
        PlotHist(self)

# Make image
# Imagefile, outfile for hist, infile

def HistFromFile(infile, xsize=None, ysize=None, xarea=None, yarea=None):
    if infile[-4:] == ".csv":  data = np.loadtxt(infile, delimiter=",")
    else:   data = np.loadtxt(infile)
    hist = HistMaker([1,2], [1,2], xsize, ysize, xarea, yarea)
    hist.H = data
    return hist


def MakeHist(infile=None):
    """ Master def, makes a hist from data accroding to inputs, calling other defs here"""
    if infile != None:  np.loadtxt(infile, ",")
    return -1


def GetArea(xdata, xsize=None, xarea=None):
    """ xdata and ydata are ordered and 1-d, such that xdata[i] corresponds to ydata[i].
        xsize, ysize are bin sizes in each dimension
        xarea, yarea should be (min, max) or None (will give min, max of data)
        If outfile is not None, then will dump the histogram to a file with that name
        labels are ['xlabel', 'ylabel']"""
    # Initialize area and array
    if xarea == None:  xmax, xmin = np.ma.max(xdata), np.ma.min(xdata)
    else:  xmin, xmax = xarea[0], xarea[1]
    if xsize == None:  xsize = (xmax-xmin) / 10.0
    xbins = int( (xmax - xmin) / xsize) + 1  # WARNING:  +1 bin may cause issues with edges if blurring
    return xbins, xmin, xmax, xsize


def BlockHist(xdata, ydata, field):
    """ xdata and ydata are ordered and 1-d, such that xdata[i] corresponds to ydata[i].
        field is a HistMaker object"""
    # Initialize area and array
    H = sc.zeros((field.ybins, field.xbins), float)
    # Fill array
    for i in range(len(xdata)):
        xi = int( (xdata[i]-field.xmin) / field.xsize )
        yi = int( (ydata[i]-field.ymin) / field.ysize )
        if xi < 0 or xi > field.xbins-1:  continue
        if yi < 0 or yi > field.ybins-1:  continue
        H[yi,xi] = H[yi,xi] + 1.0
    return H


def GaussBlurHist(H, xblur=1, yblur='same', edge=0.0):
    """ H is a y,x 2D histogram.
        xblur is the number of pixels to use when blurring in x-direction
        yblur is blur in y-direction,
        xarea, yarea should be (min, max) or None (will give min, max of data)
        If outfile is not None, then will dump the histogram to a file with that name
        labels are ['xlabel', 'ylabel']"""
    # Initialize
    if yblur == 'same':  yblur = xblur
    ybins, xbins = H.shape
    # blur in horizontal direction
    H2 = sc.zeros(H.shape, float)
    if xblur != None:
        xs = 6*xblur + 1  # size of blur array - 3 sigma each side + 1 for center
        xc = 3*xblur
        xgauss = sc.zeros(xs, float)
        for i in range(3*xblur):
            xgauss[i] = xgauss[-i] = gaussian(float(i), float(xc), float(xblur))
        xgauss[xc] = gaussian(float(xc), float(xc), float(xblur))
        xgauss = xgauss / sc.sum(xgauss)  # normalize
        #print xgauss
        # Apply blur in x
        for i in range(ybins):
            for j in range(xbins):
                for k in range(xs):
                    newj = j - xc + k  # select pixel for convolution
                    if newj < 0 or newj > xbins - 1:  H2[i,j] = H2[i,j] + xgauss[k]*edge  # Compensate for edges
                    else:  H2[i,j] = H2[i,j] + xgauss[k]*H[i,newj]  # Weighted average of local pixel
    else:  H2 = H
    # blur in vertical direction
    H3 = sc.zeros(H.shape, float)
    if yblur != None:
        ys = 6*yblur + 1  # size of blur array - 3 sigma each side + 1 for center
        yc = 3*yblur
        ygauss = sc.zeros(ys, float)
        for i in range(3*yblur):
            ygauss[i] = ygauss[-i] = gaussian(float(i), float(yc), float(yblur))
        ygauss[yc] = gaussian(float(yc), float(yc), float(yblur))
        ygauss = ygauss / sc.sum(ygauss)  # normalize
        #print ygauss
        # Apply blur in y
        for i in range(ybins):
            for j in range(xbins):
                for k in range(xs):
                    newi = i - xc + k  # select pixel for convolution
                    if newi < 0 or newi > ybins - 1:  H3[i,j] = H3[i,j] + ygauss[k]*edge  # Compensate for edges
                    else:  H3[i,j] = H3[i,j] + ygauss[k]*H2[newi,j]  # Weighted average of local pixel
    else:  H3 = H2
    return H3


def ErrBlurLinear(field, xfunc=None, yfunc=None, edge=0.0):
    # Blur each point into a Gaussian Distribuion, using functions for err(x) and err(y)
    return -1


def ErrBlurPoint(xdata, ydata, field, con=30, xerror=None, yerror=None):
    """ xdata...
        """
    # Initialize area and array
    H = sc.zeros((field.ybins, field.xbins), float)
    weight = 1.0 / float( (con+1)*(con+1) )
    # Fill array
    for i in range(len(xdata)):
        # convolve data
        deltax = convolve(xerror[i], con)
        deltay = convolve(yerror[i], con)
        # Bin convolved data
        for k in range(len(deltax)):
            for l in range(len(deltay)):
                newx = xdata[i] + deltax[k]
                xi = int( (newx-field.xmin) / field.xsize )
                newy = ydata[i] + deltay[l]
                yi = int( (newy-field.ymin) / field.ysize )
                if xi < 0 or xi > field.xbins-1:  continue
                if yi < 0 or yi > field.ybins-1:  continue
                H[yi,xi] = H[yi,xi] + weight
    return H


def gaussian(x, mu, sigma):
    bottom = np.sqrt(2.0*ma.pi*sigma*sigma)
    top = -1.0*( ( (mu - x)*(mu - x) ) / (2.0*sigma*sigma) )
    return np.exp(top) / bottom


def convolve(sig, con):
    """ convolves a point into a line of points, such that the histogram of the
        new points forms a Gaussian """
    p = 0.9973 / float(con)
    points = [0.0]
    for i in range(con/2):  points.append(getb(sig, points[i], p) )
    x = -1.0*sc.array(points[1:])
    return sc.append(sc.array(points), x)


def getb(sig, a, p):
    part1 = ss.erf( a / (sq2*sig) )
    part2 = 2.0*p + part1
    part3 = sq2*sig*ss.erfinv(part2)
    return part3


def PlotHist(field, imfile=None, cbarO='vertical', cax=None):
    """ field is a HistMaker object """
    H = field.H
    # Scale and flip if necessary
    vmin = field.varea[0]
    if field.varea[1] == None:  vmax = np.ma.max(H)
    else:  vmax = field.varea[1]
    if    field.scale == 'sqrt':  field.H = sc.sqrt(H); vmax = sc.sqrt(vmax)
    elif  field.scale == 'log':   field.H = sc.log10(H); vmax = sc.log10(vmax)
    if field.xflip == 1:  H = H[:,::-1]
    if field.yflip == 1:  H = H[::-1,:]
    # Plot the image
    if field.cmap == 'color':  cmap = spectral_wb
    elif field.cmap == 'color_c':  cmap = spec_center
    elif field.cmap == 'bw':  cmap = 'gist_yarg'
    else:  cmap = field.cmap
    fig = plt.figure(dpi=120)
    ax1 = fig.add_subplot(111)
    im = ax1.imshow(H, cmap=cmap, norm=None, aspect=3, interpolation='nearest',
               alpha=None, vmin=vmin, vmax=vmax, origin='lower', extent=None)
    # Add xTicks and labels
    xlocs, xlabels, ylocs, ylabels = [], [], [], []
    if field.ticks[0] == None:
        xpos = np.arange(field.xmin, field.xmax+0.000001, ((field.xmax-field.xmin)/10.0) )
    else:
        xpos = field.ticks[0]
    for pos in xpos:
        xlocs.append((pos-field.xmin)/field.xsize)
        xlabels.append("${0:.1f}$".format(pos))
    if field.xflip == 1:  plt.xticks((field.xbins-np.array(xlocs))[::-1], xlabels[::-1], rotation=45, fontsize=12)
    else:                 plt.xticks(xlocs, xlabels, rotation=45, fontsize=12)
    # Add yTicks and labels
    if field.ticks[1] == None:
        ypos = np.arange(field.ymin, field.ymax+0.000001, ((field.ymax-field.ymin)/10.0) )
    else:
        ypos = field.ticks[1]
    for pos in ypos:
        ylocs.append((pos-field.ymin)/field.ysize)
        ylabels.append("${0:.1f}$".format(pos))
    if field.yflip == 1:  plt.yticks((field.ybins-np.array(ylocs))[::-1], ylabels[::-1], rotation=0, fontsize=12)
    else:                 plt.yticks(ylocs, ylabels, rotation=0, fontsize=12)
    # Add axes labels
    if field.labels[0] != None:  plt.xlabel(field.labels[0], fontsize=16)
    if field.labels[1] != None:  plt.ylabel(field.labels[1], rotation=0, fontsize=16)
    if cax == None:  cbar = plt.colorbar(mappable=im, aspect=30, orientation=cbarO) #May need to adjust these ticks...
    else:  cbax = fig.add_axes(cax); cb = plt.colorbar(mappable=im, ax=ax1, cax=cbax, orientation=cbarO)
    # Save file, if outfile declared
    if imfile != None:  plt.savefig(imfile)
    else: plt.show()
    plt.close('all')
