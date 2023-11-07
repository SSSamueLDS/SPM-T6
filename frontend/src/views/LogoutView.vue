<template>
    <div class="logout">
      <h2>Logout</h2>
      <p>Are you sure you want to logout?</p>
      <button @click="logout">Yes, Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        this.$store.commit('logout');
        this.$router.push('/login'); 
      },
    },
  };
  </script>
  