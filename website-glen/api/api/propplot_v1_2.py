########################################################################################################################
#                                                                                                                      #
#   Author: Pascal Schläpfer, ETH Zürich, December 8th 2020                                                            #
#   See below for function description                                                                                 #
#                                                                                                                      #
#   Acknowledgements:                                                                                                  #
#     Dr. R. Glen Uhrig                                                                                                #
#     Dr. Devang Mehta                                                                                                 #
#     Cameron Ridderikhoff                                                                                             #
#                                                                                                                      #
########################################################################################################################


# Check if required modules are installed

# test if sys is installed in python
try:
    import sys
except ImportError:
    print('Error, module sys is required.')
    exit()
import sys

# test if shutil is installed in python
try:
    import shutil
except ImportError:
    print('Error, module shutil is required.')
    sys.exit()

# test if distutils is installed in python
try:
    from distutils.dir_util import copy_tree
except ImportError:
    print('Error, module distutils is required.')
    sys.exit()

# test if re is installed in python
try:
    import re
except ImportError:
    print('Error, module re is required.')
    sys.exit()

# test if os is installed in python
try:
    from os import listdir
except ImportError:
    print('Error, module os is required.')
    sys.exit()
try:
    from os.path import isfile, join, isdir
except ImportError:
    print('Error, module os is required.')
    sys.exit()

# test if pandas is installed in python
try:
    import pandas as pd
except ImportError:
    print('Error, module pandas is required.')
    sys.exit()

# test if statistics is installed in python
try:
    from statistics import median
except ImportError:
    print('Error, module statistics is required.')
    sys.exit()

# test if json is installed in python
try:
    import json
except ImportError:
    print('Error, module json is required.')
    sys.exit()

# test if numpy is installed in python
try:
    import numpy as np
except ImportError:
    print('Error, module numpy is required.')
    sys.exit()

# test if matplotlib is installed in python
try:
    import matplotlib
except ImportError:
    print('Error, module matplotlib is required.')
    sys.exit()
matplotlib.use('Agg')  # This is to avoid issues when running the script and producing pdfs when being connected to
# server over ssh.

# test if matplotlib is installed in python
try:
    import matplotlib.pyplot as plt
except ImportError:
    print('Error, module matplotlib is required.')
    sys.exit()

try:
    from matplotlib.patches import Polygon
except ImportError:
    print('Error, module matplotlib is required.')
    sys.exit()

# test if mpl_toolkits is installed in python
try:
    from mpl_toolkits.axes_grid1 import Divider, Size
except ImportError:
    print('Error, module mpl_toolkits is required.')
    sys.exit()
try:
    from mpl_toolkits.axes_grid1.mpl_axes import Axes
except ImportError:
    print('Error, module mpl_toolkits is required.')
    sys.exit()

# test if pathlib is installed in python
try:
    import pathlib
except ImportError:
    print('Error, module pathlib is required.')
    sys.exit()

# test if Bio is installed in python
try:
    import Bio.ExPASy.ScanProsite
except ImportError:
    print('Error, module Bio is required.')
    sys.exit()

# test if urllib is installed in python
try:
    import urllib
except ImportError:
    print('Error, module urllib is required.')
    sys.exit()

# test if urllib is installed in python
try:
    from urllib.error import HTTPError
except ImportError:
    print('Error, module urllib is required.')
    sys.exit()

# test if math is installed in python
try:
    import math
except ImportError:
    print('Error, module math is required.')
    sys.exit()

# test if time is installed in python
try:
    import time
except ImportError:
    print('Error, module time is required.')
    sys.exit()


# test if datetime is installed in python
try:
    from datetime import date
except ImportError:
    print('Error, module datetime is required.')
    sys.exit()


########################################################################################################################
#                                                                                                                      #
#  f_process_results                                                                                                   #
#  Main function of propplot.py. See help for further information                                                      #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vinputfile [string]: Indicates the location of the input fasta file.                                            #
#    - vignoredb [string] gets converted into True/False: Indicates whether previously gained results should be        #
#                                                         ignored                                                      #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vdbfolder [string]: Indicates the location of the folder where the databases of previous results should be      #
#                          built up.                                                                                   #
#    - vgroupfile [string]: Indicates the location of a tsv file that contains the information about associations of   #
#                           proteins to their protein groups. First column is fasta headers second column are user     #
#                           defined group names.                                                                       #
#    - vcolorfile [string]: Indicates the location of a tsv file that contains the information about domain coloring.  #
#                           First column is the domain name, second column is a hex code for the color                 #
#    - vignoredomainfile [string]: Indicates a file, with domains as rows. If a domain shows up in this file, it is    #
#                                  not displayed on plots.                                                             #
#    - vcutoff [string] gets converted into float: Defines if a domain should be displayed for a group of proteins.    #
#                                                  Only if the domain surpasses the cutoff in relative abundance, it   #
#                                                  is displayed.                                                       #
#    - vmaxcutoff [string] gets converted into float: Same as vcutoff, however, before the domain could exist anywhere #
#                                                     in the protein. Here the domains need to be present at the same  #
#                                                     location to make the cut.                                        #
#    - vcustom_scaling_on [string] gets converted into boolean: Allows for custom scaling of the figure. The standard  #
#                                                               case is that this is not on, and thus the scaling is   #
#                                                               the same regardless of the size of the protein. If     #
#                                                               this is on, one can set with option api (default 100   #
#                                                               amino acids per inch) the number of amino acids        #
#                                                               displayed per inch to scale the width of the figure.   #
#    - vscalingfigure [string] gets converted into float: Indicates the number of amino acids per inch that are        #
#                                                         displayed per inch of x-axis.                                #
#    - vabsolute [string] gets converted into True/False: Indicates whether absolute numbers are displayed on the      #
#                                                         y-axis.                                                      #
#    - vwarnings [string] gets converted into True/False: Indicates whether warnings are written out.                  #
#    - vfrom_scratch [0 or 1] gets converted into True/False: Indicates whether previous results should be discarded.  #
#    - vnotolderthan [string] gets converted into int: Indicates the date that should be used as cutoff to load data   #
#                                                      from databases. If the storing date is older than the date      #
#                                                      given, the data is not observed.                                #
#                                                                                                                      #
#  Optional arguments:                                                                                                 #
#    - none                                                                                                            #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - jobid_proteingroup_prosite.pdf [file]: Pdf plot for Prosite domains relative to the median length of amino acid #
#                                              sequence of all proteins in the protein group.                          #
#    - jobid_proteingroup_pfam.pdf [file]: Pdf plot as above, but for PFAM domains.                                    #
#    - jobid_proteingroup_combined.pdf [file]: Pdf plot for Prosite and PFAM domains.                                  #
#    - proteingroup_prosite_colors.txt [file]: Tsv of the domains and colors used in the plot. Can be modified and     #
#                                              funneled back into the script to modify colors. See vcolorfile for      #
#                                              structure.                                                              #
#    - proteingroup_pfam_colors.txt [file]: Same file as above, but for pfam plot.                                     #
#    - proteingroup_combined_colors.txt [file]: Same file as above, but for combined plot.                             #
#    - jobid_proteingroup_prosite.csv [file]: Results of Prosite for protein group.                                    #
#    - jobid_proteingroup_pfam.csv [file]: Results of PFAM for protein group.                                          #
#    - jobid_prosite_res.tsv [file]: Results of Prosite for this job.                                                  #
#    - jobid_pfam_res.tsv [file]: Results of PFAM for this job.                                                        #
#    - Prosite_db_[first five amino acids of sequence] [file]: TSV database files for sequences run through Prosite.   #
#    - Pfam_db_[first five amino acids of sequence] [file]: TSV database files for sequences run through PFAM.         #
#                                                                                                                      #
########################################################################################################################


