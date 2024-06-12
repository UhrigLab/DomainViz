import axios from 'axios';

// This component should be used to POST the input data from the frontend to the backend, but it is currently all inside
// of DomainViz.js. Other fetch/GET requests could also be put here, although, you may want to split this up futher between
// GET and POST requests.
export default axios.create({
    baseURL: 'localhost:3000',
    timeout: 3000,
});