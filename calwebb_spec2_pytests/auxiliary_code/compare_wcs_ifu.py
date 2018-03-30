import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from astropy.io import fits
from decimal import Decimal
from jwst.assign_wcs.tools.nirspec import compute_world_coordinates as cwc
from . import auxiliary_functions as auxfunc


"""
This script compares pipeline WCS info with ESA results for Integral Field Unit (IFU) data.

"""



def mk_plots(title, show_figs=True, save_figs=False, info_fig1=None, info_fig2=None,
             histogram=False, deltas_plt=False, msacolormap=False, fig_name=None):
    """
    This function makes all the plots of the script.
    Args:
        title: str, title of the plot
        show_figs: boolean, show figures on screen or not
        save_figs: boolean, save figures or not
        info_fig1: list, arrays, number of bins, and limits for the first figure in the plot
        info_fig2: list, arrays, number of bins, and limits for the second figure in the plot
        histogram: boolean, are the figures in the plot histograms
        deltas_plt: boolean, regular plot
        msacolormap: boolean, single figure
        fig_name: str, name of plot

    Returns:
        It either shows the resulting figure on screen and saves it, or one of the two.
    """
    font = {#'family' : 'normal',
            'weight' : 'normal',
            'size'   : 16}
    matplotlib.rc('font', **font)
    fig = plt.figure(1, figsize=(12, 10))
    plt.subplots_adjust(hspace=.4)
    alpha = 0.2
    fontsize = 15
    if not msacolormap:
        # FIGURE 1
        # number in the parenthesis are nrows, ncols, and plot number, numbering in next row starts at left
        ax = plt.subplot(211)
        if histogram:
            xlabel1, ylabel1, xarr1, yarr1, xmin, xmax, bins, x_median, x_stddev = info_fig1
            x_median = "median = {:0.3}".format(x_median)
            x_stddev = "stddev = {:0.3}".format(x_stddev)
            plt.title(title)
            plt.xlabel(xlabel1)
            plt.ylabel(ylabel1)
            plt.xlim(xmin, xmax)
            ax.text(0.7, 0.9, x_median, transform=ax.transAxes, fontsize=fontsize)
            ax.text(0.7, 0.83, x_stddev, transform=ax.transAxes, fontsize=fontsize)
            n, bins, patches = ax.hist(xarr1, bins=bins, histtype='bar', ec='k', facecolor="red", alpha=alpha)
        if deltas_plt:
            title1, xlabel1, ylabel1, xarr1, yarr1, xdelta, x_median, x_stddev = info_fig1
            plt.title(title1)
            plt.xlabel(xlabel1)
            plt.ylabel(ylabel1)
            mean_minus_1half_std = x_median - 1.5*x_stddev
            mean_minus_half_std = x_median - 0.5*x_stddev
            mean_plus_half_std = x_median + 0.5*x_stddev
            mean_plus_1half_std = x_median + 1.5*x_stddev
            """
            for xd, xi, yi in zip(xdelta, xarr1, yarr1):
                if xd > mean_plus_1half_std:
                    plt.plot(xi, yi, linewidth=7, marker='D', color='red')#, label=r"$\Delta x > \mu+1.5\sigma$")
                if xd < mean_minus_1half_std:
                    plt.plot(xi, yi, linewidth=7, marker='D', color='fuchsia')#, label=r"$\Delta x < \mu-1.5\sigma$")
                if (xd > mean_minus_1half_std) and (xd < mean_minus_half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='blue')#, label=r"$\mu-1.5\sigma < \Delta x < \mu-0.5\sigma$")
                if (xd > mean_minus_half_std) and (xd < mean_plus_half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='lime')#, label=r"$\mu-0.5\sigma$ < \Delta x < \mu+0.5\sigma$")
                if (xd > mean_plus_half_std) and (xd < mean_plus_1half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='black')#, label=r"$\mu+0.5\sigma$ < \Delta x < \mu+1.5\sigma$")
            plt.xlim(min(xarr1), max(xarr1))
            plt.ylim(min(yarr1), max(yarr1))
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='red', label=r"$\Delta \lambda > \mu+1.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='fuchsia', label=r"$\Delta \lambda < \mu-1.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='blue', label=r"$\mu-1.5\sigma < \Delta \lambda < \mu-0.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='lime', label=r"$\mu-0.5\sigma < \Delta \lambda < \mu+0.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='black', label=r"$\mu+0.5\sigma < \Delta \lambda < \mu+1.5\sigma$")
            """
            idx_red = np.where(xdelta > mean_plus_1half_std)[0]
            idx_fuchsia = np.where(xdelta < mean_minus_1half_std)[0]
            idx_blue = np.where((xdelta > mean_minus_1half_std) & (xdelta < mean_minus_half_std))[0]
            idx_lime = np.where((xdelta > mean_minus_half_std) & (xdelta < mean_plus_half_std))[0]
            idx_black = np.where((xdelta > mean_plus_half_std) & (xdelta < mean_plus_1half_std))[0]
            plt.plot(xarr1[idx_lime], yarr1[idx_lime], linewidth=2, marker='.', color='lime', label=r"$\mu-0.5\sigma < \Delta \lambda < \mu+0.5\sigma$", alpha=0.7)
            plt.plot(xarr1[idx_black], yarr1[idx_black], linewidth=2, marker='.', color='black', label=r"$\mu+0.5\sigma < \Delta \lambda < \mu+1.5\sigma$", alpha=alpha)
            plt.plot(xarr1[idx_blue], yarr1[idx_blue], linewidth=2, marker='.', color='blue', label=r"$\mu-1.5\sigma < \Delta \lambda < \mu-0.5\sigma$", alpha=alpha)
            plt.plot(xarr1[idx_red], yarr1[idx_red], linewidth=2, marker='.', color='red', label=r"$\Delta \lambda > \mu+1.5\sigma$", alpha=alpha)
            plt.plot(xarr1[idx_fuchsia], yarr1[idx_fuchsia], linewidth=2, marker='.', color='fuchsia', label=r"$\Delta \lambda < \mu-1.5\sigma$", alpha=alpha)

            # add legend
            box = ax.get_position()
            #ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
            #ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
            # shrink plotting space so that the legend is to the right
            percent = 0.72
            ax.set_position([box.x0, box.y0, box.width * percent, box.height * percent])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))   # put legend out of the plot box
            textinfig_mu = r'$\mu_x$={:<0.3e}    $\sigma_x$={:<0.3e}'.format(x_median, x_stddev)
            ax.annotate(textinfig_mu, xy=(1.02, 0.95), xycoords='axes fraction' )
        plt.minorticks_on()
        if histogram:
            ax.xaxis.set_major_locator(MaxNLocator(6))
            from matplotlib.ticker import FuncFormatter
            def MyFormatter(x, lim):
                if x == 0:
                    return 0
                return "%0.3E" % Decimal(x)
            majorFormatter = FuncFormatter(MyFormatter)
            ax.xaxis.set_major_formatter(majorFormatter)
        plt.tick_params(axis='both', which='both', bottom='on', top='on', right='on', direction='in', labelbottom='on')

        # FIGURE 2
        # number in the parenthesis are nrows, ncols, and plot number, numbering in next row starts at left
        ax = plt.subplot(212)
        if histogram:
            xlabel2, ylabel2, xarr2, yarr2, xmin, xmax, bins, y_median, y_stddev = info_fig2
            y_median = "median = {:0.3}".format(y_median)
            y_stddev = "stddev = {:0.3}".format(y_stddev)
            plt.xlabel(xlabel2)
            plt.ylabel(ylabel2)
            plt.xlim(xmin, xmax)
            ax.text(0.7, 0.9, y_median, transform=ax.transAxes, fontsize=fontsize)
            ax.text(0.7, 0.83, y_stddev, transform=ax.transAxes, fontsize=fontsize)
            n, bins, patches = ax.hist(xarr2, bins=bins, histtype='bar', ec='k', facecolor="red", alpha=alpha)
        if deltas_plt:
            title2, xlabel2, ylabel2, xarr2, yarr2, ydelta, y_median, y_stddev = info_fig2
            plt.title(title2)
            plt.xlabel(xlabel2)
            plt.ylabel(ylabel2)
            mean_minus_1half_std = y_median - 1.5*y_stddev
            mean_minus_half_std = y_median - 0.5*y_stddev
            mean_plus_half_std = y_median + 0.5*y_stddev
            mean_plus_1half_std = y_median + 1.5*y_stddev
            """
            for yd, xi, yi in zip(ydelta, xarr2, yarr2):
                if yd > mean_plus_1half_std:
                    plt.plot(xi, yi, linewidth=7, marker='D', color='red')#, label=r"$\Delta y > \mu+1.5\sigma$")
                if yd < mean_minus_1half_std:
                    plt.plot(xi, yi, linewidth=7, marker='D', color='fuchsia')#, label=r"$\Delta y < \mu-1.5\sigma$")
                if (yd > mean_minus_1half_std) and (yd < mean_minus_half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='blue')#, label=r"$\mu-1.5\sigma < \Delta y < \mu-0.5\sigma$")
                if (yd > mean_minus_half_std) and (yd < mean_plus_half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='lime')#, label=r"$\mu-0.5\sigma$ < \Delta y < \mu+0.5\sigma$")
                if (yd > mean_plus_half_std) and (yd < mean_plus_1half_std):
                    plt.plot(xi, yi, linewidth=7, marker='D', color='black')#, label=r"$\mu+0.5\sigma$ < \Delta y < \mu+1.5\sigma$")
            plt.xlim(min(xarr2), max(xarr2))
            plt.ylim(min(yarr2), max(yarr2))
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='red', label=r"$\Delta y > \mu+1.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='fuchsia', label=r"$\Delta y < \mu-1.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='blue', label=r"$\mu-1.5\sigma < \Delta y < \mu-0.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='lime', label=r"$\mu-0.5\sigma < \Delta y < \mu+0.5\sigma$")
            plt.plot(-10.0, -10.0, linewidth=7, marker='D', color='black', label=r"$\mu+0.5\sigma < \Delta y < \mu+1.5\sigma$")
            """
            idx_red = np.where(ydelta > mean_plus_1half_std)[0]
            idx_fuchsia = np.where(ydelta < mean_minus_1half_std)[0]
            idx_blue = np.where((ydelta > mean_minus_1half_std) & (ydelta < mean_minus_half_std))[0]
            idx_lime = np.where((ydelta > mean_minus_half_std) & (ydelta < mean_plus_half_std))[0]
            idx_black = np.where((ydelta > mean_plus_half_std) & (ydelta < mean_plus_1half_std))[0]
            plt.plot(xarr2[idx_lime], yarr2[idx_lime], linewidth=2, marker='.', color='lime', label=r"$\mu-0.5\sigma < \Delta y < \mu+0.5\sigma$", alpha=0.7)
            plt.plot(xarr2[idx_black], yarr2[idx_black], linewidth=2, marker='.', color='black', label=r"$\mu+0.5\sigma < \Delta y < \mu+1.5\sigma$", alpha=alpha)
            plt.plot(xarr2[idx_blue], yarr2[idx_blue], linewidth=2, marker='.', color='blue', label=r"$\mu-1.5\sigma < \Delta y < \mu-0.5\sigma$", alpha=alpha)
            plt.plot(xarr2[idx_red], yarr2[idx_red], linewidth=2, marker='.', color='red', label=r"$\Delta y > \mu+1.5\sigma$", alpha=alpha)
            plt.plot(xarr2[idx_fuchsia], yarr2[idx_fuchsia], linewidth=2, marker='.', color='fuchsia', label=r"$\Delta y < \mu-1.5\sigma$", alpha=alpha)
            # add legend
            box = ax.get_position()
            #ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
            #ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
            # shrink plotting space so that the legend is to the right
            percent = 0.72
            ax.set_position([box.x0, box.y0, box.width * percent, box.height * percent])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))   # put legend out of the plot box
            textinfig_mu = r'$\mu_y$={:<0.3e}    $\sigma_y$={:<0.3e}'.format(y_median, y_stddev)
            ax.annotate(textinfig_mu, xy=(1.02, 0.95), xycoords='axes fraction' )
        plt.tick_params(axis='both', which='both', bottom='on', top='on', right='on', direction='in', labelbottom='on')
        plt.minorticks_on()
    else:
        xlabel, ylabel, xarr, yarr, xdelta = info_fig1
        ax = plt.subplot(111)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        lim_a = -5.0e-13
        lim_b = -1.0e-15
        lim_c = 1.0e-13
        lim_d = 5.0e-13
        plt.xlim(0.0405, 0.0425)
        plt.ylim(-0.0010, 0.0010)
        #plt.xticks(np.arange(min(xarr), max(xarr), xarr[0]*5))
        #plt.yticks(np.arange(min(yarr), max(yarr), 0.000005))
        """
        for xd, xi, yi in zip(xdelta, xarr, yarr):
            if xd > lim_d:
                plt.plot(xi, yi, linewidth=7, marker='D', color='red')#, label=r"$ \Delta x > 5.0e-13 $")
            if xd < lim_a:
                plt.plot(xi, yi, linewidth=7, marker='D', color='fuchsia')#, label=r"$\Delta x < -5.0e-13 $")
            if (xd > lim_a) and (xd < lim_b):
                plt.plot(xi, yi, linewidth=7, marker='D', color='blue')#, label=r"$ -5.0e-13 < \Delta x < -1.0e-15 $")
            if (xd > lim_b) and (xd < lim_c):
                plt.plot(xi, yi, linewidth=7, marker='D', color='lime')#, label=r"$ -1.0e-15 < \Delta x < 1.0e-13 $")
            if (xd > lim_c) and (xd < lim_d):
                plt.plot(xi, yi, linewidth=7, marker='D', color='black')#, label=r"$ 1.0e-15 < \Delta x < 5.0e-13 $")
        plt.plot(-10.0, 10.0, linewidth=7, marker='D', color='red', label=r"$ \Delta x > 5.0e-13 $")
        plt.plot(-10.0, 10.0, linewidth=7, marker='D', color='fuchsia', label=r"$ \Delta x < -5.0e-13$")
        plt.plot(-10.0, 10.0, linewidth=7, marker='D', color='blue', label=r"$ -5.0e-13 < \Delta x < -1.0e-15 $")
        plt.plot(-10.0, 10.0, linewidth=7, marker='D', color='lime', label=r"$ -1.0e-15 < \Delta x < 1.0e-13 $")
        plt.plot(-10.0, 10.0, linewidth=7, marker='D', color='black', label=r"$ 1.0e-15 < \Delta x < 5.0e-13 $")
        """
        idx_red = np.where(xdelta > lim_d)[0]
        idx_fuchsia = np.where(xdelta < lim_a)[0]
        idx_blue = np.where((xdelta > lim_a) & (xdelta < lim_b))[0]
        idx_lime = np.where((xdelta > lim_b) & (xdelta < lim_c))[0]
        idx_black = np.where((xdelta > lim_c) & (xdelta < lim_d))[0]
        plt.plot(xarr[idx_lime], yarr[idx_lime], linewidth=2, marker='.', color='lime', label=r" -1.0e-15 < $\Delta \lambda$ < 1.0e-13 ", alpha=0.7)
        plt.plot(xarr[idx_black], yarr[idx_black], linewidth=2, marker='.', color='black', label=r" 1.0e-15 < $\Delta \lambda$ < 5.0e-13 ", alpha=alpha)
        plt.plot(xarr[idx_blue], yarr[idx_blue], linewidth=2, marker='.', color='blue', label=r" -5.0e-13 < $\Delta \lambda$ < -1.0e-15 ", alpha=alpha)
        plt.plot(xarr[idx_red], yarr[idx_red], linewidth=2, marker='.', color='red', label=r" $ \Delta \lambda$ > 5.0e-13 ", alpha=alpha)
        plt.plot(xarr[idx_fuchsia], yarr[idx_fuchsia], linewidth=2, marker='.', color='fuchsia', label=r"$\Delta \lambda$ < -5.0e-13 ", alpha=alpha)

        # Shrink current axis
        box = ax.get_position()
        percent = 0.99
        ax.set_position([box.x0, box.y0, box.width * percent, box.height * 1.1])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))   # put legend out of the plot box
        textinfig_mu = r'$\mu_\lambda$={:<0.3e}    $\sigma_\lambda$={:<0.3e}'.format(np.median(xdelta), np.std(xdelta))
        ax.annotate(textinfig_mu, xy=(1.02, 0.62), xycoords='axes fraction' )
        plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
        ax.xaxis.set_major_locator(MaxNLocator(6))
        plt.tight_layout()
        plt.tick_params(axis='both', which='both', bottom='on', top='on', right='on', direction='in', labelbottom='on')
        plt.minorticks_on()
    if save_figs:
        type_fig = "pdf"
        if histogram:
            if fig_name is None:
                fig_name = ".".join(("_histogram", type_fig))
        if deltas_plt:
            if fig_name is None:
                fig_name = ".".join(("_Deltas", type_fig))
        if msacolormap:
            if fig_name is None:
                fig_name = ".".join(("_MSAcolormap", type_fig))
        fig.savefig(fig_name)
        print (' Plot saved: ', fig_name)
    if show_figs:
        plt.show()
    plt.close()


