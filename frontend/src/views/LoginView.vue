<template>
  <div>
    <input v-model="userID" placeholder="Enter User ID" />
    <button @click="handleLogin">Login</button>

    <h3>Hello {{ $store.state.logged_in_staff?.staff_fname }} {{ $store.state.logged_in_staff?.staff_lname }}</h3>

    <p>{{ $store.state.logged_in_staff }}</p>
    <p>{{ $store.state.user_skills }}</p>
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      userID: ''
    };
  },
  methods: {
    handleLogin() {
      if (this.userID) {
        this.$store.dispatch('login', this.userID);
        console.log(this.$store.logged_in_staff)
      } else {
        alert('Please enter a User ID');
      }
    }
  }
}
</script>

  