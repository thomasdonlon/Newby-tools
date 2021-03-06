import sys
sys.path.insert(0, '../plotting-tools')
sys.path.insert(0, '../utilities')
sys.path.insert(0, '../fitting-tools')
import math as ma
import numpy as np
import scipy as sc
import matplotlib
import matplotlib.pyplot as plt
import plot_pack as pp
import progress as pr
import astro_coordinates as ac

def do_stuff():
    #Mgiant_hist()
    BLUE_hist()
    #book_plot()
    #test_coords()
    #mag_plots()
    #g_plots()
    #study_giants()
    #field_of_streams()

def Mgiant_hist():
    data = np.loadtxt("/home/newbym/Desktop/Mgiant_wise_sgr.csv", delimiter=",", skiprows=1)
    print data.shape
    #data[:,9] = -1.0*data[:,9]
    hist = pp.HistMaker(data[:,8], data[:,9], 1.0, 1.0, yarea=(-90.0, 90.0)) #, xarea=(20.0, 320.0) )
    #lam, bet = ac.lb2sgr(data[:,2], data[:,3], 100.0 )[3:5]   # use the proxy distance that is same as MSTOs
    #hist = pp.HistMaker(lam, bet, 1.0, 1.0, yarea=(-90, 90))
    hist.savehist(outfile="Mgiant_test3.csv", fmt='%.1f')
    hist.yflip=1
    hist.xflip=1
    hist.labels=(r"$\Lambda$",r"$B$")
    #hist.ticks = (None, [-40.0, -20.0, 0.0, 20.0, 40.0, 60.0, 80.0])
    hist.varea=(0.0, 200.0)
    pp.PlotHist(hist, imfile="Mgiant_sgr.png", cbarO='horizontal')

def BLUE_hist():
    BHB = np.loadtxt("/home/mnewby/Desktop/BLUE_all_hist.csv", delimiter=",")
    BHB = BHB[:,::-1]
    fig = plt.figure(1, figsize=(12,9), dpi=120)
    ########################################### BHBs
    sp = fig.add_subplot(111)
    #BHB = BHB[:,::-1]
    #BHB = BHB[::-1,:]
    im = sp.imshow(BHB, cmap=pp.spectral_wb, vmax=30.0)
    #plt.plot([5.0, 295.0], [60.0, 60.0], 'k--')
    #plt.plot([5.0, 295.0], [70.0, 70.0], 'k--')
    #plt.plot([5.0, 295.0], [80.0, 80.0], 'k--')
    xlocs = np.arange(0.0, 301.0, 20.0)
    xlabs = []
    for i in range(len(xlocs)):  xlabs.append("${0:.0f}$".format(xlocs[-1*(i+1)]+20))
    plt.xticks(xlocs, xlabs, fontsize=12)
    ylocs = np.arange(10.0, 121.0, 10.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format(ylocs[i]-70))
        else:  ylabs.append("")
    plt.yticks(ylocs, ylabs, fontsize=12 )
    plt.xlabel(r"$\Lambda$", fontsize=14)
    plt.ylabel(r"$B$", rotation=0, fontsize=14)
    #plt.text(135, 41, "SDSS BHB Selection", fontsize=10, family="serif",
    #    backgroundcolor="w", color="k")
    plt.xlim(0.0,300.0)
    plt.ylim(100.0, 10.0)
    plt.savefig("BLUE_stars_SDSS.png")
    plt.savefig("BLUE_stars_SDSS.ps")

