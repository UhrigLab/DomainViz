import { React } from 'react';
import { PDF } from './PDF';
import { Grid} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    button: {
        padding: theme.spacing(1),
        textAlign: 'center',
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
  }));
export const PDFMap = ({ images, uid }) => {
        const classes = useStyles()
        const groupsize = 3;

        

        return (
        <>
            {images.map((image, index) => {
                return (
                    <Grid item xs={4}>
                        <PDF pdf={image.file}></PDF>
                    </Grid>
                )
            })}
            
        </>
    );
}