import { React } from 'react';
import { Typography} from '@material-ui/core';

export const MessageMap = ({ messages }) => {

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