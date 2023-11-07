<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <!-- Restrict width to 8 columns on medium devices -->

        <div class="card">
          <div class="card-header custom-header">
            <h4 class="no-margin" style="font-weight: bold">Edit Role Listing</h4>
            <!-- <h2 style="color: white">Add A Role</h2> -->
          </div>

          <div class="card-body">
            <form @submit.prevent="onSubmit">
              <div class="row mb-3">
                <label
                  for="listing_name"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Role Title</label
                >
                <div class="col-sm-9">
                  <select id="listing_name" class="form-select" aria-label="Default select example" @change="prefillForm" v-model="selected_role">
                    <option disabled>Select role</option>
                    <option :value="role" v-for="role of all_roles" :key="role.role_id">{{role.role_name}}</option>
                  </select>
                  <div v-if="v$.listing_name.$error" class="text-danger">
                    Role listing name is required.
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <label
                  for="listing_description"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Description</label
                >
                <div class="col-sm-9">
                  <textarea
                    v-model="listing_description"
                    class="form-control"
                    id="listing_description"
                    rows="3"
                  ></textarea>
                  <div v-if="v$.listing_description.$error" class="text-danger">
                    Description is required.
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <label
                  for="listing_department"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Department</label
                >
                <div class="col-sm-9">
                  <select id="listing_department" class="form-select" aria-label="Department select" v-model="listing_department">
                    <option selected disabled>Select Department</option>
                    <option v-for="dept of all_dept" :key="dept" :value="dept">{{dept}}</option>
                  </select>
                </div>
              </div>

              <div class="row mb-3">
                <label
                  for="deadline"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Application Deadline</label
                >
                <div class="col-sm-9">
                  <input
                    v-model="deadline"
                    type="date"
                    class="form-control"
                    id="deadline"
                  />
                  <div v-if="formSubmitted && v$.deadline.$invalid" class="text-danger">
                    <span>invalid deadline</span>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <label
                  for="select_skill"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Role Skills</label>
                <div class="col-sm-9">
                  <Multiselect
                    v-model="selected_skills"
                    :options="all_skills"
                    label="name"
                    trackBy="name"
                    :searchable="true"
                    mode="tags"
                    id="select_skill"
                  />
                  <div v-if="formSubmitted && v$.selected_skills.$error" class="text-danger">
                    Please select at least one skill.
                  </div>
                </div>
              </div>

              <!-- submit button -->
              <div class="row mb-3">
                <div style="text-align: right">
                  <button
                    type="submit"
                    class="btn btn-warning"
                    id="submitButton"
                    style="color: black; font-weight: bold"
                  >
                    Submit
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import Multiselect from '@vueform/multiselect';
import Swal from 'sweetalert2';

const isFutureDate = (value) => {
  if (!value) return true;
  const currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0);
  return new Date(value) > currentDate;
};

export default {
  name: "RoleForm",
  props: {
    role_ID: {
      type: Number,
      required: true,
    },
  },
  components: {
      Multiselect,
  },
  data() {
    return {
      selected_role: null,
      listing_name: "",
      listing_description: "",
      listing_department: "",
      deadline: null,
      formSubmitted: false,
      selected_skills: null
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
    }
  },
  methods: {
    fetchRoleData() {
      this.$store.commit('setLoading', true);
      axios.get(`http://127.0.0.1:5005/listings/${this.role_ID}`)
        .then(response => {
          if (response.data && response.data.code === 200) {
            this.listing_name = response.data.data.listing_name;
            this.listing_description = response.data.data.listing_description;
            this.deadline = response.data.data.deadline;
            this.listing_department = response.data.data.dept;
            this.selected_skills = response.data.data.skill_ids;
            this.selected_role = this.all_roles.find(role => role.role_name === this.listing_name);
            this.$store.commit('setLoading', false);
          } else {
            console.error("Error fetching role data:", response.data.message);
          }
        })
        .catch(error => {
            console.error('Failed to fetch the role data:', error);
        });
    },
    prefillForm() {
      console.log(this.selected_role);
      this.listing_name = this.selected_role.role_name;
      this.listing_description = this.selected_role.role_description;
      axios.get(`http://127.0.0.1:5005/role_skill/${this.selected_role.role_id}`)
      .then((response) => {
        this.selected_skills = response.data.data.skill_ids;
      }).catch((error) => {
        console.error("Error fetching data:", error);
      });
    },
    async onSubmit() {
      this.formSubmitted = true;
      this.v$.$validate();

      if (!this.v$.$pending && !this.v$.$error) {
        this.$store.commit('setLoading', true);

        try {
          const response = await axios.put(`http://127.0.0.1:5005/update_listing/${this.role_ID}`,{
              listing_name: this.listing_name,
              listing_description: this.listing_description,
              deadline: this.deadline,
              dept: this.listing_department,
              listing_skill: this.selected_skills
            })

            Swal.fire({
              icon: 'success',
              title: 'Success!',
              text: 'Role updated successfully!',
            }).then(() => {
              this.$router.push('/posting');
            });

            console.log(response);
            
            } catch (error) {
              Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Failed to update the role. Please try again.',
              });

              this.$store.commit('setLoading', false);
            }
      }
    },
  },
  mounted() {
    this.fetchRoleData();
  },
  setup() {
    const v$ = useVuelidate();
    return { v$ };
  },
  validations: {
    listing_name: {
      required: required,
    },
    listing_description: {
      required: required,
    },
    deadline: {
      required: required,
      afterToday: isFutureDate,
    },
    listing_department:{
      required: required,
    },
    selected_skills: {
      required: value => !!value.length
    },
  },
};
</script>

<style>
.custom-header {
  background-color: black;
  color: white;
}

.no-margin {
  margin-bottom: 0;
}

.shifted-label {
  text-align: left;
  padding-left: 15px;
}
</style>
<style src="@vueform/multiselect/themes/default.css"></style>
