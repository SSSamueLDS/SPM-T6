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
          <li class="nav-item">
            <router-link to="/posting">
              <a class="nav-link" aria-current="page" href="#"
                >CREATED POSTING</a
              >
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/skills">
              <a class="nav-link" aria-current="page" href="#">SKILLS</a>
            </router-link>
          </li>
          <li class="nav-item">
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
export default {
  name: "AppNavbar",
};
</script>

<!-- You can also add styles here if needed -->
<style scoped>
/* Your styles here if any */
</style>
