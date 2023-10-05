<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <!-- Restrict width to 8 columns on medium devices -->

        <div class="card">
          <div class="card-header custom-header">
            <h4 class="no-margin" style="font-weight: bold">
              {{ mode === "edit" ? "Edit A Role" : "Add A Role" }}
            </h4>
            <!-- <h2 style="color: white">Add A Role</h2> -->
          </div>

          <div class="card-body">
            <form>
              <div class="row mb-3">
                <label
                  for="role_name"
                  class="col-sm-3 shifted-label"
                  col-from-label
                  >Role Title</label
                >
                <div class="col-sm-9">
                  <input
                    type="text"
                    class="form-control"
                    id="role_name"
                    required
                  />
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
                    class="form-control"
                    id="role_description"
                    rows="3"
                    required
                  ></textarea>
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
                    type="date"
                    class="form-control"
                    id="deadline"
                    required
                  />
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
                    type="button"
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
export default {
  name: "RoleForm",
  props: {
    mode: {
      type: String,
      default: "create",
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