# noinspection PyTypeChecker
def f_run_propplot(vjobid, vinputfile, vignoredb, vsavefolder, vdbfolder, vgroupfile, vcolorfile, vignoredomainfile,
                   vcutoff, vmaxcutoff, vcustom_scaling_on, vscalingfigure, vabsolute, vwarnings, vfrom_scratch,
                   vnotolderthan):
    # Write initial cookie
    f_write_cookie(0, vsavefolder, vjobid, 'Job initialized')

    # Constants:
    # For plotting:
    vstandardwidth = 7
    vstandardheight = 4.49
    vpaddingwidth = 1.0
    vpaddingheight = 0.7
    vfontsize = 10
    vcurrentdate = int(re.sub('-', '', str(date.fromtimestamp(time.time()))))
    
    # Write initial job:
    f_write_log(vsavefolder, vjobid, 'Job initialized with following parameters\nJobid: ' + vjobid + '\nInputfile: ' +
                vinputfile + '\nIgnoredb: ' + vignoredb + '\nSavefolder: ' + vsavefolder + '\nDbfolder: ' + vdbfolder +
                '\nGroupfile: ' + vgroupfile + '\nColorfile: ' + vcolorfile + '\nIgnoredomainfile: ' +
                vignoredomainfile + '\nCutoff: ' + vcutoff + '\nMaxcutoff: ' + vmaxcutoff + '\nCustomscaling: ' +
                vcustom_scaling_on + '\nScalingfigure: ' + vscalingfigure + '\nAbsolute: ' + vabsolute +
                '\nWarnings: ' + vwarnings + '\nFrom_scratch: ' + vfrom_scratch + '\nNotolderthan: ' + vnotolderthan +
                '\n\n', 'w')

    # Modify parameters
    f_write_log(vsavefolder, vjobid, 'Modifying parameters: ', 'a')
    if vignoredb == '0':
        vignoredb = False
    elif vignoredb == '1':
        vignoredb = True
    else:
        vignoredb = False
    vcutoff = float(vcutoff)
    vmaxcutoff = float(vmaxcutoff)
    if vcustom_scaling_on == '0':
        vcustom_scaling_on = False
    elif vcustom_scaling_on == '1':
        vcustom_scaling_on = True
    else:
        vcustom_scaling_on = False
    vscalingfigure = float(vscalingfigure)
    if vabsolute == '0':
        vabsolute = False
    elif vabsolute == '1':
        vabsolute = True
    else:
        vabsolute = False
    if vwarnings == '0':
        vwarnings = False
    elif vwarnings == '1':
        vwarnings = True
    else:
        vwarnings = False
    if vfrom_scratch == '0':
        vfrom_scratch = False
    elif vfrom_scratch == '1':
        vfrom_scratch = True
    else:
        vfrom_scratch = False
    vnotolderthan = int(vnotolderthan)
    f_success(vsavefolder, vjobid)

    # Additional internal constants
    f_write_log(vsavefolder, vjobid, 'Add internal constants parameters: ', 'a')
    vlen_dbid = 5  # Length of db names (defines how many different db files are made.)
    f_success(vsavefolder, vjobid)

    # Read in headers and sequences that were used to produce the prosite and or pfam results
    f_write_log(vsavefolder, vjobid, 'Reading in fasta file:\n', 'a')
    vheaders, vsequences = f_read_in_file(vinputfile, vsavefolder, vjobid)
    if vwarnings:
        print('Headers: ' + str(len(vheaders)) + ', Sequences: ' + str(len(vsequences)))
    f_write_log(vsavefolder, vjobid, 'Fasta file read in successfully.\n', 'a')

    # Write first cookie
    f_write_cookie(1, vsavefolder, vjobid, 'Input file successfully read')

    # Get Prosite results
    f_write_log(vsavefolder, vjobid, 'Gathering prosite domains:\n', 'a')
    vprositefile = join(vsavefolder, vjobid + '_prosite_res.tsv')

    # Check if Prosite results have been produced that can be loaded.
    f_write_log(vsavefolder, vjobid, 'Check if prosite domain results file exists: ', 'a')
    try:
        vfh_colors = open(vprositefile, 'r')
        vprosite_already_done = True
        vfh_colors.close()
        f_success(vsavefolder, vjobid)
    except IOError:
        vprosite_already_done = False
        f_no(vsavefolder, vjobid)

    # Check if results should be run from scratch
    if vfrom_scratch:
        f_write_log(vsavefolder, vjobid, 'All results for Prosite will be run from scratch (no dbs, no previous '
                                         'saves).\n', 'a')
        vprosite_already_done = False

    # Getting results from Prosite
    if not vprosite_already_done:
        f_write_log(vsavefolder, vjobid, 'Create new Prosite output file: ', 'a')
        vfh_prosite_output = open(vprositefile, 'w')  # Emptying the prosite output file.
        vfh_prosite_output.close()
        f_success(vsavefolder, vjobid)

        # Defining storing places of dbs
        if vdbfolder == '':
            vdbfiles = 'Prosite_db'
        else:
            vdbfiles = join(vdbfolder, 'Prosite_db')
        f_write_log(vsavefolder, vjobid, 'Prosite DB files stored at: ' + vdbfiles + '\n', 'a')

        # Process every header
        for vheader_id, vheader in enumerate(vheaders):
            if vwarnings:
                print('Searching header ' + str(vheader_id + 1) + ' of ' + str(len(vheaders)) + '.')
            f_write_log(vsavefolder, vjobid, 'Processing header: ' + vheader + '\n', 'a')
            vfound = False  # Defines if the header was found in the db
            vdbid = vsequences[vheader_id][0:vlen_dbid]  # Defines the db file that should be searched.
            if not vignoredb:  # If the db should be searched.
                f_write_log(vsavefolder, vjobid, 'Searching in Prosite DB ' + vdbid + ': ', 'a')
                try:  # Check if db exists.
                    vfh_db_prosite = open(vdbfiles + '_' + vdbid, 'r')  # Open db.
                    f_write_log(vsavefolder, vjobid, 'exists\n', 'a')
                    for ventry in vfh_db_prosite:  # Go through all entries of db.
                        ventry = ventry.rstrip('\n')  # Get rid of new line character at the end.
                        vsplitentry = ventry.split('\t')  # Split record into its attributes.
                        if int(vsplitentry[0]) >= vnotolderthan:  # Check if the entry is young enough.
                            if vsequences[vheader_id] == vsplitentry[1]:  # check if first attribute is sequence of
                                # interest.
                                vfound = True  # if it is, say that the sequence was found in the db.
                                f_write_log(vsavefolder, vjobid, 'Found entry in DB ' + vdbid + '\n', 'a')
                                f_write_pfam_prosite_res(vprositefile, vheader, vsplitentry[1:], False, True,
                                                         vsavefolder, vjobid)  # Write the record to the
                                # output file.
                    vfh_db_prosite.close()
                except IOError:  # If the db can not be read, it likely does not exist.
                    f_write_log(vsavefolder, vjobid, 'does not yet exist\n', 'a')
                    if vwarnings:
                        print(vdbfiles + '_' + vdbid + ' does not yet exist.')

            if not vfound:  # If the sequence has not been found in a db.
                f_write_log(vsavefolder, vjobid, 'Sending sequence to Prosite\n', 'a')
                ventry_found = f_run_sequences_through_prosite(vheader, vsequences[vheader_id], vsavefolder, vjobid,
                                                               vwarnings)
                # Search for the sequence in prosite.
                f_write_pfam_prosite_db(vdbfiles, vdbid, ventry_found, vsavefolder, vjobid, vcurrentdate)  # Write
                # the results into the db.
                f_write_pfam_prosite_res(vprositefile, vheader, ventry_found, False, False, vsavefolder, vjobid)
                # Write the results into the results file.
            # Update cookies
            vcid = math.floor((vheader_id + 1) / len(vheaders) * 100 / 5) + 1
            if vcid > 1:
                f_write_cookie(vcid, vsavefolder, vjobid, '')

    vprositedata = f_read_tsv(vprositefile, vsavefolder, vjobid)  # Read the data of prosite from the result file.
    f_write_log(vsavefolder, vjobid, 'Successfully gathered Prosite domain results.\n', 'a')
    f_write_cookie(22, vsavefolder, vjobid, 'Finished searching Prosite')

    # Get PFAM results
    f_write_log(vsavefolder, vjobid, 'Gathering PFAM domains:\n', 'a')
    vpfamfile = join(vsavefolder, vjobid + '_pfam_res.tsv')

    # Check if PFAM results have been produced that can be loaded.
    f_write_log(vsavefolder, vjobid, 'Check if PFAM domain results file exists: ', 'a')
    try:
        vfh_colors = open(vpfamfile, 'r')
        vpfam_already_done = True
        vfh_colors.close()
        f_success(vsavefolder, vjobid)
    except IOError:
        vpfam_already_done = False
        f_no(vsavefolder, vjobid)

    # Check if results should be run from scratch
    if vfrom_scratch:
        f_write_log(vsavefolder, vjobid, 'All results for PFAM will be run from scratch (no dbs, no previous '
                                         'saves).\n', 'a')
        vpfam_already_done = False

    # Getting results from PFAM (see above Prosite for reference. Only commenting when different.)
    if not vpfam_already_done:
        f_write_log(vsavefolder, vjobid, 'Create new PFAM output file: ', 'a')
        vfh_pfam_output = open(vpfamfile, 'w')  # writing the header of the pfam result file.
        # vfh_pfam_output.write('Sequence id\tFamily id\tFamily Accession\tClan\tEnv. Start\tEnv. End\tAli. Start\t'
        #                      'Ali. End\tModel Start\tModel End\tBit Score\tInd. E-value\tCond. E-value\tDescription\t'
        #                      'aliIdCount\taliL\taliM\taliN\taliSim\taliSimCount\taliaseq\talicsline\talihindex\t'
        #                      'alimline\talimmline\talimodel\talintseq\talippline\talirfline\talisqacc\talisqdesc\t'
        #                      'alisqfrom\talisqname\talisqto\tbias\tdisplay\tis_included\tis_reported\toasc\t'
        #                      'outcompeted\tsignificant\tuniq\n')
        vfh_pfam_output.write('Sequence id\tFamily id\tFamily Accession\tClan\tEnv. Start\tEnv. End\tAli. Start\t'
                              'Ali. End\tModel Start\tModel End\tBit Score\tInd. E-value\tCond. E-value\tDescription\t'
                              'outcompeted\tsignificant\tuniq\n')
        vfh_pfam_output.close()

        # Defining storing places of dbs
        if vdbfolder == '':
            vdbfiles = 'PFAM_db'
        else:
            vdbfiles = join(vdbfolder, 'PFAM_db')
        f_write_log(vsavefolder, vjobid, 'PFAM DB files stored at: ' + vdbfiles + '\n', 'a')

        # Process every header
        for vheader_id, vheader in enumerate(vheaders):
            if vwarnings:
                print('Searching header ' + str(vheader_id + 1) + ' of ' + str(len(vheaders)) + '.')
            f_write_log(vsavefolder, vjobid, 'Processing header: ' + vheader + '\n', 'a')
            vfound = False
            vdbid = vsequences[vheader_id][0:vlen_dbid]
            if not vignoredb:
                f_write_log(vsavefolder, vjobid, 'Searching in PFAM DB ' + vdbid + ': ', 'a')
                try:
                    vfh_db_pfam = open(vdbfiles + '_' + vdbid, 'r')
                    f_write_log(vsavefolder, vjobid, 'exists\n', 'a')
                    for ventry in vfh_db_pfam:
                        ventry = ventry.rstrip('\n')
                        vsplitentry = ventry.split('\t')
                        if int(vsplitentry[0]) >= vnotolderthan:  # Check if the entry is young enough.
                            if vsequences[vheader_id] == vsplitentry[1]:  # check if first attribute is sequence of
                                # interest.
                                vfound = True
                                f_write_log(vsavefolder, vjobid, 'Found entry in DB ' + vdbid + '\n', 'a')
                                if vsplitentry[len(vsplitentry) - 1 - 1] == '1':  # Checks if result was significant.
                                    # and vsplitentry[len(vsplitentry) - 1 - 2] == '0':  # This indicates that only non
                                    # outcompeted domains would be found. Decided not to display both domains, but not
                                    # non-significant ones.
                                    f_write_pfam_prosite_res(vpfamfile, vheader, vsplitentry[1:], True, True,
                                                             vsavefolder, vjobid)
                    vfh_db_pfam.close()
                except IOError:
                    f_write_log(vsavefolder, vjobid, 'does not yet exist\n', 'a')
                    if vwarnings:
                        print(vdbfiles + '_' + vdbid + ' does not yet exist.')
            if not vfound:
                f_write_log(vsavefolder, vjobid, 'Sending sequence to PFAM\n', 'a')
                ventry_found = f_run_sequences_through_pfam(vheader, vsequences[vheader_id], vsavefolder, vjobid,
                                                            vwarnings)
                ventry_screened = []
                for ventry in ventry_found:
                    if ventry[len(ventry) - 1 - 1] == '1':  # (see above)
                        # and ventry[len(ventry)-1-2] == '0':  # (see above)
                        ventry_screened.append(ventry)
                f_write_pfam_prosite_db(vdbfiles, vdbid, ventry_found, vsavefolder, vjobid, vcurrentdate)
                f_write_pfam_prosite_res(vpfamfile, vheader, ventry_screened, True, False, vsavefolder, vjobid)  # Only
                # write significant results into the result file.
            # Update cookies
            vcid = math.floor((vheader_id + 1) / len(vheaders) * 100 / 5) + 22
            if vcid > 22:
                f_write_cookie(vcid, vsavefolder, vjobid, '')
                
    vpfamdata = f_read_tsv(vpfamfile, vsavefolder, vjobid)
    f_write_log(vsavefolder, vjobid, 'Successfully gathered PFAM domain results.\n', 'a')
    f_write_cookie(43, vsavefolder, vjobid, 'Finished searching PFAM')

    # Gather protein groups of protein data
    if vgroupfile == '':  # Default case, if no group association file is handed over.
        f_write_log(vsavefolder, vjobid, 'No custom protein group file used\n', 'a')
        vgroup = []
        vgroup_u = []
        for vheader in vheaders:
            f_write_log(vsavefolder, vjobid, 'Appending ' + vheader + ' to protein group "ProteinGroup".\n', 'a')
            if vwarnings:
                print('Appending ' + vheader + ' to protein group "ProteinGroup".')
            vgroup.append('ProteinGroup')
            vgroup_u.append('ProteinGroup')
    else:
        f_write_log(vsavefolder, vjobid, 'Reading in protein group file:\n', 'a')
        vgroup, vgroup_u = f_read_in_groupfile(vgroupfile, vheaders, vsavefolder, vjobid)
    vgroup_u = list(set(vgroup_u))
    f_write_log(vsavefolder, vjobid, 'Read protein group file successfully\n', 'a')

    # Per group of protein: get median sequence length
    f_write_log(vsavefolder, vjobid, 'Calculating median length of proteins for each protein group: ', 'a')
    vmedlengroup = []
    for vgitem in vgroup_u:
        vlenproteins = []
        for vg, vitem in enumerate(vgroup):
            if vitem == vgitem:
                vlenproteins.append(len(vsequences[vg]))
        vmedlengroup.append(math.ceil(median(vlenproteins)))
    f_success(vsavefolder, vjobid)

    # Get specific coloring
    if vcolorfile != '':
        f_write_log(vsavefolder, vjobid, 'Reading in color file:\n', 'a')
        vcolor_domain, vcolor_hexcode = f_read_in_colorfile(vcolorfile, vsavefolder, vjobid)
        f_write_log(vsavefolder, vjobid, 'Read color file successfully\n', 'a')
    else:
        f_write_log(vsavefolder, vjobid, 'No custom color file used\n', 'a')
        vcolor_domain = []
        vcolor_hexcode = []

    # Get list of domains to ignore
    if vignoredomainfile != '':
        f_write_log(vsavefolder, vjobid, 'Reading in ignore domain file:\n', 'a')
        vignore_domain = f_read_in_ignoredomainfile(vignoredomainfile, vsavefolder, vjobid)
        f_write_log(vsavefolder, vjobid, 'Read ignore domain file successfully\n', 'a')
    else:
        f_write_log(vsavefolder, vjobid, 'No custom ignore domain file used\n', 'a')
        vignore_domain = []

    # Get unique list of Prosite domains
    f_write_log(vsavefolder, vjobid, 'Produce unique list of Prosite domains: ', 'a')
    vprositedomains_u = []
    vprositedomains_u_color = []
    vprositedomains_u_ignore = []
    if vprositefile != '':
        for vprdc in range(len(vprositedata.columns)):
            vprositedomains_u.append(vprositedata[vprdc][3])
        vprositedomains_u = list(set(vprositedomains_u))
        for vitem in vprositedomains_u:
            vfound = 0
            for vc, vcitem in enumerate(vcolor_domain):
                if vitem == vcitem:
                    if vfound == 0:
                        vprositedomains_u_color.append(vcolor_hexcode[vc])
                        vfound = 1
            if vfound == 0:
                vprositedomains_u_color.append('')

            vfound = 0
            for viitem in vignore_domain:
                if vitem == viitem:
                    if vfound == 0:
                        vprositedomains_u_ignore.append(1)
                        vfound = 1
            if vfound == 0:
                vprositedomains_u_ignore.append(0)
    f_success(vsavefolder, vjobid)

    # Get unique list of Pfam domains
    f_write_log(vsavefolder, vjobid, 'Produce unique list of PFAM domains: ', 'a')
    vpfamdomains_u = []
    vpfamdomains_u_color = []
    vpfamdomains_u_ignore = []
    if vpfamfile != '':
        for vpdc in range(1, len(vpfamdata.columns)):
            vpfamdomains_u.append(vpfamdata[vpdc][1])
        vpfamdomains_u = list(set(vpfamdomains_u))

        for vitem in vpfamdomains_u:
            vfound = 0
            for vc, vcitem in enumerate(vcolor_domain):
                if vitem == vcitem:
                    if vfound == 0:
                        vpfamdomains_u_color.append(vcolor_hexcode[vc])
                        vfound = 1
            if vfound == 0:
                vpfamdomains_u_color.append('')

            vfound = 0
            for viitem in vignore_domain:
                if vitem == viitem:
                    if vfound == 0:
                        vpfamdomains_u_ignore.append(1)
                        vfound = 1
            if vfound == 0:
                vpfamdomains_u_ignore.append(0)
    f_success(vsavefolder, vjobid)

    # Remove beginning ('>') from fasta
    f_write_log(vsavefolder, vjobid, 'Processing fasta headers\n', 'a')
    vheaders_no_fastastart = []
    for vitem in vheaders:
        vheaders_no_fastastart.append(vitem.lstrip('>'))

    f_write_cookie(60, vsavefolder, vjobid, 'Finished reading and processing additional data')

    # Per group of protein: get annotations of Prosite and PFAM domains and make one plot per protein group.
    f_write_log(vsavefolder, vjobid, 'Collecting Prosite and PFAM domain information per protein group\n', 'a')
    vprositedomainsofgroup_all = []
    vprositedomainsingenes_all = []
    vpfamdomainsofgroup_all = []
    vpfamdomainsingenes_all = []
    vsize_of_prosite_data_all = []
    vsize_of_pfam_data_all = []
    vprositedomainsofgroup_rel_all = []
    vpfamdomainsofgroup_rel_all = []
    vn_prot_per_group_all = []
    vprositedomainsofgroup = np.zeros((0, 0), dtype=float)
    vprositedomainsingenes = np.zeros((0, 0), dtype=float)
    vpfamdomainsofgroup = np.zeros((0, 0), dtype=float)
    vpfamdomainsingenes = np.zeros((0, 0), dtype=float)

    # Define domain colors
    if vsavefolder != '':
        vdomaincolorfile = join(vsavefolder, vjobid + '_domain_color_file.txt')
    else:
        vdomaincolorfile = vjobid + '_domain_color_file.txt'
    f_write_log(vsavefolder, vjobid, 'Storing domain color information in ' + vdomaincolorfile + '\n', 'a')
    vfh_colors = open(vdomaincolorfile, 'w')

    # Prepare switches for each domain to decide if they should be processed
    vprositedomains_u_process = []
    for _ in vprositedomains_u:
        vprositedomains_u_process.append(True)
    vpfamdomains_u_process = []
    for _ in vpfamdomains_u:
        vpfamdomains_u_process.append(True)

    # Prepare dummy figure that contains all domains of all groups to get consistent coloring
    f_write_log(vsavefolder, vjobid, 'Prepare dummy figure of all domains and proteins: ', 'a')

    if not vcustom_scaling_on:
        vscalingfigure = vscalingfigure * 500 / max(vmedlengroup)
    else:
        vstandardwidth = (vstandardwidth - 2 * vpaddingwidth) * vscalingfigure * max(vmedlengroup) / 500 + \
                         (2 * vpaddingwidth)

    fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
    h = [Size.Fixed(vpaddingwidth),
         Size.Fixed(vscalingfigure * max(vmedlengroup) / 100)]
    v = [Size.Fixed(vpaddingheight), Size.Fixed(vstandardheight - 2 * vpaddingheight)]
    divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
    ax = Axes(fig, divider.get_position())
    ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
    fig.add_axes(ax)
    for vug, vgitem in enumerate(vgroup_u):  # Go through all groups of proteins
        f_write_log(vsavefolder, vjobid, 'Processing protein group ' + vgitem + '\n', 'a')
        vn_prot_per_group = 0  # Initialize the counting of sequences per group
        if vprositefile != '':
            vprositedomainsofgroup = np.zeros((len(vprositedomains_u), vmedlengroup[vug]), dtype=float)  # Initialize
            # with number of unique prosite domains and median length of proteins
            vprositedomainsingenes = np.zeros((len(vprositedomains_u), len(vheaders)), dtype=int)  # Stores if a domain
            # has been found for a gene
        if vpfamfile != '':
            vpfamdomainsofgroup = np.zeros((len(vpfamdomains_u), vmedlengroup[vug]), dtype=float)  # Initialize with
            # number of unique prosite domains and median length of proteins
            vpfamdomainsingenes = np.zeros((len(vpfamdomains_u), len(vheaders)), dtype=int)  # Stores if a domain has
            # been found for a gene
        vseqaddedfromprosite = 0
        vseqaddedfrompfam = 0
        for vh, vitem in enumerate(vheaders_no_fastastart):  # Go through all sequences
            if vgroup[vh] == vgitem:  # If the sequence has the same group association as is currently searched
                vn_prot_per_group = vn_prot_per_group + 1  # Count the number of sequence per this group up by one

                if vprositefile != '':
                    # Process Prosite
                    for vheader_id in range(len(vprositedata.columns)):  # go through all prosite data
                        if vprositedata[vheader_id][0] == vitem:  # If the prosite data is about the sequence we
                            # currently look at
                            for vp, vpd in enumerate(vprositedomains_u):  # Go through all domains
                                if vprositedata[vheader_id][3] == vpd:  # Check if the domain is the domain we currently
                                    # look at
                                    vmedianstartbp = f_float2int((int(vprositedata[vheader_id][1]) - 1) /
                                                                 len(vsequences[vh]) * vmedlengroup[vug])  # Calculate
                                    # the start position relative to the median length of the protein group:
                                    vmedianendbp = f_float2int((int(vprositedata[vheader_id][2]) - 1) /
                                                               len(vsequences[vh]) * vmedlengroup[vug])  # Calculate the
                                    # end position relative to the median length of the protein group:
                                    vprositedomainsofgroup[vp, vmedianstartbp:vmedianendbp] += 1  # Mark the placing of
                                    # the domain
                                    vprositedomainsingenes[vp, vh] = 1  # Define that the domain has been found for that
                                    # gene
                                    vseqaddedfromprosite += 1
                if vpfamfile != '':
                    # Process PFAM
                    for vheader_id in range(len(vpfamdata.columns)):  # Go through all pfam data
                        if vpfamdata[vheader_id][0].lstrip('>') == vitem:  # If the pfam data is about the sequence we
                            # currently look at
                            for vp, vpd in enumerate(vpfamdomains_u):  # Go through all domains
                                if vpfamdata[vheader_id][1] == vpd:  # If the domain is the domain we currently look at
                                    vmedianstartbp = f_float2int((int(vpfamdata[vheader_id][6]) - 1) /
                                                                 len(vsequences[vh]) * vmedlengroup[vug])  # Calculate
                                    # the start position relative to the median length of the protein group:
                                    vmedianendbp = f_float2int((int(vpfamdata[vheader_id][7]) - 1) /
                                                               len(vsequences[vh]) * vmedlengroup[vug])  # Calculate the
                                    # end position relative to the median length of the protein group:
                                    vpfamdomainsofgroup[vp, vmedianstartbp:vmedianendbp] += 1  # Mark the placing of the
                                    # domain
                                    vpfamdomainsingenes[vp, vh] = 1  # Define that the domain has been found for
                                    # that gene
                                    vseqaddedfrompfam += 1
        f_write_log(vsavefolder, vjobid, 'Added domain information from ' + str(vseqaddedfromprosite) + ' sequences for'
                                         ' Prosite.\nAdded domain information from ' + str(vseqaddedfrompfam) +
                                         ' sequences for PFAM.\n', 'a')
        vprositedomainsingenes_all.append(vprositedomainsingenes)
        vpfamdomainsingenes_all.append(vpfamdomainsingenes)

        vsize_of_prosite_data = [0, 0]
        vsize_of_pfam_data = [0, 0]
        if vprositefile != '':
            vsize_of_prosite_data = vprositedomainsofgroup.shape
        if vpfamfile != '':
            vsize_of_pfam_data = vpfamdomainsofgroup.shape
        vsize_of_prosite_data_all.append(vsize_of_prosite_data)
        vsize_of_pfam_data_all.append(vsize_of_pfam_data)

        # Normalization of data
        f_write_log(vsavefolder, vjobid, 'Compute relative prevalence of domains per group: ', 'a')
        vprositedomainsofgroup_rel = np.zeros((0, 0), dtype=float)
        vpfamdomainsofgroup_rel = np.zeros((0, 0), dtype=float)
        if vprositefile != '':
            vprositedomainsofgroup_rel = np.zeros((len(vprositedomains_u), vmedlengroup[vug]), dtype=float)
            for vprd in range(vsize_of_prosite_data[0]):
                for vj in range(vsize_of_prosite_data[1]):
                    if vprositedomainsofgroup[vprd][vj] != 0:
                        vprositedomainsofgroup_rel[vprd][vj] = vprositedomainsofgroup[vprd][vj]/vn_prot_per_group * 100
        if vpfamfile != '':
            vpfamdomainsofgroup_rel = np.zeros((len(vpfamdomains_u), vmedlengroup[vug]), dtype=float)
            for vpfd in range(vsize_of_pfam_data[0]):
                for vj in range(vsize_of_pfam_data[1]):
                    if vpfamdomainsofgroup[vpfd][vj] != 0:
                        vpfamdomainsofgroup_rel[vpfd][vj] = vpfamdomainsofgroup[vpfd][vj]/vn_prot_per_group * 100
        vprositedomainsofgroup_rel_all.append(vprositedomainsofgroup_rel)
        vpfamdomainsofgroup_rel_all.append(vpfamdomainsofgroup_rel)
        vn_prot_per_group_all.append(vn_prot_per_group)
        f_success(vsavefolder, vjobid)

        # If not using absolute values
        if not vabsolute:
            f_write_log(vsavefolder, vjobid, 'Use relative prevalence of domains per group.\n', 'a')
            if vprositefile != '':
                vprositedomainsofgroup = vprositedomainsofgroup_rel
            if vpfamfile != '':
                vpfamdomainsofgroup = vpfamdomainsofgroup_rel
        else:
            f_write_log(vsavefolder, vjobid, 'Use absolute prevalence of domains per group.\n', 'a')
        vprositedomainsofgroup_all.append(vprositedomainsofgroup)
        vpfamdomainsofgroup_all.append(vpfamdomainsofgroup)

        # Save of data
        f_write_log(vsavefolder, vjobid, 'Save domain data of group as .csvs: ', 'a')
        if vprositefile != '':
            if vsavefolder != '':
                np.savetxt(join(vsavefolder, vjobid + '_' + vgitem + '_prosite.csv'), vprositedomainsofgroup,
                           delimiter="\t")
            else:
                np.savetxt(vjobid + '_' + vgitem + '_prosite.csv', vprositedomainsofgroup, delimiter="\t")
        if vpfamfile != '':
            if vsavefolder != '':
                np.savetxt(join(vsavefolder, vjobid + '_' + vgitem + '_pfam.csv'), vpfamdomainsofgroup, delimiter="\t")
            else:
                np.savetxt(vjobid + '_' + vgitem + '_pfam.csv', vpfamdomainsofgroup, delimiter="\t")
        f_success(vsavefolder, vjobid)

        # Plot domains into figure with all domains of all groups to get coloring identical
        f_write_log(vsavefolder, vjobid, 'Add domains into dummy figure to get consistent domain data of group as'
                                         ' .csvs: ', 'a')
        vmaxes = []
        for vprd in range(vsize_of_prosite_data[0]):
            vmaxes.append(max(vprositedomainsofgroup_rel[vprd]))
        for vpfd in range(vsize_of_pfam_data[0]):
            vmaxes.append(max(vpfamdomainsofgroup_rel[vpfd]))
        vmaxids = np.argsort(vmaxes)[::-1]
        bin_edges = np.arange(vsize_of_prosite_data[1] + 1)
        for vmaxi in vmaxids:
            if vmaxi < vsize_of_prosite_data[0]:
                if max(vprositedomainsofgroup[vmaxi]) > (vmaxcutoff * 100) and float(
                        sum(vprositedomainsingenes[vmaxi])) / float(vn_prot_per_group) > vcutoff and \
                        vprositedomains_u_ignore[vmaxi] == 0 and vprositedomains_u_process[vmaxi]:
                    if vprositedomains_u_color[vmaxi] == '':
                        vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vmaxi], width=1, alpha=0.7,
                                          label=vprositedomains_u[vmaxi])
                    else:
                        vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vmaxi], width=1, alpha=0.7,
                                          label=vprositedomains_u[vmaxi],
                                          color=vprositedomains_u_color[vmaxi])
                    vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                    vprositedomains_u_color[vmaxi] = vcurrcolor
                    vfh_colors.write(vprositedomains_u[vmaxi] + '\t' + vcurrcolor + '\n')
                    vprositedomains_u_process[vmaxi] = False
            else:
                vimod = vmaxi - vsize_of_prosite_data[0]
                if max(vpfamdomainsofgroup[vimod]) > (vmaxcutoff * 100) and float(
                        sum(vpfamdomainsingenes[vimod])) / float(vn_prot_per_group) > vcutoff and \
                        vpfamdomains_u_ignore[vimod] == 0 and vpfamdomains_u_process[vimod]:
                    if vpfamdomains_u_color[vimod] == '':
                        vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vimod], width=1, alpha=0.7,
                                          label=vpfamdomains_u[vimod])
                    else:
                        vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vimod], width=1, alpha=0.7,
                                          label=vpfamdomains_u[vimod], color=vpfamdomains_u_color[vimod])
                    vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                    vpfamdomains_u_color[vimod] = vcurrcolor
                    vfh_colors.write(vpfamdomains_u[vimod] + '\t' + vcurrcolor + '\n')
                    vpfamdomains_u_process[vimod] = False
    vfh_colors.close()

    # Write fifth cookie
    f_write_cookie(80, vsavefolder, vjobid, 'Finished collecting and formatting all data')

    for vug, vgitem in enumerate(vgroup_u):  # Go through all groups of proteins
        vprositedomainsofgroup = vprositedomainsofgroup_all[vug]
        vpfamdomainsofgroup = vpfamdomainsofgroup_all[vug]
        vn_prot_per_group = vn_prot_per_group_all[vug]
        vprositedomainsofgroup_rel = vprositedomainsofgroup_rel_all[vug]
        vpfamdomainsofgroup_rel = vpfamdomainsofgroup_rel_all[vug]
        vprositedomainsingenes = vprositedomainsingenes_all[vug]
        vpfamdomainsingenes = vpfamdomainsingenes_all[vug]
        vsize_of_prosite_data = vsize_of_prosite_data_all[vug]
        vsize_of_pfam_data = vsize_of_pfam_data_all[vug]

        # Plot data of Prosite
        f_write_log(vsavefolder, vjobid, 'Plot Prosite domains of protein group ' + vgitem + '.\n', 'a')
        if vprositefile != '':
            print('Plot data of Prosite for ' + vgitem)
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth), Size.Fixed(vscalingfigure * max(vmedlengroup) / 100)]
            v = [Size.Fixed(vpaddingheight), Size.Fixed(vstandardheight - 2 * vpaddingheight)]
            divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
            ax = Axes(fig, divider.get_position())
            ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
            fig.add_axes(ax)
            vmaxes = []
            for vprd in range(vsize_of_prosite_data[0]):
                vmaxes.append(max(vprositedomainsofgroup_rel[vprd]))
            vmaxids = np.argsort(vmaxes)[::-1]
            bin_edges = np.arange(vsize_of_prosite_data[1] + 1)
            for vheader_id in vmaxids:
                if max(vprositedomainsofgroup[vheader_id]) > (vmaxcutoff * 100) and \
                        float(sum(vprositedomainsingenes[vheader_id]))/float(vn_prot_per_group) > vcutoff and \
                        vprositedomains_u_ignore[vheader_id] == 0:
                    # Create function
                    a = min(bin_edges[:-1])  # integral lower limit
                    b = max(bin_edges[:-1])  # integral upper limit
                    x_temp = [0]
                    for vx_i in range(1, b + 1):
                        x_temp.append(vx_i)
                    x = np.array(x_temp)
                    y = vprositedomainsofgroup[vheader_id]  # Function value

                    # Create Polygon
                    ix = np.array(x_temp)
                    iy = vprositedomainsofgroup[vheader_id]
                    verts = [(a, 0), *zip(ix, iy), (b, 0)]
                    if vprositedomains_u_color[vheader_id] == '':
                        poly = Polygon(verts, alpha=0.7, label=vprositedomains_u[vheader_id])
                    else:
                        poly = Polygon(verts, facecolor=vprositedomains_u_color[vheader_id], alpha=0.7,
                                       label=vprositedomains_u[vheader_id])
                    # Plot function
                    ax.plot(x, y, 'r', linewidth=0)
                    ax.set_ylim(bottom=0)

                    # Plot Polygon
                    ax.add_patch(poly)
            plt.xlim(min(bin_edges), max(bin_edges))
            if not vabsolute:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=vfontsize)
            if vabsolute:
                plt.ylabel('# of occurrences', fontsize=vfontsize)
            else:
                plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=vfontsize)
            plt.xticks(fontsize=vfontsize)
            plt.yticks(fontsize=vfontsize)
            plt.title('Distribution of Prosite protein domains\nfor ' + vgitem, fontsize=vfontsize)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_prosite.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_prosite.pdf')

        # Plot data of PFAM
        f_write_log(vsavefolder, vjobid, 'Plot PFAM domains of protein group ' + vgitem + '.\n', 'a')
        if vpfamfile != '':
            print('Plot data of PFAM for ' + vgitem)
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth),
                 Size.Fixed(vscalingfigure * max(vmedlengroup) / 100)]
            v = [Size.Fixed(vpaddingheight), Size.Fixed(vstandardheight - 2 * vpaddingheight)]
            divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
            ax = Axes(fig, divider.get_position())
            ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
            fig.add_axes(ax)
            vmaxes = []
            for vheader_id in range(vsize_of_pfam_data[0]):
                vmaxes.append(max(vpfamdomainsofgroup_rel[vheader_id]))
            vmaxids = np.argsort(vmaxes)[::-1]
            bin_edges = np.arange(vsize_of_pfam_data[1] + 1)
            for vheader_id in vmaxids:
                if max(vpfamdomainsofgroup[vheader_id]) > (vmaxcutoff * 100) and \
                        float(sum(vpfamdomainsingenes[vheader_id])) / \
                        float(vn_prot_per_group) > vcutoff and vpfamdomains_u_ignore[vheader_id] == 0:
                    # Create function
                    a = min(bin_edges[:-1])  # integral lower limit
                    b = max(bin_edges[:-1])  # integral upper limit
                    x_temp = [0]
                    for vx_i in range(1, b + 1):
                        x_temp.append(vx_i)
                    x = np.array(x_temp)
                    y = vpfamdomainsofgroup[vheader_id]  # Function value

                    # Create Polygon
                    ix = np.array(x_temp)
                    iy = vpfamdomainsofgroup[vheader_id]
                    verts = [(a, 0), *zip(ix, iy), (b, 0)]
                    if vpfamdomains_u_color[vheader_id] == '':
                        poly = Polygon(verts, alpha=0.7, label=vpfamdomains_u[vheader_id])
                    else:
                        poly = Polygon(verts, facecolor=vpfamdomains_u_color[vheader_id], alpha=0.7,
                                       label=vpfamdomains_u[vheader_id])
                    # Plot function
                    ax.plot(x, y, 'r', linewidth=0)
                    ax.set_ylim(bottom=0)

                    # Plot Polygon
                    ax.add_patch(poly)

            plt.xlim(min(bin_edges), max(bin_edges))
            if not vabsolute:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=vfontsize)
            if vabsolute:
                plt.ylabel('# of occurrences', fontsize=vfontsize)
            else:
                plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=vfontsize)
            plt.xticks(fontsize=vfontsize)
            plt.yticks(fontsize=vfontsize)
            plt.title('Distribution of PFAM protein domains\nfor ' + vgitem, fontsize=vfontsize)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_pfam.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_pfam.pdf')

        # Combined plot
        f_write_log(vsavefolder, vjobid, 'Plot all domains of protein group ' + vgitem + '.\n', 'a')
        if vprositefile != '' and vpfamfile != '':
            print('Plot data of Prosite and PFAM for ' + vgitem)
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth),
                 Size.Fixed(vscalingfigure * max(vmedlengroup) / 100)]
            v = [Size.Fixed(vpaddingheight), Size.Fixed(vstandardheight - 2 * vpaddingheight)]
            divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
            ax = Axes(fig, divider.get_position())
            ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
            fig.add_axes(ax)
            vmaxes = []
            for vprd in range(vsize_of_prosite_data[0]):
                vmaxes.append(max(vprositedomainsofgroup_rel[vprd]))
            for vpfd in range(vsize_of_pfam_data[0]):
                vmaxes.append(max(vpfamdomainsofgroup_rel[vpfd]))
            vmaxids = np.argsort(vmaxes)[::-1]
            bin_edges = np.arange(vsize_of_prosite_data[1] + 1)
            for vmaxi in vmaxids:
                if vmaxi < vsize_of_prosite_data[0]:
                    if max(vprositedomainsofgroup[vmaxi]) > (vmaxcutoff * 100) and float(
                            sum(vprositedomainsingenes[vmaxi])) / float(vn_prot_per_group) > vcutoff and \
                            vprositedomains_u_ignore[vmaxi] == 0:
                        # Create function
                        a = min(bin_edges[:-1])  # integral lower limit
                        b = max(bin_edges[:-1])  # integral upper limit
                        x_temp = [0]
                        for vx_i in range(1, b + 1):
                            x_temp.append(vx_i)
                        x = np.array(x_temp)
                        y = vprositedomainsofgroup[vmaxi]  # Function value

                        # Create Polygon
                        ix = np.array(x_temp)
                        iy = vprositedomainsofgroup[vmaxi]
                        verts = [(a, 0), *zip(ix, iy), (b, 0)]
                        if vprositedomains_u_color[vmaxi] == '':
                            poly = Polygon(verts, alpha=0.7, label=vprositedomains_u[vmaxi])
                        else:
                            poly = Polygon(verts, facecolor=vprositedomains_u_color[vmaxi], alpha=0.7,
                                           label=vprositedomains_u[vmaxi])
                        # Plot function
                        ax.plot(x, y, 'r', linewidth=0)
                        ax.set_ylim(bottom=0)

                        # Plot Polygon
                        ax.add_patch(poly)
                else:
                    vimod = vmaxi - vsize_of_prosite_data[0]
                    if max(vpfamdomainsofgroup[vimod]) > (vmaxcutoff * 100) and float(
                            sum(vpfamdomainsingenes[vimod])) / float(vn_prot_per_group) > vcutoff and \
                            vpfamdomains_u_ignore[vimod] == 0:
                        # Create function
                        a = min(bin_edges[:-1])  # integral lower limit
                        b = max(bin_edges[:-1])  # integral upper limit
                        x_temp = [0]
                        for vx_i in range(1, b + 1):
                            x_temp.append(vx_i)
                        x = np.array(x_temp)
                        y = vpfamdomainsofgroup[vimod]  # Function value

                        # Create Polygon
                        ix = np.array(x_temp)
                        iy = vpfamdomainsofgroup[vimod]
                        verts = [(a, 0), *zip(ix, iy), (b, 0)]
                        if vpfamdomains_u_color[vimod] == '':
                            poly = Polygon(verts, alpha=0.7, label=vpfamdomains_u[vimod])
                        else:
                            poly = Polygon(verts, facecolor=vpfamdomains_u_color[vimod], alpha=0.7,
                                           label=vpfamdomains_u[vimod])
                        # Plot function
                        ax.plot(x, y, 'r', linewidth=0)
                        ax.set_ylim(bottom=0)

                        # Plot Polygon
                        ax.add_patch(poly)

            plt.xlim(min(bin_edges), max(bin_edges))
            if not vabsolute:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=vfontsize)
            if vabsolute:
                plt.ylabel('# of occurrences', fontsize=vfontsize)
            else:
                plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=vfontsize)
            plt.xticks(fontsize=vfontsize)
            plt.yticks(fontsize=vfontsize)
            plt.title('Distribution of protein domains\nfor ' + vgitem, fontsize=vfontsize)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_combined.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_combined.pdf')
    # Write fifth cookie
    f_write_cookie(100, vsavefolder, vjobid, 'Job ' + vjobid + 'successful')
    f_write_log(vsavefolder, vjobid, 'Job ' + vjobid + ' ran successfully.\n', 'a')
    print('done')


