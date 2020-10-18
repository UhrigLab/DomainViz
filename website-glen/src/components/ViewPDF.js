import React from 'react';
import { List } from 'semantic-ui-react';
import { PDF } from './PDF';

export const ViewPDF = ({ images }) => {
    return (
       <List>
           {images.map(image => {
               return (
                   <List.Item key={image.userID}>
                       <PDF pdf={image.filepath}></PDF>
                   </List.Item>
               )
           })}
       </List>
    );
}