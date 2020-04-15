# NIRSpec Pipe Testing Tool (we affectionately call it PTT)


## What is a Pytest

Simply put, a Pytest is a pass or fail Python test. For instance, with the WCS step, we 
have Python scripts (which we are calling auxiliary code within the frame of the testing 
tool) that compare the pipeline product with the ESA corresponding intermediary file, and 
calculates a difference. The Pytest is to assert if that difference is less than or equal 
to an X threshold value. Hence, a failed test means that the condition was not met. If an
error should occur with the pipeline, the test will be flagged as an error.



## Possible Outcomes of the Pytest

- Passed = the assertion was true, so the test condition was met.
- Failed = the assertion was false, the test condition was NOT met (there will be an
AssertionError on-screen and in the html file, with a clear PTT customized message of
what happened).
- Skipped = the test was skipped (there will be a message on the html report and on-screen
explaining why the test was skipped).
- Error = this is a coding error, a bug in either the pipeline or the PTT code. Please
contact the testing campaign lead to determine how to proceed.



## Useful links

- PTT Documentation:
https://innerspace.stsci.edu/pages/viewpage.action?pageId=123011558

- Testing data sets:
https://innerspace.stsci.edu/display/JWST/NIRSpec+Pipeline+Testing+Build+7.1+part+2

- SCSB GitHub repository: 
https://github.com/spacetelescope/jwst

- Pipeline Documentation:
http://jwst-pipeline.readthedocs.io

- Validation Notebooks
https://github.com/spacetelescope/jwst_validation_notebooks



## Quick Start Guide


NOTE: This guide assumes that Conda has been installed. If you have not yet done 
so, please follow the instructions at:
https://astroconda.readthedocs.io/en/latest/
Please use the latest python version (3.6 is the minimum supported)


THREE THINGS BEFORE STARTING

I.- You may want to clean your PYTHONPATH so that you do not get mysterious failures. To 
do this simply type the following command in the terminal:
```bash
unset PYTHONPATH
```
You can do this every time you run the pytests, or when you start getting strange 
failures. Another option is not to define PYTHONPATH at all in the .profile (or 
equivalent: .bashrc, .bash_profile, .cshrc, .login, etc.) file.

II.- If you work outside the internal network, i.e. in the visitors network or at home, 
you also want to set the following environment variables in the terminal or add them to 
your .profile (or equivalent) file:
```bash
export CRDS_SERVER_URL=https://jwst-crds.stsci.edu
export CRDS_PATH=${HOME}/crds_cache
```
These changes will not affect your work while working with the internal network at ST.

III.- A brief description of what each pipeline step does, as well as a brief description
of all the pytests implemented in the tool, the tests that are still in concept phase, and 
the tests that are still needed, can be found in the Confluence space for PTT. You can
get to it from the main page of NIRSpec/NIRSpec JWST Pipeline/NIRSpec Calibration
Pipeline Testing Tool (PTT), or by clicking in the following link:
https://confluence.stsci.edu/pages/viewpage.action?pageId=123011558


QUICK START GUIDE

1. Create the conda environment for testing and get the configuration files.  

a. Conda environment for this testing campaign:
- Current testing version and ulr file can be found at https://github.com/spacetelescope/jwst
under the "Installing a DMS Operational Build". The commands are similar to the following:
```bash
conda create -n jwst_b751 --file url_depending_on_your_system
```
for the current release candidate, the ulr options are:
- Linux: http://ssb.stsci.edu/releases/jwstdp/0.15.1/latest-linux
- OS X: http://ssb.stsci.edu/releases/jwstdp/0.15.1/latest-osx


The most stable release candidate will be listed in the top line under the section
"Software vs DMS build version map" at https://github.com/spacetelescope/jwst

NOTE FOR PIPELINE DEVELOPERS:

