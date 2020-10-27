###############################################################
#  Please look at the end for the entry point of the script.  #
###############################################################
########################################################################################################################
#                                                                                                                      #
#  f_process_results                                                                                                   #
#  prints the help page of propplot.py                                                                                 #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vfolder: String. Folder where fasta sequences are kept                                                          #
#    - voutputlead: String. Filename start of fasta file that can be loaded to Prosite or PFAM                         #
#    - vprositefile: String. Full file and location of prosite results                                                 #
#    - vpfamfile: String. Full file and location of pfam results                                                       #
#    - vgroupfile: String. Full file and location of the group file. A tsv file where in the first column, there is    #
#                  the header of the fasta files the second column of the file describes the protein group.            #
#    - vcolorfile: String. Full file and location of the color file. A tsv file where in the first column, there is    #
#                  the domain name, then the second column represents a hexcode of color, e.g. #ffffff                 #
#    - vignoredomainfile: String. Full file and location of the ignore domain file. A file where every line is a       #
#                         domain name. If the name is present, the domain will not be printed.                         #
#    - vabsolute: 
#    - vcutoff
#    - vmaxcutoff
#    - vscalingfigure
#    - vwarnings
#    - vsavefolder
#                                                                                                                      #
#  Output:                                                                                                             #
#    - files:                                                                                                          #
#      - per domain one pdf plot for Prosite domains, one for PFAM domains, and one combined plot for both types of    #
#        domains.                                                                                                      #
#                                                                                                                      #
########################################################################################################################


