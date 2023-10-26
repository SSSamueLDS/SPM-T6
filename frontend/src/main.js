import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/store";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';


Promise.all([
    store.dispatch('fetchAllSkills'),
    store.dispatch('fetchAllDept'),
    store.dispatch('fetchAllRoles'),
]).catch(error => {
    console.error("An error occurred during one or more API calls:", error);
});

const app = createApp(App);
app.use(VueSweetalert2);
app.use(router);
app.use(store);
app.mount("#app");