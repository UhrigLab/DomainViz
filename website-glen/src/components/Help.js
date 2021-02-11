import React from 'react';
import { Grid, Paper, Typography, Link } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import HelpImage from './img/help-file.png'


const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    textAlign: 'left',
    color: theme.palette.text.secondary,
  },
  link: {
    fontWeight: 'fontWeightBold',
    color: 'black',
    textDecoration: 'underline',
  },
  body2: {
    fontWeight: 1000,
    fontSize: 20,
  },
  img: {
    height: "393px",
    width: "1200px"
},
}));
export const Help = () => {
  const classes = useStyles()

  return (
    <Grid container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }}>
      <Grid item xs={11}>
        <Typography variant='h4'>Help</Typography>

        <Paper className={classes.paper} variant='outlined'>
          <Typography variant='h5'>Introduction</Typography>
          <Typography variant='body1' display='inline'>DomainViz allows users to identify and visualize protein domains on multiple protein sequences using multiple domain prediction platforms{' '}(</Typography>
          <Link className={classes.link} to='http://pfam.xfam.org/'>Pfam</Link>
          <Typography variant='body1' display='inline'>{' '}and{' '}</Typography>
          <Link className={classes.link} to='https://prosite.expasy.org/'>Prosite</Link>
          <Typography variant='body1' display='inline'>) to understand the consensus positionality and abundance of different domains within protein groups and families. For example, DomainViz can be used to visualize the extent to which particular protein domains are evolutionarily conserved across homologous proteins, and also to visualize domain conservation between members of a single protein family. </Typography>
          <Typography variant='body1' paragraph/>
          <Typography variant='body1' paragraph>While Pfam and Prosite each individually provide domain information for a single sequence, searching and visualizing multiple proteins is not possible with these tools. DomainViz automates the simultaneous identification of domains from multiple proteins and provides both consolidated and consensus outputs for further analysis and publication. This is facilitated by the production of a ‘consensus’ histogram plot that depicts the frequency distribution and positionality of domains within a representative median protein sequence derived from the input protein sequences.</Typography>
          
          <Typography variant='h5'>General Operations</Typography>
          <Typography variant='h6'>File Upload:</Typography>
          <Typography variant='body1' paragraph>DomainViz accepts a single multiple sequence fasta file. The file extension should be .FA or .FASTA and the file size should be less than 10 Mb. Each sequence present within the fasta file should be formatted as follows:</Typography>
          
          <Typography variant='caption'>{'>'}AT3G19040.1|PACid:19663337_AtTAFIIb</Typography>
          <Typography variant='caption' paragraph>
            MICRVDYGSNDEEYDGPELQVVTEEDHLLPKREYLSSEIAESRR
            YREVIRSEREEEKRRKAKQKKKLQRGILENYPPRRNDGISSESGQNINSLCVSDFERNRTEYAPQPKRRKKGQVGLANILESIVDTLRVKEVNVSYLFLK
            PVTKKEAPNYLEIVKCPMDLSTIRDKVRRMEYRDRQQFRHDVWQIKFNAHLYNDGRNLSIPPLADELLVKCDRLLDEYRDELKEAEKGIVDSSDSLR*
          </Typography>
          <Typography variant='body1' paragraph>The chevron denotes the header line containing unique identifying information, which is ended by a line return. Sequences of 16 amino acids or less, and greater than 5000 amino acids are not compatible with DomainViz.</Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>NOTE: </Typography>
          <Typography variant='body1' display='inline'>Ensure that standard amino acid code is used. Accepted characters are GALMFWKQESPVICYHRNDTX, in upper or lower case.</Typography>
          <Typography paragraph/>


          <Typography variant='h6'>Submit Task and Analysis:</Typography>
          <Typography variant='body1' paragraph>Once a file is successfully uploaded, use the Submit Task button to start the analysis. This will redirect to  a new results page with an unique identifying 32 digit  Result ID. Please copy and save the Result ID. You can use this ID to retrieve results for a period of 7 days post analysis. Please note that some searches can take a long time, from several minutes to hours and you can check the status of your analysis using your Result ID. </Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Example Result ID: </Typography>
          <Typography variant='body1' display='inline' paragraph>5ff3eeda.5842.5879.d627.f4d1faea3c84</Typography>
          <Typography variant='body1' paragraph/>
          <Typography variant='body1' paragraph>Without a Result ID, the data will not be retrievable and the analysis will need to be re-run. If an error occurs, please follow the directions in the pop-up box that results.</Typography>
          
          <Typography variant='h6'>Data Retrieval:</Typography>
          <Typography variant='body1' paragraph>To retrieve a previous analysis, enter the Result ID into the "Result ID" textbox on the DomainViz homepage. Analyses are retained for a total of 7 days prior to automatic deletion.</Typography>
          <Typography variant='h6'>Load Example:</Typography> 
          <Typography variant='body1' paragraph>This option will automatically load a .fa or .fasta file to produce an example analysis visualization as well as an example downloadable output.</Typography>
          
          <Typography variant='h5'>Settings</Typography>
          <Typography variant='h6'>Absolute Results</Typography>
          <Typography variant='body1' paragraph>Absolute results means that we will plot absolute numbers on y axis of plots instead of relative ones. If the box is unchecked, we plot relative results, if it is checked, we plot absolute results.</Typography>

          <Typography variant='h6'>Minimum domain prevalence</Typography>
          <Typography variant='body1' paragraph>Only domains occuring in a ratio higher than the number are plotted will be present in the output (e.g. If the value is 0.5, the domain has to be present in  at least 50% of the input sequences).</Typography>

          <Typography variant='h6'>Minimum domain position conservation</Typography>
          <Typography variant='body1' display='inline'>Only domains occuring at a ratio higher than this number at a specific place in the protein group will be presented in the output (e.g. if value is 0.5, 50% of the sequences have to have this domain{' '}</Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>at the same relative position</Typography>
          <Typography variant='body1' display='inline'>).</Typography>
          <Typography variant='body1' paragraph/>

          <Typography variant='h6'>Figure Scaling</Typography>
          <Typography variant='body1' paragraph>The number input here represents the number of inches per 100 amino acids that the plot will use to display each visualization.</Typography>

          <Typography variant='h5'>Data Interpretation</Typography>
          <Typography variant='body1'>The histograms depict both the position and prevalence of each protein domain within the group of proteins input by the user.</Typography>
          <Typography variant='body1' paragraph>Note: interactive example is accessible by submitting the “Load Example” dataset on the main DomainViz page. </Typography>

          <img src={HelpImage} alt="Data Interpretations" className={classes.img}/>

          <Typography variant='body1' paragraph>Generally, results with non-overlapping domains can be directly interpreted as showing the prevalence and position of each domain with different degrees of conservation within the protein group.</Typography>
          <Typography variant='body1' paragraph>In rare cases, the visualization of a group of proteins may show two perfectly overlapping domains, for example, Domains A and B, each with 50% prevalence. There are three possible explanations:</Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Case 1: </Typography>
          <Typography variant='body1' display='inline'>A subset of proteins have no domain predicted, while the remaining subset of proteins have both domains A and B predicted at the same spot. (In this case, the subsets are each half of the total set of proteins).</Typography>
          <Typography paragraph/>
          <Typography className={classes.body2} variant='body1' display='inline'>Case 2: </Typography>
          <Typography variant='body1' display='inline'> Half the proteins have domain A and the other other half have domain B at the same position.</Typography>
          <Typography paragraph/>
          <Typography className={classes.body2} variant='body1' display='inline'>Case 3: </Typography>
          <Typography variant='body1' display='inline'>Any combination of Case 1 and Case 2 leading to the same prevalence ratios.</Typography>
          <Typography paragraph/>
          <Typography variant='body1' paragraph>Only further investigation of the results files available upon Download can further discriminate the cases.</Typography>

          <Typography variant='h5'>Downloadable Outputs</Typography>
          <Typography variant='body1'>The DomainViz output is available for download as a .zip file containing multiple files.</Typography>
          <Typography variant='body1' paragraph>This includes: Job.id.tsv files containing the raw output data from Pfam and Prosite. Job.id_ProteinGroup.csv allows users to replot the data used in creating each visualized histogram. Lastly, Job.id_ProteinGroup.pdf files that are high resolution vector files that can be used for further manipulation using any standard vector image editor (e.g. Adobe Illustrator or Affinity Designer) and/or publication.</Typography>
          <Typography className={classes.body2} variant='body1'>Result output: Job.id_pfam_res.tsv</Typography>
          <Typography variant='body1' paragraph>All results of the PFAM search as a single tab separated file. This result file mimics the tabulated files that can be downloaded for results from PFAM directly, however is not produced by PFAM. Each row depicts one domain/sequence pair. The headers are as follows: </Typography>
          <Typography variant='body1'>Sequence id: The fasta sequence header that was submitted to DomainViz.</Typography>
          <Typography variant='body1'>Family id: PFAM family identifier, can be used to find out more about the domain.</Typography>
          <Typography variant='body1'>Family Accession: PFAM family grouping: A family is a collection of related protein regions.</Typography>
          <Typography variant='body1'>Clan: PFAM clan grouping: A clan is a collection of related Pfam entries. The relationship may be defined by similarity of sequence, structure or profile-HMM.
            Env. Start: Pfam hit start. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Env. End: Pfam hit end. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Env. End: Pfam hit end. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#envelope-coordinates</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Ali. Start: Pfam hit start. See{' '} 
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Ali. End: Pfam hit end. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#alignment-coordinates</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Model Start: Start for the hidden markov model hit. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Model End: End for the hidden markov model hit. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer'>https://pfam-docs.readthedocs.io/en/latest/glossary.html?highlight=envelope#hmmer</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Bit Score: PFAM Scoring. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/scores.html'>https://pfam-docs.readthedocs.io/en/latest/scores.html</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Ind. E-value: PFAM Scoring. See{' '} 
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/scores.html'>https://pfam-docs.readthedocs.io/en/latest/scores.html</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Cond. E-value: PFAM Scoring. See{' '}
            <Link className={classes.link} to='https://pfam-docs.readthedocs.io/en/latest/scores.html'>https://pfam-docs.readthedocs.io/en/latest/scores.html</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Description: Description of the domain that is saved by PFAM.</Typography>
          <Typography variant='body1'>Outcompeted: Contains the information whether PFAM considers the domain to be outcompeted by another domain.</Typography>
          <Typography variant='body1'>Significant: Contains the information whether PFAM terms the finding as to be significant (see web output of a sequence)</Typography>
          <Typography variant='body1' paragraph>Uniq: Unique identifier for hit (unused)</Typography>
          
          <Typography className={classes.body2} variant='body1'>Result output: Job.id_prosite_res.tsv</Typography>
          <Typography variant='body1'>All results of the ProSite search as a tab separated file. This result file mimics the tabulated files that can be downloaded for results from ProSite directly, however is not produced by ProSite. It has no header. However each column contains the following information:</Typography>
          <Typography variant='body1'>Column 1: The fasta sequence header that was submitted to DomainViz.</Typography>
          <Typography variant='body1'>Column 2: Domain start.</Typography>
          <Typography variant='body1'>Column 3: Domain end.</Typography>
          <Typography variant='body1'>Column 4: Domain identifier from ProSite.</Typography>
          <Typography variant='body1'>Column 5: ProSite score</Typography>
          <Typography variant='body1'>Column 6: Prosite level. See{' '}
            <Link className={classes.link} to='https://prosite.expasy.org/prosuser.html'>https://prosite.expasy.org/prosuser.html</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1'>Column 7: Prosite level tag. See{' '}
            <Link className={classes.link} to='https://prosite.expasy.org/prosuser.html'>https://prosite.expasy.org/prosuser.html</Link>
            {' '}for reference.
          </Typography>
          <Typography variant='body1' paragraph>Column 8: Unused</Typography>

          <Typography className={classes.body2} variant='body1'>Result output: Job.id_prosite_res.tsv</Typography>
          <Typography variant='body1' paragraph>A combined plot of both pfam and prosite domains, visualized on an artificial protein with the length as the median length of the proteins in the protein group of the fasta file. Depending on the settings given as input, output files display differently and may not be represented well (in the case of too large scaling) on the webpage.</Typography>

          <Typography className={classes.body2} variant='body1'>Result Output: Job.id_ProteinGroup_pfam.pdf</Typography>
          <Typography variant='body1' paragraph>The same as the combined plot, however displaying only PFAM domains.</Typography>

          <Typography className={classes.body2} variant='body1'>Result Output: Job.id_ProteinGroup_pfam_domain_results_per_aa.tsv</Typography>
          <Typography variant='body1' paragraph>A Tab separated file, with each of the ‘artificial’ amino acid positions of the median length protein as rows, and each of the domains for PFAM as columns, showing the y-axis value displayed in the plots as numbers.</Typography>

          <Typography className={classes.body2} variant='body1'>Result Output: Job.id_ProteinGroup_prosite_domain_results_per_aa.tsv</Typography>
          <Typography variant='body1' paragraph>The same as Job.id_ProteinGroup_pfam.csv, however for ProSite domains.</Typography>


          <Typography variant='h5'>FAQ</Typography>
          <Typography variant='body1' display='inline'>1. </Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Q. How do I retrieve my results after navigating away from the processing results?</Typography>
          <Typography variant='body1'>A. Ensure that you retain the 32-character unique identifier result ID displayed on the Results page. Enter this code into the Result ID field on the home  page and hit “Go to My Results”. Alternatively, bookmark the Results page and revisit it after some time. </Typography>
          <Typography paragraph/>
          <Typography variant='body1' display='inline'>2. </Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Q. I have been warned that I have duplicate sequences in my FASTA file?</Typography>
          <Typography variant='body1'>A. DomainViz will still process your file under the assumption that duplicate sequences refer to independent proteins that share the same sequence. We advise checking that spurious duplicate sequences were not accidentally introduced during input file creation as they can lead to altered results.</Typography>
          <Typography paragraph/>
          <Typography variant='body1' display='inline'>3. </Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Q. What is the maximum number of protein sequences that can be analyzed at once?</Typography>
          <Typography variant='body1'>A. DomainViz can currently assess 1000 protein sequences at once. NOTE: The more sequences in a single query the longer the analysis will take.</Typography>
          <Typography paragraph/>
          <Typography variant='body1' display='inline'>4. </Typography>
          <Typography className={classes.body2} variant='body1' display='inline'>Q. My fasta isn't uploading, it says there is a problem with one of my lines? How do I fix this?</Typography>
          <Typography variant='body1'>A. Please remove the lines that are causing issues.</Typography>
          <Typography paragraph/>

        </Paper>
      </Grid>
    </Grid>
  );
}