def f_run_propplot(vjobid, vinputfile, vignoredb, vsavefolder, vdbfolder, vgroupfile, vcolorfile, vignoredomainfile, vcutoff, vmaxcutoff, vscalingfigure , vabsolute, vwarnings):
    vabsolute = int(vabsolute)
    vcutoff = float(vcutoff)
    vmaxcutoff = float(vmaxcutoff)
    vscalingfigure = float(vscalingfigure)
    vwarnings = int(vwarnings)
    vignoredb = int(vignoredb)


    # Read in headers and sequences that were used to produce the prosite and or pfam results
    vheaders, vsequences = f_read_in_file(vinputfile)
    print('Headers: ' + str(len(vheaders)) + ', Sequences: ' + str(len(vsequences)))

    # Get Prosite results
    vprositefile = join(vsavefolder, vjobid + '_prosite_res.tsv')
    try:
        vfh = open(vprositefile,'r')
        vProsite_already_done = True
        vfh.close()
    except IOError:
        vProsite_already_done = False

    vProsite_already_done = False
    if vProsite_already_done == False:
        vfh = open(vprositefile, 'w')
        vfh.close()
        vLenDBID = 5
        if vdbfolder == '':
            vDBFiles = 'Prosite_db'
        else:
            vDBFiles = join(vdbfolder, 'Prosite_db')
        for vi, vitem in enumerate(vheaders):
            vFound = False
            if vignoredb == 0:
                vDBID = vsequences[vi][0:vLenDBID]
                try:
                    vfh = open(vDBFiles + '_' + vDBID, 'r')
                    for ventry in vfh:
                        ventry = ventry.rstrip('\n')
                        vsplitentry = ventry.split('\t')
                        if vsequences[vi] == vsplitentry[0]:
                            vFound = True
                            f_write_pfam_prosite_res(vprositefile, vitem, vsplitentry, 1, False, True)
                except IOError:
                    if vwarnings == 1:
                        print(vDBFiles + '_' + vDBID + ' does not yet exist.')

            if vFound == False:
                ventry_found, vnentry_found = f_run_sequences_through_prosite(vitem, vsequences[vi])
                f_write_pfam_prosite_db(vDBFiles, vDBID, ventry_found, vnentry_found)
                f_write_pfam_prosite_res(vprositefile, vitem, ventry_found, vnentry_found, False, False)

    vprositedata = f_read_tsv(vprositefile)

    # Get PFAM results
    vpfamfile = ''


    #vpfamfile = join(vsavefolder, vjobid + '_pfam_res.tsv')
    #try:
    #    vfh = open(vpfamfile,'r')
    #    vPFAM_already_done = True
    #    vfh.close()
    #except IOError:
    #    vPFAM_already_done = False
    #
    #vPFAM_already_done = False
    #if vPFAM_already_done == False:
    #    vfh = open(vpfamfile, 'w')
    #    vfh.write(
    #        'seq id  alignment start alignment end   envelope start  envelope end    hmm acc hmm name        hmm start       hmm end hmm length      bit score       Individual E-value      Conditional E-value     database significant    outcompeted     clan\n')
    #    vfh.close()
    #
    #    vLenDBID = 5
    #    if vdbfolder == '':
    #        vDBFiles = 'PFAM_db'
    #    else:
    #        vDBFiles = join(vdbfolder, 'PFAM_db')
    #    for vi, vitem in enumerate(vheaders):
    #        vFound = False
    #        if vignoredb == 0:
    #            vDBID = vsequences[vi][0:vLenDBID]
    #            try:
    #                vfh = open(vDBFiles + '_' + vDBID, 'r')
    #                for ventry in vfh:
    #                    ventry = ventry.rstrip('\n')
    #                    vsplitentry = ventry.split('\t')
    #                    if vsequences[vi] == vsplitentry[0]:
    #                        vFound = True
    #                        f_write_pfam_prosite_res(vpfamfile, vitem, vsplitentry, 1, True, True)
    #                vfh.close()
    #            except IOError:
    #                if vwarnings == 1:
    #                    print(vDBFiles + '_' + vDBID + ' does not yet exist.')
    #        if vFound == False:
    #            ventry_found, vnentry_found = f_run_sequences_through_pfam(vitem, vsequences[vi])
    #            print('Entries: ' + str(vnentry_found))
    #            print(ventry_found)
    #            f_write_pfam_prosite_db(vDBFiles, vDBID, ventry_found, vnentry_found)
    #            f_write_pfam_prosite_res(vpfamfile, vitem, ventry_found, vnentry_found, True, False)
    #
    #vpfamdata = f_read_tsv(join(vsavefolder, vpfamfile))

    # Get groups of proteins
    if vgroupfile == '':  # Default case, if no group association file is handed over.
        vgroup = []
        vgroup_u = []
        for vitem in vheaders:
            vgroup.append('ProteinGroup')
            vgroup_u.append('ProteinGroup')
    else:
        vgroup, vgroup_u = f_read_in_groupfile(vgroupfile, vheaders)
    vgroup_u = list(set(vgroup_u))

    # Per group of protein: get median sequence length
    vmedlengroup = []
    for vgitem in vgroup_u:
        vlenproteins = []
        for vg, vitem in enumerate(vgroup):
            if vitem == vgitem:
                vlenproteins.append(len(vsequences[vg]))
        vmedlengroup.append(median(vlenproteins))

    # Get specific coloring
    if vcolorfile != '':
        vcolor_domain, vcolor_hexcode = f_read_in_colorfile(vcolorfile)
    else:
        vcolor_domain = []
        vcolor_hexcode = []

    # Get list of domains to ignore
    if vignoredomainfile != '':
        vignore_domain = f_read_in_ignoredomainfile(vignoredomainfile)
    else:
        vignore_domain = []

    # Get unique list of Prosite domains
    if vprositefile != '':
        vprositedomains_u = []
        for vprdc in range(len(vprositedata.columns)):
            print(vprdc)
            vprositedomains_u.append(vprositedata[vprdc][3])
        vprositedomains_u = list(set(vprositedomains_u))
        vprositedomains_u_color = []
        vprositedomains_u_ignore = []
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

    # Get unique list of Pfam domains
    if vpfamfile != '':
        vpfamdomains_u = []
        for vpdc in range(1, len(vpfamdata.columns)):
            vpfamdomains_u.append(vpfamdata[vpdc][6])
        vpfamdomains_u = list(set(vpfamdomains_u))
        vpfamdomains_u_color = []
        vpfamdomains_u_ignore = []
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

    # Remove beginning ('>') from fasta
    vheaders_no_fastastart = []
    for vitem in vheaders:
        vheaders_no_fastastart.append(vitem.lstrip('>'))

    # Per group of protein: get annotations of Prosite and PFAM domains and make one plot per protein group.
    for vug, vgitem in enumerate(vgroup_u):  # Go through all groups of proteins
        vn_prot_per_group = 0  # Initialize the counting of sequences per group
        if vprositefile != '':
            vprositedomainsofgroup = np.zeros((len(vprositedomains_u), vmedlengroup[vug]), dtype=float)  # Initialize with
            # number of unique prosite domains and median length of proteins
            vprositedomainsingenes = np.zeros((len(vprositedomains_u), len(vheaders)), dtype=int)  # Stores if a domain
            # has been found for a gene
        if vpfamfile != '':
            vpfamdomainsofgroup = np.zeros((len(vpfamdomains_u), vmedlengroup[vug]), dtype=float)  # Initialize with number
            # of unique prosite domains and median length of proteins
            vpfamdomainsingenes = np.zeros((len(vpfamdomains_u), len(vheaders)), dtype=int)  # Stores if a domain has been
            # found for a gene
        for vh, vitem in enumerate(vheaders_no_fastastart):  # Go through all sequences
            if vgroup[vh] == vgitem:  # If the sequence has the same group association as is currently searched
                vn_prot_per_group = vn_prot_per_group + 1  # Count the number of sequence per this group up by one

                if vprositefile != '':
                    # Process Prosite
                    for vi in range(len(vprositedata.columns)):  # go through all prosite data
                        if vprositedata[vi][0] == vitem:  # If the prosite data is about the sequence we currently look at
                            for vp, vpd in enumerate(vprositedomains_u):  # Go through all domains
                                if vprositedata[vi][3] == vpd:  # If the domain is the domain we currently look at
                                    vprositedomainsofgroup[vp, (int(vprositedata[vi][1]) - 1):(int(vprositedata[vi][2])
                                                                                               - 1)] += 1  # Mark the
                                    # placing of the domain
                                    vprositedomainsingenes[vp, vh] = 1  # Define that the domain has been found for that
                                    # gene
                if vpfamfile != '':
                    # Process PFAM
                    for vi in range(len(vpfamdata.columns)):  # Go through all pfam data
                        if vpfamdata[vi][0] == vitem:  # If the pfam data is about the sequence we currently look at
                            for vp, vpd in enumerate(vpfamdomains_u):  # Go through all domains
                                if vpfamdata[vi][3] == vpd:  # If the domain is the domain we currently look at
                                    vpfamdomainsofgroup[vp, (int(vpfamdata[vi][1]) - 1):(int(vpfamdata[vi][2]) - 1)] += 1
                                    #  Mark the placing of the domain
                                    vpfamdomainsingenes[vp, vh] = 1  # Define that the domain has been found for that gene
        if vprositefile != '':
            vsize_of_prosite_data = vprositedomainsofgroup.shape
        if vpfamfile != '':
            vsize_of_pfam_data = vpfamdomainsofgroup.shape

        # Normalization of data
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

        # If not using absolute values
        if vabsolute == 0:
            if vprositefile != '':
                vprositedomainsofgroup = vprositedomainsofgroup_rel
            if vpfamfile != '':
                vpfamdomainsofgroup = vprositedomainsofgroup_rel

        # Save of data
        if vprositefile != '':
            if vsavefolder != '':
                np.savetxt(join(vsavefolder, vjobid + '_' + vgitem + '_prosite.csv'), vprositedomainsofgroup, delimiter="\t")
            else:
                np.savetxt(vjobid + '_' + vgitem + '_prosite.csv', vprositedomainsofgroup, delimiter="\t")
        if vpfamfile != '':
            if vsavefolder != '':
                np.savetxt(join(vsavefolder, vjobid + '_' + vgitem + '_pfam.csv'), vpfamdomainsofgroup, delimiter="\t")
            else:
                np.savetxt(vjobid + '_' + vgitem + '_pfam.csv', vpfamdomainsofgroup, delimiter="\t")

        # Plot data of Prosite
        if vprositefile != '':
            print('Plot data of Prosite for ' + vgitem)
            vstandardwidth = 10
            vstandardheight = 8
            vpaddingwidth = 1.0
            vpaddingheight = 0.7
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth), Size.Fixed(vscalingfigure * vmedlengroup[vug] / 100)]
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
            if vsavefolder != '':
                vfh = open(join(vsavefolder, vgitem + '_prosite_colors.txt'), 'w')
            else:
                vfh = open(vgitem + '_prosite_colors.txt', 'w')
            for vi in vmaxids:
                if max(vprositedomainsofgroup_rel[vi]) > (vmaxcutoff * 100) and \
                        float(sum(vprositedomainsingenes[vi]))/float(vn_prot_per_group) > vcutoff and \
                        vprositedomains_u_ignore[vi] == 0:
                    if vprositedomains_u_color[vi] == '':
                        vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vi], width=1, alpha=0.7,
                                          label=vprositedomains_u[vi])
                    else:
                        vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vi], width=1, alpha=0.7,
                                          label=vprositedomains_u[vi], color=vprositedomains_u_color[vi])
                    vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                    vfh.write(vprositedomains_u[vi] + '\t' + vcurrcolor + '\n')
            vfh.close()
            plt.xlim(min(bin_edges), max(bin_edges))
            if vabsolute == 0:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=15)
            plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=15)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.title('Distribution of Prosite protein domains for ' + vgitem, fontsize=15)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_prosite.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_prosite.pdf')

        # Plot data of PFAM
        if vpfamfile != '':
            print('Plot data of PFAM for ' + vgitem)
            vstandardwidth = 10
            vstandardheight = 8
            vpaddingwidth = 1.0
            vpaddingheight = 0.7
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth),
                 Size.Fixed(vscalingfigure * vmedlengroup[vug] / 100)]
            v = [Size.Fixed(vpaddingheight), Size.Fixed(vstandardheight - 2 * vpaddingheight)]
            divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
            ax = Axes(fig, divider.get_position())
            ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
            fig.add_axes(ax)
            vmaxes = []
            for vi in range(vsize_of_pfam_data[0]):
                vmaxes.append(max(vpfamdomainsofgroup_rel[vi]))
            vmaxids = np.argsort(vmaxes)[::-1]
            bin_edges = np.arange(vsize_of_pfam_data[1] + 1)
            if vsavefolder != '':
                vfh = open(join(vsavefolder, vgitem + '_pfam_colors.txt'), 'w')
            else:
                vfh = open(vgitem + '_pfam_colors.txt', 'w')
            for vi in vmaxids:
                if max(vpfamdomainsofgroup_rel[vi]) > (vmaxcutoff * 100) and float(sum(vpfamdomainsingenes[vi])) / \
                        float(vn_prot_per_group) > vcutoff and vpfamdomains_u_ignore[vi] == 0:
                    if vpfamdomains_u_color[vi] == '':
                        vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vi], width=1, alpha=0.7,
                               label=vpfamdomains_u[vi])
                    else:
                        vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vi], width=1, alpha=0.7,
                               label=vpfamdomains_u[vi], color=vpfamdomains_u_color[vi])
                    vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                    vfh.write(vpfamdomains_u[vi] + '\t' + vcurrcolor + '\n')
            vfh.close()

            plt.xlim(min(bin_edges), max(bin_edges))
            if vabsolute == 0:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=15)
            plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=15)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.title('Distribution of PFAM protein domains for ' + vgitem, fontsize=15)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_pfam.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_pfam.pdf')

        # Combined plot
        if vprositefile != '' and vpfamfile != '':
            print('Plot data of Prosite and PFAM for ' + vgitem)
            vstandardwidth = 10
            vstandardheight = 8
            vpaddingwidth = 1.0
            vpaddingheight = 0.7
            fig = plt.figure(figsize=[vstandardwidth, vstandardheight])
            h = [Size.Fixed(vpaddingwidth),
                 Size.Fixed(vscalingfigure * vmedlengroup[vug] / 100)]
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
            if vsavefolder != '':
                vfh = open(join(vsavefolder, vgitem + '_combined_colors.txt'), 'w')
            else:
                vfh = open(vgitem + '_combined_colors.txt', 'w')
            for vmaxi in vmaxids:
                if vmaxi < vsize_of_prosite_data[0]:
                    if max(vprositedomainsofgroup_rel[vmaxi]) > (vmaxcutoff * 100) and float(
                            sum(vprositedomainsingenes[vmaxi])) / float(vn_prot_per_group) > vcutoff and \
                            vprositedomains_u_ignore[vmaxi] == 0:
                        if vprositedomains_u_color[vmaxi] == '':
                            vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vmaxi], width=1, alpha=0.7,
                                              label=vprositedomains_u[vmaxi])
                        else:
                            vcurrbar = ax.bar(bin_edges[:-1], vprositedomainsofgroup[vmaxi], width=1, alpha=0.7,
                                              label=vprositedomains_u[vmaxi], color=vprositedomains_u_color[vmaxi])
                        vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                        vfh.write(vprositedomains_u[vmaxi] + '\t' + vcurrcolor + '\n')
                else:
                    vimod = vmaxi - vsize_of_prosite_data[0]
                    if max(vpfamdomainsofgroup_rel[vimod]) > (vmaxcutoff * 100) and float(
                            sum(vpfamdomainsingenes[vimod])) / float(vn_prot_per_group) > vcutoff and \
                            vpfamdomains_u_ignore[vimod] == 0:
                        if vprositedomains_u_color[vimod] == '':
                            vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vimod], width=1, alpha=0.7,
                                              label=vpfamdomains_u[vimod])
                        else:
                            vcurrbar = ax.bar(bin_edges[:-1], vpfamdomainsofgroup[vimod], width=1, alpha=0.7,
                                              label=vpfamdomains_u[vimod], color=vpfamdomains_u_color[vimod])
                        vcurrcolor = f_get_hex(vcurrbar.patches[0].get_facecolor())
                        vfh.write(vpfamdomains_u[vimod] + '\t' + vcurrcolor + '\n')
            vfh.close()

            plt.xlim(min(bin_edges), max(bin_edges))
            if vabsolute == 0:
                plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Median length: ' + str(vmedlengroup[vug]) + ' bp', fontsize=15)
            plt.ylabel('Percent occurrence (n = ' + str(vn_prot_per_group) + ')', fontsize=15)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.title('Distribution of protein domains for ' + vgitem, fontsize=15)
            plt.legend(loc='upper left', frameon=False)
            if vsavefolder != '':
                plt.savefig(join(vsavefolder, vjobid + '_' + vgitem + '_combined.pdf'))
            else:
                plt.savefig(vjobid + '_' + vgitem + '_combined.pdf')

    print('done')


