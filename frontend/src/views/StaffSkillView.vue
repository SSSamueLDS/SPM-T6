<template>
    <div class="View Applicant's Skills">
    <div class="container text-center col-10 mt-5">

      <div class="row mb-3">
        <div class="col-9">
        <div class="card text-start">
          <div class="card-header text-bg-secondary">
            <h5><strong>Staff's Personal Details</strong></h5>
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
                   
      

      <!-- OTHER SKILLS POSSESSED BY THE staff -->
      
      <span class="text-start"><h5>Skills Possessed by staff</h5></span>
      <div class="row">
      <div class="col">
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th scope="col">Employee Skills</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(skill, id) in employee_skills" :key="id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ employee_skills[id] }}</td>
            <td>{{ employee_skills[skill] }}</td>
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
      application: {},
      employee_skills: {},
      listing_skills: [],
      applicant: [],
      staffInfo: {},
    };
  },
  computed: {
    applicationId(){
      return this.$route.params.id;
    },
    all_skills() {
      return this.$store.state.all_skills;
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
    }
    this.fetchStaffInfo();
    this. fetchEmployeeSkills();
  },
  
  methods: {
    fetchEmployeeSkills(staffId) {
      axios
        .get(`http://127.0.0.1:5004/staffs/display_skills/${staffId}`)
        .then((response) => {
          // Assuming the API response has a property named "skillName"
          this.employee_skills = response.data.data;
          console.log("employee skills="+this.employee_skills);
        })
        .catch((error) => {
          console.error("Error fetching applicant skill:", error);
        });
    },
    fetchStaffInfo(staffId) {
      axios
        .get(`http://127.0.0.1:5004/staffs/${staffId}`)
        .then((response) => {
          this.staffInfo = response.data.data;
          console.log("Applicant Info:", this.staffInfo);
        })
        .catch((error) => {
          console.error("Error fetching applicant info:", error);
        });
    },
    getChunks(arr, size) {
        let chunks = [];
        for (let i = 0; i < arr.length; i += size) {
            chunks.push(arr.slice(i, i + size));
        }
        return chunks;
    },
    
    getSkillNameById(skillId) {
      const skillObj = this.all_skills.find(skill => skill.skill_id === skillId);
      return skillObj ? skillObj.skill_name : 'Unknown';
    },
  },
};
</script>