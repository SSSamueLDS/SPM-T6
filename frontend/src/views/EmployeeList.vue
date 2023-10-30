<template>
  <p>
    <!-- {{ user_skills }} -->
    <!-- {{ $store.state.all_skills }} -->
  </p>

  <div class="PostingView">
    <div class="container text-center mt-5">
      <div class="row">
        <!-- FILTER -->
        <div class="col-2" style="text-align: left">
          <h4 style="font-weight: bold" class="mb-3">SEARCH FILTER</h4>
          <div class="row" id="departmentFilter">
            <p style="font-weight: 500" class="mb-2">Department</p>
            <hr class="mx-2 w-75" />
            <div class="w-75">
              <!-- Checkbox filters go here -->
              <div class="form-check" v-for="(value,name) in all_skills" :key = value>
                <input class="form-check-input" type="checkbox" :value="value.value" :id="name" v-model="skill_filter">
                <label class="form-check-label" :for="name">
                  {{value.name}}
                </label>
              </div>
            </div>
          </div>

          <div class="row" id="AnotherFilter">
            <p style="font-weight: 500" class="my-2">Another Filter</p>
            <hr class="mx-2 w-75" />
            <div class="w-75">
              <!-- Another set of checkbox filters go here -->
            </div>
          </div>
        </div>
        <div class="col-10">
          <div class="row">
            <div
              class="col-5 d-flex align-items-center col-sm-10 col-md-12 col-lg-12 col-xl-12"
            >
              <form class="form-inline d-flex w-100">
                <div class="input-group">
                  <input
                    class="form-control mr-2 flex-grow-1"
                    type="search"
                    placeholder="Search"
                    aria-label="Search"
                  />
                  <button
                    class="btn btn-outline-success my-2 my-sm-0 p-2"
                    type="submit"
                  >
                    Search
                  </button>
                </div>
              </form>
            </div>
          </div>

          <div
            class="row mx-2 mt-3 w-100"
            style="background-color: grey; color: white; border-radius: 10px"
          >
            <h5 class="title m-3" style="text-align: left">Sort By</h5>
          </div>
          
            <!--{{ listings }-->
          <!-- APPLICANTS -->
          <div class="row mt-3">
            <!-- Vue.js role listings go here -->
            <div v-for="listing in filteredEmployees" :key="listing.staff_id" class="row mt-3">
              <div class="mx-2 justify-content-center align-items-center">
                <!-- Card for each employee -->
                  <div class="card-body text-left" style="text-align: left">
                    <h5 class="card-title">{{ listing.staff_fname }} {{ listing.staff_lname }}</h5>                    
                    
                    <p class="card-text">
                      ID: {{ listing.staff_id }}</p>
                    <p class="card-text">
                      Department: {{ listing.dept }}</p>
                      <p class="card-text">
                      Country: {{ listing.country }}</p>
                      <p class="card-text">
                      email: {{ listing.email }}</p>
                    
                    <div class="col" style="text-align: right">
                      <!-- Button to trigger applicants modal -->
                      <!-- {{ listing.listing_id }} -->
                      <button
                        href="#"
                        class="btn btn-dark"
                        style="color: greenyellow; font-weight: bold"
                        @click="applyForListings(listing.staff_id)"
                        >View Detail</button
                      >

                      
                    
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ApplyRole",

  components: {}, 

  data() {
    return {
      listings: [], 
      listing_skills: null,
      listingsWithSkills: {},
      skill_filter: [],
      employee_skills: {}
    };
  },
  computed: {
    all_skills() {
      return this.$store.state.all_skills.map(item => {
        return {
          value: item.skill_id,
          name: item.skill_name
        }})
    },
    filteredEmployees() {
      if (this.skill_filter.length === 0) {
        return this.listings;
      } else {
        return this.listings.filter(employee => {
          const skills = this.employee_skills[employee.staff_id] || [];
          return this.skill_filter.every(skill => skills.includes(skill));
        });
      }
    },
    all_roles() {
      return this.$store.state.all_roles;
    },
    all_dept() {
      return this.$store.state.all_dept;
    },
    // all_listing() {
    //   return this.$store.state.all_listing;
    // },
    user_skills() {
        return this.$store.state.user_skills;
    },
    
  },

  methods: {
   
    fetchData() {
      Promise.all([
        axios.get("http://127.0.0.1:5004/staffs"),
        axios.get("http://127.0.0.1:5004/staff_skill")
      ])
      .then((responses) => {
        this.listings = responses[0].data.data;
        console.log(this.listings);
        // Handle responses[1] as needed for staff_skill
        this.employee_skills = responses[1].data.data;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });

    },


    

    applyForListing(staffId) {
    const staffIdStr = staffId.toString(); // Ensure staffId is a string
    const link = `http://localhost:8080/employees/${staffIdStr}`;
    
    // Navigate to the link
    window.location.href = link;
},
applyForListings(staffId) {
    // Use Vue Router to navigate to the destination component with 'staffId' as a query parameter
    this.$router.push({ path: `/employees/${staffId}`, query: { staffId: staffId } });
  }

  },

  created(){
    this.$store.commit('setLoading', true);
    this.fetchData();
    this.$store.commit('setLoading', false);
  }
};
</script>

<style scoped>

h5 {
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    "Open Sans",
    "Helvetica Neue",
    sans-serif;
}
</style>