########################################################################################################################
#                                                                                                                      #
#  f_float2int                                                                                                         #
#  Writes success.\n into log file.                                                                                    #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfloat [float]: The number that should be rounded to an integer                                                 #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - [int]: of the number above.                                                                                     #
#                                                                                                                      #
########################################################################################################################

def f_float2int(vfloat):
    if vfloat - math.floor(vfloat) >= 0.5:
        return int(math.ceil(vfloat))
    else:
        return int(math.floor(vfloat))


########################################################################################################################
#                                                                                                                      #
#  f_success                                                                                                           #
#  Writes success.\n into log file.                                                                                    #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - Entry in [jobid]_log.log [file]: Log file.                                                                      #
#                                                                                                                      #
########################################################################################################################

def f_success(vsavefolder, vjobid):
    f_write_log(vsavefolder, vjobid, 'success.\n', 'a')


########################################################################################################################
#                                                                                                                      #
#  f_no                                                                                                           #
#  Writes no.\n into log file.                                                                                    #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - Entry in [jobid]_log.log [file]: Log file.                                                                      #
#                                                                                                                      #
########################################################################################################################

def f_no(vsavefolder, vjobid):
    f_write_log(vsavefolder, vjobid, 'no.\n', 'a')


########################################################################################################################
#                                                                                                                      #
#  f_write_log                                                                                                         #
#  Writes a log file to give output if something breaks.                                                               #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vmessage [string]: Message that is written into the file.                                                       #
#    - vmode [string]: Should either be 'w' for write or 'a' for append.                                               #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - [jobid]_log.log [file]: Log file.                                                                               #
#                                                                                                                      #
########################################################################################################################