def book_plot():
    #BHB = np.loadtxt("/home/newbym/Desktop/bhbs_all_hist.csv", delimiter=",")
    #MSTO = np.loadtxt("/home/newbym/Desktop/FTO_All_hist.csv", delimiter=",")
    BHB = np.loadtxt("/home/newbym/Desktop/BLUE_all_hist.csv", delimiter=",")
    MSTO = np.loadtxt("/home/newbym/Desktop/MSTO_all_hist.csv", delimiter=",")
    #RGB = np.loadtxt("/home/newbym/Desktop/Mgiant_test1.csv", delimiter=",")
    RGB = np.loadtxt("Mgiant_test3.csv", delimiter=",")
    r_steps, rx_min, rx_max, ry_min, ry_max = 1.0, 0.0, 360.0, -90.0, 90.0
    f_steps, fx_min, fx_max, fy_min, fy_max = 0.5, 20.0, 320.0, -70.0, 40.0
    b_steps, bx_min, bx_max, by_min, by_max = 1.0, 20.0, 320.0, -70.0, 40.0
    fig = plt.figure(1, figsize=(12,9), dpi=120)
    plt.subplots_adjust(hspace=0.001, wspace=0.001)
    ########################################### BHBs
    sp3 = fig.add_subplot(313)
    BHB = BHB[:,::-1]
    #BHB = BHB[::-1,:]
    #im3 = sp3.imshow(BHB, cmap='bone', vmax=35.0)
    #im3 = sp3.imshow(BHB, cmap='gist_yarg', vmax=30.0)
    im3 = sp3.imshow(BHB, cmap=pp.spectral_wb, vmax=25.0)
    plt.plot([5.0, 295.0], [60.0, 60.0], 'k--')
    plt.plot([5.0, 295.0], [70.0, 70.0], 'k--')
    plt.plot([5.0, 295.0], [80.0, 80.0], 'k--')
    xlocs = np.arange(0.0, 301.0, 20.0)
    xlabs = []
    for i in range(len(xlocs)):  xlabs.append("${0:.0f}$".format(xlocs[-1*(i+1)]+20))
    plt.xticks(xlocs, xlabs, fontsize=12)
    ylocs = np.arange(10.0, 120.0, 10.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format(ylocs[i]-70))
        else:  ylabs.append("")
    plt.yticks(ylocs, ylabs, fontsize=12 )
    plt.xlabel(r"$\Lambda$", fontsize=14)
    plt.ylabel(r"$B$", rotation=0, fontsize=14)
    plt.text(135, 41, "SDSS BHB Selection", fontsize=10, family="serif",
        backgroundcolor="w", color="k")
    plt.xlim(0.0,300.0)
    plt.ylim(110.0, 30.0)
    ########################################### RGBs
    sp1 = plt.subplot(311) #, sharex=sp3)
    RGB = RGB[:,::-1]
    RGB = RGB[::-1,:]
    #sp1.imshow(RGB[20:131,20:320], cmap='hot', vmax=5.0)
    #sp1.imshow(RGB[20:131,20:320], cmap='gist_yarg', vmax=5.0)
    sp1.imshow(RGB[20:131,20:320], cmap=pp.spectral_wb, vmax=5.0)
    plt.plot([5.0, 295.0], [60.0, 60.0], 'k--')
    plt.plot([5.0, 295.0], [70.0, 70.0], 'k--')
    plt.plot([5.0, 295.0], [80.0, 80.0], 'k--')
    plt.xticks(np.arange(20.0, 320.0, 20.0))
    plt.setp(sp1.get_xticklabels(), visible=False)
    ylocs = np.arange(10.0, 120.0, 10.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format(ylocs[i]-70))
        else:  ylabs.append("")
    plt.yticks(ylocs[:-1], ylabs[:-1], fontsize=12 )
    plt.ylabel(r"$B$", rotation=0, fontsize=14)
    plt.text(135, 41, "WISE RGB Selection", fontsize=10, family="serif",
        backgroundcolor="w", color="k")
    plt.xlim(0.0,300.0)
    plt.ylim(110.0, 30.0)
    ########################################### MSTOs
    sp2 = plt.subplot(312) #, sharex=sp3)
    MSTO = MSTO[:,::-1]
    #MSTO = MSTO[::-1,:]
    #sp2.imshow(MSTO, cmap='afmhot', vmax=120.0)
    #sp2.imshow(MSTO, cmap='gist_yarg', vmax=80.0)
    sp2.imshow(MSTO, cmap=pp.spectral_wb, vmax=120.0)
    plt.plot([10.0, 590.0], [120.0, 120.0], 'k--')
    plt.plot([10.0, 590.0], [140.0, 140.0], 'k--')
    plt.plot([10.0, 590.0], [160.0, 160.0], 'k--')
    plt.xticks(np.arange(40.0, 620.0, 40.0))
    plt.setp(sp2.get_xticklabels(), visible=False)
    ylocs = np.arange(20.0, 240.0, 20.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format((ylocs[i]/2.0)-70))
        else:  ylabs.append("")
    plt.yticks(ylocs[:-1], ylabs[:-1], fontsize=12 )
    plt.ylabel(r"$B$", rotation=0, fontsize=14)
    plt.text(266, 82, "SDSS MSTO Selection", fontsize=10, family="serif",
        backgroundcolor="w", color="k")
    plt.xlim(0.0,600.0)
    plt.ylim(220.0, 60.0)
    # plot
    #plt.savefig("figure_color.ps")
    plt.savefig("figure_color_test3.png")

