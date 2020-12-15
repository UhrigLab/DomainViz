let fileReader;

async function canReadFile(file) {
    // Check if file exists.
    try {
        return file.text().then(text => {
            return true;
        })   
    }
    catch (error) {
        console.error(error);
        return false;
    }
}

async function checkFasta(file) {
    return file.text().then(content => {
        let headers = [];
        let lines = content.split('\n');
        for (var i in lines) {
            let line = lines[i];
    
            if (line === '') {
                return false, 'Fasta file contains empty line on line ' + i.toString() + '.';
            }
            else if (line[0] =='>') {
                headers.push(line);
            }
            else if (line.trim().match('^[GALMFWKQESPVICYHRNDTXgalmfwkqespvicyhrndtx\*\n]*$') == null) {
                // 1) Check if line only consists of the following characters
                // GALMFWKQESPVICYHRNDTgalmfwkqespvicyhrndt* and space and new line character (\n)
                // If the line contains any other character, or is completely empty, the regex will return null
                return false, 'Fasta file contains forbidden characters on line ' + i.toString() + '. Only allowed characters: ' + 'GALMFWKQESPVICYHRNDTXgalmfwkqespvicyhrndtx*';
            }
        }
        //make sure there are no repeated headers
        if ((new Set(headers)).size == headers.length) {
            return true
        }
        else {
            return  false, "You cannot have duplicate headers.";
        }
    });
    
}
async function isFasta(file) {
    // Check if file can be read
    let valid = false;
    await canReadFile(file).then(result => {
        valid=true;
    }).catch((error) => {
        console.error(error);
        alert("Could not read file.")
    });

    if (!valid) {
        return false
    }

    // Check if file is fasta file:
    // Check if file consists only of headers and protein sequences. 
    //Collect all headers to then check if there are duplicates.
    await checkFasta(file).then(result => {
        if (result != true) {
            valid = false;
            alert(result);
        }
    });

    return valid;
    
 
}
export default isFasta
// def is_groupfile(filename):
//     # Default values
//     vreturn = True
//     vreturn_id = 0
//     vreturn_message = ''

//     # check if file exists
//     vfile_exists, vfile_exists_id, vfile_exists_message = is_file(filename)
//     if not vfile_exists:
//         vreturn = vfile_exists
//         vreturn_id = vfile_exists_id
//         vreturn_message = vfile_exists_message
//         return vreturn, vreturn_id, vreturn_message

//     # Check if file can be read
//     vfile_can_be_read, vfile_can_be_read_id, vfile_can_be_read_message = is_file(filename)
//     if not vfile_can_be_read:
//         vreturn = vfile_can_be_read
//         vreturn_id = vfile_can_be_read_id + 1
//         vreturn_message = vfile_can_be_read_message
//         return vreturn, vreturn_id, vreturn_message

//     # check if all lines have two columns separated with one tab
//     # check if all headers are given a proteingroup
//     vfh = open(filename, 'r')
//     vheaders = []
//     for vl, line in enumerate(vfh):
//         line = line.rstrip('\r').rstrip('\n')
//         vsplit = line.split('\t')
//         if not len(vsplit) == 2:
//             vreturn = False
//             vreturn_id = 3
//             vreturn_message = 'File ' + filename + ' contains more or less than two columns separated by one tab ' + \
//                 'line ' + str(vl) + '.'
//             return vreturn, vreturn_id, vreturn_message
//         if not vsplit[0].startswith('>'):
//             vreturn = False
//             vreturn_id = 4
//             vreturn_message = 'File ' + filename + ' contains header not starting with ">" on ' + \
//                               'line ' + str(vl) + '.'
//             return vreturn, vreturn_id, vreturn_message
//         if vsplit[1] == '':
//             vreturn = False
//             vreturn_id = 4
//             vreturn_message = 'File ' + filename + ' contains no proteingroup on ' + \
//                               'line ' + str(vl) + '.'
//             return vreturn, vreturn_id, vreturn_message
//         vheaders.append(vsplit[0])  # Collect headers to then do check for double entries.

//     # check if every header is present only once
//     if not len(vheaders) == len(list(set(vheaders))):
//         vbad_headers = ''
//         for vh, vheader in vheaders:
//             for vh2 in range(vh + 1, len(vheaders)):
//                 if vheader == vheaders[vh2]:
//                     vbad_headers = vbad_headers + ', ' + vheader
//         vbad_headers.lstrip(', ')
//         vreturn = False
//         vreturn_id = 5
//         vreturn_message = 'File ' + filename + ' contains double entries for headers ' + vbad_headers + '.'
//         return vreturn, vreturn_id, vreturn_message
//     vfh.close()
//     return vreturn, vreturn_id, vreturn_message


// def is_colorfile(filename):
//     # Default values
//     vreturn = True
//     vreturn_id = 0
//     vreturn_message = ''

//     # check if file exists
//     vfile_exists, vfile_exists_id, vfile_exists_message = is_file(filename)
//     if not vfile_exists:
//         vreturn = vfile_exists
//         vreturn_id = vfile_exists_id
//         vreturn_message = vfile_exists_message
//         return vreturn, vreturn_id, vreturn_message