########################################################################################################################
#                                                                                                                      #
#  f_get_hex                                                                                                           #
#  Converts a 3 value tuple into hex code (tuple is assumed to be between 0 and 1)                                     #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vtuple: a list of numbers e.g. (0,0.5,0.912)                                                                    #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - string: hex color code e.g. #af0010                                                                             #
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
#  Input:                                                                                                              #
#    - vfile: String towards a text file containing the domain names to ignore                                         #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vignore_domain: List of strings representing domain names of Prosite or PFAM                                    #
#                                                                                                                      #
########################################################################################################################


def f_read_in_ignoredomainfile(vfile):
    vignore_domain = []
    try:
        vfile_fh = open(vfile, 'r')
        for vline in vfile_fh:
            vline = re.sub("[\n\r]", "", vline)
            vsplit = vline.split('\t')
            vignore_domain.append(vsplit[0])
        vfile_fh.close()
    except IOError:
        print('Can not read file: ' + vfile)
        sys.exit()
    return vignore_domain


########################################################################################################################
#                                                                                                                      #
#  f_read_in_colorfile                                                                                                 #
#  Reads a tab separated file in where each line is assumed to first contain a Prosite or PFAM domain, and the second  #
#  column contains a hexcode for a color to be applied in the figures.                                                 #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vfile: String towards a text file containing the domain color matchings.                                        #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vcolor_domain: List of strings representing domain names of Prosite or PFAM                                     #
#    - vcolor_hexcode: List of hex codes for the coloring of the domains. e.g. #af0010                                 #
#                                                                                                                      #
########################################################################################################################


