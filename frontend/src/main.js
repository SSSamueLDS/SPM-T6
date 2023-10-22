import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/store";
import "bootstrap/dist/css/bootstrap.css";

import "bootstrap/dist/js/bootstrap.js";


Promise.all([
    store.dispatch('fetchAllSkills'),
    store.dispatch('fetchAllDept'),
    store.dispatch('fetchAllRoles'),
]).catch(error => {
    console.error("An error occurred during one or more API calls:", error);
});

createApp(App).use(router).use(store).mount("#app");