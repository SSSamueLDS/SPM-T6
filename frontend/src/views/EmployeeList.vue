<template>

  <div class="PostingView">
    <div class="container text-center mt-5">
      <div class="row">
        <!-- FILTER -->
        <div class="col-2" style="text-align: left">
          <h4 style="font-weight: bold" class="mb-3">SEARCH FILTER</h4>
          <div class="row" id="skillsFilter">
            <p style="font-weight: 500" class="mb-2">Skills</p>
            <hr class="mx-2 w-75" />
            <div class="w-75">
              <div class="dropdown">
                <button class="btn btn-dark dropdown-toggle" type="button" id="dropdownMenuButton"
                style="color: greenyellow; font-weight: bold"
                data-bs-toggle="dropdown" aria-expanded="false">
                Skills filter
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="max-height: 200px; overflow-y: auto;">
                    <li>
                        <div class="m-3" @click.stop>
                            <div class="form-check" v-for="(value,name) in all_skills" :key = value>
                                <input class="form-check-input" type="checkbox" :value="value.value" :id="name" v-model="skill_filter" @click.stop @click="resetCurrentPage"/>
                                <label class="form-check-label" :for="name" @click.stop>{{value.name}}</label>
                            </div>
                        </div>
                    </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="col-10">       
          <!-- APPLICANTS -->
          <div class="row mt-3">
            <!-- Vue.js role listings go here -->
            <p v-if="employee_loading">Loading...</p>
            <p v-else-if="filteredEmployees.length == 0">No employees with such skill</p>
            <div v-else v-for="listing in groupedEmployees[currentPage]" :key="listing.staff_id" class="row mt-3">
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
          <PaginationComponent :totalPages="totalPages" v-model:currentPage="currentPage">

          </PaginationComponent>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import PaginationComponent from "@/components/PaginationComponent.vue";

export default {
  name: "ApplyRole",

  components: {
    PaginationComponent
  }, 

  data() {
    return {
      listings: [], 
      listing_skills: null,
      skill_filter: [],
      employee_skills: {},
      employee_loading: false,
      currentPage: 0,
      listingsPerPage: 5
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
    groupedEmployees() {
      let result = [];
      if (this.filteredEmployees) {
        for (let i = 0; i < this.filteredEmployees?.length; i += this.listingsPerPage) {
          let group = this.filteredEmployees.slice(i, i + this.listingsPerPage);
          result.push(group);
        }
      }
      return result;
    },
    shownListings() {
      return this.groupedEmployees[this.currentPage] || [];
    },
    totalPages() {
      return this.groupedEmployees?.length;
    }
  },

  methods: {
   
    fetchData() {
      this.employee_loading = true;
      Promise.all([
        axios.get("http://127.0.0.1:5004/staffs"),
        axios.get("http://127.0.0.1:5004/staff_skill")
      ])
      .then((responses) => {
        this.employee_loading = false;
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
    },
    resetCurrentPage(){
      this.currentPage = 0
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