a. The development version of the pipeline was phased out. Currently, the installation is run
through ```pip```. SCSB recommends creating a new environment:
```bash
conda create -n jwst_env python
conda activate jwst_env
```
To install the corresponding build in this way you would type (with the activated environment):
```bash
pip install numpy
pip install git+https://github.com/spacetelescope/jwst#0.0.0
```
where #0.0.0 is the jwst version number, e.g. 0.15.1. For for installing the latest development version use:
```bash
pip install numpy
pip install git+https://github.com/spacetelescope/jwst
```

b. Configuration files corresponding to this build. Create a directory (e.g. 
```build_XX_cfg_files```) somewhere in your testing working space, and ```cd``` into it. Now 
type the following command within the conda environment you just created (see step 2).
```bash
collect_pipeline_cfgs .
```


2. Activate the conda environment for testing the pipeline, if you have not already done so, e.g. type:
```bash
source activate your_newly_created_environment
```
If the above command does not work try:
```bash
conda activate your_newly_created_environment
```
From here on, every step of this guide should happen within the conda testig environment.

NOTE: 

- If you forget what did you name your new environment type:
```bash
conda env list
```
this will list all environments you have created.

- If you want to remove an old testing environment type:
```bash
conda env remove -n name_of_your_old_environment
```


3. Install PTT. There are three ways to install the tool:

- Option A. For non-developers and without PTT source code. In the terminal type:
```bash
pip install git+https://github.com/spacetelescope/nirspec_pipe_testing_tool@master
```
This will install the latest version of PTT and all necessary dependencies to run the tool.
However, this will not install the pipeline, PTT will assume you already have installed the
pipeline version you need.

- Option B. For non-developers and with the PTT source code. After you clone PTT, go into
the directory, then type:
```bash
pip install .
```

- Option C. For developers and with the PTT source code. After you clone PTT, go into
the directory, then type the same command as with Option B with an additional ```-e``` flag
at the end of the command.

NOTE:  You can install the latest pipeline version, but this will replace any existing
version of the pipeline. Hence, you most likely want to create a new conda environment,
install PTT, and then type the command:
```bash
pip install -e ".[pipeline]"
```

NOTE: If you are considering to become a PTT code contributor please choose to fork the
repository rather than cloning it.


IF YOU WANT THE SOURCE CODE

Clone or fork the PTT repository. If you are planing to contribute with code to PTT, fork
the repo, otherwise choose to clone it. To do this click at the top right of this page,
in the dropdown button that says clone or download, then copy the ulr that appears there.
Now, within the conda testing environment, go to or create the directory where you want
the PTT to "live" in. However, make sure that the configuration files directory is, at
least, at the top level of the directory tree where the PTT will live, e.g. the
```b713cfg_files``` directory and the ```nirspec_pipe_testing_tool``` directory can be at
the same level, but the ```b713cfg_files``` directory cannot be inside the
```nirspec_pipe_testing_tool``` directory because the .cfg files will be picked up by Git,
and will be recognized as changes to the repo. Remember you are in the GitHub repository
page so go all the way to the top of the page, click on the green button and copy the ulr
that appears there.
```bash
git clone the_ulr_you_copied
```
After this is done, you should see a full copy of the PTT in your directory.

NOTE: 
- If you have already cloned or forked the repository, in the terminal go to where you placed
the ```nirspec_pipe_testing_tool``` directory. Then, use the following command to update 
the code:
```git pull```
- If, however, you had written script(s) in the tool's directory tree, git will not let 
you continue until you move the script(s) to another directory. 


4. Prepare the data to run through the pipeline. To do this:

a. Copy the test data you will use from the NIRSpec vault directory. Go to the directory 
where you want to have the testing data, and from there type:
```bash
cp -r /grp/jwst/wit4/nirspec_vault/prelaunch_data/testing_sets/b7.1_pipeline_testing/test_data_suite/the_data_you_want_to_copy .
```

