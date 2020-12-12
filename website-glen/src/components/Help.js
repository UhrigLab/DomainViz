import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    textAlign: 'left',
    color: theme.palette.text.secondary,
  },
}));
export const Help = () => {
  const classes = useStyles()

  return (
    <Grid container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }}>
      <Grid item xs={11}>
        <Typography variant='h5'>Help</Typography>

        <Paper className={classes.paper} variant='outlined'>
          <Typography variant='h5'>Introduction</Typography>
          <Typography variant='body1' paragraph>DomainViz allows users to identify and visualize protein domains on one or more  sequences across multiple domain prediction platforms (PFAM and Prosite) to understand the consensus positionality and abundance of different domains within protein groups and families.</Typography>
            
            <Typography variant='h5'>General Operations</Typography>
            <Typography variant='h6'>File Upload:</Typography>
            <Typography variant='body1' paragraph>DomainViz accepts a single multiple sequence fasta file. The file extension should be .FA or .FASTA and the file size should be less than 10 Mb. Each sequence present within the fasta file should be formatted as follows:</Typography>
            
            <Typography variant='h6'>File Upload:</Typography>
            <Typography variant='caption' paragraph>
              {'>'}AT3G19040.1|PACid:19663337_AtTAFIIb
              MICRVDYGSNDEEYDGPELQVVTEEDHLLPKREYLSAAFALSGLNSRASVFDDEDYDEQGGQEKEHVPVEKSFDSEEREPVVLKEEKPV
              KHEKEASILGNKNQMDTGDVQEELVVGLSEATLDEKRVTPLPTLYLEDDGMVILQFSEIFAIQEPQKKRQKREIRCITYRDKYISMDISELIEDDEEVLL
              KSHGRIDTHGKKTDQIQLDVPLPIRERSQLVKSGIVRDTTSESREFTKLGRDSCIMGELLKQDLKDDNSSLCQSQLTMEVFPLDQQEWEHLILWEISPQF
              SANCCEGFKSGLESAGIMVQVRASNSVTEQESLNVMNSGGQTQGDNNNMLEPFFVNPLESFGSRGSQSTNESTNKSRHHPQLLRLESQWDEDHYRENGDA
              GRENLKQLNSDARGRLSGLALQDRDMWDESWLDSIIWESDKDLSRSKLIFDLQDEQMIFEVPNNKERKYLQLHAGSRIVSRSSKSKDGSFQEGCGSNSGW
              QFNISNDKFYMNGKSAQKLQGNAKKSTVHSLRVFHSAPAIKLQTMKIKLSNKERANFHRPKALWYPHDNELAIKQQKILPTQGSMTIVVKSLGGKGSLLT
              VGREESVSSLKAKASRKLDFKETEAVKMFYMGKELEDEKSLAEQNVQPNSLVHLLRTKVHLWPWAQKLPGENKSLRPPGAFKKKSDLSNQDGHVFLMEYC
              EERPLMLSNAGMGANLCTYYQKSSPEDQHGNLLRNQSDTLGSVIILEHGNKSPFLGEVHGGCSQSSVETNMYKAPVFPHRLQSTDYLLVRSAKGKLSLRR
              INKIVAVGQQEPRMEIMSPASKNLHAYLVNRMMAYVYREFKHRDRIAADELSFSFSNISDATVRKYMQVCSDLERDANGKACWSKKRKFDKIPLGLNTLV
              APEDVCSYESMLAGLFRLKHLGITRFTLPASISTALAQLPDERIAAASHIARELQITPWNLSSSFVTCATQGRENIERLEITGVGDPSGRGLGFSYVRVA
              PKSSAASEHKKKKAAACRGVPTVTGTDADPRRLSMEAAREVLLKFNVPDEIIAKQTQRHRTAMIRKISSEQAASGGKVGPTTVGMFSRSQRMSFLQLQQQ
              AREMCHEIWDRQRLSLSACDDDGNESENEANSDLDSFVGDLEDLLDAEDGGEGEESNKSMNEKLDGVKGLKMRRWPSQVEKDEEIEDEAAEYVELCRLLM
              QDENDKKKKKLKDVGEGIGSFPPPRSNFEPFIDKKYIATEPDASFLIVNESTVKHTKNVDKATSKSPKDKQVKEIGTPICQMKKILKENQKVFMGKKTAR
              ANFVCGACGQHGHMKTNKHCPKYRRNTESQPESMDMKKSTGKPSSSDLSGEVWLTPIDNKKPAPKSATKISVNEATKVGDSTSKTPGSSDVAAVSEIDSG
              TKLTSRKLKISSKAKPKASKVESDSPFHSLMPAYSRERGESELHNPSVSGQLLPSTETDQAASSRYTTSVPQPSLSIDKDQAESCRPHRVIWPPTGKEHS
              QKKLVIKRLKEITDHDSGSLEETPQFESRKTKRMAELADFQRQQRLRLSENFLDWGPKDDRKWRKEQDISTELHREGKVRRAYDDSTVSEERSEIAESRR
              YREVIRSEREEEKRRKAKQKKKLQRGILENYPPRRNDGISSESGQNINSLCVSDFERNRTEYAPQPKRRKKGQVGLANILESIVDTLRVKEVNVSYLFLK
              PVTKKEAPNYLEIVKCPMDLSTIRDKVRRMEYRDRQQFRHDVWQIKFNAHLYNDGRNLSIPPLADELLVKCDRLLDEYRDELKEAEKGIVDSSDSLR*
            </Typography>
            <Typography variant='body1' paragraph>The chevron denotes the header line containing unique identifying information, which is ended by a line return to denote this as a separate entity from the sequence. At the end of each sequence should be a (*) to ensure the end of the sequence is denoted. Sequences of 16 amino acids or less, and greater than 5000 amino acids are not compatible with DomainViz.</Typography>
            
            <Typography variant='h6'>Submit Task and Analysis:</Typography>
            <Typography variant='body1' paragraph>Once a file is successfully uploaded, the GO button is engaged to start the analysis. This will automatically transition to a new, analysis-specific page with an unique identifying 32 digit code that should be retained for subsequent retrieval of the results files for upto 7 days post analysis.</Typography>
            <Typography variant='body1' paragraph>For example: 5ff3eeda.5842.5879.d627.f4d1faea3c84</Typography>
            <Typography variant='body1' paragraph>Without this code, the data will not be retrievable and the analysis will need to be re-run. If an error occurs, please follow the directions in the pop-up box that results.</Typography>
            
            <Typography variant='h6'>Data Retrieval:</Typography>
            <Typography variant='body1' paragraph>To retrieve a previous analysis, the code provided upon initiation of an analysis needs to be placed into the “User ID” text box on the main page of DomainViz. Analyses are retained for a total of 7 days prior to automatic deletion.</Typography>
            <Typography variant='h6'>Load Example:</Typography> 
            <Typography variant='body1' paragraph>This option will automatically load a .fa or .fasta file to produce an example analysis visualization as well as an example downloadable output.</Typography>
            
            <Typography variant='h5'>Settings</Typography>
            <Typography variant='h6'>Absolute Results</Typography>
            <Typography variant='body1' paragraph>Absolute results means that we will plot absolute numbers on y axis of plots instead of relative ones. If the box is unchecked, we plot relative results, if it is checked, we plot absolute results. </Typography>

            <Typography variant='h6'>Minimum domain prevalence</Typography>
            <Typography variant='body1' paragraph>Only domains occuring in a ratio higher than the number are plotted will be present in the visualized and compiled output (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).</Typography>

            <Typography variant='h6'>Minimum domain position conservation</Typography>
            <Typography variant='body1' paragraph>Only domains occuring in a ratio higher than the number at at least one relative place in the protein group will be present in the visualized and compiled output (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).</Typography>

            <Typography variant='h6'>Figure Scaling</Typography>
            <Typography variant='body1' paragraph>The number input here represents the number of inches per 100base pairs that the plot will use to display each visualization.</Typography>

            <Typography variant='h5'>Interpretation of the data</Typography>
            <Typography variant='body1' paragraph>If the visualization of a group of proteins shows two overlapping domains A and B, at for example each 0.5 prevalence, then there are three ways how the figure could have been compiled in this way.</Typography>
            <Typography variant='body1' paragraph>Case 1: A subset of proteins have no domain predicted, while the remaining subset of proteins have both domains A and B predicted at the same spot. (In this case, the subsets are each half of the total set of proteins).</Typography>
            <Typography variant='body1' paragraph>Case 2: A subset of proteins have domain A predicted, and the an other subset of proteins have domain B predicted. (In this case, the subsets are each half of the total set of proteins.</Typography>
            <Typography variant='body1' paragraph>Case 3: Any combination of Case 1 and Case 2 leading to the same prevalence ratios. Only further investigation of the results available in the download option can discriminate the case.</Typography>

            <Typography variant='h5'>FAQ</Typography>
          </Paper>
      </Grid>
    </Grid>
  );
}

