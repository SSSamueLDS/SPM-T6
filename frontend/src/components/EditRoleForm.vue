<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <!-- Restrict width to 8 columns on medium devices -->

        <div class="card">
          <div class="card-header custom-header">
            <h4 class="no-margin" style="font-weight: bold">Edit a Role</h4>
            <!-- <h2 style="color: white">Add A Role</h2> -->
          </div>

          <div class="card-body">
            <form @submit.prevent="onSubmit">
              <div class="row mb-3">
                <label
                  for="role_name"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Role Title</label
                >
                <div class="col-sm-9">
                  <input
                    v-model="role_name"
                    type="text"
                    class="form-control"
                    id="role_name"
                  />
                  <div v-if="v$.role_name.$error" class="text-danger">
                    Role name is required.
                  </div>
                </div>
              </div>
              <div class="row mb-3">
                <label
                  for="role_description"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Description</label
                >
                <div class="col-sm-9">
                  <textarea
                    v-model="role_description"
                    class="form-control"
                    id="role_description"
                    rows="3"
                  ></textarea>
                  <div v-if="v$.role_description.$error" class="text-danger">
                    Description is required.
                  </div>
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
                  <div v-if="v$.deadline.$invalid" class="text-danger">
                    <span v-if="!v$.deadline.required">Date is required.</span>
                    <span v-if="!v$.deadline.afterToday"
                      >Date must be after today.</span
                    >
                  </div>
                </div>
              </div>

              <!-- submit button -->
              <div class="row mb-3">
                <div style="text-align: right">
                  <a
                    href="/HR/select_skills.html"
                    id="selectSkillButton"
                    class="btn btn-outline-dark"
                    style="margin-right: 10px"
                    >Select Skill</a
                  >
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
      // Added prop for role_ID
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      role_name: "",
      role_description: "",
      deadline: null,
      formSubmitted: false,
    };
  },
  methods: {
    async fetchRoleData() {
      try {
        const response = await axios.get(
          `http://localhost:5002/roles/${this.role_ID}`
        );
        if (response.data && response.data.code === 200) {
          this.role_name = response.data.data.role_name;
          this.role_description = response.data.data.role_description;
          this.deadline = response.data.data.deadline;
        } else {
          console.error("Error fetching role data:", response.data.message);
        }
      } catch (error) {
        console.error("Error fetching role data:", error);
      }
    },
    async onSubmit() {
      this.formSubmitted = true;
      this.v$.$validate();

      if (!this.v$.$pending && !this.v$.$error) {
        try {
          const response = await axios.put(
            `http://localhost:5002/update_role/${this.role_ID}`,
            {
              role_name: this.role_name,
              role_description: this.role_description,
              deadline: this.deadline,
            }
          );

          if (response.data.code === 200) {
            alert("Role updated successfully!");
          } else {
            alert(response.data.message);
          }
        } catch (error) {
          console.error("Error updating role:", error);
          alert("There was an error updating the role. Please try again.");
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
    role_name: {
      required: required,
    },
    role_description: {
      required: required,
    },
    deadline: {
      required: required,
      afterToday: isFutureDate,
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