def f_write_log(vsavefolder, vjobid, vmessage, vmode):
    vfh_c = open(join(vsavefolder, vjobid + '_log.log'), vmode)
    vfh_c.write(vmessage)
    vfh_c.close()


########################################################################################################################
#                                                                                                                      #
#  f_write_cookie                                                                                                      #
#  Writes a cookie file to give output to where the job currently is.                                                  #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vid [int]: Id of the cookie to be written.                                                                      #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vmessage [string]: Message that is written into the file.                                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - cookie_[id] [file]: Cookie defining the progress (1 - 5) or failure (-1).                                       #
#                                                                                                                      #
########################################################################################################################

def f_write_cookie(vid, vsavefolder, vjobid, vmessage):
    vfh_c = open(join(vsavefolder, vjobid + '_cookie_' + str(vid)), 'w')
    vfh_c.write(vmessage + '\n')
    vfh_c.close()


########################################################################################################################
#                                                                                                                      #
#  f_get_hex                                                                                                           #
#  Converts a 3 value tuple into hex code (tuple is assumed to be between 0 and 1).                                    #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vtuple [list]: a list of numbers e.g. (0,0.5,0.912).                                                            #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - [string]: hex color code e.g. #af0010.                                                                          #
#                                                                                                                      #
########################################################################################################################


def f_get_hex(vtuple):
    vr = '%02x' % int(round(vtuple[0] * 255))
    vg = '%02x' % int(round(vtuple[1] * 255))
    vb = '%02x' % int(round(vtuple[2] * 255))
    return '#' + vr + vg + vb


########################################################################################################################
#                                                                                                                      #
#  f_read_in_ignoredomainfile                                                                                          #
#  Reads a file on where each line is assumed to either be the name of a Prosite or a PFAM domain. This list is then   #
#  later used to ignore the domains when making figures.                                                               #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: Should indicate a text file containing the domain names to ignore.                              #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vignore_domain [list]: Strings representing domain names of Prosite or PFAM.                                    #
#                                                                                                                      #
########################################################################################################################


def f_read_in_ignoredomainfile(vfile, vsavefolder, vjobid):
    vignore_domain = []
    try:
        vfile_fh = open(vfile, 'r')
        for vline in vfile_fh:
            vline = re.sub("[\n\r]", "", vline)
            vsplit = vline.split('\t')
            vignore_domain.append(vsplit[0])
        vfile_fh.close()
    except IOError:
        f_write_log(vsavefolder, vjobid, 'Can not read ignore domain file ' + vfile + '\n', 'a')
        print('Can not read file: ' + vfile)
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Can not read ignore domain file ' + vfile)
        sys.exit()
    return vignore_domain


########################################################################################################################
#                                                                                                                      #
#  f_read_in_colorfile                                                                                                 #
#  Reads a tab separated file in where each line is assumed to first contain a Prosite or PFAM domain, and the second  #
#  column contains a hexcode for a color to be applied in the figures.                                                 #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: Should indicate a text file containing the domain color matchings.                              #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vcolor_domain [list]: Strings representing domain names of Prosite or PFAM.                                     #
#    - vcolor_hexcode [list]: Hex codes for the coloring of the domains. e.g. #af0010.                                 #
#                                                                                                                      #
########################################################################################################################


def f_read_in_colorfile(vfile, vsavefolder, vjobid):
    vcolor_domain = []
    vcolor_hexcode = []
    try:
        vfile_fh = open(vfile, 'r')
        for vline in vfile_fh:
            vline = re.sub("[\n\r]", "", vline)
            vsplit = vline.split('\t')
            vcolor_domain.append(vsplit[0])
            vcolor_hexcode.append(vsplit[1])
        vfile_fh.close()
    except IOError:
        f_write_log(vsavefolder, vjobid, 'Can not read color file ' + vfile + '\n', 'a')
        print('Can not read color file: ' + vfile)
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Can not read color file ' + vfile)
        sys.exit()
    return vcolor_domain, vcolor_hexcode


########################################################################################################################
#                                                                                                                      #
#  f_read_in_groupfile                                                                                                 #
#  Reads a tab separated file in where each line is assumed to first contain a sequence header, and the second column  #
#  contains a group identifier by which the sequences should be grouped by.                                            #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: String indicating a text file containing the domain color matchings.                            #
#    - vheaders [list]: Fasta headers that should be used to search for domain associations.                           #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vgroup [list]: Group associations that match to the sequence headers.                                           #
#    - vgroup_u [list]: the same list as above, but as a unique set, to later ensure that a independent set of unique  #
#                       groups can be made.                                                                            #
#                                                                                                                      #
########################################################################################################################


def f_read_in_groupfile(vfile, vheaders, vsavefolder, vjobid):
    vgroup = []
    vgroup_u = []
    try:
        for vitem in vheaders:
            vfile_fh = open(vfile, 'r')
            vhit = 0
            for vline in vfile_fh:
                vline = re.sub("[\n\r]", "", vline)
                vsplit = vline.split('\t')
                if vsplit[0] == vitem:
                    if vhit == 0:
                        vgroup.append(vsplit[1])
                        vgroup_u.append(vsplit[1])
                        vhit += 1
                    else:
                        print('Warning: group domain file has more than one entry for ' + vitem + '. Only first '
                              'instance is used.')
                        f_write_log(vsavefolder, vjobid, 'Warning: group domain file has more than one entry '
                                                         'for ' + vitem + '. Only first instance is used.\n', 'a')
            vfile_fh.close()
            if vhit == 0:
                f_write_log(vsavefolder, vjobid, 'Warning: no protein group entry found for ' + vitem +
                                                 '. Please add one in ' + vfile + '\nUsing "ProteinGroup" as group name'
                                                 ' instead.\n', 'a')
                print('Warning: no protein group entry found for ' + vitem + '. Please add one in ' + vfile)
                vgroup.append('ProteinGroup')
                vgroup_u.append('ProteinGroup')
    except IOError:
        f_write_log(vsavefolder, vjobid, 'Unable to read protein group file ' + vfile + '\n', 'a')
        print('Can not read protein group file: ' + vfile)
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Can not read protein group file: ' + vfile)
        sys.exit()
    return vgroup, vgroup_u


########################################################################################################################
#                                                                                                                      #
#  f_read_tsv                                                                                                          #
#  Reads a tab separated file and gives back a pandas data frame with the information stored in the tsv.               #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: String indicating a tsv file.                                                                   #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vtable [pandas data frame]: pandas data frame containing the information of the tsv.                            #
#                                                                                                                      #
########################################################################################################################


def f_read_tsv(vfile, vsavefolder, vjobid):
    try:
        vinit = True
        vtable = pd.DataFrame()
        vfile_fh = open(vfile, 'r')
        vw = -1
        vn_split = 0
        for vline in vfile_fh:
            if vline.find('\t') != -1:
                vline = re.sub("[\n\r]", "", vline)
                vsplit = vline.split('\t')
                if vinit:
                    vtable = pd.DataFrame(vsplit)
                    vn_split = len(vsplit)
                    vw += 1
                else:
                    if len(vsplit) == vn_split:
                        vw += 1
                        vtable[vw] = vsplit
                vinit = False
        vfile_fh.close()
    except IOError:
        print('Can not read file: ' + vfile)
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Can not read result file.')
        sys.exit()
    return vtable