def f_read_in_colorfile(vfile):
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
        print('Can not read file: ' + vfile)
        sys.exit()
    return vcolor_domain, vcolor_hexcode


########################################################################################################################
#                                                                                                                      #
#  f_read_in_groupfile                                                                                                 #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vfile: String towards a text file containing the domain color matchings.                                        #
#    - vheaders: A list of fasta headers that should be used to search for domain associations.
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vgroup: list of group associations that match to the headers.                                                   #
#    - vgroup_u: the same list as above to later ensure that a independent set of unique groups can be made            #
#                                                                                                                      #
########################################################################################################################


def f_read_in_groupfile(vfile, vheaders):
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
                        print('Warning: group domain file has more than one entry for ' + vitem +'. Only first instance is used.')
            vfile_fh.close()
            if vhit == 0:
                print('Warning: no protein group entry found for ' + vitem + '. Please add one in ' + vfile)
                vgroup.append('ProteinGroup')
                vgroup_u.append('ProteinGroup')
    except IOError:
        print('Can not read file: ' + vfile)
        sys.exit()
    return vgroup, vgroup_u


########################################################################################################################
#                                                                                                                      #
#  f_read_tsv                                                                                                          #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vfile: String towards a text file containing the domain color matchings.                                        #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vtable: pandas dataframe containing the information of the tsv.                                                 #
#                                                                                                                      #
########################################################################################################################


