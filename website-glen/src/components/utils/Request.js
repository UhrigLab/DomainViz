import axios from 'axios';

export default axios.create({
    baseURL: 'localhost:3000',
    timeout: 3000,
});