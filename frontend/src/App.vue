<template>
  <!-- This is our Navbar -->
  <AppNavbar v-if="showNavbar"></AppNavbar>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
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
        return this.$route.name !== 'login';  // 'login' should be the name of your login route
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
