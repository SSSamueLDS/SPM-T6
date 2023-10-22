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
  computed: {
    logged_in_staff() {
      return this.$store.logged_in_staff
    }
  },
  methods: {
  async handleLogin() {
    if (this.userID) {
      try {
        await this.$store.dispatch('login', this.userID);
        const role = this.$store.state.logged_in_staff?.role;

        if (role) {
          switch(role) {
            case "User":
              this.$router.push('/apply-role');
              break;
            case "HR":
              this.$router.push('/posting');
              break;
            default:
              this.$router.push('/posting');
          }
        }
      } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed, please try again.');
      }
    } else {
      alert('Please enter a User ID');
    }
  }
}

}
</script>

  