def test_coords():
    # test Li Jing's coord transforms
    #ra,dec,l,b,j0,k0,w10,w20,lambda,beta
    arcsec = 1.0 / 3600.0
    data = np.loadtxt("/home/newbym/Desktop/Mgiant_wise_sgr.csv", delimiter=",", skiprows=1)
    ra, dec = data[:,0], data[:,1]
    l, b = data[:,2], data[:,3]
    lam, bet = data[:,8], data[:,9]
    badl, badb, badlam, badbet, badlam2, badbet2 = [], [], [], [], [], []
    for i in range(data.shape[0]):
        new_l, new_b = ac.EqTolb(ra[i], dec[i])
        if np.abs(new_l - l[i]) > arcsec:  badl.append(new_l - l[i])
        if np.abs(new_b - b[i]) > arcsec:  badb.append(new_b - b[i])
        new_lam, new_bet = ac.lb2sgr(l[i],b[i], 30.)[3:5]
        if np.abs(new_lam - lam[i]) > arcsec:  badlam.append(lam[i])
        if np.abs(new_bet - bet[i]) > arcsec:  badbet.append(bet[i])
        new_lam2, new_bet2 = ac.lb2sgr(new_l,new_b, 30.)[3:5]
        if np.abs(new_lam2 - lam[i]) > arcsec:  badlam2.append(lam[i])
        if np.abs(new_bet2 - bet[i]) > arcsec:  badbet2.append(bet[i])
    print data.shape[0]
    print np.mean(badl), np.mean(badb)
    print np.mean(badlam), np.mean(badbet), np.std(badbet)
    print np.mean(badlam2), np.mean(badbet2), np.std(badbet2)
    print "Done"

def mag_plots(gmin=16.0, gmax=22.5):
    path = "/home/mnewby/Desktop/"
    #path="/home/newbym/Desktop/FTO-stars/"
    #files = [path+"MSTO_North_plus20.csv", path+"MSTO_South_minus20.csv"]
    #files = [path+"MSTO_North.csv", path+"MSTO_South.csv"]
    files = [path+"blue_all.csv"]
    out = []
    for f in files:
        data = np.loadtxt(f, delimiter=",", skiprows=1)
        print "Loaded:", f
        pb = pr.Progressbar(steps=data.shape[0], prefix="Loading Stars:", suffix=None,
        symbol="#", active="=", brackets="[]", percent=True, size=40)
        for i in range(data.shape[0]):
            #if data[i,2] < ac.getr(16.0):  continue
            #if data[i,2] > ac.getr(22.5):  continue
            gmag = data[i,3]  # for BHB data
            #gmag = data[i,2]  #for MSTO data
            if gmag < gmin:  continue
            if gmag > gmax:  continue
            lam, bet = (ac.lb2sgr(data[i,0], data[i,1], 30.0))[3:5]
            if lam > 170.0:
                #if bet > 10.0:  continue
                #if bet < 2.5:  continue
                if bet > -2.5:  continue
                if bet < -10.0:  continue
            else:
                #if bet <  -2.5:  continue
                #if bet > 5.0:  continue
                if bet >  -5.0:  continue
                if bet < -12.5:  continue
            out.append([lam, bet, gmag])
            if i % 10000 == 0:  pb.updatebar(float(i)/float(data.shape[0]) )
        pb.endbar()
        print "Transformed coordinates:", f
    out = np.array(out)
    hist = pp.HistMaker(out[:,0], out[:,2], 0.5, 0.1, yarea=(16.0, 22.5), xarea=(0.0, 360.0) )
    hist.savehist(outfile="blue_faint_faint_hist.csv", fmt='%.1f')
    hist.yflip=0
    hist.xflip=1
    hist.labels=(r"$\Lambda$",r"$g_0$")
    hist.ticks = (sc.arange(20.0, 321.0, 20.0), sc.arange(16.0, 22.6, 0.5) )
    #hist.ticklabels = (None, ["16.0", "16.5", "17.0", "17.5", "18.0", "18.5", "19.0", "19.5", "20.0",
    #                            "20.5", "21.0", "21.5", "22.0", "22.5"])
    hist.varea=(0.0, 30.0)
    pp.PlotHist(hist, imfile="blue_faint_faint.png", cbarO='horizontal')
    pp.PlotHist(hist, imfile="blue_faint_faint.ps", cbarO='horizontal')

