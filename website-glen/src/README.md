# Cameron's Style Guide
This guide is to be used to understand how I styled my ReactJS components. The short answer is "poorly". This was the first website I created, and as such, the styling leaves much to be desired.

Each page is set up using the material-ui `<Grid></Grid>` component. The Grid is setup in rows, and every `{12}` xs points is equal to one row with the spacing that I used.

For example, `<Grid item xs={12} />` is one row, or, 
```html
<Grid item xs={6}> </Grid>
<Grid item xs={3}> </Grid>
<Grid item xs={2}> </Grid>
<Grid item xs={1}> </Grid>
```
is also one single row.

Sometimes there are empty `<Grid item xs={XYZ} />` objects, these are used to create empty space
Every 12 xs points are separated from the next with a blank line.

# Cameron's Component Guide
All components are functional components. Look up a React functional components guide if you need help.

For some reason, some of my components are set up as `function xyz() {}` and others as `const xyz = () => {}`. This is likely caused by me looking at different coding practices, and not realizing what the difference between the two are, or why one would choose either. This should be changed, for consistency.

As well, some components use a tab spacing of 2 spaces, and others use a spacing of 4 spaces. I'm honestly not sure when this happened, but by the time I noticed it, it would have been too much work to rectify, so I left it as is.