<template>
    <div class="View Applicant's Skills">
      <div class="container text-center col-10 mt-5">
        <div class="col mb-3"></div>
        <div class="row mb-3">
          <!-- APPLICANT'S DETAILS -->
          <div class="col">
            <div class="card text-start">
              <div class="card-header text-bg-secondary">
                <h5><strong>Staff Details</strong></h5>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <h6><strong>ID: {{ staffInfo.staff_id }}</strong></h6>
                </li>
                <li class="list-group-item">
                  <h6><strong>Name: {{ staffInfo.staff_fname }} {{ staffInfo.staff_lname }}</strong></h6>
                </li>
                <li class="list-group-item">
                  <h6><strong>Email: {{ staffInfo.email }}</strong></h6>
                </li>
                <li class="list-group-item">
                  <h6><strong>Department: {{ staffInfo.dept }}</strong></h6>
                </li>
                <li class="list-group-item">
                  <h6><strong>Country: {{ staffInfo.country }}</strong></h6>
                </li>
              </ul>
            </div>
          </div>
        </div>
  
        <!-- APPLICANT'S SKILLS VS REQUIRED SKILLS TABLE -->
        <div class="row">
          <div class="col">
            <table class="table table-striped">
            <thead class="table-dark">
                <tr>
                <th scope="col">#</th>
                <th scope="col">Skill Name</th>
                </tr>
            </thead>
            <tbody>
                <!-- Use a conditional statement to check if employee_skills is empty -->
                <tr v-if="employee_skills.length === 0">
                <td colspan="2">No skill</td>
                </tr>
                <!-- If employee_skills is not empty, loop through and display skills -->
                <tr v-else v-for="(skill, index) in employee_skills" :key="index">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ getSkillNameById(skill) }}</td>
                </tr>
            </tbody>
            </table>

          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "ApplicantSkillView",
    data() {
      return {
        employee_skills: [],
        staffInfo: {},
      };
    },
    computed: {
      all_skills() {
        return this.$store.state.all_skills;
      },
      staffId() {
      return this.$route.query.staffId;
    },
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
      }
      this.fetchStaffInfo(this.$route.query.staffId);
      this.fetchEmployeeSkills(this.$route.query.staffId);
    },
    methods: {
       
      fetchStaffInfo(staffId) {
        console.log("staffId", staffId);
        //setLoadingstate
        this.$store.commit('setLoading', true);
        axios
          .get(`http://127.0.0.1:5005/staffs/${staffId}`)
          .then((response) => {
            this.staffInfo = response.data.data;
          })
          .catch((error) => {
            console.error("Error fetching staff info:", error);
          })
          .finally(()=>{
              this.$store.commit('setLoading', false);
          });
      },
  
      fetchEmployeeSkills(staffId) {
        console.log("employeefetchingskill", staffId);
        //setLoadingstate
          this.$store.commit('setLoading', true);
        axios
        
          .get(`http://127.0.0.1:5005/staffs/skills/${staffId}`)
          .then((response) => {
            console.log(response.data)
            if (response.data.data.length === 0) {
              this.employee_skills = [];
              return;
            }
            this.employee_skills = response.data.data;
            console.log("employee skills="+this.employee_skills);
          })
          .catch((error) => {
            console.error("Error fetching employee skill:", error);
          })
          .finally(()=>{
              this.$store.commit('setLoading', false);
          });
      },
  
      getSkillNameById(skillId) {
        const skillObj = this.all_skills.find((skill) => skill.skill_id === skillId);
        return skillObj ? skillObj.skill_name : "Unknown";
      },
    },
  };
  </script>
  