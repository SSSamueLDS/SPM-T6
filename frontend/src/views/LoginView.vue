<template>
  <div>
    <input v-model="userID" placeholder="Enter User ID" />
    <button @click="handleLogin">Login</button>

    <h3>Hello {{ $store.state.staff_fname }} {{ $store.state.staff_lname }}</h3>
    <!-- <p>{{ $store.state.staff_id }}</p>
    <p>{{ $store.state.staff_fname }}</p>
    <p>{{ $store.state.staff_lname }}</p> -->
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
        console.log(this.$store)
      } else {
        alert('Please enter a User ID');
      }
    }
  }
}
</script>

  