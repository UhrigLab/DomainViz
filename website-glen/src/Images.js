import React from 'react';
import { List, Header } from 'semantic-ui-react';

export const Images = ({ images }) => {
    return (
       <List>
           {images.map(image => {
               return (
                   <List.Item key={image.userID}>
                       <Header>{image.userID}</Header>
                   </List.Item>
               )
           })}
       </List>
    );
}