//     # Check if file can be read
//     vfile_can_be_read, vfile_can_be_read_id, vfile_can_be_read_message = is_file(filename)
//     if not vfile_can_be_read:
//         vreturn = vfile_can_be_read
//         vreturn_id = vfile_can_be_read_id + 1
//         vreturn_message = vfile_can_be_read_message
//         return vreturn, vreturn_id, vreturn_message

//         # check if all lines have two columns separated with one tab
//         # check if all headers are given a proteingroup
//         vfh = open(filename, 'r')
//         vdomains = []
//         vcolors = []
//         for vl, line in enumerate(vfh):
//             line = line.rstrip('\r').rstrip('\n')
//             vsplit = line.split('\t')
//             if not len(vsplit) == 2:
//                 vreturn = False
//                 vreturn_id = 2
//                 vreturn_message = 'File ' + filename + ' contains more or less than two columns separated by one tab ' + \
//                                   'line ' + str(vl) + '.'
//                 return vreturn, vreturn_id, vreturn_message
//             if vsplit[1] == '':
//                 vreturn = False
//                 vreturn_id = 3
//                 vreturn_message = 'File ' + filename + ' contains no color (e.g. #000000) on ' + \
//                                   'line ' + str(vl) + '.'
//                 return vreturn, vreturn_id, vreturn_message
//             if not len(vsplit[1]) == 7:
//                 vreturn = False
//                 vreturn_id = 4
//                 vreturn_message = 'File ' + filename + ' contains a bad color description on ' + \
//                                   'line ' + str(vl) + '.'
//                 return vreturn, vreturn_id, vreturn_message
//             if not vsplit[1].startswith('#'):
//                 vreturn = False
//                 vreturn_id = 4
//                 vreturn_message = 'File ' + filename + ' contains a bad color description on ' + \
//                                   'line ' + str(vl) + '.'
//                 return vreturn, vreturn_id, vreturn_message
//             vhex = vsplit[1].lstrip('#')
//             try:
//                 vhexit = int(vhex, 16)
//             except ValueError:
//                 vreturn = False
//                 vreturn_id = 4
//                 vreturn_message = 'File ' + filename + ' contains a bad color description on ' + \
//                                   'line ' + str(vl) + '.'
//                 return vreturn, vreturn_id, vreturn_message
//             vdomains.append(vsplit[0])  # Collect domains to then do check for double entries.
//             vcolors.append(vsplit[0])  # Collect colors to then do check for double entries.

//         # check if every domain is present only once
//         if not len(vdomains) == len(list(set(vdomains))):
//             vbad_vdomains = ''
//             for vd, vdomain in vdomains:
//                 for vd2 in range(vd + 1, len(vdomains)):
//                     if vdomain == vdomains[vh2]:
//                         vbad_vdomains = vbad_vdomains + ', ' + vdomain
//             vbad_vdomains.lstrip(', ')
//             vreturn = False
//             vreturn_id = 5
//             vreturn_message = 'File ' + filename + ' contains double entries for domains ' + vbad_vdomains + '.'
//             return vreturn, vreturn_id, vreturn_message

//         # check if every color is present only once
//         if not len(vcolors) == len(list(set(vcolors))):
//             vbad_vcolors = ''
//             for vc, vcolor in vcolors:
//                 for vc2 in range(vc + 1, len(vcolors)):
//                     if vcolor == vcolors[vc2]:
//                         vbad_vcolors = vbad_vcolors + ', ' + vcolor
//             vbad_vcolors.lstrip(', ')
//             vreturn = False
//             vreturn_id = 6
//             vreturn_message = 'File ' + filename + ' contains double entries for colors ' + vbad_vcolors + '.'
//             return vreturn, vreturn_id, vreturn_message
//     vfh.close()
//     return vreturn, vreturn_id, vreturn_message


// def is_ignorefile(filename):
//     # Default values
//     vreturn = True
//     vreturn_id = 0
//     vreturn_message = ''

//     # check if file exists
//     vfile_exists, vfile_exists_id, vfile_exists_message = is_file(filename)
//     if not vfile_exists:
//         vreturn = vfile_exists
//         vreturn_id = vfile_exists_id
//         vreturn_message = vfile_exists_message
//         return vreturn, vreturn_id, vreturn_message

//     # Check if file can be read
//     vfile_can_be_read, vfile_can_be_read_id, vfile_can_be_read_message = is_file(filename)
//     if not vfile_can_be_read:
//         vreturn = vfile_can_be_read
//         vreturn_id = vfile_can_be_read_id + 1
//         vreturn_message = vfile_can_be_read_message
//         return vreturn, vreturn_id, vreturn_message

//     vfh = open(filename, 'r')
//     for vl, line in enumerate(vfh):
//         line = line.rstrip('\r').rstrip('\n')
//         vsplit = line.split('\t')
//         if not len(vsplit) == 1:
//             vreturn = False
//             vreturn_id = 2
//             vreturn_message = 'File ' + filename + ' contains more than one column separated by one tab ' + \
//                               'line ' + str(vl) + '.'
//             return vreturn, vreturn_id, vreturn_message
//     vfh.close()
//     return vreturn, vreturn_id, vreturn_message