def f_read_tsv(vfile):
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
        sys.exit()
    return vtable


########################################################################################################################
#                                                                                                                      #
#  f_read_in_file                                                                                                     #
#                                                                                                                      #
#  Input:                                                                                                              #
#    - vfile: String towards a text file containing the domain color matchings.                                        #
#                                                                                                                      #
#  Output:                                                                                                             #
#    - vtable
#                                                                                                                      #
########################################################################################################################


def f_read_in_file(vfile):
    # Load all fasta sequences
    vheaders = []
    vsequences = []
    vinit = 1
    vfile_fh = open(vfile)
    for vline in vfile_fh:
        vline = re.sub("[\n\r]", "", vline)
        if vline.startswith('>'):
            if vinit == 0:
                if len(vtempsequence) > 0:
                    vheaders.append(vtempheader)
                    vsequences.append(vtempsequence)
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
    return vheaders, vsequences

def f_run_sequences_through_prosite(vhead, vseq):
    vwarnings = 0
    vout_all = []
    try:
        print('@> Submitted Prosite search for sequence "' + vseq[0:16] + '...".')
        vhandle = Bio.ExPASy.ScanProsite.scan(vseq, mirror='https://www.expasy.org', output='xml')
        vresults = Bio.ExPASy.ScanProsite.read(vhandle)
        if len(vresults) > 0:
            for record in vresults:
                vout = []
                vout.append(vseq)
                for vi in range(7):
                    vout.append('')
                for key in record.keys():
                    vout = f_dissect_prosite_key(vout, key, record[key])
                    if isinstance(record[key], dict):
                        for key2 in record[key].keys():
                            vout = f_dissect_pfam_key(vout, key2, record[key][key2])
                            if isinstance(vresults[key][key2], dict):
                                for key3 in record[key][key2].keys():
                                    vout = f_dissect_pfam_key(vout, key3, record[key][key2][key3])
                vout_all.append(vout)
        else:
            vout = []
            vout.append(vseq)
            for vi in range(7):
                vout.append('')
            vout_all.append(vout)
            if vwarnings == 1:
                print(vhead + ' has no results in prosite.')
    except ValueError:
        vout = []
        vout.append(vseq)
        for vi in range(7):
            vout.append('')
        vout_all.append(vout)
        if vwarnings == 1:
            print(vhead + ' has no results in prosite.')
    return vout_all, len(vout_all)