########################################################################################################################
#                                                                                                                      #
#  f_read_in_file                                                                                                      #
#  Reads a fasta file and gives back a list of headers and sequences.                                                  #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: String towards a fasta file.                                                                    #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vheaders [list]: List of headers of fasta file sequences.                                                       #
#    - vsequences [list]: List of fasta file sequences.                                                                #
#                                                                                                                      #
########################################################################################################################


def f_read_in_file(vfile, vsavefolder, vjobid):
    # Load all fasta sequences
    vheaders = []
    vsequences = []
    vinit = 1
    vfile_fh = open(vfile)
    vtempsequence = []
    vtempheader = []
    vh = 0
    for vline in vfile_fh:
        vline = re.sub("[\n\r]", "", vline)
        if vline.startswith('>'):

            if vinit == 0:
                if len(vtempsequence) > 0:
                    vheaders.append(vtempheader)
                    vsequences.append(vtempsequence)
                    f_success(vsavefolder, vjobid)
            vh += 1
            f_write_log(vsavefolder, vjobid, 'Reading in header ' + str(vh) + ': ', 'a')
            vtempheader = vline
            vtempsequence = []
            vinit = 0
        else:
            if len(vtempsequence) == 0:
                vtempsequence = str(re.sub("[*]?", "", vline))
            else:
                vtempsequence = str(vtempsequence) + str(re.sub("[*]?", "", vline))
    vfile_fh.close()
    if len(vtempsequence) > 0:
        vheaders.append(vtempheader)
        vsequences.append(vtempsequence)
    f_write_log(vsavefolder, vjobid, 'Read ' + str(len(vheaders)) + ' headers and ' + str(len(vsequences)) +
                                     ' sequences.\n', 'a')
    return vheaders, vsequences


########################################################################################################################
#                                                                                                                      #
#  f_run_sequences_through_prosite                                                                                     #
#  Runs an amino acid sequence through prosite and gives back a list of lists containing all protein domains that were #
#  found.                                                                                                              #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vhead [string]: Fasta sequence header.                                                                          #
#    - vseq [string]: Protein sequence.                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vwarnings_prosite [boolean]: If warnings should be given out or not.                                            #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vout_all [list]: List of lists, containing the results as sublist, with the sequence header as the first item,  #
#                       followed by all other information collected from prosite.                                      #
#                                                                                                                      #
########################################################################################################################


def f_run_sequences_through_prosite(vhead, vseq, vsavefolder, vjobid, vwarnings_prosite):
    # Write that sequences are run to Prosite to the stdout
    f_write_log(vsavefolder, vjobid, 'Submitted Prosite search for sequence "' + vseq[0:16] + '...".\n', 'a')
    if vwarnings_prosite:
        print('@> Submitted Prosite search for sequence "' + vseq[0:16] + '...".')

    # Check for sequence length
    vout_all = []
    if 16 <= len(vseq):
        # Run sequence
        try:
            # If a 404 error occurs, then the reason might be that the mirror https://prosite.expasy.org changed to
            # something else. Check if you use a search machine on the internet, and look for expasy and change it to
            # the URL that you get.
            vhandle = Bio.ExPASy.ScanProsite.scan(vseq, mirror='https://prosite.expasy.org', output='xml')
            vresults = Bio.ExPASy.ScanProsite.read(vhandle)
            if len(vresults) > 0:
                for record in vresults:
                    vout = [vseq]
                    for _ in range(7):
                        vout.append('')
                    for key in record.keys():
                        vout = f_dissect_prosite_key(vout, key, record[key])
                        if isinstance(record[key], dict):
                            for key2 in record[key].keys():
                                vout = f_dissect_prosite_key(vout, key2, record[key][key2])
                                if isinstance(vresults[key][key2], dict):
                                    for key3 in record[key][key2].keys():
                                        vout = f_dissect_prosite_key(vout, key3, record[key][key2][key3])
                    vout_all.append(vout)
            else:
                f_write_log(vsavefolder, vjobid, 'Warning, sequence has no results\n', 'a')
                vout = [vseq]
                for _ in range(7):
                    vout.append('')
                vout_all.append(vout)
                if vwarnings_prosite:
                    print(vhead + ' has no results in prosite.')
        except ValueError:
            f_write_log(vsavefolder, vjobid, 'Warning, sequence resulted in a ValueError.\n', 'a')
            vout = [vseq]
            for _ in range(7):
                vout.append('')
            vout_all.append(vout)
            if vwarnings_prosite:
                print(vhead + ' has no results in prosite.')
    else:
        f_write_log(vsavefolder, vjobid, 'Warning, sequence too short (<16 amino acids).\n', 'a')
        vout = [vseq]
        for _ in range(7):
            vout.append('')
        vout_all.append(vout)
        if vwarnings_prosite:
            print(vhead + ' is too short to be run through Prosite (<16 amino acids).')
    return vout_all


########################################################################################################################
#                                                                                                                      #
#  f_run_sequences_through_pfam                                                                                        #
#  Runs an amino acid sequence through pfam and gives back a list of lists containing all protein domains that were    #
#  found.                                                                                                              #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vhead [string]: Fasta sequence header.                                                                          #
#    - vseq [string]: Protein sequence.                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vwarnings_pfam [boolean]: If warnings should be given out or not.                                               #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vout_all [list]: List of lists, containing the results as sublist, with the sequence header as the first item,  #
#                       followed by all other information collected from pfam.                                         #
#                                                                                                                      #
########################################################################################################################


def f_run_sequences_through_pfam(vhead, vseq, vsavefolder, vjobid, vwarnings_pfam):
    # Constants:
    vmax_pfam_503_iterations = 6
    vinitial_503_wait_time_multiplier = 5
    vcurrent_503_try = 0

    # Write that sequences are run to PFAM to the stdout
    f_write_log(vsavefolder, vjobid, 'Submitted PFAM search for sequence "' + vseq[0:16] + '...".\n', 'a')
    if vwarnings_pfam:
        print('@> Submitted PFAM search for sequence "' + vseq[0:16] + '...".')

    # Check for sequence length
    vout_all = []
    if 16 <= len(vseq) <= 5000:
        # Run sequence
        try:
            verrorcode, vheader, vresults = f_query_pfam(vseq, vsavefolder, vjobid)  # Call PFAM with sequence
            if verrorcode == 503 or verrorcode == 500 or verrorcode == -2:
                if vwarnings_pfam:
                    verrorcode_2_display = str(verrorcode)
                    if verrorcode_2_display == '-2':
                        verrorcode_2_display = 'A seldom error that usually can be rescued was found. '
                    else:
                        verrorcode_2_display = 'HTTP ' + verrorcode_2_display + ' Error occurred. '
                    print(verrorcode_2_display + 'Try to rescue.')
                f_write_log(vsavefolder, vjobid, verrorcode_2_display + '\nTrying to rescue.\n', 'a')
                vcurrent_503_try += 1
                vpassed = False
                while vcurrent_503_try <= vmax_pfam_503_iterations and vpassed is False:
                    if vwarnings_pfam:
                        print('HTTP 500, 503, or a seldom other Error occurred. Rescue attempt #' +
                              str(vcurrent_503_try) + ' of ' + str(vmax_pfam_503_iterations))
                    f_write_log(vsavefolder, vjobid,
                                'Rescue attempt #' + str(vcurrent_503_try) + ' of ' + str(vmax_pfam_503_iterations) +
                                '.\n', 'a')
                    vwaittime = 4 ^ vcurrent_503_try * vinitial_503_wait_time_multiplier
                    print('Waiting ' + str(vwaittime) + ' seconds.')
                    time.sleep(vwaittime)
                    verrorcode, vheader, vresults = f_query_pfam(vseq, vsavefolder, vjobid)  # Call PFAM with sequence
                    if verrorcode == -1:
                        vpassed = True
                    elif verrorcode == 503:
                        if vwarnings_pfam:
                            print('HTTP 503 Error occurred again.')
                    elif verrorcode == 500:
                        if vwarnings_pfam:
                            print('HTTP 500 Error occurred again.')
                    elif verrorcode == -2:
                        if vwarnings_pfam:
                            print('Other error than HTTP occurred again. Experience says: just try another time.')
                    else:
                        f_handle_pfam_error(verrorcode, vsavefolder, vjobid, vwarnings_pfam)
                    vcurrent_503_try += 1
                if vpassed is False:
                    f_write_log(vsavefolder, vjobid, 'Was unable to rescue 500/503.\nAbort.\n', 'a')
                    print('HTTPError 500 or 503, or other seldom errors occurred too many times when trying to access '
                          'PFAM result.')
                    f_write_log(vsavefolder, vjobid, 'HTTPError 500, 503 or seldom other errors occurred when trying '
                                                     'to access PFAM result.\n', 'a')
                    f_write_cookie(-1, vsavefolder, vjobid, 'HTTPError 500, 503 or seldom other errors occurred too '
                                                            'many times when trying to access PFAM result.')
                    sys.exit()
            else:
                f_handle_pfam_error(verrorcode, vsavefolder, vjobid, vwarnings_pfam)

            if len(vresults) > 0:  # If at least one result was found
                for vr, vresult in enumerate(vresults):  # For every result (id vr)
                    vout = [vseq]  # Attach sequence as identifier
                    # for _ in range(42 - 1):  # Prepare storing variable in case not all attributes can be filled
                    for _ in range(17 - 1):  # Prepare storing variable in case not all attributes can be filled
                        vout.append('')
                    # for vi_41, vitem in enumerate(vresult):  # Check for all attributes and fill them into the output
                    for vi_16, vitem in enumerate(
                            vresult):  # Check for all attributes and fill them into the output
                        # vout = f_dissect_pfam_key(vout, vheader[vi_41], vitem)
                        vout = f_dissect_pfam_key(vout, vheader[vi_16], vitem)
                    vout_all.append(vout)  # Append the output of this result to the output of all other results
            else:  # In case no result was found, prepare standard output (see lines above for meaning)
                f_write_log(vsavefolder, vjobid, 'Warning, sequence has no results\n', 'a')
                vout = [vseq]
                # for _ in range(42 - 1):
                for _ in range(17 - 1):
                    vout.append('')
                vout_all.append(vout)
                if vwarnings_pfam:
                    print(vhead + ' has no results in pfam.')
        except ValueError:  # If we were not able to run results through PFAM (see lines above for meaning)
            f_write_log(vsavefolder, vjobid, 'Warning, sequence resulted in a ValueError.\n', 'a')
            vout = [vseq]
            # for _ in range(42 - 1):
            for _ in range(17 - 1):
                vout.append('')
            vout_all.append(vout)
            if vwarnings_pfam:
                print(vhead + ' has no results in pfam.')
    elif 16 > len(vseq):
        f_write_log(vsavefolder, vjobid, 'Warning, sequence too short (<16 amino acids).\n', 'a')
        vout = [vseq]
        # for _ in range(42 - 1):
        for _ in range(17 - 1):
            vout.append('')
        vout_all.append(vout)
        if vwarnings_pfam:
            print(vhead + ' is too short to be run through PFAM (<16 amino acids).')
    elif len(vseq) > 5000:
        f_write_log(vsavefolder, vjobid, 'Warning, sequence too long (>5000 amino acids).\n', 'a')
        vout = [vseq]
        # for _ in range(42 - 1):
        for _ in range(17 - 1):
            vout.append('')
        vout_all.append(vout)
        if vwarnings_pfam:
            print(vhead + ' is too long to be run through PFAM (>5000 amino acids).')
    return vout_all  # Return all results


########################################################################################################################
#                                                                                                                      #
#  f_handle_pfam_error                                                                                                 #
#  Handles errors given out by running sequences through PFAM                                                          #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - verrorcode [string]: Error code that needs handling.                                                            #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#    - vwarnings_pfam [boolean]: If warnings should be given out or not.                                               #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vout_all [list]: List of lists, containing the results as sublist, with the sequence header as the first item,  #
#                       followed by all other information collected from pfam.                                         #
#                                                                                                                      #
########################################################################################################################


def f_handle_pfam_error(verrorcode, vsavefolder, vjobid, vwarnings_pfam):
    if verrorcode == -1:
        if vwarnings_pfam:
            print('Results of search received.')
    elif verrorcode == 400:
        print('HTTPError 400 occurred when trying to access PFAM result.')
        f_write_log(vsavefolder, vjobid, 'HTTPError 400 occurred when trying to access PFAM '
                                         'result.\n', 'a')
        f_write_cookie(-1, vsavefolder, vjobid, 'HTTPError 400 occurred when trying to access '
                                                'PFAM result.')
        sys.exit()
    elif verrorcode == 404:
        print('HTTPError 404 occurred when trying to access PFAM result.')
        f_write_log(vsavefolder, vjobid, 'HTTPError 404 occurred when trying to access PFAM '
                                         'result.\n', 'a')
        f_write_cookie(-1, vsavefolder, vjobid, 'HTTPError 404 occurred when trying to access '
                                                'PFAM result.')
        sys.exit()
    elif verrorcode == -2:
        print('Error other than HTTPError occurred when trying to access PFAM result.')
        f_write_log(vsavefolder, vjobid, 'Error other than HTTPError occurred when trying to access PFAM '
                                         'result.\n', 'a')
        f_write_cookie(-1, vsavefolder, vjobid, 'Error other than HTTPError occurred when trying to access '
                                                'PFAM result.')
        sys.exit()
    else:
        print('Unknown error ' + str(verrorcode) + ' occurred: ')
        f_write_log(vsavefolder, vjobid, 'Unknown error ' + str(verrorcode) + ' occurred while trying '
                                                                              'to reach PFAM.\n', 'a')
        f_write_cookie(-1, vsavefolder, vjobid, 'Unknown error ' + str(verrorcode) + ' occurred while trying '
                                                                                     'to reach PFAM.')
        sys.exit()


########################################################################################################################
#                                                                                                                      #
#  f_read_hmmer_xml                                                                                                    #
#  Reads the xml output of an hmmer search and gives the domain results back as a list of lists.                       #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: Either indicates the place where the xml is stored, or it is a byte string of that file.        #
#    - vtype [string]: String indicating whether vfile indicates a byte string ('string') or a file ('file').          #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vrecords [list]: A list of lists, containing the results of a hmmer search as lists stored in a list.           #
#                                                                                                                      #
########################################################################################################################


