# Help

## Introduction
DomainViz allows users to identify and visualize protein domains on one or more protein sequences using multiple domain prediction platforms (Pfam and Prosite) to understand the consensus positionality and abundance of different domains within protein groups and families. While Pfam and Prosite each individually provide domain information for a single sequence, searching multiple proteins is not possible, requiring extensive manual curation. DomainViz automates the simultaneous identification of domains from multiple proteins and provides both consolidated and consensus outputs for further analysis and publication. This is highlighted by the production of a ‘consensus’ histogram plot that depicts the distribution and positionality of domains within a representative median protein sequence derived from the input protein sequences. 

### General Operations
File Upload: DomainViz accepts a single multiple sequence fasta file. The file extension should be .FA or .FASTA and the file size should be less than 10 Mb. Each sequence present within the fasta file should be formatted as follows: 

>AT3G19040.1|PACid:19663337_AtTAFIIb
MICRVDYGSNDEEYDGPELQVVTEEDHLLPKREYLSSEIAESRR
YREVIRSEREEEKRRKAKQKKKLQRGILENYPPRRNDGISSESGQNINSLCVSDFERNRTEYAPQPKRRKKGQVGLANILESIVDTLRVKEVNVSYLFLK
PVTKKEAPNYLEIVKCPMDLSTIRDKVRRMEYRDRQQFRHDVWQIKFNAHLYNDGRNLSIPPLADELLVKCDRLLDEYRDELKEAEKGIVDSSDSLR*

The chevron denotes the header line containing unique identifying information, which is ended by a line return to denote this as a separate entity from the sequence. At the end of each sequence should be a (*) to ensure the end of the sequence is denoted. Sequences of 16 amino acids or less, and greater than 10005000 amino acids are not compatible with DomainViz. 

#### NOTE: Ensure that headers and sequences are not duplicated in the file and that standard amino acid code is used. Accepted characters are GALMFWKQESPVICYHRNDTX, in upper or lower case.

### Submit Task and Analysis: 
Once a file is successfully uploaded, use the Submit Task button to start the analysis. This will redirect to  a new results page with an unique identifying 32 digit  Result ID. Please copy and save the Result ID. You can use this ID to retrieve results for a period of 7 days post analysis. Please note that some searches can take a long time, from several minutes to hours and you can check the status of your analysis using your Result ID. 
#### Example Result ID: 5ff3eeda_5842_5879_d627_f4d1faea3c84

Without a Result ID , the data will not be retrievable and the analysis will need to be re-run. If an error occurs, please follow the directions in the pop-up box that results.

### Data Retrieval: 
To retrieve a previous analysis, enter the Result ID into  the “Result ID” text box on the DomainViz homepage . Analyses are retained for a total of 7 days prior to automatic deletion.

### Load Example: 
This option will automatically load a .fa or .fasta file to produce an example analysis visualization as well as an example downloadable output.

## Settings
### Absolute Results: 
Absolute results means that we will plot absolute numbers on y axis of plots instead of relative ones. If the box is unchecked, we plot relative results, if it is checked, we plot absolute results. 

### Minimum Domain Prevalence: 
Only domains occuring in a ratio higher than the number are plotted will be present in the  visualized and compiled output (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).

### Minimum domain position conservation: 
Only domains occuring at a ratio higher than this number at a specific place in the protein group will be presented in the output (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).

### Scale: 
The number input here represents the number of inches per 100 amino acids that the plot will use to display each visualization.


## Data Interpretation

The histograms depict both the position and prevalence of eachspecific protein domains (identified from the Pfam and Prosite databases) within the group of proteins input by the user. 

Generally, results with non-overlapping domains can be directly interpreted as showing the prevalence and position of each domain with different degrees of conservation within the protein group. 

If the visualization of a group of proteins shows two overlapping domains (e.g. A and B), at for example each with 50% 0.5 prevalence, then there are three possible explanations:ways how the figure could have been compiled in this way.

#### Case 1: A subset of proteins have no domain predicted, while the remaining subset of proteins have both domains A and B predicted at the same spot. (In this case, the subsets are each half of the total set of proteins).

#### Case 2: A subset of proteins have domain A predicted, and the possess an other subset of proteins have domain B predicted. (In this case, the subsets are each half of the total set of proteins.

#### Case 3: Any combination of Case 1 and Case 2 leading to the same prevalence ratios. Only further investigation of the results available in the download option can discriminate the case.

### Downloadable DomainViz Outputs
The DomainViz output is available for download as a .zip file containing multiple files types. This includes: Job.id.tsv files containing the raw output data from Pfam and Prosite. Job.id_ProteinGroup.csv allows users to replot the data used in creating each visualized histogram. Lastly, Job.id_ProteinGroup.pdf files that are high resolution vector files that can be used for further manipulation and/or publication. 

## FAQ
1.  Q. How do I retrieve my results after navigating away from the processing results?
    A. Ensure that you retain the 32-character unique identifier result ID displayed on the Results page. EnterPlace this code into the Result ID field on the homemain page and hit “Go to My Results”. Alternatively, bookmark the Results page and revisit it after some time. 

2.  Q. I have been warned that I have duplicate sequences in my FASTA file?
    A. DomainViz will still process your file under the assumption that duplicate sequences refer to independent proteins that share the same sequence. We advise checking that spurious duplicate sequences were not accidentally introduced during input file creation as they can lead to altered results. run; however, it is recommended that these be removed before proceeding further.

3.  Q. What is the maximal number of protein sequences that can be analyzed at once?
    A. DomainViz can currently assess 1000 protein sequences at once. NOTE: The more sequences in a single query the longer the analysis will take. 

4. Q. My fasta isn't uploading, it says there is a problem with one of my lines? How do I fix this?
    A. Please remove the lines that are causing issues.