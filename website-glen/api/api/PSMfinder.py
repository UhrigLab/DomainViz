########################################################################################################################
#                                                                                                                      #
# PSMfinder is a function that uses a list of peptides that were modified to look up aminoacid sequences of fixed      #
# length in a translatome. It converts the list into a list of unmodified peptides, creates a blast database, uses     #
# blastp to find the unmodified peptides, and then searches for each modification and extracts the aminoacid sequences #
# of a fixed length around the modification. It then uses a list of unique aminoacid sequences to run MoMo, a software #
# free for Peptide motiv analysis (commercial use needs a license). The script has only two parts the __main__ which   #
# is the entry point of the script, handling in and out, and the script PSMfinder itself.                                                                    #
#                                                                                                                      #
########################################################################################################################
#
#
# Inputs (all mandatory, no additional input allowed):
#   vmod_peptides_file: Path to file that contains the modified peptides.
#   vmod_spec_file: Tab separated file that contains modifications. First column describes the modification (e.g. S*,
#                   T*, Y*, ...). Second column describes what the modified amino acid would look like if it were not
#                   modified (e.g. S, T, Y, ...). Third column describes if the modification is of interest or not (1 if
#                   of interest 0 if not). This column makes it easier to get rid of unwanted modifications and allows
#                   for avoiding pre-processing the modified peptide file. Make sure that more complex modifications are
#                   described first, because the modifications are searched in order of their occurfence. For example if
#                   ABC denotes modification Z and AB denotes modification Y, and the peptide sequence is ABCMLNABOP,
#                   then if the modifications are written such that the first line is AB[tab]Y[tab]1 and the second line
#                   isABC[tab]Z[tab]1 then the resulting unmodified peptide would be YCMLNYOP which is wrong. It should
#                   be ZMLNYOP. But since AB is first recognized, it gets replaced. Thus the first line needs to be
#                   ABC[tab]Z[tab]1 and the second line AB[tab]Y[tab]1, because ABC is more complex than AB.
#   vtranslatome_file: Path to file where translatome is saved in fasta format.
#   vrange: Number of AA that should be displayed up and downstream of a modification
#   voutput_file_name: Path to file that should be created with all the output.
#
# Outputs (none is handed over directly, only files):
#   File at the path specified with voutput_file_name containing all the results in tsv format. Organization
#     of the file: peptide id, modified peptide, unmodified peptide, position of modification, modification type, target
#     sequence the peptide was found, position where peptide is modified, sequence of peptide centered (if possible)
#     around the modification, extended sequence (using Xes to indicate where there was the border of the protein).
#   File at the path specified with voutput_file_name but with the ending '.momo.txt' which represents the input file
#     for MoMo (Cheng et al, 2019).
#   Folder at the path that the script is run called momo_out containing the output files of MoMo
#   Temporary files:
#     Blast database: (Temp_find_Pep.blastDB.phr, Temp_find_Pep.blastDB.pog, Temp_find_Pep.blastDB.psi,
#                      Temp_find_Pep.blastDB.pin, Temp_find_Pep.blastDB.psd, Temp_find_Pep.blastDB.psq)
#     TempPept.fa: File containing the peptides in fasta format using >TestPeptide1, >Testpeptide2, ... as headers.
#     TempPept.out: File containing the blastp output
#
# Call:
#   python PSMfinder.py [vmod_peptides_file] [vmod_spec_file] [vtranslatome_file] [vrange] [voutput_file_name]
#
# Author information:
# June 2019 - June 2020
# Pascal Schlapfer, Devang Mehta, R. Glen Uhrig

# Defining the function the actual handling of input and output (entry of the system) comes afterwards at if __name__


