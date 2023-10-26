<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" style="color: #7fffd4" href="#">THE JOB SEEKER</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">

          <!-- For HR Role -->
        
          <li v-if="userRole === 'Manager'" class="nav-item">
            <router-link to="/posting">
              <a class="nav-link" aria-current="page" href="#">JOB POSTINGS</a>
            </router-link>
          </li>

          <li v-if="userRole === 'Admin'" class="nav-item">
            <router-link to="/posting">
              <a class="nav-link" aria-current="page" href="#">JOB POSTINGS</a>
            </router-link>
          </li>

          <li v-if="userRole === 'User'" class="nav-item">
            <router-link to="/apply-role">
              <a class="nav-link">FIND JOB</a>
            </router-link>
          </li>

          <!-- <li class="nav-item">
            <router-link to="/skills">
              <a class="nav-link" aria-current="page" href="#">SKILLS</a>
            </router-link>
          </li> -->

          <li v-if="userRole === 'Manager'" class="nav-item">
            <router-link to="/employees">
              <a class="nav-link" aria-current="page" href="#">EMPLOYEES</a>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/logout">
              <a class="nav-link" aria-current="page" href="#">LOGOUT</a>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: "AppNavbar",
  computed: {
    ...mapState(['logged_in_staff']),
    userRole() {
      return this.logged_in_staff ? this.logged_in_staff.role : null;
    }
  },
  mounted() {
  console.log("Logged in staff:", this.logged_in_staff);
  }
};

</script>

<!-- You can also add styles here if needed -->
<style scoped>
/* Your styles here if any */
</style>