def f_run_sequences_through_pfam(vhead, vseq):
    vwarnings = 0
    vout_all = []
    try:
        vresults = prody.searchPfam(vseq)
        print(vresults)
        sys.exit()
        #if len(vresults.keys()) > 1:
        #    print(vresults)
        #    print(len(vresults.keys()))
        #    sys.exit()
        if len(vresults.keys()) > 0:
            for key in vresults.keys():
                vout = []
                vout.append(vseq)
                for vi in range(14):
                    vout.append('')
                vout = f_dissect_pfam_key(vout, key, vresults[key])
                if isinstance(vresults[key], dict):
                    for key2 in vresults[key].keys():
                        vout = f_dissect_pfam_key(vout, key2, vresults[key][key2])
                        if isinstance(vresults[key][key2], dict):
                            for key3 in vresults[key][key2].keys():
                                vout = f_dissect_pfam_key(vout, key3, vresults[key][key2][key3])
                vout_all.append(vout)
        else:
            vout = []
            vout.append(vseq)
            for vi in range(14):
                vout.append('')
            vout_all.append(vout)
            if vwarnings == 1:
                print(vhead + ' has no results in pfam.')
    except ValueError:
        vout = []
        vout.append(vseq)
        for vi in range(14):
            vout.append('')
        vout_all.append(vout)
        if vwarnings == 1:
            print(vhead + ' has no results in pfam.')
    return vout_all, len(vout_all)

def f_write_pfam_prosite_db(vDBFiles, vDBID, ventry_found, vnentry_found):
    try:
        vdb_fh = open(vDBFiles + '_' + vDBID, 'a')
        for entry in ventry_found:
            for vj, item2 in enumerate(entry):
                if vj == 0:
                    vdb_fh.write(str(item2))
                else:
                    vdb_fh.write('\t' + str(item2))
            vdb_fh.write('\n')
    except IOError:
        print('Can not write file ' + vDBFiles + '_' + vDBID)
        sys.exit()
    vdb_fh.close()

def f_write_pfam_prosite_res(vfile, vitem, ventry_found, vnentry_found, ispfam, isfromdb):
    try:
        vdb_fh = open(vfile, 'a')
        if isfromdb == True:
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
        else:
            for entry in ventry_found:
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
    except IOError:
        print('Can not write file ' + vfile)
        sys.exit()
    vdb_fh.close()

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

def f_dissect_pfam_key(vout, key, value):
    if key == 'ali_start':
        vout[1] = value
    elif key == 'ali_end':
        vout[2] = value
    elif key == 'start':
        vout[3] = value
    elif key == 'end':
        vout[4] = value
    elif key == 'accession':
        vout[5] = value
    elif key == 'id':
        vout[6] = value
    elif key == 'hmm_start':
        vout[7] = value
    elif key == 'hmm_end':
        vout[8] = value
    elif key == 'bitscore':
        vout[10] = value
    elif key == 'ind_evalue':
        vout[11] = value
    elif key == 'cond_evalue':
        vout[12] = value
    return vout


########################################################################################################################
#                                                                                                                      #
#  f_print_help                                                                                                        #
#  prints the help page of propplot.py                                                                                 #
#                                                                                                                      #
########################################################################################################################