def f_read_hmmer_xml(vfile, vtype, vsavefolder, vjobid):
    # Parameters
    vsilent = 1

    # Open file for real if type is file
    if vtype == 'file':
        # Test if file can be opened, else abort.
        try:
            vfh_xml = open(vfile, 'r')
            vfh_xml.close()
        except IOError:
            print('Can not open file ' + vfile + '.\n')
            # Write kill cookie
            f_write_cookie(-1, vsavefolder, vjobid, 'Can not open xml file.')
            sys.exit()
        vfh_xml = open(vfile, 'r')
    elif vtype == 'string':
        vfh_xml = vfile.decode("utf-8").split('\n')
    else:
        print('Type of input ' + vtype + ' is unknown.\nShould be either file or string.')
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Unknown input type of hmmer search.')
        sys.exit()

    # read in file line by line
    vparent = 'root'
    vcurr_parent = vparent
    vrecords = []
    for vl, vline in enumerate(vfh_xml):
        vline_stripped = vline.strip()
        if vline_stripped == '':
            if vsilent == 0:
                print('Warning: Empty line: ' + str(vl))
        else:
            vtypeline = f_check_type_line(vline)
            if vtypeline == 0 or vtypeline == 1:
                vrecord, vcurr_parent = f_read_single_record(vline, vcurr_parent, vtypeline)
                vrecords.append(vrecord)
            elif vtypeline == 2:
                vcurr_parent = f_get_parent(vrecords, vline)
            else:
                print('Line is not a correct xml line.')
                print(vline)
                # Write kill cookie
                f_write_cookie(-1, vsavefolder, vjobid, 'Incorrect xml line found: ' + vline)
                sys.exit()
    if vtype == 'file':
        vfh_xml.close()

    # return output
    return vrecords


########################################################################################################################
#                                                                                                                      #
#  f_get_parent                                                                                                        #
#  If an xml file has the object <\object>, it looks for the last record that has object as child and returns the      #
#  parent of that object.                                                                                              #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vrecords [list]: A list of lists, containing the results of a hmmer search as lists stored in a list.           #
#    - vline [string]: A line of an xml search to be used to figure out what the parent was of that object that is     #
#                      listed.                                                                                         #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vparent [string]: The parental object according to the records.                                                 #
#                                                                                                                      #
########################################################################################################################


def f_get_parent(vrecords, vline):
    vline = vline.strip()  # Removes white space around string
    vline = vline.lstrip('</')  # Removes leading </
    vline = vline.rstrip('>')  # Removes tailing </
    vline = vline.strip()  # Removes white space around string

    vparent = ''  # Initialize output
    for vitem in reversed(vrecords):  # Go through records in reverse order
        if vitem[1] == vline:  # Check if the child of the record is the object that is present in the line.
            vparent = vitem[0]  # Get the parent of the child.
            break  # Stop searching.
    return vparent  # Return parent.


########################################################################################################################
#                                                                                                                      #
#  f_check_type_line                                                                                                   #
#  Figures out for a line of an xml document, if it is just indicating a new record <object>, if it is indicating a    #
#  new record with some attributes <object attribute="attribute value">, or whether it is indicating the closing of a  #
#  record <\object>.                                                                                                   #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vline [string]: A line of an xml search to be used to figure out what kind of record it is.                     #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vreturn [int]: Indicates record with attributes as 0, end of record as 2 and other records as 1, and -1 if the  #
#                     type was not found.                                                                              #
#                                                                                                                      #
########################################################################################################################


def f_check_type_line(vline):
    vline = vline.strip()
    vline = vline.rstrip('\n')
    if vline.startswith('<') and vline.endswith('/>'):
        vreturn = 0
    elif vline.startswith('</') and vline.endswith('>'):
        vreturn = 2
    elif vline.startswith('<') and vline.endswith('>'):
        vreturn = 1
    else:
        vreturn = -1
    return vreturn


########################################################################################################################
#                                                                                                                      #
#  f_read_single_record                                                                                                #
#  Reads an xml line and extracts the information. It stores the parent, the child id, then attributes of that record  #
#  and the attribute values of the record.                                                                             #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vline [string]: A line of an xml search.                                                                        #
#    - vcurr_parent [string]: The parent of the current xml line.                                                      #
#    - vtype [int]: The type of the current line (see above).                                                          #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vrecord [list]: the line as record (with parent, child, the different attributes as list and the attribute      #
#                      values as list.                                                                                 #
#    - vnew_parent [string]: The parent of the next line. If a new record was opened                                   #
#                                                                                                                      #
########################################################################################################################


def f_read_single_record(vline, vcurr_parent, vtype):
    vline = vline.strip()
    vline = vline.lstrip('<')
    if vtype == 0:
        vline = vline.rstrip('/>')
    elif vtype == 1:
        vline = vline.rstrip('>')
    vline = vline.strip()
    vsplit = vline.split(' ')
    vchild_id = vsplit[0]
    vline = vline.lstrip(vchild_id)
    vline = vline.lstrip()
    vsplittmp = vline.split(' ')
    vsplit = []
    vtempitem = ''
    for vitem in vsplittmp:
        if vtempitem == '':
            vtempitem = vitem
        else:
            vtempitem = vtempitem + ' ' + vitem
        if vtempitem.endswith('"') and not vtempitem.endswith('="'):
            vsplit.append(vtempitem)
            vtempitem = ''
    vattributes = []
    vattribute_values = []
    if len(vsplit) > 0:
        for vitem_id, vitem in enumerate(vsplit):
            if vitem_id > 0:
                vsplit_2_temp = vitem.split('=')
                vsplit_2 = [vsplit_2_temp[0]]
                vtempsplit_2 = vsplit_2_temp[1]
                for vj, vitem2 in enumerate(vsplit_2_temp):
                    if vj > 1:
                        vtempsplit_2 = vtempsplit_2 + '=' + vitem2
                vsplit_2.append(vtempsplit_2)
                vattributes.append(vsplit_2[0])
                vattribute_values.append(vsplit_2[1])

    vrecord = [vcurr_parent, vchild_id, vattributes, vattribute_values]
    if vtype == 0:
        vnew_parent = vcurr_parent
    elif vtype == 1:
        vnew_parent = vchild_id
    else:
        vnew_parent = ''

    return vrecord, vnew_parent


########################################################################################################################
#                                                                                                                      #
#  f_convert_hmmer_xml_tsv                                                                                             #
#  Converts the hmmer xml output into a list of lists, similar to a tsv. It gives the header of the list as separate   #
#  output.                                                                                                             #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: Either indicates the place where the xml is stored, or it is a byte string of that file.        #
#    - vtype [string]: String indicating whether vfile indicates a byte string ('string') or a file ('file').          #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vheader [list]: Header indicators with the first few headers being the same as in the tsv output of hmmer.      #
#    - vnew_records [list]: All domains that were found in the hmmer output.                                           #
#                                                                                                                      #
########################################################################################################################


def f_convert_hmmer_xml_tsv(vfile, vtype, vsavefolder, vjobid):
    vrecords = f_read_hmmer_xml(vfile, vtype, vsavefolder, vjobid)

    # Create tsv header and the ids that are listed in the xml
    vheader = []
    vheader_ids = []
    vheader.append('Family id')  # 1
    vheader_ids.append('alihmmname')
    vheader.append('Family Accession')  # 2
    vheader_ids.append('alihmmacc')
    vheader.append('Clan')  # 3
    vheader_ids.append('clan')
    vheader.append('Env. Start')  # 4
    vheader_ids.append('ienv')
    vheader.append('Env. End')  # 5
    vheader_ids.append('jenv')
    vheader.append('Ali. Start')  # 6
    vheader_ids.append('iali')
    vheader.append('Ali. End')  # 7
    vheader_ids.append('jali')
    vheader.append('Model Start')  # 8
    vheader_ids.append('alihmmfrom')
    vheader.append('Model End')  # 9
    vheader_ids.append('alihmmto')
    vheader.append('Bit Score')  # 10
    vheader_ids.append('bitscore')
    vheader.append('Ind. E-value')  # 11
    vheader_ids.append('ievalue')
    vheader.append('Cond. E-value')  # 12
    vheader_ids.append('cevalue')
    vheader.append('Description')  # 13
    vheader_ids.append('alihmmdesc')

    # Complete header of attributes
    for vrecord in vrecords:
        vchild_id = vrecord[1]
        if vchild_id == 'domains':
            for vattribute in vrecord[2]:
                vfound = False
                for vheader_id in vheader_ids:
                    if vattribute == vheader_id:
                        vfound = True
                if not vfound:
                    vheader.append(vattribute)
                    vheader_ids.append(vattribute)

    # Get attribute values
    vnew_records = []
    for vrecord in vrecords:
        vchild_id = vrecord[1]
        if vchild_id == 'domains':
            vnew_record = []
            vattributes = vrecord[2]
            for vheader_id in vheader_ids:
                vattribute_found = False
                for va, attribute_value in enumerate(vrecord[3]):
                    if vattributes[va] == vheader_id:
                        vnew_record.append(attribute_value)
                        vattribute_found = True
                if not vattribute_found:
                    vnew_record.append('')
            vnew_records.append(vnew_record)
    return vheader, vnew_records


########################################################################################################################
#                                                                                                                      #
#  f_query_pfam                                                                                                        #
#  Runs a protein sequence through PFAM and gets the results as xml byte string. This is then reformulated as a tsv    #
#  result.                                                                                                             #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vseq [string]: Protein sequence.                                                                                #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - verrorcode [list]: Error code to check what is going on.                                                        #
#    - vheader [list]: The header of the records, indicating what is what.                                             #
#    - vrecords [list]: List of lists with every list being a domain, and every sublist an attribute of the domain     #
#                       record.                                                                                        #
#                                                                                                                      #
########################################################################################################################


# noinspection PyBroadException
def f_query_pfam(vseq, vsavefolder, vjobid):
    verrorcode = -1
    # Modify sequence
    vseq = ''.join(vseq.split())  # remove spaces within the sequence
    vseq = '>Seq\n' + vseq  # Format sequence for running through hmmer.

    # Run sequence through hmmer site
    vparameters = {'hmmdb': 'pfam', 'seq': vseq}
    vparameters_encoded = urllib.parse.urlencode(vparameters).encode('utf-8')
    vurllib_request_run = urllib.request.Request('https://www.ebi.ac.uk/Tools/hmmer/search/hmmscan',
                                                 vparameters_encoded)
    vperform_retrieval = True
    vperform_conversion = False
    vheader = []
    vrecords = []
    try:
        vresult_url = urllib.request.urlopen(vurllib_request_run).geturl()
    except HTTPError as e:
        vperform_retrieval = False
        verrorcode = e.code
        f_write_log(vsavefolder, vjobid, e.reason + '\n', 'a')
    except:
        vperform_retrieval = False
        verrorcode = -2

    if vperform_retrieval:
        vresult_parameters = {'format': 'xml'}
        vresult_parameters_encoded = urllib.parse.urlencode(vresult_parameters)
        vresult_url_with_parameters = vresult_url.replace('results', 'download') + '?' + vresult_parameters_encoded
        vurllib_request_result = urllib.request.Request(vresult_url_with_parameters)

        # Get results
        vperform_conversion = True
        vxml_result = ''
        try:
            vxml_result = urllib.request.urlopen(vurllib_request_result).read()
        except HTTPError as e:
            vperform_conversion = False
            if e.code == 500:
                verrorcode = -1  # Is ok, This means, that no domains were found.
            else:
                verrorcode = e.code
                f_write_log(vsavefolder, vjobid, e.reason + '\n', 'a')
        except:
            vperform_conversion = False
            verrorcode = -2

    # Modify results such that it comes in form of a table
    if vperform_conversion:
        vheader, vrecords = f_convert_hmmer_xml_tsv(vxml_result, 'string', vsavefolder, vjobid)
    return verrorcode, vheader, vrecords


########################################################################################################################
#                                                                                                                      #
#  f_write_pfam_prosite_db                                                                                             #
#  Writes the data base files for PFAM and Prosite to store previous results, to not overuse hmmer and prosite         #
#  websites.                                                                                                           #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vdbfiles [string]: Indicating the location of dbs.                                                              #
#    - vdbid [string]: Indicating the Id of the db that should be used (refers to the start of the protein.            #
#    - ventry_found [list]: Is the entry that should be saved. First item is the sequence itself.                      #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - no direct output                                                                                                #
#    - writes into the file vdbfiles_vdbid                                                                             #
#                                                                                                                      #
########################################################################################################################


def f_write_pfam_prosite_db(vdbfiles, vdbid, ventry_found, vsavefolder, vjobid, vcurrentdate):
    try:
        vdb_fh = open(vdbfiles + '_' + vdbid, 'a')
        for ve, entry in enumerate(ventry_found):
            vdb_fh.write(str(vcurrentdate))
            for vj, item2 in enumerate(entry):
                vdb_fh.write('\t' + str(item2))
            vdb_fh.write('\n')
            f_write_log(vsavefolder, vjobid, 'Wrote entry ' + str(ve + 1) + ' into DB ' + vdbid + '\n', 'a')
    except IOError:
        print('Can not write file ' + vdbfiles + '_' + vdbid)
        f_write_log(vsavefolder, vjobid, 'Can not write into DB file ' + vdbfiles + '_' + vdbid + '\nRun aborted\n',
                    'a')
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Can not write into DB file ' + vdbfiles + '_' + vdbid)
        sys.exit()
    vdb_fh.close()


########################################################################################################################
#                                                                                                                      #
#  f_write_pfam_prosite_res                                                                                            #
#  Writes the results files for PFAM and Prosite results.                                                              #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vfile [string]: Indicating the result file that should be written to.                                           #
#    - vitem [list]: Indicating the results that should be written.                                                    #
#    - ventry_found [list]: Is the entry that should be saved. First item is the sequence itself.                      #
#    - ispfam [boolean]: Indicates if the entry stems from PFAM (or otherwise it is Prosite).                          #
#    - isfromdb [boolean]: Indicates if the entry stems from a search or from a database file.                         #
#    - ventry_found [list]: Is the entry that should be saved. First item is the sequence itself.                      #
#    - vsavefolder [string]: Indicates the location of the folder where result files should be saved.                  #
#    - vjobid [string]: Id of the run. Is used to produce the output file names.                                       #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - no direct output                                                                                                #
#    - writes into the file vfile                                                                                      #
#                                                                                                                      #
########################################################################################################################


