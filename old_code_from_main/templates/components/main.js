// main.js
import Navbar from './navbar.js';  // Adjust the path to navbar.js if necessary

const app = Vue.createApp({});

app.component('navbar', Navbar);

app.mount('#app');