def g_plots():
    #path =
    MSTO = np.loadtxt("MSTO_b15g_hist.csv", delimiter=",")
    BHB = np.loadtxt("BHB_b10g_hist.csv", delimiter=",")
    fig = plt.figure(1, figsize=(12,9), dpi=120)
    plt.subplots_adjust(hspace=0.001, wspace=0.001)
    ########################################### BHBs
    sp3 = fig.add_subplot(212)
    #BHB = BHB[:,::-1]
    #BHB = BHB[::-1,:]
    #im3 = sp3.imshow(BHB, cmap='bone', vmax=35.0)
    #im3 = sp3.imshow(BHB, cmap='gist_yarg', vmax=30.0)
    im3 = sp3.imshow(BHB, cmap=pp.spectral_wb, vmax=25.0, aspect=2)
    xlocs = np.arange(0.0, 720.0, 40.0)
    xlabs = []
    for i in range(len(xlocs)):  xlabs.append("${0:.0f}$".format(xlocs[(i)]/2.0))
    plt.xticks(xlocs, xlabs, fontsize=12)
    ylocs = np.arange(0.0, 65.1, 5.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format(0.1*ylocs[i]+16.0))
        else:  ylabs.append("")
    plt.yticks(ylocs, ylabs, fontsize=10 )
    plt.xlabel(r"$\Lambda$", fontsize=14)
    plt.ylabel(r"$g_0$", rotation=0, fontsize=14)
    #plt.text(135, 41, "SDSS BHB Selection", fontsize=10, family="serif",
    #    backgroundcolor="w", color="k")
    plt.xlim(720.0, 0.0)
    plt.ylim(0.0, 65.0)
    ########################################### MSTOs
    sp2 = plt.subplot(211)#, sharex=sp3)
    #MSTO = MSTO[:,::-1]
    #MSTO = MSTO[::-1,:]
    #sp2.imshow(MSTO, cmap='afmhot', vmax=120.0)
    #sp2.imshow(MSTO, cmap='gist_yarg', vmax=80.0)
    sp2.imshow(MSTO, cmap=pp.spectral_wb, vmax=25.0, aspect=0.25)
    plt.xticks(np.arange(0.0, 720.0, 40.0))
    plt.setp(sp2.get_xticklabels(), visible=False)
    ylocs = np.arange(0.0, 651.0, 50.0)
    ylabs = []
    for i in range(len(ylocs)):
        if i % 2 == 0:  ylabs.append("${0:.0f}$".format((0.01*ylocs[i])+16.0))
        else:  ylabs.append("")
    plt.yticks(ylocs[:-1], ylabs[:-1], fontsize=10 )
    plt.ylabel(r"$g_0$", rotation=0, fontsize=14)
    #plt.text(266, 82, "SDSS MSTO Selection", fontsize=10, family="serif",
    #    backgroundcolor="w", color="k")
    plt.xlim(720.0, 0.0)
    plt.ylim(0.0, 650.0)
    #plt.show()
    plt.savefig("BHB_MSTO_g.png")
    #print BHB.shape
    #print MSTO.shape

def study_giants():
    path = "/usr/home/f/081/tug08879/Desktop/"
    #data = np.loadtxt(path+"Mgiant_wise_sgr.csv", delimiter=",", skiprows=1)
    #hist = pp.HistMaker( (data[:,4]-data[:,5]), data[:,5], 0.01, 0.1) #, yarea=(8.0, 15.0), xarea=(-0.1, 1.5) )
    #hist.savehist(outfile="giantCMD_hist.csv", fmt='%.1f')
    #hist.yflip=1
    #hist.xflip=0
    #hist.labels=(r"$J-K$",r"$K$")
    #hist.ticks = (None, None)
    #hist.varea=(0.0, 500.0)
    #pp.PlotHist(hist, imfile="giantCMD_faint.png", cbarO='horizontal')
    #pp.PlotHist(hist, imfile="BHB_bright_faint.ps", cbarO='horizontal')
    iso = np.loadtxt(path+"sgrIso_10Gyr_FeH-0.8.dat", skiprows=1)
    plt.figure()
    plt.plot(iso[:,8]-iso[:,10], iso[:,10])
    plt.plot([0.8, 0.8], [-6.0,10.0], "k:")
    #plt.xlim(0.8, 1.3)
    plt.ylim(10.0, -6.0)
    plt.show()

