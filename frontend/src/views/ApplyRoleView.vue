<template>
  <p>
    <!-- {{$store.state.user_skills}}
    {{ listingsWithSkills }} -->
    
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
            <!-- <div class="col-5 m-0 col-sm-5 col-md-6 col-lg-3 col-xl-2">
              <a
                href="/create-posting"
                class="btn btn-dark w-100 m-2"
                style="color: greenyellow; font-weight: bold"
                >CREATE POSTING</a
              >
            </div> -->
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

          <!-- APPLICANTS -->
          <div class="row mt-3">
            <!-- Vue.js role listings go here -->
            <div v-for="listing in $store.state.all_listing" :key="listing.listing_id" class="row mt-3">
              <div class="mx-2 justify-content-center align-items-center">
                <!-- Card for each role -->
                <div
                  class="card rounded-4"
                  v-bind:data-bs-target="'#' + listing.role_tag + 'Modal'"
                  :id="listing.role_ID"
                  data-bs-toggle="modal"
                  style="cursor: pointer"
                >
                  <div class="card-body text-left" style="text-align: left">
                    <h5 class="card-title">{{ listing.listing_name }}</h5>
                    <p class="card-text">
                      Skill Match: {{ skillMatchPercentage(listingsWithSkills[listing.listing_id]) }}%
                    </p>
                    <p class="card-text">{{ listing.listing_description }}</p>
                    <p class="card-text">
                        Skill Required: 
                        <span v-for="skill in listingsWithSkills[listing.listing_id]" :key="skill">
                            <span :style="{ backgroundColor: userHasSkill(skill) ? 'yellow' : 'grey', borderRadius: '5px', padding: '5px', marginRight: '5px' }">
                                {{ skill }}
                            </span>
                        </span>
                    </p>

                    <p class="card-text">
                      Department: {{ listing.dept }}</p>
                    <p class="card-text">
                      <small class="text-muted">
                        Deadline: {{ listing.deadline }}</small
                      >
                    </p>
                    <div class="col" style="text-align: right">
                      <!-- Button to trigger applicants modal -->
                      <button
                        href="#"
                        class="btn btn-dark"
                        style="color: greenyellow; font-weight: bold"
                        >Apply</button
                      >
                      <!-- <a
                        :href="`edit_role_listing.html?role_id=${role.role_ID}`"
                        class="btn btn-dark"
                        style="color: greenyellow; font-weight: bold"
                        >Edit</a
                      > -->
                      <!-- <router-link
                        :to="{ name: 'EditPosting', params: { roleID: role.role_ID } }"
                        class="btn btn-dark"
                        style="{ color: 'greenyellow', 'font-weight': 'bold' }"

                      >
                        Edit
                      </router-link> -->
                    </div>
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
// import { ref, onMounted } from 'vue';
import axios from 'axios';
// import { mapState } from 'vuex';

export default {
  name: "ApplyRole",

  components: {}, 

  data() {
    return {
      selected_role: null,
      listing_name: "",
      listing_description: "",
      listing_department: "",
      deadline: null,
      // formSubmitted: false,
      staffID: 140025,
      listingsWithSkills: {},
      
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
    all_roles() {
      return this.$store.state.all_roles;
    },
    all_dept() {
      return this.$store.state.all_dept;
    },
    all_listing() {
      return this.$store.state.all_listing;
    },
    user_skills() {
        return this.$store.state.user_skills;
    }
  },

  methods: {
    async fetchSkillsForListing(listing_id) {
    try {
      // Fetch the skill ids for the given listing
      const response = await axios.get(`http://127.0.0.1:5002/listing_skill/${listing_id}`);
      const skill_ids = response.data.data.skill_ids;

      // Now for each skill id, fetch the skill details
      const skills = [];
      for (const skill_id of skill_ids) {
        const skillResponse = await axios.get(`http://127.0.0.1:5003/skills/${skill_id}`);
        skills.push(skillResponse.data.data.skill_name);
      }

      // Store the skills in the listingsWithSkills object
      this.listingsWithSkills[listing_id] = skills;
      console.log(skills);

    } catch (error) {
      console.error("Error fetching skills for listing:", error);
    }
    },

    userHasSkill(skill){
      return this.user_skills.includes(skill);
    },

    skillMatchPercentage(skillsForListing) {
      if (!skillsForListing || !skillsForListing.length) return 0;  // <-- Add this line

      let matchCount = 0;

      skillsForListing.forEach(skill => {
          if (this.user_skills.includes(skill)) {
              matchCount++;
          }
      });

      let percentage = (matchCount / skillsForListing.length) * 100;
      return Math.round(percentage);  // <-- Use Math.round() here
    }

  },

  created(){
    this.$store.dispatch('fetchAllListing');
    this.$store.dispatch('fetchSkillsForUser', this.staffID);
    this.$store.state.all_listing.forEach(listing => {
    this.fetchSkillsForListing(listing.listing_id);
    // console.log(listing.listing_id);
    // console.log(listing.listing_id);
  });
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
