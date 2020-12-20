# Downloadable DomainViz Outputs
The DomainViz output is available for download as a .zip file containing multiple files.
This includes: Job.id.tsv files containing the raw output data from Pfam and Prosite. Job.id_ProteinGroup.tsv allows users to replot the data used in creating each visualized histogram. Lastly, Job.id_ProteinGroup.pdf files that are high resolution vector files that can be used for further manipulation and/or publication. 

### Result output: Job.id_pfam_res.tsv
All results of the PFAM search as a single tab separated file. This result file mimics the tabulated files that can be downloaded for results from PFAM directly, however is not produced by PFAM. Each row depicts one domain/sequence pair. The headers are as follows:
**Sequence id:** The fasta sequence header that was submitted to DomainViz.
**Family id:** PFAM family identifier, can be used to find out more about the domain.
**Family Accession:** PFAM family grouping: A family is a collection of related protein regions.
**Clan:** PFAM clan grouping: A clan is a collection of related Pfam entries. The relationship may be defined by similarity of sequence, structure or profile-HMM.
**Env. Start:** Pfam hit start. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates) for reference.
**Env. End:** Pfam hit end. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates) for reference.
**Ali. Start:** Pfam hit start. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates) for reference.
**Ali. End:** Pfam hit end. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates) for reference.
**Model Start:** Start for the hidden markov model hit. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer)
**Model End:** End for the hidden markov model hit. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer)
**Bit Score:** PFAM Scoring. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/scores.html)
**Ind. E-value:** PFAM Scoring. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/scores.html)
**Cond. E-value:** PFAM Scoring. See [Pfam docs](https://pfam-docs.readthedocs.io/en/latest/scores.html)
**Description:** Description of the domain that is saved by PFAM.
**Outcompeted:** Contains the information whether PFAM considers the domain to be outcompeted by another domain.
**Significant:** Contains the information whether PFAM terms the finding as to be significant (see web output of a sequence)
**Uniq:** Unique identifier for hit (unused)

### Result output: Job.id_prosite_res.tsv
All results of the ProSite search as a tab separated file. This result file mimics the tabulated files that can be downloaded for results from ProSite directly, however is not produced by ProSite. It has no header. However each column contains the following information:
**Column 1:** The fasta sequence header that was submitted to DomainViz.
**Column 2:** Domain start.
**Column 3:** Domain end.
**Column 4:** Domain identifier from ProSite.
**Column 5:** ProSite score
**Column 6:** Prosite level. See [Prosite docs](https://prosite.expasy.org/prosuser.html) for reference.
**Column 7:** Prosite level tag. See [Prosite docs](https://prosite.expasy.org/prosuser.html) for reference.
**Column 8:** unused

### Result Output: Job.id_ProteinGroup_combined.pdf
A combined plot of both pfam and prosite domains, visualized on an artificial protein with the length as the median length of the proteins in the protein group of the fasta file. Depending on the settings given as input, output files display differently and may not be represented well (in the case of too large scaling) on the webpage.

### Result Output: Job.id_ProteinGroup_pfam.pdf
The same as the combined plot, however displaying only PFAM domains.

### Result Output: Job.id_ProteinGroup_prosite.pdf
The same as the combined plot, however displaying only ProSite domains.

### Result Output: Job.id_ProteinGroup_pfam_domain_results_per_aa.tsv
A Tab separated file, with each of the ‘artificial’ amino acid positions of the median length protein as rows, and each of the domains for PFAM as columns, showing the y-axis value displayed in the plots as numbers.

### Result Output: Job.id_ProteinGroup_prosite_domain_results_per_aa.tsv
The same as Job.id_ProteinGroup_pfam.tsv, however for ProSite domains.