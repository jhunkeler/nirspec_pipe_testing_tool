import os
import subprocess
import argparse
from astropy.io import fits

"""

This script looks in the final ouptut from cal_detector1, to check that the filter was indeed OPAQUE before
changing it to a science filter in the input for calwebb_spec2. The script can also change the filter from
OPAQUE to a science filter.

Example usage:
    The code is automatically called within the PTT. However, it can also be a stand alone script that
    runs from the terminal within the pipeline conda environment.

    In any directory, type:
        > python /path_to_this_script/change_filter_opaque2science.py blah.fits
    this will create a new file with the filter changed in the same directory as the blah.fits file.

"""

# HEADER
__author__ = "M. A. Pena-Guerrero"
__version__ = "1.0"

# HISTORY
# Nov 2017 - Version 1.0: initial version completed


def change_filter_opaque(cal_detector1_output, calwebb_spec2_pytests_dir=None, step=None, force_filter_change=False):
    """
    This function  checks that the filter was indeed set to opaque in the final output file from
    cal_detector1, the corresponding switch in the PTT config file, and then does the change
    Args:
        cal_detector1_output: string, path and name of the final output file from cal_detector1
        calwebb_spec2_pytests_dir: string, path to the utils directory
        step: string, name of the step to be ran in within the testing tool
        force_filter_change: boolean, switch to force the code to make the filter change

    Returns:
        change_filter2opaque: boolean, True if the filter was changed
    """

    gain_scale_basename = os.path.basename(cal_detector1_output)
    exp_type = fits.getval(cal_detector1_output, "EXP_TYPE", 0)
    filt = fits.getval(cal_detector1_output, "FILTER", 0)
    grat = fits.getval(cal_detector1_output, "GRATING", 0)
    print ("The file: ", cal_detector1_output)
    print (" has the this configuration:    EXP_TYPE =", exp_type, "    FILTER =", filt, "    GRATING =", grat)

    if force_filter_change:
        change_filter_opaque = True
    else:
        # get the switch in the configuration file
        if calwebb_spec2_pytests_dir is None:
            auxiliary_code_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
            calwebb_spec2_pytests_dir = auxiliary_code_dir.replace("/auxiliary_code", "")
        PPT_cfg_file = os.path.join(calwebb_spec2_pytests_dir, "PTT_config.cfg")
        print ("PPT_cfg_file=", PPT_cfg_file)
        with open(PPT_cfg_file, "r") as cfg:
            for line in cfg.readlines():
                if "#" not in line:
                    if "change_filter_opaque" in line:
                        change_filter_opaque = bool(line.split("=")[-1].replace("\n", ""))

    # Default value for the script to perform the filter change from science to OPAQUE
    filter2opaque_change = True

    if filt != "OPAQUE":
        is_filter_opaque = False
        print ("\n The filter was *NOT* set to OPAQUE for cal_detector1. ")

        # Exit the code when appropriate
        if change_filter_opaque:
            print (" The switch to change the filter is set to True, so the filter will be changed to OPAQUE.\n")
        else:
            print (" The switch to change the filter is set to False, so the filter will *NOT* be changed.\n")
            return is_filter_opaque, cal_detector1_output
        if not force_filter_change:
            if step is not None  and  step!="assign_wcs":
                return is_filter_opaque, cal_detector1_output

    else:
        print ("\n The filter was set to OPAQUE for cal_detector1. ")
        is_filter_opaque = True

        # Change the filter from OPAQUE to science
        filter2opaque_change = False

        # Exit the code when appropriate
        if change_filter_opaque:
            print (" The switch to change the filter is set to True, so the filter will be changed.\n")
        else:
            print (" The switch to change the filter is set to False, so the filter will *NOT* be changed.\n")
            return is_filter_opaque, cal_detector1_output
        if not force_filter_change:
            if step is not None  and  step!="assign_wcs":
                return is_filter_opaque, cal_detector1_output

    # make a copy of the file with the suffix _opaque
    file_dir = cal_detector1_output.replace(gain_scale_basename, "")

    if filter2opaque_change:
        opaque_gain_scale_basename = gain_scale_basename.replace(".fits", "_opaque.fits")
        opaque_gain_scale = os.path.join(file_dir, opaque_gain_scale_basename)
        subprocess.run(["cp", cal_detector1_output, opaque_gain_scale])
        fits.setval(opaque_gain_scale, "FILTER", 0, value="OPAQUE")
        is_filter_opaque = True
        new_input_file = opaque_gain_scale
    else:
        # change the filter keyword in the new file
        lamp = fits.getval(cal_detector1_output, "LAMP", 0)
        if 'LINE1' in lamp:
            filt = 'F100LP'
        elif 'LINE2' in lamp:
            filt = 'F170LP'
        elif 'LINE3' in lamp:
            filt = 'F290LP'
        elif 'LINE4' in lamp:
            filt = 'CLEAR'
        elif 'FLAT4' in lamp:
            filt = 'F070LP'
        elif 'REF' in lamp:
            filt = 'F100LP'
        print ("Since  LAMP =", lamp, "  =>  setting  FILTER =", filt)
        filt_gain_scale_basename = gain_scale_basename.replace(".fits", "_"+filt+".fits")
        filt_gain_scale = os.path.join(file_dir, filt_gain_scale_basename)
        subprocess.run(["cp", cal_detector1_output, filt_gain_scale])
        fits.setval(filt_gain_scale, "FILTER", 0, value=filt)
        is_filter_opaque = False
        new_input_file = filt_gain_scale

    return is_filter_opaque, new_input_file




if __name__ == '__main__':

    # Get arguments to run script
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("fits_file",
                        action='store',
                        default=None,
                        help='Name of fits file, i.e. blah.fits')
    args = parser.parse_args()

    # Set the variables
    fits_file = args.fits_file

    # Run the function
    is_filter_opaque, new_input_file = change_filter_opaque(fits_file, force_filter_change=True)

    """
    # This is a simple test of the code
    pipeline_path = "/Users/pena/Documents/PyCharmProjects/nirspec/pipeline"
    # input parameters that the script expects
    calwebb_spec2_pytests_dir = pipeline_path+"/src/nirspec_pipe_testing_tool/calwebb_spec2_pytests"
    data_dir = "/Users/pena/Documents/PyCharmProjects/nirspec/pipeline/build7.1/part1_JanuaryDeadline/IFU_CV3/G140M_F100LP/pipe_testing_files_and_reports/491_processing/opaque_test_Nadiasfix"
    cal_detector1_output = data_dir+"/gain_scale.fits"
    is_filter_opaque, new_input_file = change_filter_opaque(cal_detector1_output, calwebb_spec2_pytests_dir)
    """

    print (" * Script  change_filter_opaque2science.py  finished. * \n")


