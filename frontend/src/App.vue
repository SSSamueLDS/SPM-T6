<template>

  <AppNavbar v-if="showNavbar"></AppNavbar>
  <router-view />
  <LoadingComponent />
</template>

<script>
import AppNavbar from "./components/AppNavbar.vue";
import LoadingComponent from "./components/LoadingComponent.vue";

export default {
  components: {
    AppNavbar,
    LoadingComponent
  },

  computed:{
    loggedInStaff(){
      return this.$store.state.loggedInStaff;
    },
    showNavbar() {
        return this.$route.name !== 'login';
    }


  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
