import { React, useState, Fragment } from 'react';
import { Button, Grid, makeStyles, TextField, Typography} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    button: {
        padding: theme.spacing(1),
        textAlign: 'center',
    },
}));

export const FastaFileMap = ({ fastaFiles, changeName }) => {
        const classes = useStyles();
        const [faFileNames, setFAFileNames] = useState([]);

        const handleFAFilesChange = (event, faFileName, index) => {
            if (faFileNames.length < fastaFiles.length) {
                let names = []
                for (let i=0; i<fastaFiles.length; i++) {
                    names.push(fastaFiles[i].name);
                }
                setFAFileNames([
                    ...names.slice(0, index),
                    faFileName,
                    ...names.slice(index+1)
                ]);
            }
            else {
                setFAFileNames([
                    ...faFileNames.slice(0, index),
                    faFileName,
                    ...faFileNames.slice(index+1)
                ]);
            }
        }

        const returnName = (event, index) => {
            if (faFileNames.length !== 0) {
                changeName(index, faFileNames[index]);
            }
            else {
                alert("Please change a name before clicking the \"Confirm\" button.")
            }
        }

        return (
        <>
            {fastaFiles.map((file, i) => {
                return (
                    
                    <Fragment key={i}>
                        {(file.name !== "test" && file.file !== "test") &&
                            <>
                                <Grid item xs={4}>
                                    <Typography>{"Rename: " + file.name}</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <TextField name="fasta-filename-${i}" onChange={(e) => handleFAFilesChange(e, e.target.value, i)}/>
                                </Grid>
                                <Grid item xs={4}>
                                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={(e) => returnName(e, i)}>Confirm</Button>
                                </Grid>
                            </>
                        }
                    </Fragment>
                )
            })}
        </>
    );
}