def compare_wcs(infile_name, esa_files_path=None, auxiliary_code_path=None,
                show_figs=True, save_figs=False, plot_names=None, threshold_diff=1.0e-14, debug=False):
    """
    This function does the WCS comparison from the world coordinates calculated using the
    compute_world_coordinates.py script with the ESA files. The function calls that script.

    Args:
        infile_name: str, name of the output fits file from the 2d_extract step (with full path)
        esa_files_path: str, full path of where to find all ESA intermediary products to make comparisons for the tests
        auxiliary_code_path: str, path where to find the auxiliary code. If not set the code will assume
                            it is in the the auxiliary code directory
        show_figs: boolean, whether to show plots or not
        save_figs: boolean, save the plots (the 3 plots can be saved or not independently with the function call)
        plot_names: list of 3 strings, desired names (if names are not given, the plot function will name the plots by
                    default)
        threshold_diff: float, threshold difference between pipeline output and ESA file
        debug: boolean, if true a series of print statements will show on-screen

    Returns:
        - 2 plots, if told to save and/or show them.
        - median_diff: Boolean, True if smaller or equal to 1e-14

    """

    # get grating and filter info from the rate file header
    det = fits.getval(infile_name, "DETECTOR", 0)
    print('infile_name=', infile_name)
    lamp = fits.getval(infile_name, "LAMP", 0)
    grat = fits.getval(infile_name, "GRATING", 0)
    filt = fits.getval(infile_name, "FILTER", 0)
    print ("Info from WCS file  -->     Detector:", det, "   Grating:", grat, "   Filter:", filt, "   Lamp:", lamp)


    # Run compute_world_coordinates.py in order to produce the necessary file
    # !!! note that the code expects to be in the build environment !!!
    if auxiliary_code_path is None:
        auxiliary_code_path = "./"

    # compute world coordinates with Nadia's script
    print ("running compute_world_coordinates.py script...")
    cwc.ifu_coords(infile_name)
    print (" ... done.")

    # The world coordinate file was created but it needs to be renamed
    basenameinfile_name = os.path.basename(infile_name)
    fileID = basenameinfile_name.split("_")[0]   # obtain the id of the file
    working_dir_path = os.getcwd()
    wcoordfile = working_dir_path+"/"+fileID+"_world_coordinates.fits"
    #print (wcoordfile)
    # to move file to location of infile
    #cwc_fname = infile_name.replace(".fits", "_world_coordinates.fits")
    # to rename file within the working directory
    cwc_fname = basenameinfile_name.replace(".fits", "_world_coordinates.fits")
    #print (cwc_fname)
    cwc_fname = infile_name.replace(basenameinfile_name, cwc_fname)
    os.system("mv "+wcoordfile+" "+cwc_fname)

    # loop over the slits
    wchdu = fits.open(cwc_fname)
    slices = len(wchdu)
    sci_ext_list = auxfunc.get_sci_extensions(infile_name)
    print ('sci_ext_list=', sci_ext_list, '\n')

    for wc_ext in range(1, slices):
        try:
            print("-> opening extension =", wc_ext, "  in ", cwc_fname)
            hdr = wchdu[wc_ext].header
        except:
            IndexError
            break

        # what is the slice of this exposure
        pslit = hdr["SLIT"].replace("SLIT_", "")
        if float(pslit) < 10.0:
            IFUslice = "0"+pslit
        else:
            IFUslice = pslit

        print("working with slice: ", IFUslice)

        # for matched spectrum, get the wavelength and Delta_Y values
        fdata = fits.getdata(cwc_fname, ext=wc_ext)
        pwave = fdata[0,:,:] * 1.0e-6
        pdy = fdata[3,:,:]
        pskyx = fdata[1,:,:]
        pskyy = fdata[2,:,:]

        # get the subwindow origin (technically no subwindows for IFU, but need it for comparing with IDT extractions)
        px0 = fits.getval(cwc_fname, "CRVAL1", wc_ext)
        py0 = fits.getval(cwc_fname, "CRVAL2", wc_ext)
        if debug:
            print ("px0=",px0, "   py0=", py0)

        # get the count rates for this spectrum
        counts = fits.getdata(infile_name, 1)
        n_p = np.shape(pwave)
        if debug:
            print("n_p =", n_p)
        npx = n_p[1]
        npy = n_p[0]
        px = np.arange(npx)+px0
        py = np.arange(npy)+py0
        if debug:
            print  ("px =", px)
            print  ("px0+npx-1 =", px0+npx-1)
            print  ("py =", py)
            print  ("py0+npy-1 =", py0+npy-1)

        # read in the ESA file using raw data root file name
        #raw_data_root_file = "NRSSMOS-MOD-G1M-17-5344175105_1_491_SE_2015-12-10T18h00m06.fits"
        _, raw_data_root_file = auxfunc.get_modeused_and_rawdatrt_PTT_cfg_file()
        specifics = [IFUslice]
        esafile = auxfunc.get_esafile(esa_files_path, raw_data_root_file, "IFU", specifics)

        esahdulist = fits.open(esafile)
        print ("* ESA file contents ")
        esahdulist.info()
        esahdr1 = esahdulist[1].header
        enext = []
        for ext in esahdulist:
            enext.append(ext)
        eflux = fits.getdata(esafile, 1)
        ewave = fits.getdata(esafile, 4)
        edy = fits.getdata(esafile, 5)
        emsax = fits.getdata(esafile, 6)
        emsay = fits.getdata(esafile, 7)
        esahdulist.close()
        n_p = np.shape(eflux)
        nex = n_p[1]
        ney = n_p[0]
        # get the origin of the subwindow
        ex0 = esahdr1["CRVAL1"] - esahdr1["CRPIX1"] + 1
        ey0 = esahdr1["CRVAL2"] - esahdr1["CRPIX2"] + 1
        ex = np.arange(nex) + ex0
        ey = np.arange(ney) + ey0
        print("ESA subwindow corner pixel ID: ", ex0, ey0)
        if debug:
            print("From ESA file: ")
            print("   ex0 =", ex0)
            print("   ey0 =", ey0)
            print("   ex=", ex, "   ey=", ey)

        # match up the correct elements in each data set
        subpx, subex = auxfunc.do_idl_match(px, ex)
        subpy, subey = auxfunc.do_idl_match(py, ey)
        imp, ime = [], []
        for spy in subpy:
            im0 = subpx + npx * spy
            imp.append(im0)
        for sey in subey:
            im0 = subex + nex * sey
            ime.append(im0)
        imp, ime = np.array(imp), np.array(ime)
        imp, ime  = imp.flatten(), ime.flatten()

        if debug:
            print ("SAHPES subpx, subex: ", np.shape(subpx), np.shape(subex))
            print ("SHAPES subpy, subey: ", np.shape(subpy), np.shape(subey))


        # get the difference between the two in units of m
        # do not include pixels where one or the other solution is 0 or NaN
        flat_pwave, flat_ewave = pwave.flatten(), ewave.flatten()
        ig = []
        for ip, ie, ig_i in zip(imp, ime, range(len(imp))):
            if all( [flat_pwave[ip] != 0 and flat_ewave[ie].size != 0 and np.isfinite(flat_pwave[ip]) and np.isfinite(flat_ewave[ip])] ):
                ig.append(ig_i)

        pxr, pyr = np.array([]), np.array([])
        for _ in range(npy):
            pxr = np.concatenate((pxr, px))
        pxr = pxr.astype(int)
        reshaped_py = py.reshape(npy, 1)
        for rpy_i in reshaped_py:
            for _ in range(npx):
                pyr = np.concatenate((pyr, rpy_i))
        pyr = pyr.astype(int)

        pxrg, pyrg, deldy, delwave = [], [], [], []
        flat_pdy, flat_edy = pdy.flatten(), edy.flatten()
        emsax, emsay = emsax.flatten(), emsay.flatten()
        arrx, arry = [], []
        for ig_i in ig:
            if np.isfinite(flat_pdy[imp[ig_i]]) and np.isfinite(flat_edy[ime[ig_i]]):
                pxrg_i = pxr[imp[ig_i]]
                pxrg.append(pxrg_i)
                pyrg_i = pyr[imp[ig_i]]
                pyrg.append(pyrg_i)
                deldy_i = flat_pdy[imp[ig_i]] - flat_edy[ime[ig_i]]
                deldy.append(deldy_i)
                delw = flat_pwave[imp[ig_i]] - flat_ewave[ime[ig_i]]
                delwave.append(delw)
                # for the MSA color plot
                arrx.append(emsax[ime[ig_i]])
                arry.append(emsay[ime[ig_i]])

        pxrg, pyrg, deldy, delwave = np.array(pxrg), np.array(pyrg), np.array(deldy), np.array(delwave)
        arrx, arry = np.array(arrx), np.array(arry)

        for dw in delwave:
            if not np.isfinite(dw):
                print("Got a NaN, median and standard deviation will fail for delta_wavelength array.")

        for dy_i in deldy:
            if not np.isfinite(dy_i):
                print("Got a NaN, median and standard deviation of delta_y array will fail.")

        if debug:
            print("shapes of px, py: ", np.shape(px), np.shape(py))
            print("shapes of pxr, pyr: ", np.shape(pxr), np.shape(pyr))
            print("shapes of pdy, edy: ", np.shape(pdy), np.shape(edy))
            print("shapes of ig, delwave: ", np.shape(ig), np.shape(delwave))
            print("shapes of pwave, ewave, imp, ime: ", np.shape(pwave), np.shape(ewave), np.shape(imp), np.shape(ime))

        # get the median and standard deviations
        median_diff = False
        if len(delwave) > 1:
            delwave_median, delwave_stddev = np.median(delwave), np.std(delwave)
            deldy_median, deldy_stddev = np.median(deldy), np.std(deldy)
            print("\n  delwave:   median =", delwave_median, "   stdev =", delwave_stddev)
            print("\n  deldy:   median =", deldy_median, "   stdev =", deldy_stddev)

            # This is the key argument for the assert pytest function
            if abs(delwave_median) <= threshold_diff:
                median_diff = True
            if median_diff:
                test_result = "PASSED"
            else:
                test_result = "FAILED"
            print (" *** Result of the test: ",test_result)

        # PLOTS
        if show_figs or save_figs and (len(delwave) != 0) and np.isfinite(deldy_median):
            print ("\n * Making WCS plots *")
            if plot_names is not None:
                hist_name, deltas_name, msacolormap_name = plot_names
            else:
                #hist_name, deltas_name, msacolormap_name = None, None, None
                hist_name = infile_name.replace(".fits", "_"+IFUslice+"_wcs_histogram.pdf")
                deltas_name = infile_name.replace(".fits", "_"+IFUslice+"_wcs_Deltas.pdf")
                msacolormap_name = infile_name.replace(".fits", "_"+IFUslice+"_wcs_MSAcolormap.pdf")

            # HISTOGRAM
            print("\n Making histogram...")
            if filt == "OPAQUE":
                filt = lamp
            title = filt+"   "+grat+"   slice ID: "+IFUslice
            xmin1 = min(delwave) - (max(delwave)-min(delwave))*0.1
            xmax1 = max(delwave) + (max(delwave)-min(delwave))*0.1
            exp = int(str(xmax1).split('e')[-1])
            xlabel1, ylabel1 = r"$\lambda_{pipe} - \lambda_{ESA}$  (10^"+repr(exp)+"m)", "N"
            yarr = None
            bins = 15
            info_fig1 = [xlabel1, ylabel1, delwave, yarr, xmin1, xmax1, bins, delwave_median, delwave_stddev]
            xmin2 = min(deldy) - (max(deldy)-min(deldy))*0.1
            xmax2 = max(deldy) + (max(deldy)-min(deldy))*0.1
            xlabel2, ylabel2 = r"$\Delta y_{pipe}$ - $\Delta y_{ESA}$  (relative slit position)", "N"
            info_fig2 = [xlabel2, ylabel2, deldy, yarr, xmin2, xmax2, bins, deldy_median, deldy_stddev]
            mk_plots(title, info_fig1=info_fig1, info_fig2=info_fig2, show_figs=show_figs, save_figs=save_figs,
                     histogram=True, fig_name=hist_name)

            # DELTAS PLOT
            print("\n Making deltas plot...")
            title = ""
            title1, xlabel1, ylabel1 = r"$\Delta \lambda$", "x (pixels)", "y (pixels)"
            info_fig1 = [title1, xlabel1, ylabel1, pxrg, pyrg, delwave, delwave_median, delwave_stddev]
            title2, xlabel2, ylabel2 = "Relative slit position", "x (pixels)", "y (pixels)"
            info_fig2 = [title2, xlabel2, ylabel2, pxrg, pyrg, deldy, deldy_median, deldy_stddev]
            mk_plots(title, info_fig1=info_fig1, info_fig2=info_fig2, show_figs=show_figs, save_figs=save_figs,
                     deltas_plt=True, fig_name=deltas_name)

            # MSA COLOR MAP
            print("\n Making color map...")
            title = "MSA Color Map"
            xlabel, ylabel = "MSA_x (m)", "MSA_y (m)"
            info_fig1 = [xlabel, ylabel, arrx, arry, delwave]
            mk_plots(title, info_fig1=info_fig1, show_figs=show_figs, save_figs=save_figs,
                     msacolormap=True, fig_name=msacolormap_name)

            print("Done.")

        else:
            if not show_figs or not save_figs:
                print ("NO plots were made because show_figs and save_figs were both set to False. \n")
            if len(delwave) == 0:
                print ("NO plots were made because the delta_wavelength array is emtpy.  \n")
            if not np.isfinite(deldy_median):
                print ("NO plots were made because the median of delta_y array is NaN.  \n")

    return median_diff



