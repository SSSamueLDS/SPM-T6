<template>
  <div class="PostingView">
    <div class="container mt-5">
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
          <div class="row ">
            <div
              class="col-5 d-flex col-sm-10 col-md-12 col-lg-12 col-xl-12"
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

              <!-- Use the child component with v-for and pass necessary props -->
              <ListingCard 
              v-for="listing in validListings" 
              :key="listing.listing_id"
              :listing="listing"
              :userSkills="user_skills"
              :skillMatchPercentage="skillMatchPercentage"
              :truncateDescription="truncateDescription"
              :userHasSkill="userHasSkill"
              :applyForListing="applyForListing"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ListingCard from '../components/ListingCard.vue';

export default {
  name: "ApplyRole",

  components: {
    ListingCard
  }, 

  data() {
    return {
      listings: [], 
      listing_skills: null,
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
    // all_listing() {
    //   return this.$store.state.all_listing;
    // },
    user_skills() {
        return this.$store.state.user_skills;
    },
    validListings() {
        return this.listings?.filter(listing => !this.isListingExpired(listing.deadline));
    }
  },

  methods: {
    processListingName(listingName) {
      // Remove all occurrences of '#' from listingName
      return listingName.replace(/[^a-zA-Z0-9\s]/g, "").replace(/\s/g, "_");
    },
    fetchData() {
      axios.get("http://127.0.0.1:5002/listing_skill")
        .then((response) => {
          this.listing_skills = response.data.data;
          return axios.get("http://127.0.0.1:5002/listings");
        })
        .then((response) => {
          this.listings = response.data.data;
          this.listings.forEach((listing) => {
            listing.listing_tag = this.processListingName(listing.listing_name);
            let skillIdsForListing = this.listing_skills?.[listing.listing_id] || [];
            listing.skill_ids = skillIdsForListing;
            listing.skill_names = skillIdsForListing.map(id => {
                const skill = this.all_skills.find(skill => skill.value === id);
                return skill ? skill.name : "Unknown Skill";
            });
          });
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
        
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
    }, 

    truncateDescription(description) {
        const words = description.split(' ');
        if (words.length > 100) {
            return words.slice(0, 100).join(' ') + '...';
        }
        return description;
    },

    isListingExpired(deadline) {
        const today = new Date();
        const listingDeadline = new Date(deadline);
        return today > listingDeadline;
    },

    applyForListing(listingId) {
  // Example data format - adjust as per your backend's expectations
  const applicationData = {
    staff_id: this.$store.state.logged_in_staff["staff_id"], 
     // Assuming you store userId in your Vuex store
     listing_id: listingId
  };

  axios.post("http://127.0.0.1:5006/apply", applicationData)
    .then(response => {
      if (response.status === 201) {
        this.$swal({
        title: 'Suceess!',
        text: 'Your Job Application is Successful',
        icon: 'success',
        confirmButtonText: 'Okay'
      });
        
      } else {
        console.log(applicationData);
        this.$swal({
            title: 'Oops!',
            text: 'There was an issue submitting your application.',
            icon: 'error',
            confirmButtonText: 'Try Again'
        });
      }
    })
    .catch(error => {
      if (error.response){
        console.log(error.response.data.message);
        this.$swal({
            title: 'Error!',
            text: error.response.data.message,
            icon: 'error',
            confirmButtonText: 'Try Again'
        });
      }
    });
    },

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