def field_of_streams(xa = (0.0,360.0), ya=(-90.0, 90.0), normed=1, file=None, hname=""):
    #xa = (110.0,230.0), ya=(-5.0, 60.0), normed=1):
    path = "/usr/home/f/081/tug08879/Desktop/"
    #file = "MSTO_North.csv"
    hname = "_sgrtweaked"
    if file != None:
        data = np.loadtxt(path+file, delimiter=",", skiprows=1)
        print "Loaded data"
        # change coordinates
        for i in range(data.shape[0]):
            ra, dec = ac.lbToEq(data[i,0], data[i,1])
            data[i,0], data[i,1] = ra, dec
        print "Changed Coordinates"
        #Wr, Br, Gr, Rr, Kr = 20.0+0.25, 20.66+0.25, 21.33+0.25, 22.0+0.25, 23.0+0.25  #Belokurov 2006 + g-r=0.25
        Wr, Br, Gr, Rr, Kr = 19.0, 21.0, 21.75, 22.5, 23.0
        # bins for each color
        W, B, G, R, K = [], [], [], [], []
        for i in range(len(data[:,0])):
            if   data[i,2] < Wr:  W.append(data[i,:])
            elif data[i,2] < Br:  B.append(data[i,:])
            elif data[i,2] < Gr:  G.append(data[i,:])
            elif data[i,2] < Rr:  R.append(data[i,:])
            else:  pass
        if R == []:  R = [[0.0,0.0,0.0]]  #failsafe
        if G == []:  G = [[0.0,0.0,0.0]]  #failsafe
        if B == []:  B = [[0.0,0.0,0.0]]  #failsafe
        B = np.array(B)
        Bhist = pp.HistMaker(B[:,0], B[:,1], xsize=0.25, ysize=0.25, xarea=xa, yarea=ya)
        Bhist.varea = (0.0,200.0)
        Bhist.savehist("Bhist.csv")
        G = np.array(G)
        Ghist = pp.HistMaker(G[:,0], G[:,1], xsize=0.25, ysize=0.25, xarea=xa, yarea=ya)
        Ghist.varea = (0.0,200.0)
        Ghist.savehist("Ghist.csv")
        R = np.array(R)
        Rhist = pp.HistMaker(R[:,0], R[:,1], xsize=0.25, ysize=0.25, xarea=xa, yarea=ya)
        Rhist.varea = (0.0,200.0)
        Rhist.savehist("Rhist.csv")
    else:
        Bhist = pp.HistFromFile("Bhist"+hname+".csv")
        Ghist = pp.HistFromFile("Ghist"+hname+".csv")
        Rhist = pp.HistFromFile("Rhist"+hname+".csv")
    #print np.ma.max(Bhist.H), np.ma.max(Ghist.H), np.ma.max(Rhist.H)
    # Now correct for bin size changes due to declination
    for j in range(Bhist.H.shape[0]):
        decl = (j - 360)*0.25
        mod = 1.0 / np.cos(decl*ma.pi/180.0)
        Bhist.H[j,:] = Bhist.H[j,:]*mod
        Ghist.H[j,:] = Ghist.H[j,:]*mod
        Rhist.H[j,:] = Rhist.H[j,:]*mod
    if normed == 1:
        Bhist.H = Bhist.H / 25.0 #np.ma.max(Bhist.H)  #Normalize individually
        Ghist.H = Ghist.H / 12.0 #np.ma.max(Ghist.H)
        Rhist.H = Rhist.H / 12.0 #np.ma.max(Rhist.H)
    else:
        #norm = max(np.ma.max(Bhist.H), np.ma.max(Ghist.H), np.ma.max(Rhist.H))
        norm = 100.0
        Bhist.H = norm_hist(Bhist.H, norm)
        Ghist.H = norm_hist(Ghist.H, norm)
        Rhist.H = norm_hist(Rhist.H, norm)
    RGB = np.dstack( (Rhist.H, Ghist.H, Bhist.H) )
    fig = plt.figure(dpi=300, figsize=(5.0,4.0) )
    sp = plt.subplot(111)
    plt.imshow(RGB, origin='lower')
    plt.setp(sp.get_xticklabels(), visible=False)
    plt.setp(sp.get_yticklabels(), visible=False)
    plt.xlim(1075.0, 425.0)
    plt.ylim(340.0, 640.0)
    plt.savefig("FoS_smallbins.png", dpi=300)
    #plt.savefig("FoS_smallbins.ps", dpi=300)
    #plt.show()
    #plt.close('all')

def norm_hist(H, norm):
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            if H[i,j] > norm:  H[i,j] = 1.0
        else:  H[i,j] = H[i,j] / norm
    return H


if __name__ == "__main__":  do_stuff()
