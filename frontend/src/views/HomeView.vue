<template>
  <div class="background-radial-gradient overflow-hidden">
    <div class="container px-4 py-5 px-md-5 text-center text-lg-start my-5">
    <div class="row gx-lg-5 align-items-center mb-5">
      <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10">
        <h1 class="my-5 display-5 fw-bold ls-tight" style="color: hsl(218, 81%, 95%)">
          Discover Opportunities Within <br />
          <span style="color: hsl(218, 81%, 75%)">ALL IN ONE</span>
        </h1>
        <p class="mb-4 opacity-70" style="color: hsl(218, 81%, 85%)">
          Designed exclusively for our dedicated employees, this platform opens the door to exciting job opportunities within our organization. HR professionals can also use this platform to discover and connect with the best candidates, ensuring that every role is filled by the perfect fit.
        </p>
      </div>

      <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
        <div id="radius-shape-1" class="position-absolute rounded-circle shadow-5-strong"></div>
        <div id="radius-shape-2" class="position-absolute shadow-5-strong"></div>

        <div class="card bg-glass">
          <div class="card-body px-4 py-5 px-md-5">
            <form>
              <!-- 2 column grid layout with text inputs for the first and last names -->
              <div class="row">
                <div class="col-md-6 mb-4">
                  <div class="form-outline">
                    <input type="text" id="form3Example1" class="form-control" />
                    <label class="form-label" for="form3Example1">First name</label>
                  </div>
                </div>
                <div class="col-md-6 mb-4">
                  <div class="form-outline">
                    <input type="text" id="form3Example2" class="form-control" />
                    <label class="form-label" for="form3Example2">Last name</label>
                  </div>
                </div>
              </div>

              <!-- Email input -->
              <div class="form-outline mb-4">
                <input type="number" v-model="userID" id="form3Example3" class="form-control" />
                <label class="form-label" for="form3Example3">Staff ID</label>
              </div>

              <!-- Password input -->
              <div class="form-outline mb-4">
                <input type="password" id="form3Example4" class="form-control" />
                <label class="form-label" for="form3Example4">Password</label>
              </div>

              <!-- Submit button -->
              <button type="button" @click="handleLogin" class="btn btn-primary btn-block mb-4">Sign In</button>

            </form>

            <!-- <h3>Hello {{ $store.state.logged_in_staff?.staff_fname }} {{ $store.state.logged_in_staff?.staff_lname }}</h3> -->
              <!-- <p>{{ $store.state.logged_in_staff }}</p>
              <p>{{ $store.state.user_skills }}</p> -->
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
// @ is an alias to /src
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
        console.log("Logging in with userID:", this.userID);

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


<style>
.background-radial-gradient {
      background-color: hsl(218, 41%, 15%);
      background-image: radial-gradient(650px circle at 0% 0%,
          hsl(218, 41%, 35%) 15%,
          hsl(218, 41%, 30%) 35%,
          hsl(218, 41%, 20%) 75%,
          hsl(218, 41%, 19%) 80%,
          transparent 100%),
        radial-gradient(1250px circle at 100% 100%,
          hsl(218, 41%, 45%) 15%,
          hsl(218, 41%, 30%) 35%,
          hsl(218, 41%, 20%) 75%,
          hsl(218, 41%, 19%) 80%,
          transparent 100%);
    }

    #radius-shape-1 {
      height: 220px;
      width: 220px;
      top: -60px;
      left: -130px;
      background: radial-gradient(#44006b, #ad1fff);
      overflow: hidden;
    }

    #radius-shape-2 {
      border-radius: 38% 62% 63% 37% / 70% 33% 67% 30%;
      bottom: -60px;
      right: -110px;
      width: 300px;
      height: 300px;
      background: radial-gradient(#44006b, #ad1fff);
      overflow: hidden;
    }

    .bg-glass {
      background-color: hsla(0, 0%, 100%, 0.9) !important;
      backdrop-filter: saturate(200%) blur(25px);
    }
</style>