def PSMfinder(vmod_peptides_file, vmod_spec_file, vtranslatome_file, vrange, voutput_file_name):

    vverbose = 1 # standard setting for screen output is minimal (more screen output the higher the number)

    if not vrange.isdigit:  # test if the content of vrange (string) does not contain a digit (number).
        print('Error, Argument 4 is not a number.')
    else:
        vrange = int(vrange)

    # try: For error handling it is better to use try: than just writing import csv. If the import fails, because csv
    # was not previously installed, then you get an ugly error. This way you can test if it works, and if it fails it
    # generates a customized answer. The exception (errors) are indicated with the type of error (ImportError) is true
    # if the module could not be imported.

    # Test if csv can be loaded
    try:  # checks if the following code can be executed without exceptions (no errors).
        import csv  # Package to read symbol separated files
    except ImportError:  # If import fails and gives ImportError, then print out the below statement and end the code.
        print('Error, Module csv is required.')  # Error message.
        sys.exit()  # End script prematurely.

    # Test if re can be loaded
    try:  # see above
        import re  # Package to use regular expressions
    except ImportError:  # see above
        print('Error, Module re is required.')  # see above
        sys.exit()  # see above

    # Test if subprocesses can be run
    try:  # see above
        import subprocess  # Package to run system commands (bash)
    except ImportError:  # see above
        print('Error, Module subprocess is required.')  # see above
        sys.exit()  # see above

    # Test if blastp is installed on machine
    try:  # see above
        vres = subprocess.check_output(["which", "blastp"])  # this runs which[space]blastp, checks for its installation
        if vverbose >= 2:  # if vverbose set to level 2, then screen output is produced, else not.
            print('blastp installed')
            print(vres)  # print what usually would be displayed as screen output by blastp
    except subprocess.CalledProcessError:  # Error if the call of the line is giving out an error.
        print('Error, blastp needs to be installed or loaded before running script.')  # see above
        sys.exit()  # see above

    # I will omit the "# see above" from here. If I do not comment something, I have commented it above.

    # Test if makeblastdb is installed
    try:
        vres = subprocess.check_output(["which", "makeblastdb"])
        if vverbose >= 2:
            print('makeblastdb installed')
            print(vres)
    except subprocess.CalledProcessError:
        print('Error, blastp needs to be installed or loaded before running script.')
        sys.exit()

    # Test if momo is installed
    try:
        vres = subprocess.check_output(["which", "momo"])
        if vverbose >= 2:
            print('momo installed')
            print(vres)
    except subprocess.CalledProcessError:
        print('Error, momo needs to be installed or loaded before running script.')
        print('Visit http://meme-suite.org/doc/download.html/ to download momo.')
        print('Install with:')
        print('tar zxf meme-5.1.1.tar.gz')
        print('cd meme-5.1.1')
        print('./configure --prefix=$HOME/meme --with-url=http://meme-suite.org/ --enable-build-libxml2 --enable-build-libxslt')
        print('make')
        print('make test')
        print('make install')
        print('')
        print('Then add to permanent path:')
        print('export PATH=$HOME/meme/bin:$HOME/meme/libexec/meme-5.1.1:$PATH')
        sys.exit()

    # Read in Peptide Sequences
    if vverbose >= 1:
        print('Read in peptides:')
    try:
        vpeptides = open(vmod_peptides_file, 'r')  # This opens the file containing the peptides in read mode
        # vpeptides is the filehandle
    except IOError:  # If file does not exist or cannot be read (permission error)
        print(['Error, peptide file ' + vmod_peptides_file + ' not readable.'])
        sys.exit()

    vpeplist = []  # preparing the storing of all the modified peptides into a list for permanent availability
    for line in vpeptides:  # Go through content of the file vpeptides line by line
        vpeplist.append(line)  # Attach the latest line to the list of peptides.
    vpeptides.close()  # Close the filehandle (close the file)

    # Remove duplicates
    vpeplist = list(set(vpeplist))

    # Read in Modification identifiers and what they should be replaced with
    if vverbose >= 1:
        print('Read in modifications:')
    try:
        vmodifications = open(vmod_spec_file, 'r')  # Open the modification specification file
    except IOError:
        print(['Error, modifications file ' + vmod_spec_file + ' not readable.'])
        sys.exit()
    rd = csv.reader(vmodifications, delimiter="\t")  # read in using the csv reader, but using [tab] as a separator
    vmodlist = []  # prepare the list of modifications
    # This will contain three columns, first one contains the modifications, the second what the aminoacid should be,
    # the third if the user is interested in the modification or not.
    for row in rd:
        vmodlist.append(row)
    vmodifications.close()

    # Create a list of unmodified peptides and create a list of peptides with the modifications that we want to track
    if vverbose >= 1:
        print('Create list of unmodified peptides and remove uninteresting modifications:')
    vunmodpeplist1 = vpeplist  # initiate the unmodified peptide list
    vmodpeplist1 = vpeplist  # initiate the modified peptide list, containing only interesting modifications
    for row in vmodlist:  # for each modification, starting with the top line in the file
        vunmodpeplist2 = []  # create a new list, to save the modifications
        for item in vunmodpeplist1:  # for each peptide
            vunmodpeplist2.append(re.sub(re.escape(row[0]), re.escape(row[1]), item))  # apply the modification
            # re.escape makes sure that the string in row[0] or row[1] is used literally. This means wild cards such as
            # * are not interpreted as wildcards but as actual asterisk
        vunmodpeplist1 = vunmodpeplist2
        if int(row[2]) == 0:  # Only remove if it is marked as not interesting
            vmodpeplist2 = []
            for item in vmodpeplist1:
                vmodpeplist2.append(re.sub(re.escape(row[0]), re.escape(row[1]), item))
            vmodpeplist1 = vmodpeplist2

    # Measure length of unmodified peptideds
    vunmodpeplist1_len = []
    for item in vunmodpeplist1:
        vunmodpeplist1_len.append(len(str(item.rstrip())))  # rstrip removes all new line characters

    # Create a blast db of the translatome
    if vverbose >= 1:
        print('Create blast db of translatome Temp_find_Pep.blastDB: ')
    try:
        vproteome = open(vtranslatome_file, 'r')
    except IOError:
        print(['Error, proteome file ' + vtranslatome_file + ' not readable.'])
        sys.exit()
    vproteome.close()

    try:
        vres = subprocess.check_output(['makeblastdb', '-in', vtranslatome_file, '-parse_seqids', '-dbtype', 'prot',
                                        '-out', 'Temp_find_Pep.blastDB'])
        if vverbose >= 3:  # if level 3 output is activated, write out the output of the makeblastdb call (vres)
            print('Ran makeblastdb')
            print(vres)
    except subprocess.CalledProcessError:
        print('Error, makeblastdb did not run properly.')
        sys.exit()

    # Combine sequences of peptides into one fasta file named TempPept.fa
    if vverbose >= 1:
        print('Combine peptides into fasta file TempPept.fa:')
    try:
        vtestfile = open('TempPept.fa', 'w')  # Open file in writing mode
    except IOError:
        print('Error, can not write temporary file TempPept.fa.')
        sys.exit()
    vpep = 0  # prepare Peptide counter
    for vitem in vunmodpeplist1:
        vpep += 1  # Count for every peptide up.
        vline = '>TestPeptide' + str(vpep) + '\n'  # Create the header of the peptide, e.g. >TestPeptide1
        vtestfile.write(vline)  # write the header
        vline = vitem + '\n'  # Create the peptide information (add a new line character at the end of the peptide).
        vtestfile.write(vline)
    vtestfile.close()  # close the file that is written to.

    # For each Peptide, blast the peptide against the translatome
    if vverbose >= 1:
        print('Perform blastp producing TempPept.out:')
    try:
        vres = subprocess.check_output(['blastp', '-query', 'TempPept.fa', '-db', 'Temp_find_Pep.blastDB', '-out',
                                        'TempPept.out', '-outfmt', '6 qseqid sseqid pident length sstart', '-ungapped',
                                        '-comp_based_stats', 'F'])
        # Perform blast call using tabular format with query sequence id, target sequence id, percent identity, query
        # coverage, and sequence start as attributes to be written out.
        if vverbose >= 3:
            print('Ran blastp')
            print(('Command: blastp -query TempPept.fa -db Temp_find_Pep.blastDB -out TempPept.out -outfmt "6 qseqid '
                   'sseqid pident qcovs sstart" -ungapped -comp_based_stats F'))  # makes it easier for the user to see
            # what was blasted.
            print(vres)
    except subprocess.CalledProcessError:
        print('Error, blastp call did not run properly.')
        sys.exit()

    # Read in blast results
    if vverbose >= 1:
        print('Read in blastp results:')
    try:
        vblastresults = open('TempPept.out', 'r')
    except IOError:
        print('Can not read temporary blast results TempPept.out')
        sys.exit()
    rd = csv.reader(vblastresults, delimiter="\t")
    vbr = []  # Prepare the storing of all blastp results
    for row in rd:
        vbr.append(row)
    vblastresults.close()
    if vverbose >= 2:
        print('Number of blastp hits: ' + str(len(vbr)))  # prints out the number of results that were found by blastp

    # Remove results that do not have 100% identity and 100% length
    if vverbose >= 1:
        print('Remove results if not 100% identitiy or not 100% coverage:')
    vbr2 = []  # Prepare the storing of the subset of results that follow above rules.
    for row in vbr:
        # check first for 100% identity and also for 100% of coverage
        # the latter expression compares the fourth row (length) against the length computed for the same peptide
        if float(row[2]) == 100 and int(row[3]) == vunmodpeplist1_len[int(re.sub('TestPeptide', '', row[0])) - 1]:
            vbr2.append(row)
    if vverbose >= 2:
        print('Number of blastp hits with 100% identity and 100% coverage: ' + str(len(vbr2)))

    # Read in proteome
    if vverbose >= 1:
        print('Read in translatome:')
    vproteome = open(vtranslatome_file, 'r')  # open translatome fasta file.
    vheader = []  # Prepare storing of header of proteins
    vbody = []  # Prepare storing of protein sequences
    vinit = 1  # indicate that the first time a header appears, there is no body that needs to be written
    vcollect = []  # Prepare storing of the proteinsequence that is typically split over several lines.
    vrid = 0  # This is the row of the file, to do debugging, when vverbose is larger than 2.
    for row in vproteome:
        if vverbose >= 5:
            vrid += 1
            print('Processing translatome line ' + str(vrid))  # Print out current line of the file
        if row.startswith(">"):  # check for header lines.
            if vinit == 0:  # if it is not the first header, then append the protein sequence that was collected to body
                vbody.append(re.sub('[*]?', '', vcollect))  # re.sub replaces all stars (protein end) with nothing.
            vheader.append(row)  # store the header information
            vcollect = ''  # reset the collection of the protein sequence
            vinit = 0  # reset that all further headerlines are not the first ones, and the body needs to be recorded
        else:  # if it is body information (protein sequence)
            vcollect = str(vcollect) + row.rstrip()  # extend already present protein information with the new info.
            # Remove trailing new line characters.
    vbody.append(vcollect)  # Record the last protein sequence in the file
    vproteome.close()
    if vverbose >= 2:
        print('Number of proteins in translatome: ' + str(len(vbody)))  # Print out the number of protein sequences.

    # Prepare Outputfile
    if vverbose >= 1:
        print('Prepare Outputfile:')
    try:
        voutputfile = open(voutput_file_name, 'w')  # Try to open the output file in writing mode
    except IOError:
        print('Can not write output file ' + str(voutput_file_name))
        sys.exit()

    # For each result, expand to up and down stream range. If range is overreaching end, fill in with filler (X)
    if vverbose >= 1:
        print('Combine results and extract sequences and write Outputfile:')
        print(len(vbr2))
    vrid = 0  # prepare counter in case vverbose is 3, this is used.
    if len(vbr2) > 0:
        # Write header if there is at least one result
        vwriteline = 'Peptide id\tModified peptide\tUnmodified peptide\tRelative position of modification in peptide' \
                     '\tModification\tProtein id where peptide can be found\tAbsolute position of modification in ' \
                     'Protein\tMax ' + str(vrange) + 'AA window\tOver extended ' + str(vrange) + 'AA window\n'
        voutputfile.write(vwriteline)  # write the line.
    vsequenceext_collect = []  # prepare saving space for momo input
    for row in vbr2:
        if vverbose >= 5:
            vrid += 1  # count the number of row one up
            print('Processing result ' + str(vrid) + ' of ' + str(len(vbr2)))  # Give screen output about current row
        vindex = [i for i, x in enumerate(vheader) if '>' + row[1] + ' ' in x]  # this makes a list of headers and a
        # list of numbers representing the headers. It then checks for every item (x and i, where x is the current
        # header and i is the internal number of that current headers entry) if it is the same as in the blast result
        # sequence id. if there is a match, save the number = index.
        vcurrpep = vmodpeplist1[int(re.sub('TestPeptide', '', row[0])) - 1]  # Take the query id, remove TestPeptide.
        # This results in the number of the TestPeptide. This number minus one is the index of the testpeptide stored in
        # vmodpeplist1. This peptide is stored as the current peptide that is looked at. It has modifications.

        vnothingfound = 0  # This is used to indicate if in the last iteraction of the while loop below, there was some
        # finding of modifications
        while vnothingfound == 0:  # indicate that as long as something is found, continue to search for something else.
            vid = []  # This is the list of positions where modifications occur.
            for row2 in vmodlist:  # go through all possible types of modifications
                if row2[2] == '1':  # if the modification type is of interest (last row in the file is a 1) then try to
                    # find the modification
                    vpos = vcurrpep.find(row2[0])  # find the first occurence of the modification
                    if vpos == -1:  # if the position is -1, the modification is not found. if so, change the number to
                        # an arbitrary large number so that when using min the modifcation that occurs first can be
                        # found.
                        vpos = 1000000000  # if modification was not found set to huge number.
                else:  # If the modification is of no interest, set the position to arbitrary huge number.
                    vpos = 1000000000
                vid.append(vpos)  # Add position to the list of positions of modifications.
            minvid = min(vid)  # get the position that occurs the first on the peptide (when looking from the left)
            if minvid == 1000000000:  # if the minimal position is the arbitrary number, there is no modification left
                # to find in this peptide
                vnothingfound = 1
            else:  # if there is a position, then
                vitem = [i for i, x in enumerate(vid) if x == minvid]  # find the modification type
                vcurrmod = vmodlist[vitem[0]]  # record the current modification
                vcurrpep = vcurrpep.replace(vcurrmod[0], vcurrmod[1], 1)  # replace the current modification with the AA
                # that is not modified
                vsstart = row[4]  # record the start of the peptide in the target sequence
                vcurrbody = vbody[vindex[0]]  # record the amino acid sequence of the target sequence
                vlenbody = len(vcurrbody)  # record the length of the amino acid sequence of the target sequence
                vrelpos = minvid + 1  # record the relative position of the modification in the peptide
                vabspos = int(vsstart) + vrelpos - 1  # record the absolute position of the modification in the target
                # sequence
                vsequenceext = ''  # generate the placeholder for recording the extended sequence around the
                # modification
                vsequence = ''  # generate the placeholder for recording the sequence around the modification

                if vabspos >= vrange + 1 and vabspos + vrange <= vlenbody:  # if the modified AA and the surrounding
                    # sequence defined by the vrange is completely within the protein sequence
                    vsequenceext = vcurrbody[vabspos - vrange - 1:vabspos + vrange]  # record the surrounding sequence
                    # of the position with extensions (which here are not necessary)
                    vsequence = vcurrbody[vabspos - vrange - 1:vabspos + vrange]  # record the surrounding sequence of
                    # the modified position
                elif vabspos < vrange + 1 and vabspos + vrange <= vlenbody:  # if the modified AA is very close to the
                    # start of the protein, then record the start and extend the extended sequence with the necessary
                    # number of amino acids denoted as X
                    vmiss_x_start_len = abs(vabspos - 1 - vrange)  # check how many AA are missing at the start
                    vmiss_x_start = 'X' * vmiss_x_start_len  # Create the sequence of AAs in X
                    vsequenceext = vmiss_x_start + vcurrbody[0:(vabspos + vrange)]  # combine the sequence and the
                    # extension
                    vsequence = vcurrbody[0:(vabspos + vrange)]  # record the sequence only
                elif vabspos >= vrange + 1 and vabspos + vrange > vlenbody:  # same as above, but here it checks if the
                    # modified position is close to the end of the protein
                    vmiss_x_end_len = (vabspos + vrange) - vlenbody  # check how many AAs are missing at the end
                    vmiss_x_end = 'X' * vmiss_x_end_len
                    vsequenceext = vcurrbody[vabspos - vrange - 1:vabspos + vrange - vmiss_x_end_len] + vmiss_x_end
                    vsequence = vcurrbody[vabspos - vrange - 1:vabspos + vrange - vmiss_x_end_len]
                elif vabspos < vrange + 1 and vabspos + vrange > vlenbody:  # if it is a very short protein, and the
                    # modification is both close to the beginning and the end
                    vmiss_x_end_len = (vabspos + vrange) - vlenbody
                    vmiss_x_end = 'X' * vmiss_x_end_len
                    vmiss_x_start_len = abs(vabspos - 1 - vrange)
                    vmiss_x_start = 'X' * vmiss_x_start_len

                    # Short proteins never occurred, therefore this part of the code was not tested and in case it
                    # occurs, it needs to be revised. Thus there is a sys.exit() at the end to prematurely end the code.
                    print('Attention: this part of code was not tested because it did not occur in the original data.')
                    print('Check if correct Sequence. Please contact author of script.')
                    print('Result:\n' + str(row))
                    print('Peptide:\n' + str(vcurrpep))
                    print('Sequence start: ' + str(vsstart))
                    print('Body:\n' + str(vcurrbody))
                    print('Length of body: ' + str(vlenbody))
                    print('Relative position: ' + str(vrelpos))
                    print('Absolute position: ' + str(vabspos))
                    print('Sequence: ' + vmiss_x_start + vcurrbody[0:vabspos + vrange - vmiss_x_end_len] + vmiss_x_end)
                    # vsequenceext = vmiss_x_start + vcurrbody[0:vabspos + vrange - vmiss_x_end_len] + vmiss_x_end
                    # vsequence = vcurrbody[0:vabspos + vrange - vmiss_x_end_len]
                    sys.exit()
                # Peptide id, modified peptide, unmodified peptide, position, modification, Target, position, Sequence,
                # extended sequence
                vwriteline = row[0] + '\t' + str(vmodpeplist1[int(re.sub('TestPeptide', '', row[0])) - 1]).rstrip() + \
                    '\t' + vunmodpeplist1[int(re.sub('TestPeptide', '', row[0])) - 1].rstrip() + '\t' + str(vrelpos)\
                    + '\t' + str(vcurrmod[0]) + '\t' + row[1] + '\t' + str(vabspos) + '\t' + vsequence + '\t' + \
                    vsequenceext + '\n'  # compose the line, according to above attributes.
                vsequenceext_collect.append(vsequenceext)  # attach the extended peptide.
                voutputfile.write(vwriteline)  # write the line.
    voutputfile.close()  # close output file
    vsequenceext_collect_unique = list(set(vsequenceext_collect))

    # Prepare Inputfile for momo
    vmomo_input_file_name = voutput_file_name + '.momo.txt'  # Create filename
    if vverbose >= 1:
        print('Prepare input file for momo:')
    try:
        vmomoinputfile = open(vmomo_input_file_name, 'w')  # Try to open the output file in writing mode
    except IOError:
        print('Can not write output file ' + str(vmomo_input_file_name))
        sys.exit()

    # Add all unique peptides to the file
    for row in vsequenceext_collect_unique:
        vmomoinputfile.write(row + '\n')

    vmomoinputfile.close()  # close momo input file

    # Run momo
    vmomowidth = vrange * 2 + 1
    if vverbose >= 1:
        print('Perform momo using ' + vmomo_input_file_name + ':')
    try:
        vres = subprocess.check_output(['momo', 'motifx', '--width', str(vmomowidth), '--protein-database', vtranslatome_file,
                                        '--remove-unknowns', 'F', vmomo_input_file_name])
        # Perform blast call using tabular format with query sequence id, target sequence id, percent identity, query
        # coverage, and sequence start as attributes to be written out.
        if vverbose >= 3:
            print('Ran momo')
            print(('Command: momo motifx --width ' + str(vmomowidth) + ' --protein-database ' + vtranslatome_file + ' --remove-unknowns F ' + vmomo_input_file_name))  # makes it easier for the user to see
            # what was blasted.
            print(vres)
    except subprocess.CalledProcessError:
        print('Error, momo call did not run properly.')
        sys.exit()

    print('Code ran successfully.')  # give some statement that code ran sucessfully


# The below function represents the actual entry of the system
# This tests if the number of arguments were correct and if the system is linux


if __name__ == "__main__":

    # test if sys is installed in python
    try:
        import sys
    except ImportError:
        print('Error, module sys is required.')
        exit()
    if len(sys.argv) != 6:  # Test if number of arguments is 5 (the function itself is also argument)
        print('Error, number of arguments is not 5. Need to give File of Peptides, File of modifications, Proteome '
              'file number of up and downstream AA, Outfilename.')
        sys.exit()
    v1 = sys.argv[1]  # Store arguments
    v2 = sys.argv[2]
    v3 = sys.argv[3]
    v4 = sys.argv[4]
    v5 = sys.argv[5]
    PSMfinder(v1, v2, v3, v4, v5)  # Call of the function