def f_print_help():
    print('Use propplot.py in a two step process:')
    print('First call (prepare input for Prosite and PFAM):')
    print('propplot.py collect Path/to/folder/containing/fasta/sequences OutputFilenameLead')
    print('Options:')
    print('  -w 0 or warning 0: avoid warnings.')
    print('This prepares the input files for both PFAM and Prosite.')
    print('The path needs to contain fasta sequences in files named either .fa or .fasta.')
    print('Follow the screen output to the webpages given to run your PFAM and Prosite run(s).')
    print('Select options to let you sent results in a table format.')
    print('Copy results from your mails into two single text files. One for all PFAM results and one for all Prosite ' +
          'results.')
    print('Example call:')
    print('python propplot.py collect /Users/myuser/propplotdata/data/ Testdata.today -w 0')
    print('\n')
    print('Second call (analyze Prosite and PFAM results and plot them):')
    print('python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead prosite ' +
          'Path/to/prositeresultfile')
    print('or')
    print('python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead pfam ' +
          'Path/to/pfamresultfile')
    print('or')
    print('python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead prosite ' +
          'Path/to/prositeresultfile pfam Path/to/pfamresultfile')
    print('order of pfam / prosite is unimportant, but at least one option must be given.')
    print('Options:')
    print('  warnings (or -w) 0: avoid warnings.')
    print('  groupfile (or -g) Path/to/group_association_file: give a tab separated file that in the first column ' +
          'has the sequence headers and the second column a name for the group the sequence belongs to. This allows ' +
          'to run all fasta sequences in one go, but then split the sequences and results into different groups of ' +
          'sequences, for example by grouping them into groups of sequences from different clades of organisms.')
    print('  colorfile (or -c) Path/to/domain_color_file: give a tab separated list of domain names in column one, ' +
          'with hexcodes (e.g. #fffff) in colomn 2 to have custom coloring')
    print('  ignorefile (or -i) Path/to/domain_ignore_file: give a list of domain names in one column, that should ' +
          'be ignored when plotting.')
    print('  absoluteresults (or -a) 1: print absolute numbers on y axis of plots instead of relative ones')
    print('  cutoff (or -cf) N: Set N to a number between 0 and 1. Only domains occuring in a ratio higher than the ' +
          'number are plotted (e.g. if value is 0.5 the domain has to occure somewhere in the protein of at least ' +
          '50% of sequences).')
    print('  maxcutoff (or -mcf) N: Set N to a number between 0 and 1. Only domains that have a maximum prevalence ' +
          'at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the ' +
          'sequences have to have this domain at the same relative position).')
    print('  scalefigure (or -s) N: Set N to a number larger than 0. Represents the N inches per 100pb that the plot ' +
          'is used to display.')
    print('Example call:')
    print('python propplot.py process /Users/myuser/propplotdata/data/ Testdata.today prosite ' + 
          'Path/to/prositeresultfile')


########################################################################################################################
#                                                                                                                      #
#  Usual starting point of the software.                                                                               #
#  propplot is assumed to be started from the command line with arguments (optional and non-optional ones)             #
#                                                                                                                      #
########################################################################################################################