if __name__ == '__main__':

    # This is a simple test of the code
    pipeline_path = "/Users/pena/Documents/PyCharmProjects/nirspec/pipeline"

    # input parameters that the script expects
    auxiliary_code_path = pipeline_path+"/src/nirspec_pipe_testing_tool/calwebb_spec2_pytests/auxiliary_code"
    #working_dir = "/Users/pena/Documents/PyCharmProjects/nirspec/pipeline/build7.1/part1_JanuaryDeadline/IFU_CV3/PRISM_CLEAR/pipe_testing_files_and_reports/6007022859_491_processing"
    working_dir = "/Users/pena/Documents/PyCharmProjects/nirspec/pipeline/build7.1/part1_JanuaryDeadline/IFU_CV3/G140M_F100LP/pipe_testing_files_and_reports/491_processing/Nadias_fix_run2"
    infile_name = working_dir+"/gain_scale_assign_wcs.fits"
    #esa_files_path=pipeline_path+"/build7/test_data/ESA_intermediary_products/RegressionTestData_CV3_March2017_IFU/"
    esa_files_path = "/grp/jwst/wit4/nirspec_vault/prelaunch_data/testing_sets/b7.1_pipeline_testing/test_data_suite/IFU_CV3/ESA_Int_products"

    # set the names of the resulting plots
    hist_name = infile_name.replace("fits", "")+"_wcs_histogram.pdf"
    deltas_name = infile_name.replace("fits", "")+"_wcs_deltas.pdf"
    msacolormap_name = infile_name.replace("fits", "")+"_wcs_msacolormap.pdf"
    plot_names = None #[hist_name, deltas_name, msacolormap_name]

    # Run the principal function of the script
    median_diff = compare_wcs(infile_name, esa_files_path=esa_files_path, auxiliary_code_path=auxiliary_code_path,
                              plot_names=plot_names, show_figs=False, save_figs=True, threshold_diff=9.9e-14, debug=False)