def f_write_pfam_prosite_res(vfile, vitem, ventry_found, ispfam, isfromdb, vsavefolder, vjobid):
    if ispfam:
        vdbname = 'PFAM'
    else:
        vdbname = 'Prosite'
    try:
        vdb_fh = open(vfile, 'a')
        if isfromdb:
            vwriteit = True
            for vj, item2 in enumerate(ventry_found):
                if vj == 1:
                    if item2 == '':
                        vwriteit = False
                    break
            if vwriteit:
                for vj, item2 in enumerate(ventry_found):
                    if vj == 0:
                        if ispfam:
                            vdb_fh.write(str(vitem))
                        else:
                            vitemt = vitem.lstrip(">")
                            vdb_fh.write(vitemt)
                    else:
                        vdb_fh.write('\t' + str(item2))
                vdb_fh.write('\n')
                f_write_log(vsavefolder, vjobid, 'Added entry 1 from ' + vdbname + ' DB.\n', 'a')
        else:
            for ve, entry in enumerate(ventry_found):
                vwriteit = True
                for vj, item2 in enumerate(entry):
                    if vj == 1:
                        if item2 == '':
                            vwriteit = False
                        break
                if vwriteit:
                    for vj, item2 in enumerate(entry):
                        if vj == 0:
                            if ispfam:
                                vdb_fh.write(str(vitem))
                            else:
                                vitemt = vitem.lstrip(">")
                                vdb_fh.write(vitemt)
                        else:
                            vdb_fh.write('\t' + str(item2))
                    vdb_fh.write('\n')
                    f_write_log(vsavefolder, vjobid, 'Added entry ' + str(ve + 1) + ' from ' + vdbname + ' results.\n',
                                'a')
    except IOError:
        print('Can not write file ' + vfile + '\nRun aborted.\n')
        f_write_log(vsavefolder, vjobid, 'Can not write ' + vdbname + ' output file: ' + vfile + '\n', 'a')
        # Write kill cookie
        f_write_cookie(-1, vsavefolder, vjobid, 'Could not write ' + vdbname + ' file.')
        sys.exit()
    vdb_fh.close()


########################################################################################################################
#                                                                                                                      #
#  f_dissect_prosite_key                                                                                               #
#  Reorders the individual outputs of the Prosite results depending on a here defined order. A total of 7 attributes   #
#  are collected.                                                                                                      #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vout [list]: Storing variable.                                                                                  #
#    - key[string]: Attribute of a prosite result.                                                                     #
#    - value [string]: Attribute value.                                                                                #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vout [list]: Modified storing variable.                                                                         #
#                                                                                                                      #
########################################################################################################################


def f_dissect_prosite_key(vout, key, value):
    if key == 'start':
        vout[1] = value
    elif key == 'stop':
        vout[2] = value
    elif key == 'signature_ac':
        vout[3] = value
    elif key == 'score':
        vout[4] = value
    elif key == 'level':
        vout[5] = value
    elif key == 'level_tag':
        vout[6] = value
    return vout


########################################################################################################################
#                                                                                                                      #
#  f_dissect_pfam_key                                                                                                  #
#  Reorders the individual outputs of the PFAM results depending on a here defined order. A total of 41 attributes     #
#  are collected.                                                                                                      #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vout [list]: Storing variable.                                                                                  #
#    - key[string]: Attribute of a PFAM result.                                                                        #
#    - value [string]: Attribute value.                                                                                #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vout [list]: Modified storing variable.                                                                         #
#                                                                                                                      #
########################################################################################################################


def f_dissect_pfam_key(vout, key, value):
    value = value.lstrip('"').rstrip('"')  # The xml attribute values come with leading and tailing '"'.
    if key == 'Family id':
        vout[1] = value
    elif key == 'Family Accession':
        vout[2] = value
    elif key == 'Clan':
        vout[3] = value
    elif key == 'Env. Start':
        vout[4] = value
    elif key == 'Env. End':
        vout[5] = value
    elif key == 'Ali. Start':
        vout[6] = value
    elif key == 'Ali. End':
        vout[7] = value
    elif key == 'Model Start':
        vout[8] = value
    elif key == 'Model End':
        vout[9] = value
    elif key == 'Bit Score':
        vout[10] = value
    elif key == 'Ind. E-value':
        vout[11] = value
    elif key == 'Cond. E-value':
        vout[12] = value
    elif key == 'Description':
        vout[13] = value
    elif key == 'outcompeted':
        vout[14] = value
    elif key == 'significant':
        vout[15] = value
    elif key == 'uniq':
        vout[16] = value
    # elif key == 'aliIdCount':
    #     vout[14] = value
    # elif key == 'aliL':
    #     vout[15] = value
    # elif key == 'aliM':
    #     vout[16] = value
    # elif key == 'aliN':
    #     vout[17] = value
    # elif key == 'aliSim':
    #     vout[18] = value
    # elif key == 'aliSimCount':
    #     vout[19] = value
    # elif key == 'aliaseq':
    #     vout[20] = value
    # elif key == 'alicsline':
    #     vout[21] = value
    # elif key == 'alihindex':
    #     vout[22] = value
    # elif key == 'alimline':
    #     vout[23] = value
    # elif key == 'alimmline':
    #     vout[24] = value
    # elif key == 'alimodel':
    #     vout[25] = value
    # elif key == 'alintseq':
    #     vout[26] = value
    # elif key == 'alippline':
    #     vout[27] = value
    # elif key == 'alirfline':
    #     vout[28] = value
    # elif key == 'alisqacc':
    #     vout[29] = value
    # elif key == 'alisqdesc':
    #     vout[30] = value
    # elif key == 'alisqfrom':
    #     vout[31] = value
    # elif key == 'alisqname':
    #     vout[32] = value
    # elif key == 'alisqto':
    #     vout[33] = value
    # elif key == 'bias':
    #     vout[34] = value
    # elif key == 'display':
    #     vout[35] = value
    # elif key == 'is_included':
    #     vout[36] = value
    # elif key == 'is_reported':
    #     vout[37] = value
    # elif key == 'oasc':
    #     vout[38] = value
    # elif key == 'outcompeted':
    #     vout[39] = value
    # elif key == 'significant':
    #     vout[40] = value
    # elif key == 'uniq':
    #     vout[41] = value
    return vout


########################################################################################################################
#                                                                                                                      #
#  f_reinitialize_dbs                                                                                                  #
#  Re-initializes the database running all current sequences in the database another time through the predictors. It   #
#  saves the new databases on a temporary folder and if an argument overwrite is given, it then replaces the old       #
#  databases at the given location.                                                                                    #
#                                                                                                                      #
#  Mandatory arguments:                                                                                                #
#    - vjobid_ri [string]: Id of the run. Is used to produce the output file names.                                    #
#    - vignoredb_ri [string] gets converted into True/False: Indicates whether previously gained results should be     #
#                                                            ignored                                                   #
#    - vsavefolder_ri [string]: Indicates the location of the folder where result files should be saved.               #
#    - vdbfolder_ri [string]: Indicates the location of the folder where the databases of previous results should be   #
#                             built up.                                                                                #
#    - vgroupfile_ri [string]: Indicates the location of a tsv file that contains the information about associations   #
#                              of proteins to their protein groups. First column is fasta headers second column are    #
#                              user defined group names.                                                               #
#    - vcolorfile_ri [string]: Indicates the location of a tsv file that contains the information about domain         #
#                              coloring. First column is the domain name, second column is a hex code for the color.   #
#    - vignoredomainfile_ri [string]: Indicates a file, with domains as rows. If a domain shows up in this file, it is #
#                                     not displayed on plots.                                                          #
#    - vcutoff_ri [string] gets converted into float: Defines if a domain should be displayed for a group of proteins. #
#                                                     Only if the domain surpasses the cutoff in relative abundance,   #
#                                                     it is displayed.                                                 #
#    - vmaxcutoff_ri [string] gets converted into float: Same as vcutoff, however, before the domain could exist       #
#                                                        anywhere in the protein. Here the domains need to be present  #
#                                                        at the same location to make the cut.                         #
#    - vcustom_scaling_on_ri [string] gets converted into boolean: Allows for custom scaling of the figure. The        #
#                                                                  standard case is that this is not on, and thus the  #
#                                                                  scaling is the same regardless of the size of the   #
#                                                                  protein. If this is on, one can set with option api #
#                                                                  (default 100 amino acids per inch) the number of    #
#                                                                  amino acids displayed per inch to scale the width   #
#                                                                  of the figure.                                      #
#    - vscalingfigure_ri [string] gets converted into float: Indicates the number of amino acids per inch that are     #
#                                                         displayed per inch of x-axis.                                #
#    - vabsolute_ri [string] gets converted into True/False: Indicates whether absolute numbers are displayed on the   #
#                                                            y-axis.                                                   #
#    - vwarnings_ri [string] gets converted into True/False: Indicates whether warnings are written out.               #
#    - vfrom_scratch_ri [0 or 1] gets converted into True/False: Indicates whether previous results should be          #
#                                                                discarded.                                            #
#    - vnotolderthan_ri [string] gets converted into int: Indicates the date that should be used as cutoff to load     #
#                                                         data from databases. If the storing date is older than the   #
#                                                         date given, the data is not observed.                        #
#    - vtemp_db_place_ri [string]: Indicates the location of the temporary databases to be built up.                   #
#                                                                                                                      #
#  Optional arguments:                                                                                                 #
#    - none                                                                                                            #
#                                                                                                                      #
#  Output:                                                                                                             #
#      - Prosite_db_[first five amino acids of sequence] [file]: TSV database files for sequences run through          #
#                                                                Prosite.                                              #
#      - Pfam_db_[first five amino acids of sequence] [file]: TSV database files for sequences run through PFAM.       #
#                                                                                                                      #
########################################################################################################################


def f_reinitialize_dbs(vjobid_ri, vignoredb_ri, vsavefolder_ri, vdbfolder_ri, vgroupfile_ri,
                       vcolorfile_ri, vignoredomainfile_ri, vcutoff_ri, vmaxcutoff_ri, vcustom_scaling_on_ri,
                       vscalefigure_ri, vabsoluteresults_ri, vwarnings_ri, vfrom_scratch_ri, vnotolderthan_ri,
                       vtemp_db_place_ri):

    # Create fasta input file from the databases
    vfastafile = join(vtemp_db_place_ri, vjobid_ri + '_reinitialize.fa')
    vfh_ri_out = open(vfastafile, 'w')

    # For all files starting with Prosite_db_
    vsequences = []
    vdb_files = [f for f in listdir(vdbfolder_ri) if isfile(join(vdbfolder_ri, f))]  # Get all files
    for vfile in vdb_files:  # For every file
        if vfile.startswith('Prosite_db_'):  # If it is a file from the Prosite_db_
            vfh_in = open(join(vdbfolder_ri, vfile), 'r')  # Open the file
            for vline in vfh_in:  # Read every line
                vsplit = vline.split('\t')  # Split by tabs
                vsequences.append(vsplit[0])  # Get the sequence entry
            vfh_in.close()  # Close file

    vsequences = list(set(vsequences))  # Make unique list of sequences
    for vs, vsequence in enumerate(vsequences):  # Go through all sequences and numerate them
        vfh_ri_out.write('>Seq_' + str(vs + 1) + '\n')  # Write header
        vfh_ri_out.write(vsequence)  # Write sequence
        if vs + 1 < len(vsequences):  # Don't add a new line character at the very end.
            vfh_ri_out.write('\n')
    vfh_ri_out.close()  # Close temporary Fasta file

    # Run propplot
    f_run_propplot(vjobid_ri, vfastafile, vignoredb_ri, vsavefolder_ri, vtemp_db_place_ri, vgroupfile_ri,
                   vcolorfile_ri, vignoredomainfile_ri, vcutoff_ri, vmaxcutoff_ri, vcustom_scaling_on_ri,
                   vscalefigure_ri, vabsoluteresults_ri, vwarnings_ri, vfrom_scratch_ri, vnotolderthan_ri)  # Run the
    # domain search

    print('Still has to be implemented')

    # Replace old databases with new ones
    shutil.rmtree(vdbfolder_ri)  # Remove old databases

    # Make the folder again
    try:  # Check if the db folder is present or if it can be created if it is not present.
        pathlib.Path(vdbfolder_ri).mkdir(parents=True, exist_ok=True)
    except IOError:
        print('Path ' + vdbfolder_ri + ' can not be created.')
        sys.exit()

    copy_tree(vtemp_db_place_ri, vdbfolder_ri)  # Replace old databases with new ones

    shutil.rmtree(vtemp_db_place_ri)  # Remove the temporary db folder

    shutil.rmtree(vsavefolder_ri)  # Delete result file folder

    print('Old database files have been updated.\n')


########################################################################################################################
#                                                                                                                      #
#  f_print_help                                                                                                        #
#  Prints the help page of propplot.py                                                                                 #
#  Can be activated by either running just propplot.py or propplot.py -h                                               #
#                                                                                                                      #
########################################################################################################################


def f_print_help():
    print('Function: propplot.py\n'
          'Function description:\n'
          'propplot is a script that takes protein sequences as an input, runs them through Prosite and PFAM and\n'
          'evaluates which predicted protein domains are existing in many of the proteins delivered and displays\n'
          'the results as a histogram, relative to the median of the protein length.\n'
          '\n'
          'Mandatory arguments:\n'
          '  -id [job_id]: Job id, used for output file names.\n'
          '  -in [file]: Fasta sequence file that contains the protein sequences that should be run.\n'
          '\n'
          'Optional arguments:\n'
          '  -idb [0 or 1]: Indicates if saved information should be ignored.\n'
          '  -w [0 or 1]: Indicates whether warnings should be given out.\n'
          '  -sf [folder]: Indicates the location of the folder that results are stored to.\n'
          '  -dbf [folder]: Indicates the location of db files.\n'
          '  -gf [file]: A tab separated file that contains the protein headers in column 1 and the groupings of\n'
          '              proteins in column 2.\n'
          '  -cf [file]: A tab separated file that contains the domain names in column 1 and the hex codes of colors\n'
          '              that the domains should be colored in in column 2.\n'
          '  -if [file]: A file that contains the domains in rows that should not be displayed.\n'
          '  -ar [0 or 1]: Indicates whether absolute or relative results should be used.\n'
          '  -cut [number between 0 and 1]: Indicates at what cutoff domains should be displayed. If more than -cut\n'
          '                                 proteins have the domain, it will be displayed.\n'
          '  -mcut [number between 0 and 1]: Indicates at what cutoff domains should be displayed, but is position\n'
          '                                  specific. Only domains that have a maximum prevalence at a relative\n'
          '                                  place in the protein group above this ratio are plotted (e.g. if value\n'
          '                                  is 0.5, 50% of the sequences have to have this domain at the same \n'
          '                                  relative position).\n'
          '  -cs [0 or 1]: Can set custom scaling of figure on (default is off = 0).\n'
          '  -api [number larger than 0]: Indicates the scaling of amino acids per inch of x axis that is used for\n'
          '                               figures.\n'
          '  -fs [0 or 1]: Indicates if previous results should be overwritten.'
          '\n'
          'Output:\n'
          'Note: Multiple outputs can be given, if more than one protein group exists.\n'
          '  - jobid_proteingroup_prosite.pdf [file]: Pdf plot for Prosite domains relative to the median length of\n'
          '                                           amino acid sequence of all proteins in the protein group.\n'
          '  - jobid_proteingroup_pfam.pdf [file]: Pdf plot as above, but for PFAM domains.\n'
          '  - jobid_proteingroup_combined.pdf [file]: Pdf plot for Prosite and PFAM domains.\n'
          '  - jobid_domain_color_file.txt [file]: Tsv of the domains and colors used in the plots. Can be modified\n'
          '                                        and funneled back into the script to modify colors. See vcolorfile\n'
          '                                        for structure.\n'
          '  - jobid_proteingroup_prosite.csv [file]: Results of Prosite for protein group.\n'
          '  - jobid_proteingroup_pfam.csv [file]: Results of PFAM for protein group.\n'
          '  - jobid_prosite_res.tsv [file]: Results of Prosite for this job.\n'
          '  - jobid_pfam_res.tsv [file]: Results of PFAM for this job.\n'
          '  - jobid_cookie[id] [file]: Cookie that shows that this part of code was processed. If cookie -1 shows\n'
          '                             up, the process was killed.\n'
          '\n'
          'Alternative Mode 1:\n'
          'Mandatory arguments:\n'
          '  -h: This help is printed.\n'
          '\n'
          'Output:\n'
          'Only this screen output.\n'
          '\n'
          'Alternative Mode 2:\n'
          'Mandatory arguments:\n'
          '  -ri [folder]: Reinitialize all databases and search them with the algorithms. Give a folder after the\n'
          '                parameter to suggest where temporary databases are built up. Old ones will be deleted.\n'
          '  -dbf [folder]: Indicates the location of db files.\n'
          '\n'
          'Optional arguments:\n'
          '  -w [0 or 1]: Indicates whether warnings should be given out.\n'
          '\n'
          'Output:\n'
          'New db files at old locations given by parameter -dbf.\n')

