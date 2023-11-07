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

              <!-- Email input -->
              <div class="form-outline mb-4">
                <label class="form-label" for="form3Example3">Staff ID</label>
                <input type="number" v-model="userID" id="form3Example3" class="form-control" />
              </div>

              <!-- Password input -->
              <div class="form-outline mb-4">
                <div v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </div>
              </div>

              <!-- Submit button -->
              <button type="button" @click="handleLogin" class="btn btn-primary btn-block mb-4">Sign In</button>

            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userID: '',
      errorMessage: '',
    };
  },
  computed: {
    logged_in_staff() {
      return this.$store.logged_in_staff
    }
  },
  methods: {
    async handleLogin() {
    this.errorMessage = ''; 
    
    if (!this.userID) {
        this.errorMessage = 'Please enter a User ID';
        return;
    }
    
    try {
        await this.$store.dispatch('login', this.userID);
        const role = this.$store.state.logged_in_staff?.role;

        if (!role) {
            throw new Error('Role not assigned to user.');
        }

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
    } catch (error) {
        console.error('Login failed:', error);
        
        if (error.message.includes('Role not assigned')) {
            this.errorMessage = 'Your account does not have an assigned role. Please contact the system administrator.';
        } else {
            
            this.errorMessage = 'Invalid StaffID, please re-enter and try again.';
        }
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

    .error-message {
    color: red;
    border: 1px solid red;
    padding: 10px;
    margin-top: 10px;
    border-radius: 5px;
    }

</style>