if __name__ == "__main__":

    # test if sys is installed in python
    try:
        import sys
    except ImportError:
        print('Error, module sys is required.')
        exit()
    import sys

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
        import matplotlib.pyplot as plt
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

    # test if prody is installed in python
    # try:
    #     import prody
    # except ImportError:
    #     print('Error, module prody is required.')
    #     sys.exit()

    # # test if Bio is installed in python
    try:
        import Bio.ExPASy.ScanProsite
    except ImportError:
        print('Error, module Bio is required.')
        sys.exit()

    if len(sys.argv) <= 1: # If only scriptname is given, print help
        f_print_help()
        sys.exit()
    else:
        vjobid = ''
        vwarnings = '0'
        vsavefolder = ''
        vdbfolder = ''
        vinputfile = ''
        vgroupfile = ''
        vcolorfile = ''
        vignoredomainfile = ''
        vstandardcutoff = '0.05'
        vstandardmaxcutoff = '0.05'
        vcutoff = '0.05'
        vmaxcutoff = '0.05'
        vscalefigure = '1'
        vstandardscalefigure = '1'
        vabsoluteresults = '0'
        vignoredb = '0'

        if vstandardcutoff != vcutoff:
            print('error in script, vstandardcutoff and vcutoff need to be the same.')
            sys.exit()
        if vstandardmaxcutoff != vmaxcutoff:
            print('error in script, vstandardmaxcutoff and vmaxcutoff need to be the same.')
            sys.exit()

        for vi in range(1, len(sys.argv)):
            if sys.argv[vi] == '-id':
                vjobid = sys.argv[vi + 1]
            elif sys.argv[vi] == '-idb':
                vignoredb = sys.argv[vi + 1]
            elif sys.argv[vi] == '-w':
                vwarnings = sys.argv[vi + 1]
                if vwarnings == '0':
                    print('Warnings are off.')
                elif vwarnings != '1':
                    print('Unknown warnings setting: ' + vwarnings)
                    sys.exit()
            elif sys.argv[vi] == '-sf':
                if len(sys.argv) == vi + 1:
                    print('To enter folder to save files, give a folder name after savefolder or -save.')
                    sys.exit()
                vsavefolder = sys.argv[vi + 1]
                try:
                    pathlib.Path(vsavefolder).mkdir(parents=True, exist_ok=True)
                except IOError:
                    print('Path ' + vsavefolder + ' can not be created.')
                    sys.exit()
                if vwarnings == 1:
                    print('Folder to save intermediate and output files: ' + vsavefolder)
            elif sys.argv[vi] == '-dbf':
                if len(sys.argv) == vi + 1:
                    print('To enter folder to save dbs, give a folder name after -dbf.')
                    sys.exit()
                vdbfolder = sys.argv[vi + 1]
                try:
                    pathlib.Path(vdbfolder).mkdir(parents=True, exist_ok=True)
                except IOError:
                    print('Path ' + vdbfolder + ' can not be created.')
                    sys.exit()
                if vwarnings == 1:
                    print('Folder to save dbs: ' + vdbfolder)
            elif sys.argv[vi] == '-in':
                vinputfile = sys.argv[vi + 1]
                try:
                    vfh = open(vinputfile, 'r')
                except IOError:
                    print('Can not read ' + vinputfile)
                    sys.exit()
                vfh.close()
                if vwarnings == 1:
                    print('Input file stored in: ' + vinputfile)
            elif sys.argv[vi] == '-gf':
                vgroupfile = sys.argv[vi + 1]
                try:
                    vfh = open(vgroupfile, 'r')
                except IOError:
                    print('Can not read ' + vgroupfile)
                    sys.exit()
                vfh.close()
                if vwarnings == 1:
                    print('Group association information stored in: ' + vgroupfile)
            if sys.argv[vi] == '-cf':
                vcolorfile = sys.argv[vi + 1]
                try:
                    vfh = open(vcolorfile, 'r')
                except IOError:
                    print('Can not read ' + vcolorfile)
                    sys.exit()
                vfh.close()
                if vwarnings == 1:
                    print('Domain color information stored in: ' + vcolorfile)
            if sys.argv[vi] == '-if':
                vignoredomainfile = sys.argv[vi + 1]
                try:
                    vfh = open(vignoredomainfile, 'r')
                except IOError:
                    print('Can not read ' + vignoredomainfile)
                    sys.exit()
                vfh.close()
                if vwarnings == 1:
                    print('Information which domains to ignore stored in: ' + vignoredomainfile)
            if sys.argv[vi] == '-ar':
                vabsoluteresults = sys.argv[vi + 1]
                if vabsoluteresults == '1':
                    if vwarnings == 1:
                        print('Using absolute results.')
                elif vabsoluteresults != '0':
                    print('Unknown option: ' + sys.argv[vi] + ' ' + sys.argv[vi + 1])
                    sys.exit()
            if sys.argv[vi] == '-cut':
                vcutoff = sys.argv[vi + 1]
                if vwarnings == 1:
                    print('Domain display threshold values: ' + vcutoff)
            if sys.argv[vi] == '-mcut':
                vmaxcutoff = sys.argv[vi + 1]
                if vwarnings == 1:
                    print('Domain display threshold values: ' + vmaxcutoff)
            if sys.argv[vi] == '-sbp':
                vscalefigure = sys.argv[vi + 1]
                if vwarnings == 1:
                    print('Figure scale is 100pb per ' + vmaxcutoff + 'inch.')

        if vwarnings == '1':
            print('Warnings are on. Change warnings to be on (1) or off (0) by entering 1 or 0 after warning ' +
                  'or -w.')

        if vinputfile == '':
            print('Input file not set. use -in inputfile to set.')
            sys.exit()
        if vjobid == '':
            print('Job id not set with -id.')
            sys.exist()

        if vstandardcutoff == vcutoff:
            if vwarnings == '1':
                print('Domains that do not occur in at least ' + str(float(vcutoff) * 100) +
                      '% of sequences are not shown. Change setting using cutoff or -cf followed by a number between ' +
                      '0 and 1.')
        if vstandardmaxcutoff == vmaxcutoff:
            if vwarnings == '1':
                print('Domains that do not occur in at least ' + str(float(vmaxcutoff) * 100) +
                      '% of sequences at the same relative position are not shown. Change setting using maxcutoff or ' +
                      '-mcf followed by a number betwen 0 and 1.')

        if vabsoluteresults == '0':
            if vwarnings == '1':
                print('Using relative results. Change setting with absoluteresults or -a followed by 0 or 1.')
        if vstandardscalefigure == vscalefigure:
            if vwarnings == '1':
                print('Using figure scaling of 100 bp per ' + str(vscalefigure) + ' inches. Change setting with ' +
                      'scalefigure or -s followed by a value greater than 0.')

        f_run_propplot(vjobid, vinputfile, vignoredb, vsavefolder, vdbfolder, vgroupfile, vcolorfile, vignoredomainfile, vcutoff, vmaxcutoff, vscalefigure, vabsoluteresults, vwarnings)