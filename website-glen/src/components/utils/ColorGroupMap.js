import { React, useState } from 'react';
import { Grid, Typography} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { SketchPicker } from 'react-color';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    button: {
        padding: theme.spacing(1),
        textAlign: 'center',
    },
    colorPicker: {
        position: 'fixed',
        top: '0px',
        right: '0px',
        bottom: '0px',
        left: '0px',
    },
  }));
export const ColorGroupMap = ({ colorGroups }) => {
        const classes = useStyles()
        const [cgColors, setCgColors] = useState(colorGroups);

        const handleCgColorChange = (color, event, index) => {
            let newCgColor = {"group": cgColors[index]["group"], "color": color.hex}
            setCgColors([
                ...cgColors.slice(0, index),
                newCgColor,
                ...cgColors.slice(index+1)
            ])
            console.log(index)
            // let newColors = cgColors;
            // setCgColors(...cgColors, color.hex);
        }
        
        return (
        <>
            {colorGroups.map((group, i) => {
                return (
                    <>
                        <Typography>{cgColors[i]["group"]}</Typography>
                        <SketchPicker name="sketch-${i}" color={ cgColors[i]["color"] } onChangeComplete={(c, e) => handleCgColorChange(c, e, i) }/>
                    </>
                )
            })}
            
        </>
    );
}