NOTE:
You can start with the FS benchmark data to make sure you are doing the right thing. To 
get the data go to 
```bash
/grp/jwst/wit4/nirspec_vault/pipe_testing_tool/PTT_FS_benchmark_run
```
There you will find a FS raw file, a ```PTT_config.cfg``` file, and a directory called
```results_491```, which contains all the intermediary fits products obtained from running
```calwebb_detector1```, the output text files from running the corresponding script 
(which include the ```cal_detector1_outputs_and_times_DETECTOR.txt``` and the added 
keywords to the ```_uncal``` file), the all the intermediary fits products obtained from 
running ```calwebb_spec2```, and all the plots created with the PTT. You can use the
```PTT_config.cfg``` (changing the paths appropriately) in there to make sure you
obtain the same results from the PTT run. Alternatively, you can create your
```PTT_config.cfg``` by running the described in step 5 of this guide.


b. In the directory where you copied the test data, you will need to run a script PER
fits file you want to test. Do not worry, this will only be done once. This script will
create a new subdirectory with the necessary input file to run the SSB script 
that converts raw data into uncal type files. You can choose to either keep this 
subdirectory, or tell the script to remove it after the operation is done. In the 
terminal type:
```bash
nptt_prepare_data2run fits_file.fits MODE -u
```
where the MODE is expected to be one of: FS, MOS, IFU, BOTS, dark, image, confirm,
taconfirm, wata, msata, focus, mimf, or MOS_sim (use this last one only for MOS
simulations, simulations for other modes should use the corresponding mode). This command
will update the uncal keyword header without creating a new file, and will also keep the
subdirectory. To remove it, simply add ```-rm``` at the end. To save the keyword changes
in a new fits file (instead of updating), remove the ```-u```. The new uncal fits file
is now ready for pipeline ingest.

This module can also be called from a script in the following way:
```bash
# import the tool
import nirspec_pipe_testing_tool as nptt

# set the variables
fits_file = 'blah.fits'
mode = 'FS'
rm_prep_data = True
only_update = True

# run the module
nptt.utils.prepare_data2run.prep_data2run(fits_file, mode, rm_prep_data, only_update)
```

c. Optional. Check the file header. If you want to see the header of any file, you can
use the another script in the ```utils``` directory of the PTT. If you just want to see
on-screen the header, go where your fits file "lives" and type:
```bash
nptt_read_hdr fits_file.fits -s
```
This command will show the main header. To save the header to a text file add a ```-s``` 
at the end. If you want to see/save a different extension add at the end ```-e=1``` for 
extension 1, and so on.

This module can also be called from a script in the following way:
```bash
# set the variables
fits_file = 'blah.fits'
save_txt = True
ext_number = 1

# run the module
nptt.utils.read_hdr.read_hdr(fits_file_name, save_txt, ext_number)
```


d. Now, the data is ready to be ran through cal_detector1. Please go ahead with the next
step of this guide to do that.


5. Set the PTT configuration file. This is the file that controls all the input that
the tool needs. To create ```PTT_config.cfg```, run the following command:
```bash
nptt_mk_pttconfig_file output_directory input_file mode_used raw_data_root_file
```
where ```output_directory``` is the path where you want to save all the PTT outputs and
pipeline products, ```input_file``` is the basename of the count rate file (e.g. the
final product of ```calwebb_detector1```), ```mode_used``` is the instrument mode used
(e.g. FS), and ```raw_data_root_file``` is the basename of the raw data file used to
create the uncal input file for ```calwebb_detector1```.

As an additional check, you can open the file and see if:
- All the paths point to the right places. The files can be located anywhere, but both,
the pipeline and the tool, will run faster if the files are local on your computer.
- The input file for the PTT is the final output file from ```calwebb_detector1```.
- The adequate mode for the data to be tested is set correctly, choices are: FS, IFU,
MOS, BOTS, dark, or MOS_sim.
- The variable ```change_filter_opaque``` should be set to False unless you want to change
the FILTER keyword back to OPAQUE.
- The variable ```raw_data_root_file``` should be the name of the raw file you downloaded
from the NIRSpec vault; for ground observations it starts with NRS. If you are running 
simulations then you can look into the ```ESA_Int_products``` directory and see what is
the name of the directory that corresponds to your data, copy that name and add .fits to
the end, e.g. for my simulation file ```F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1.fits```
go into ```/grp/jwst/wit4/nirspec_vault/prelaunch_data/testing_sets/b7.1_pipeline_testing/test_data_suite/simulations/ESA_Int_products```,
then set ```raw_data_root_file = F170LP-G235M_MOS_observation-6-c0e0_001.fits```
- The steps that you want to be ran or not are set to True or False.
- In the bottom part of the file, all the additional arguments for the PTT are 
correct, e.g. threshold values, figure switches, and additional fits files.


