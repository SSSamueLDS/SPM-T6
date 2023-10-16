<template>
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
            <div class="col-5 m-0 col-sm-5 col-md-6 col-lg-3 col-xl-2">
              <a
                href="/create-posting"
                class="btn btn-dark w-100 m-2"
                style="color: greenyellow; font-weight: bold"
                >CREATE POSTING</a
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
            <div v-for="(role, id) in roles" :key="id" class="row mt-3">
              <div class="mx-2 justify-content-center align-items-center">
                <!-- Card for each role -->
                <div
                  class="card rounded-4"
                  v-bind:data-bs-target="'#' + role.role_tag + 'Modal'"
                  :id="role.role_ID"
                  data-bs-toggle="modal"
                  style="cursor: pointer"
                >
                  <div class="card-body text-left" style="text-align: left">
                    <h5 class="card-title">{{ role.role_name }}</h5>
                    <p class="card-text">{{ role.role_description }}</p>
                    <p class="card-text">
                      <small class="text-muted">
                        Deadline: {{ role.deadline }}</small
                      >
                    </p>
                    <div class="col" style="text-align: right">
                      <!-- Button to trigger applicants modal -->
                      <a
                        href="#"
                        class="btn btn-dark"
                        data-bs-toggle="modal"
                        v-bind:data-bs-target="
                          '#' + role.role_tag + 'ApplicantsModal'
                        "
                        style="color: greenyellow; font-weight: bold"
                        >View Applicants</a
                      >
                      <!-- <a
                        :href="`edit_role_listing.html?role_id=${role.role_ID}`"
                        class="btn btn-dark"
                        style="color: greenyellow; font-weight: bold"
                        >Edit</a
                      > -->
                      <router-link
                        :to="{ name: 'EditPosting', params: { roleID: role.role_ID } }"
                        class="btn btn-dark"
                        style="{ color: 'greenyellow', 'font-weight': 'bold' }"

                      >
                        Edit
                      </router-link>

                    </div>
                  </div>
                </div>
              </div>

              <!-- Role-specific cards pop up description -->
              <div
                class="modal fade"
                :id="role.role_tag + 'Modal'"
                tabindex="-1"
                :aria-labelledby="role.role_tag"
                aria-hidden="true"
              >
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" :id="role.role_tag">
                        {{ role.role_name }}
                      </h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body" style="text-align: left">
                      <!-- Role-specific details go here -->
                      <p style="font-weight: bold">
                        Application Deadline: {{ role.deadline }}
                      </p>
                      <p>Required Skills: {{ role.skill_names.join(', ') }}</p>
                      <p style="font-weight: bold">About the role</p>
                      <p>{{ role.role_description }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Role-specific Applicants Modal -->
              <div
                class="modal fade"
                :id="role.role_tag + 'ApplicantsModal'"
                tabindex="-1"
                :aria-labelledby="role.role_tag + 'ApplicantsModalLabel'"
                aria-hidden="true"
              >
                <div
                  class="modal-dialog modal-dialog-centered modal-dialog-scrollable"
                >
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5
                        class="modal-title"
                        :id="role.role_tag + 'ApplicantsModalLabel'"
                      >
                        Applicants for {{ role.role_name }}
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
                        {{ role.role_name }} position.
                      </p>
                      <div class="row">
                        <table class="table">
                          <thead>
                            <tr>
                              <th scope="col" class="col-1">#</th>
                              <th scope="col" class="col-5">Name</th>
                              <th scope="col" class="col-5">Email</th>
                              <th scope="col" class="col-1"></th>
                            </tr>
                          </thead>
                          <tbody class="text-center align-middle">
                            <!-- Applicants table rows go here -->
                          </tbody>
                        </table>
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
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PostingView",
  components: {},
  data() {
    return {
      roles: [],
      role_skills: null,
      skill_lookup: null
    };
  },
  methods: {
    processRoleName(roleName) {
      // Remove all occurrences of '#' from roleName
      return roleName.replace(/[^a-zA-Z0-9\s]/g, "").replace(/\s/g, "_");
    },
    fetchData() {
      // First, fetch the skills lookup data
      axios.get("http://127.0.0.1:5003/skills")
        .then((response) => {
          this.skillLookup = response.data.data.reduce((acc, skill) => {
            acc[skill.skill_ID] = skill.skill_name;
            return acc;
          }, {});
          return axios.get("http://127.0.0.1:5002/role_skill");
        })
        .then((response) => {
          this.role_skills = response.data.data;
          return axios.get("http://127.0.0.1:5002/roles");
        })
        .then((response) => {
          this.roles = response.data.data;
          this.roles.forEach((role) => {
            role.role_tag = this.processRoleName(role.role_name);
            let skillIdsForRole = this.role_skills?.[role.role_ID] || [];
            role.skill_names = skillIdsForRole.map(id => this.skillLookup[id] || 'Unknown Skill');
          });
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    fetchRoles() {
      // Replace with your API endpoint to fetch role listings
      axios
        .get("http://127.0.0.1:5002/roles") // Change the URL to your API endpoint
        .then((response) => {
          this.roles = response.data.data;
          this.roles.forEach((role) => {
            role.role_tag = this.processRoleName(role.role_name);
          });
        })
        .catch((error) => {
          console.error("Error fetching roles:", error);
        });
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
