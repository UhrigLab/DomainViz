import { React, useState } from 'react';
import { Typography} from '@material-ui/core';
import { SketchPicker } from 'react-color';

export const ColorGroupMap = ({ colorGroups }) => {
        const [cgColors, setCgColors] = useState(colorGroups);

        const handleCgColorChange = (color, event, index) => {
            let newCgColor = {"group": cgColors[index]["group"], "color": color.hex}
            setCgColors([
                ...cgColors.slice(0, index),
                newCgColor,
                ...cgColors.slice(index+1)
            ]);
            // let newColors = cgColors;
            // setCgColors(...cgColors, color.hex);
        }
        
        return (
        <>
            {colorGroups.map((group, i) => {
                return (
                    <>
                        <Typography>{cgColors[i]["group"]}</Typography>
                        <SketchPicker name={`sketch-${i}`} color={ cgColors[i]["color"] } onChangeComplete={(c, e) => handleCgColorChange(c, e, i) }/>
                    </>
                )
            })}
            
        </>
    );
}