import { React } from 'react';
import { Typography} from '@material-ui/core';

export const MessageMap = ({ messages }) => {
    /* This component displays the messages received from the cookies generated by Pascal's domainviz.py script,
     * 
     * As a `Map` component, this component receives a list of objects, strings in this instance,
     * and displays each object in a way that allows reusability, and conciseness.
     * 
     * Must be used inside of a Grid item component. 
     * Should be used inside of a Paper component for best styling.
     */
    return (
        <>
            <Typography variant='h5'>{"Information about the run: "}</Typography>
            {messages.map((message, index) => {
                return (
                    <>
                        <Typography variant='h5'>{message}</Typography>
                    </>
                    
                )
            })}
        </>
    );
}