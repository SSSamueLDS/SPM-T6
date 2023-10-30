<template>
  <div class="PostingView">
    <div class="container text-center mt-5">
      <div class="row">
        <!-- FILTER -->
        <div class="col-2" style="text-align: left">
          <h4 style="font-weight: bold" class="mb-3">Filter By:</h4>
          <div class="row" id="departmentFilter">
            <p style="font-weight: 500" class="mb-2">Department</p>
            <hr class="mx-2 w-75" />
            <div class="w-75">
              <!-- Checkbox filters go here -->
              <div class="form-check" v-for="(department,id) in departments" :key = id>
                <input class="form-check-input" type="checkbox" :value="department" :id="department" v-model="selected_departments">
                <label class="form-check-label" :for="department">
                  {{department}}
                </label>
              </div>
              <div class="button">
                <button class="btn btn-dark" @click="update_listings">Filter</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-10">
          <div class="row">
            <div class="col-5 m-0 col-sm-5 col-md-6 col-lg-3 col-xl-2">
              <a
                v-if="logged_in_staff.role=='HR'||logged_in_staff.role=='Admin'"
                href="/create-posting"
                class="btn btn-dark w-100 m-2"
                style="color: rgb(252, 254, 254); font-weight: bold"
                >CREATE LISTING</a
              >
            </div>
            <div
              class="col-5 d-flex align-items-center col-sm-7 col-md-6 col-lg-9 col-xl-10"
            >
              <form class="form-inline d-flex w-100">
                <div class="input-group">
                  <input
                    class="form-control mr-2 flex-grow-1"
                    type="search"
                    placeholder="Search"
                    aria-label="Search"
                    v-model="search_term"
                  />
                  <select v-model="search_by">
                    <option value="ID">By Listing ID</option>
                    <option value="Role Name">By Role Name</option>
                  </select>
                </div>                
              </form>
              <button class="btn btn-outline-success my-2 my-sm-0 p-2"
                    @click="update_listings">
                    Search
              </button>
            </div>
          </div>

          <!-- APPLICANTS -->
          <div class="row mt-3">
            <!-- Vue.js listing listings go here -->
            <div v-if="loading_listings==true">Loading...</div>
            <div v-else-if="listings.length == 0 && loading_listings == false">No listings found</div>
            <div v-else v-for="(listing, id) in grouped_listings[current_page-1]" :key="id" class="row mt-3">
              <div class="mx-2 justify-content-center align-items-center">
                <!-- Card for each listing -->
                <div
                  class="card rounded-4"
                  style="cursor: pointer"
                  :id="listing.listing_ID"
                >
                  <div class="card-body text-left" style="text-align: left">

                    <h5 class="card-title">Listing #{{ listing.listing_id }}: {{ listing.listing_name }}</h5>
                    <p class="card-text">{{ listing.listing_description }}</p>
                    <p class="card-text">
                      <small class="text-muted">
                        Department: {{ listing.dept }}<br>
                        Deadline: {{ listing.deadline }} <br>
                        Listing ID: {{ listing.listing_id }}
                      </small>
                        
                    </p>

                    <div class="col" style="text-align: right">
                      <button
                        href="#"
                        class="btn btn-dark"
                        v-if="logged_in_staff.role=='HR'||logged_in_staff.role=='Admin'"
                        @click="toEditPage(listing.listing_id)"
                        style="color: greenyellow; font-weight: bold"
                        >Edit</button
                      >
                      <button
                        href="#"
                        class="btn btn-dark"
                        @click="fetchApplications(listing.listing_id)"
                        data-bs-toggle="modal"
                        v-bind:data-bs-target="
                          '#' + listing.listing_tag + 'ApplicantsModal'
                        "
                        style="color: greenyellow; font-weight: bold"
                        >View Applicants</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Listing-specific cards pop up description -->
              <div
                class="modal fade"
                :id="listing.listing_tag + 'Modal'"
                tabindex="-1"
                :aria-labelledby="listing.listing_tag"
                aria-hidden="true"
              >
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" :id="listing.listing_tag">
                        {{ listing.listing_name }}
                      </h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body" style="text-align: left">
                      <!-- Listing-specific details go here -->
                      <p style="font-weight: bold">
                        Application Deadline: {{ listing.deadline }}
                      </p>
                      <p>Required Skills: {{ listing.skill_names.join(", ") }}</p>
                      <p style="font-weight: bold">About the listing</p>
                      <p>{{ listing.listing_description }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Listing-specific Applicants Modal -->
              <div
                class="modal fade"
                :id="listing.listing_tag + 'ApplicantsModal'"
                tabindex="-1"
                :aria-labelledby="listing.listing_tag + 'ApplicantsModalLabel'"
                aria-hidden="true"
                ref="applicantsModal"
              >
                <div
                  class="modal-dialog modal-dialog-centered modal-dialog-scrollable"
                >
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5
                        class="modal-title"
                        :id="listing.listing_tag + 'ApplicantsModalLabel'"
                      >
                        Applicants for {{ listing.listing_name }}
                      </h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <p>
                        List of applicants for the
                        {{ listing.listing_name }} position.
                      </p>
                      <div class="row">
                        <p v-if="loading_applications == true">Loading...</p>
                        <p v-else-if="filteredApplications.length == 0 && loading_applications == false">No applicants yet</p>
                        <table v-else class="table">
                          <thead>
                            <tr>
                              <th scope="col=" class="col-1">#</th>
                              <th scope="col" class="col-3">Staff ID</th>
                              <th scope="col" class="col-3">Staff Name</th>
                              <th scope="col" class="col-3">Date Applied</th>
                              <th scope="col" class="col-1"></th>
                            </tr>
                          </thead>
                          <tbody class="text-center align-middle">
                            <!-- Applicants table rows go here -->
                            <!-- {{ listing.listing_name }} -->
                            <tr v-for="(application, index) in filteredApplications" :key="application.application_id" :currentListing="listing">
                              
                                <th scope="row" class="col-1">{{ index + 1 }}</th>
                                <td class="col-3">{{ application.staff_id }}</td>
                                <td class="col-3">{{ application.staff_name }}</td>
                                <td class="col-3">{{ application.date_applied }}</td>
                                <td class="col-1">
                                    <!-- {{ listing.listing_name }} -->
                                    <button type="button"
                                      data-bs-dismiss="modal"
                                      aria-label="Close"
                                    class="btn btn-sm btn-primary" @click="viewApplicant(application.application_id, listing.listing_name)">View</button>
                                </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>                      
          </div>
          <nav aria-label="Skill page navigation" v-if="grouped_listings.length>0">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link text-black" @click="go_previous_page()"
                  >Previous</a
                >
              </li>
              <li class="page-item" v-for="i in grouped_listings.length" :key="i">
                <a class="page-link text-black" @click="go_page(i)">{{ i }}</a>
              </li>
              <li class="page-item">
                <a class="page-link text-black" @click="go_next_page()">Next</a>
              </li>
            </ul>
          </nav>
        </div>       
      </div>
    </div>
  </div>
</template>

  <script>
  import axios from "axios";

export default {
  name: "PostingView",
  components: {},
  data() {
    return {
      listings: [],
      shown_listings: [],
      listing_skills: null,
      search_by: "ID",
      grouped_listings: [],
      current_page: 1,
      departments: [],
      selected_departments: [],
      search_term: "",
      applications: [],
      loading_listings: false,
      loading_applications: false
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
    filteredApplications() {
      return this.applications?.length ? this.applications : [];
    },
    logged_in_staff() {
      return this.$store.state.logged_in_staff;
    }
  },
  methods: {

    update_listings(){
      var result = this.listings
      //if no departments are selected, show all listings
      if (this.selected_departments.length == 0){
        result = this.listings
      }
      //else, show only listings from selected departments
      else{
        result = this.listings.filter(listing => this.selected_departments.includes(listing.dept))
      }

      //if search term is not empty
      if (this.search_term != ""){
        //if search by is ID, filter listings by ID
        if (this.search_by == "ID"){
          result = result.filter(listing => listing.listing_id == this.search_term)
        }
        // else if search by is Role Name, filter listings by Role Name
        else if (this.search_by == "Role Name"){
          result = result.filter(listing => listing.listing_name.toLowerCase().includes(this.search_term.toLowerCase()))
        }
      }
      

      this.shown_listings = result
      this.grouped_listings = this.group_listings();
      this.current_page = 1;

    },
    go_page(i) {
      this.current_page = i;
    },
    go_previous_page() {
      if (this.current_page > 1) {
        this.current_page--;
      }
    },
    go_next_page() {
      if (this.current_page < this.grouped_listings.length - 1) {
        this.current_page++;
      }
    },
    group_listings() {
      var grouped_listings = [];
      var group = [];
      var i = 0;
      if (this.shown_listings.length == 0){
        return []
      }
      for (i = 0; i < this.shown_listings.length; i++) {
        if (i % 5 == 0 && i != 0) {
          grouped_listings.push(group);
          group = [];
        }
        group.push(this.shown_listings[i]);
      }
      grouped_listings.push(group);
      console.log(grouped_listings);
      return grouped_listings;
    },

    toEditPage(listingId) {
      this.$router.push(`/edit-posting/${listingId}`)
    },
    processListingName(listingName) {
      // Remove all occurrences of '#' from listingName
      return listingName.replace(/[^a-zA-Z0-9\s]/g, "").replace(/\s/g, "_");
    },
    fetchData() {
      this.loading_listings = true;
      axios.get("http://127.0.0.1:5002/listing_skill")
        .then((response) => {
          this.listing_skills = response.data.data;
          return axios.get("http://127.0.0.1:5002/listings");
        })
        .then((response) => {
          this.listings = response.data.data;
          //remove listings which have expired
          this.listings = this.listings.filter(listing => new Date(listing.deadline) > new Date())

          this.listings.forEach((listing) => {
            listing.listing_tag = this.processListingName(listing.listing_name);
            let skillIdsForListing = this.listing_skills?.[listing.listing_id] || [];
            listing.skill_names = skillIdsForListing.map(id => {
                const skill = this.all_skills.find(skill => skill.value === id);
                return skill ? skill.name : "Unknown Skill";
            });
          this.loading_listings = false;
          });
          //show all listings by default
          this.shown_listings = this.listings
          console.log(this.shown_listings.length)
          
                
          //find out all the departments from all listings
          for (var i = 0; i<this.shown_listings.length; i++){
            if (!this.departments.includes(this.shown_listings[i].dept)){
              this.departments.push(this.shown_listings[i].dept)
            }
          }
          //arrange departments array alphabetically
          this.departments.sort()
          console.log(this.departments.length)

          //group listings in groups of 5, for display purposes
          this.grouped_listings = this.group_listings();
          console.log(this.grouped_listings.length)

        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    fetchApplications(listingId){
      this.loading_applications = true;
      this.applications = [];
      axios.get(`http://127.0.0.1:5006/listings/${listingId}/applications`)
      .then(appResponse => {
        this.applications = appResponse.data.data;
        this.loading_applications = false;
      })
      .catch(error => {
        console.error("Error fetching applications:", error);
      });
    },
    viewApplicant(applicantionId, listingName){
      console.log("listingName before route push:", listingName);
      this.$router.push(`/view-applicant-skill/${applicantionId}`);
    }
  },
  created() {
    if (this.$store.state.logged_in_staff == null) {
      this.$router.push("/login")
    }
    var role = this.$store.state.logged_in_staff.role;
    switch(role) {
      case "User":
          this.$router.push('/apply-role');
          break;
      case "Manager":
          this.$router.push('/posting');
          break;
    }
    this.fetchData();
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