6. Run the ```calwebb_detector1``` pipeline. The final output of this is the level 2 data
required to run the PTT. In a terminal, please make sure that the testing conda environment
is active, and that you are in the directory where your ```PTT_config.cfg``` lives. Type
the following command:
```bash
nptt_run_cal_detector1 /path_where_the_uncal_file_lives/uncal_file.fits
```
This command runs the the calwebb detector 1 pipeline in a single run, and will create the
log file ```caldetector1_pipeline_DETECTOR.log```. This file will be used to determine
the times that each step took to run.

To run calwebb detector 1 step-by-step, simply add ```-sbs``` flag at the end of
the previous command. Note that running the pipeline in full for calwebb detector 1 takes 
about half the time as it does running it step-by-step, due to IO processing time.

This module can also be called from a script in the following way:
```bash
# set the variables
fits_input_uncal_file = 'blah.fits'
step_by_step = False

# run the module
nptt.utils.run_cal_detector1.run_caldet1(fits_input_uncal_file, step_by_step)
```

If everything went well, you will see a text file called
```cal_detector1_outputs_and_times_DETECTOR.txt```, which contains the steps ran, the 
name of the output fits file, and the time each step took to run. This text file, along 
with the intermediary products will be located in the path you set for the 
```output_directory``` variable in the configuration file of the PTT.

NOTE ON ```calwebb_detector1``` ERRORS:
- If you were not able to get the file to run though cal detector1 due to an error saying 
that the pipeline was not able to find a best reference for dark or superbias, it is 
possible this is due to the filter keyword in the main header set to OPAQUE.
- In this case, you can run the module ```change_filter_opaque2science``` by typing:
```bash
nptt_change_filter_opaque2science file.fits
```

This module can also be called from a script in the following way:
```bash
# set the variables
fits_file = 'blah.fits'
force_filter_change = True

# run the module
is_filter_opaque, new_input_file = nptt.calwebb_spec2_pytests.auxiliary_code.change_filter_opaque2science.change_filter_opaque(fits_file, force_filter_change)

# change_filter2opaque -> boolean, True if the filter was changed
# new_input_file -> string, file with updated filter
```

If all went well and you have a ```final_output_caldet1_DETECTOR.fits``` file, where
```DETECTOR``` can be either ```NRS1``` or ```NRS2```. The calwebb detector 1 pipeline
is currently being tested through unit tests and regression tests that run automatically
when the developers test the entire pipeline. Hence, PTT does not contain any tests for
the calwebb detector 1 pipeline.


*****

NOTE FOR SIMULATIONS:

If you are working with simulations you may need to convert the count rate map to an STScI
pipeline-ingestible file (with all the keyword header modifications). In order to do this
run the module ```crm2STpipeline```:
To run this type:
```bash
nptt_crm2STpipeline file.fits MODE -r -p -t -n
```
where ```MODE``` is FS, MOS, IFU, BOTS, or dark. The input file for this module generally
has a ```.crm``` or ```.cts``` suffix. The output files of this script can be directly
ingested into the cal_spec2 pipeline, no need to run cal_dedector1. The flag ```-r```
is used only for IFU data, when needing to add the reference pixels. The other three
flags are to modify the keyword values to match IPS information: the flag ```-p``` is
to modify the proposal title header keyword, the ```-t``` flag is to modify the target
name header keyword, and the ```-n``` flag is to create a new file with updated header.