########################################################################################################################
#                                                                                                                      #
#  Usual entry point of the script.                                                                                    #
#  propplot is assumed to be started from the command line with arguments (optional and non-optional ones)             #
#  Please refer to the help (propplot -h) for more information
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":

    if len(sys.argv) <= 1:  # If only script name is given, print help
        f_print_help()
        sys.exit()
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        f_print_help()
        sys.exit()
    elif len(sys.argv) >= 2 and sys.argv[1] == '-ri':

        vjobid_main = 're_init'
        vwarnings_main = '0'
        vsavefolder_main = './re_init_temp_files/'
        vdbfolder_main = ''
        vinputfile_main = ''
        vgroupfile_main = ''
        vcolorfile_main = ''
        vignoredomainfile_main = ''
        vstandardcutoff_main = '0.05'
        vstandardmaxcutoff_main = '0.05'
        vcutoff_main = '0.05'
        vmaxcutoff_main = '0.05'
        vscalefigure_main = '1'
        vstandardscalefigure_main = '1'
        vcustom_scaling_on_main = '0'
        vabsoluteresults_main = '0'
        vignoredb_main = '1'
        vfrom_scratch_main = '1'  # get to do all data from scratch
        vtemp_db_place_main = ''
        vnotolderthan_main = '0'

        # Read out of arguments
        print('Reading arguments:')
        vi = 1
        while vi < len(sys.argv):
            if sys.argv[vi] == '-ri':  # reinitialize the databases, give temp save folder for temp databases.
                if len(sys.argv) == vi + 1:  # make sure that there is an argument after -ri.
                    print('To enter folder to save dbs temporarily, give a folder name after -ri.')
                    sys.exit()
                vtemp_db_place_main = sys.argv[vi + 1]
                vi += 1
            elif sys.argv[vi] == '-w':  # Indicates whether warnings should be given out.
                vwarnings_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == '0':
                    print('Warnings are off.')  # Produce Output that warnings are off.
                elif vwarnings_main != '1':  # Check that only 0 and 1 are options to be handed over.
                    print('Unknown warnings setting: ' + vwarnings_main)
                    sys.exit()
            elif sys.argv[vi] == '-dbf':  # Indicates the location of db files.
                if len(sys.argv) == vi + 1:  # make sure that there is an argument after -dbf.
                    print('To enter folder to save dbs, give a folder name after -dbf.')
                    sys.exit()
                vdbfolder_main = sys.argv[vi + 1]
                vi += 1
            vi += 1

        # Check if dbf was given else exit
        if vdbfolder_main == '':
            print('Option -dbs is mandatory, to be able to create the re-initialization file and replace the dbs.\n'
                  'Give a folder name after -dbf.')
            sys.exit()

        try:  # Check if the save folder is present or if it can be created if it is not present.
            pathlib.Path(vsavefolder_main).mkdir(parents=True, exist_ok=True)
        except IOError:
            print('Path ' + vsavefolder_main + ' can not be created.')
            sys.exit()
        try:  # Check if the db folder is present or if it can be created if it is not present.
            pathlib.Path(vdbfolder_main).mkdir(parents=True, exist_ok=True)
        except IOError:
            print('Path ' + vdbfolder_main + ' can not be created.')
            sys.exit()
        try:  # Check if the temporary db folder is present or if it can be created if it is not present.
            pathlib.Path(vtemp_db_place_main).mkdir(parents=True, exist_ok=True)
        except IOError:
            print('Path ' + vtemp_db_place_main + ' can not be created.')
            sys.exit()
        if vwarnings_main == 1:  # Give output about where the db location is, if warnings are on.
            print('Folder to save dbs: ' + vdbfolder_main)
        f_reinitialize_dbs(vjobid_main, vignoredb_main, vsavefolder_main, vdbfolder_main, vgroupfile_main,
                           vcolorfile_main, vignoredomainfile_main, vcutoff_main, vmaxcutoff_main,
                           vcustom_scaling_on_main, vscalefigure_main, vabsoluteresults_main, vwarnings_main,
                           vfrom_scratch_main, vnotolderthan_main, vtemp_db_place_main)
    else:
        # Define default parameters (see below or help for explanations)
        vjobid_main = ''
        vwarnings_main = '0'
        vsavefolder_main = ''
        vdbfolder_main = ''
        vinputfile_main = ''
        vgroupfile_main = ''
        vcolorfile_main = ''
        vignoredomainfile_main = ''
        vstandardcutoff_main = '0.05'
        vstandardmaxcutoff_main = '0.05'
        vcutoff_main = '0.05'
        vmaxcutoff_main = '0.05'
        vscalefigure_main = '1'
        vstandardscalefigure_main = '1'
        vcustom_scaling_on_main = '0'
        vabsoluteresults_main = '0'
        vignoredb_main = '0'
        vfrom_scratch_main = '0'
        vnotolderthan_main = '0'

        # Test that cutoffs were defined consistently.
        if vstandardcutoff_main != vcutoff_main:
            print('error in script, vstandardcutoff and vcutoff need to be the same.')
            sys.exit()
        if vstandardmaxcutoff_main != vmaxcutoff_main:
            print('error in script, vstandardmaxcutoff and vmaxcutoff need to be the same.')
            sys.exit()

        # Read out of arguments
        print('Reading arguments:')
        vi = 1
        while vi < len(sys.argv):
            if sys.argv[vi] == '-id':  # Job id, used for output file names.
                vjobid_main = sys.argv[vi + 1]
                vi += 1
            elif sys.argv[vi] == '-idb':  # Indicates if saved information should be ignored.
                vignoredb_main = sys.argv[vi + 1]
                vi += 1
            elif sys.argv[vi] == '-w':  # Indicates whether warnings should be given out.
                vwarnings_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == '0':
                    print('Warnings are off.')  # Produce Output that warnings are off.
                elif vwarnings_main != '1':  # Check that only 0 and 1 are options to be handed over.
                    print('Unknown warnings setting: ' + vwarnings_main)
                    sys.exit()
            elif sys.argv[vi] == '-sf':  # Indicates the location of the folder that results are stored to.
                if len(sys.argv) == vi + 1:  # make sure that there is an argument after -sf.
                    print('To enter folder to save files, give a folder name after savefolder or -save.')
                    sys.exit()
                vsavefolder_main = sys.argv[vi + 1]
                vi += 1
                try:  # Check if the folder is present or if it can be created if it is not present.
                    pathlib.Path(vsavefolder_main).mkdir(parents=True, exist_ok=True)
                except IOError:
                    print('Path ' + vsavefolder_main + ' can not be created.')
                    sys.exit()
                if vwarnings_main == 1:  # Give output about where the storing location is, if warnings are on.
                    print('Folder to save intermediate and output files: ' + vsavefolder_main)
            elif sys.argv[vi] == '-dbf':  # Indicates the location of db files.
                if len(sys.argv) == vi + 1:  # make sure that there is an argument after -dbf.
                    print('To enter folder to save dbs, give a folder name after -dbf.')
                    sys.exit()
                vdbfolder_main = sys.argv[vi + 1]
                vi += 1
                try:  # Check if the folder is present or if it can be created if it is not present.
                    pathlib.Path(vdbfolder_main).mkdir(parents=True, exist_ok=True)
                except IOError:
                    print('Path ' + vdbfolder_main + ' can not be created.')
                    sys.exit()
                if vwarnings_main == 1:  # Give output about where the db location is, if warnings are on.
                    print('Folder to save dbs: ' + vdbfolder_main)
            elif sys.argv[vi] == '-in':  # Fasta sequence file that contains the protein sequences that should be run.
                vinputfile_main = sys.argv[vi + 1]
                vi += 1
                try:  # check if file can be read.
                    vfh = open(vinputfile_main, 'r')
                except IOError:
                    print('Can not read ' + vinputfile_main)
                    sys.exit()
                vfh.close()
                if vwarnings_main == 1:  # Give output about where the fasta sequences are, if warnings are on.
                    print('Input file stored in: ' + vinputfile_main)
            elif sys.argv[vi] == '-gf':  # A file that contains the groupings of proteins.
                vgroupfile_main = sys.argv[vi + 1]
                vi += 1
                try:
                    vfh = open(vgroupfile_main, 'r')
                except IOError:
                    print('Can not read ' + vgroupfile_main)
                    sys.exit()
                vfh.close()
                if vwarnings_main == 1:
                    print('Group association information stored in: ' + vgroupfile_main)
            elif sys.argv[vi] == '-cf':  # A file that contains the coloring of domains.
                vcolorfile_main = sys.argv[vi + 1]
                vi += 1
                try:
                    vfh = open(vcolorfile_main, 'r')
                except IOError:
                    print('Can not read ' + vcolorfile_main)
                    sys.exit()
                vfh.close()
                if vwarnings_main == 1:
                    print('Domain color information stored in: ' + vcolorfile_main)
            elif sys.argv[vi] == '-if':  # A file that contains domains that should not be printed out.
                vignoredomainfile_main = sys.argv[vi + 1]
                vi += 1
                try:
                    vfh_main = open(vignoredomainfile_main, 'r')
                except IOError:
                    print('Can not read ' + vignoredomainfile_main)
                    sys.exit()
                vfh_main.close()
                if vwarnings_main == 1:
                    print('Information which domains to ignore stored in: ' + vignoredomainfile_main)
            elif sys.argv[vi] == '-ar':  # Indicates whether absolute or relative results should be used.
                vabsoluteresults_main = sys.argv[vi + 1]
                vi += 1
                if vabsoluteresults_main == '1':
                    if vwarnings_main == 1:
                        print('Using absolute results.')
                elif vabsoluteresults_main != '0':
                    print('Unknown option: ' + sys.argv[vi] + ' ' + sys.argv[vi + 1])
                    sys.exit()
            elif sys.argv[vi] == '-cut':  # Indicates at what cutoff domains should be displayed.
                vcutoff_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    print('Domain display threshold values: ' + vcutoff_main)
            elif sys.argv[vi] == '-mcut':  # Only domains that have a maximum prevalence at a relative place in the
                # protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have
                # this domain at the same relative position).
                vmaxcutoff_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    print('Domain display threshold values at bp level: ' + vmaxcutoff_main)
            elif sys.argv[vi] == '-api':  # Indicates the scaling of amino acids per inch.
                vscalefigure_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    print('Figure scale is 100pb per ' + vmaxcutoff_main + 'inch.')
            elif sys.argv[vi] == '-cs':  # Indicates the scaling of amino acids per inch.
                vcustom_scaling_on_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    if vcustom_scaling_on_main == '1':
                        print('Custom scaling is on.')
                    else:
                        print('Custom scaling is off.')
            elif sys.argv[vi] == '-fs':
                vfrom_scratch_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    print('All previous results ignored.')
            elif sys.argv[vi] == '-not':
                vnotolderthan_main = sys.argv[vi + 1]
                vi += 1
                if vwarnings_main == 1:
                    print('Results recovered from databases should not be older than ' + vnotolderthan_main + '.')
            vi += 1

        # Check if we give warnings.
        if vwarnings_main == '1':
            print('Warnings are on. Change warnings to be on (1) or off (0) by entering 1 or 0 after warning ' +
                  'or -w.')

        # Check if input can be read
        if vinputfile_main == '':
            print('Input file not set. use -in inputfile to set.')
            sys.exit()
        if vjobid_main == '':
            print('Job id not set with -id id.')
            sys.exit()

        # Check if we need to produce output about the change of cutoffs.
        if vstandardcutoff_main == vcutoff_main:
            if vwarnings_main == '1':
                print('Domains that do not occur in at least ' + str(float(vcutoff_main) * 100) +
                      '% of sequences are not shown. Change setting using -cut followed by a number between ' +
                      '0 and 1.')
        if vstandardmaxcutoff_main == vmaxcutoff_main:
            if vwarnings_main == '1':
                print('Domains that do not occur in at least ' + str(float(vmaxcutoff_main) * 100) +
                      '% of sequences at the same relative position are not shown. Change setting using ' +
                      '-mcut followed by a number between 0 and 1.')

        # Produce output in for whether absolute results are used or relative ones (default).
        if vabsoluteresults_main == '0':
            if vwarnings_main == '1':
                print('Using relative results. Change setting with -ar followed by 0 or 1.')

        # Produce output about the scaling of the figure
        if vstandardscalefigure_main == vscalefigure_main:
            if vwarnings_main == '1':
                print('Using standard figure scaling. Change setting with scalefigure or -api followed by a value '
                      'greater than 0 in combination with -cs 1.')

        # Run the script and produce the plots
        print('Running script:')
        f_run_propplot(vjobid_main, vinputfile_main, vignoredb_main, vsavefolder_main, vdbfolder_main, vgroupfile_main,
                       vcolorfile_main, vignoredomainfile_main, vcutoff_main, vmaxcutoff_main, vcustom_scaling_on_main,
                       vscalefigure_main, vabsoluteresults_main, vwarnings_main, vfrom_scratch_main, vnotolderthan_main)