This module can also be called from a script in the following way:
```bash
# set the variables
input_fits_file = 'blah.fits'
mode = 'FS'
add_ref_pix = True
only_update = True
proposal_title = 'my_title'
target_name = 'my_target'
new_file = 'a_new_name'  # this is only used if only_update=False

# create the pipeline-ready count rate file
stsci_pipe_ready_file = nptt.utils.crm2STpipeline.crm2pipe(input_fits_file, mode_used, add_ref_pix, only_update)

# create the dictionary of special arguments
additional_args_dict = {'TITLE': proposal_title, 'TARGNAME': target_name, 'new_file': new_file}

# modify the keyword values to match IPS information
nptt.utils.level2b_hdr_keywd_dict_map2sim.match_IPS_keywords(stsci_pipe_ready_file, input_fits_file,
                                                             additional_args_dict=additional_args_dict)
```

*****
*****

NOTE FOR MOS DATA:

If you are working with MOS data, you may need to create the shutter configuration file to be able
to process the data through  the ```cal_spec2``` stage. To create the shutter configuration file
you need the ```.msa.fits``` files from APT, or for simulations, you need the nod ```.csv```
files. Once you have those files you can use the module ```create_metafile``` for MOS data,
simulations, or to fix an old shutter configuration file (to update from format of build 7.3).

Use this command to create a new shutter configuration file:
```bash
nptt_create_metafile /path_to_file/blah.msa.fits
```

To fix an old shutter configuration file use:
```bash
nptt_create_metafile /path_to_file/blah_metafile_msa.fits -f
```

To create new shutter configuration file for simulations and/or dithers:
```bash
nptt_create_metafile /path_to_file/blah.msa.fits -d=obs1.csv,obs2.csv,obs3.csv
```
Note that for the simulations, the nod files are in a list separated by commas without spaces.

In all cases the module ```create_metafile``` will output a file called
```blah_metafile_msa.fits```.

This module can also be called from a script in the following way:
```bash
# to create a shutter configuration file for the pipeline
config_binary_file = 'CB10-GD-B.msa.fits'
fix_old_config_file = False
targ_file_list = 'obs1.csv, obs1.csv'   # list of dither files

# to fix an old shutter configuration file for the pipeline
config_binary_file = 'V9621500100101_metafile_msa.fits'
fix_old_config_file = True
targ_file_list = False

# run the module
nptt.calwebb_spec2_pytests.auxiliary_code.create_metafile.run_create_metafile(config_binary_file,
                                                                              fix_old_config_file,
                                                                              targ_file_list)
```


*****

7. Fix the pointing keywords in the count rate file. This will only be possible if you have the
APT file that corresponds to your testing data. Skip this step if you do not have the
corresponding APT file for your data set. PTT used default dummy values so the pipeline will
not break, but the spec3 pipeline may get wrong results unless these dummy values are replaced.

If you do have the corresponding APT files for your data set, you will manually need to get
the following information from the APT file: the target's RA, DEC, V2, and V3, as well as
the aperture position angle. Sample values for these quantities are: ra_targ = 53.16199112,
dec_targ = -27.79127312,  v2_targ = 393.86285, v3_targ = -424.00329, and aper_angle = 45.0.
To fix the keywords use the following command from the terminal:
```bash
nptt_fix_pointing blah.fits 53.16199112, -27.79127312, 393.86285, -424.00329, 45.0
```

If the data is IFU add the flag -ifu at the end of the command. The output will be the
updated file.

To create a new updated file add flag -nf to the above command. 

This module can also be called from a script in the following way:
```bash
# set the variables
input_fits_file = 'blah.fits'
ra_targ = 53.16199112
dec_targ = -27.79127312
v2_targ = 393.86285
v3_targ = -424.00329
aper_angle = 45.0
ifu_used = True

# run the module
nptt.utils.fix_pointing.fix_header_pointing(input_file, ra_targ, dec_targ, v2_targ, v3_targ, apa, ifu=ifu_used)
```

8. Optional. Test to run PTT. To ensure that everything is in order, and to see what pytests
will be executed and in which order, in the terminal type go to the top level directory where
PTT lives, then type:
```bash
cd nirspec_pipe_testing_tool/calwebb_spec2_pytests
pytest --collect-only
```


9. Do the first PTT run. Go back to the output directory. As an output of the testing tool
you will see an html file, called ```report.html```, and an intermediary product text file
name map will appear. The output fits files of intermediary products will also be saved in
the output directory. In the terminal type:
```bash
nptt_run_PTT name_of_the_html_report PTT_config.cfg
```

This module can also be called from a script in the following way:
```bash
# set the variables
report_name = 'my_report'

# run the module
nptt.utils.run_PTT.run_PTT(report_name, PTT_config.cfg)
```


TO RUN A SINGLE PIPELINE STEP: 

-> If you are running a single pipeline step (or only the corresponding pytest), PTT will
create a log file specifically named with the step you are studying. At the end of the 
run you will see 2 log files, one from the pipeline and one from PTT. This will not 
overwrite the full pipeline run log files.

TO RUN A FEW PIPELINE STEPS: 

-> To only run a few pipeline steps you need to:
a) Make sure that the variable ```run_calwebb_spec2``` in the ```PTT_config.cfg``` file
is set to False (otherwise the pipeline will run in full and we have no control of
individual steps).
b) Turn off (i.e. set to False) the steps you do not want to run in the ```PTT_config.cfg``` 
file, which are located in the section ```run_pipe_steps``` of the file.

TO RUN A FEW PYTEST: 

-> To run a few pytest you need to select which pytest to run (i.e. set to True) in the 
```PTT_config.cfg``` file, which are located in the section ```run_pytest``` of the file.

-> To only run pytest and skip running the pipeline entirely:
a) Make sure that the variable ```run_calwebb_spec2``` in the ```PTT_config.cfg``` file
is set to False.
b) Set to False all the pipeline steps in the ```PTT_config.cfg``` file. The steps are 
located in the section ```run_pipe_steps``` of the file.
c) Set to True all pytest you want to run in the ```PTT_config.cfg``` file. These are 
located in the section ```run_pytest``` of the file.


10. Report your findings. Contact the testing lead to determine if you should create a
report Jira ticket per step. If this is the case, you will need to link the ticket to any
corresponding bug or problem found (each bug or issue should have its own Jira bug
issue). In the ticket you can link to either the validation notebook or the corresponding
web page of this repo, and remember to add the following information to the Jira report
ticket:
- Version of the pipeline tested
- Description of the test performed
- Link to code used
- What data set was used
- Result


## TO KEEP IN MIND

- A text file containing an intermediary product name map will be created in the pytests 
directory.
- If any of the central store directory calls do not respond (e.g. when looking at the 
flats), the pytest will be skipped even if the step is set to True in the config file. 
The failing message will say that the step was set to False (this is a known bug). To 
force the tests run, you will have to download the files the tool is calling, and change 
the corresponding paths in the configuration file.
- The output in the terminal can be a bit overwhelming if there was a failed test or an 
error, since it shows both, the pipeline messages and the PTT messages. In the html 
report is much clearer to understand what happened.
- As part of the testing campaign, it is important that you run the pipeline from the 
command line as well, and that you make sure that the outcome intermediary files are 
consistent with the ones ran with scripts, i.e. the PTT. This sanity check is minor 
but important to verify. If you have the PTT source code, you will find two very
 useful text files in the ```utils/data``` directory. The two text files are named
```terminal_commands_calwebb_detector1_steps.txt``` and
```terminal_commands_calwebb_spec2_steps.txt```. These files contain all the commands 
you can use from the terminal to run the calwebb_detector1 and calwebb spec2 steps,
respectively.
- Finally, remember that:

a. Whenever you need to read either the main or science headers of a file,
you can always use the ```nptt_read_hdr``` module.

b. If you need to change/add a keyword value to a specific extension of a file, you can
use the ```nptt_change_keywd``` module.



## ADDING TESTING ROUTINES

Talk to the testing lead to determine if the test you have in mind should be a script or
a Jupyter Notebook (link to validation Notebooks at the top of this page).

To add additional testing routines you will need to have forked the PTT repository. The
tests have to be written in python 3.6 or greater.



## Enjoy your pipeline testing!

