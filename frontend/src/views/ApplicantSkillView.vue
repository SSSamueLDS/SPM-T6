<template>
    <div class="View Applicant's Skills">
    <div class="container text-center col-10 mt-5">

      <div class="col mb-3">
        <div class="card text-start">
          <div class="card-header text-bg-dark">
            <h5><strong>{{ listingName }}</strong></h5>
          </div>
          
        </div> 
        </div>


      <div class="row mb-3">
        <!-- APPLICANT'S DETAILS -->
        <div class="col-9">
        <div class="card text-start">
          <div class="card-header text-bg-secondary">
            <h5><strong>Applicant's Personal Details</strong></h5>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <h6><strong>ID: {{ applicantInfo.staff_id }}</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Name: {{ applicantInfo.staff_fname }} {{ applicantInfo.staff_lname }}</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Email: {{ applicantInfo.email }}</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Department: {{ applicantInfo.country }}</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Country: Singapore</strong></h6>
            </li>
          </ul>
        </div> 
        </div>

        <!-- PERCENTAGE SKILL MATCH -->
        <div class="col-3">
        <div class="card" style="height:100%">
          <div class="card-header text-bg-secondary">
            <h5><strong>Percentage Skill Match</strong></h5>
          </div>
          <div class="card-body d-flex align-items-center justify-content-center">
            <p class="card-text">
                      {{ skillMatchPercentage(listing_skills) }}%
                    </p>
                    
          </div>
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
              <th scope="col">Required Skill</th>
              <th scope="col">Possessed by Applicant</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(skill, index) in listing_skills" :key="index">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ getSkillNameById(skill) }}</td>
            <td>{{ employee_skills.includes(skill) ? 'Yes' : 'No' }}</td>
        </tr>
          </tbody>
        </table>
      </div>
      </div>

      <!-- OTHER SKILLS POSSESSED BY THE APPLICANT -->
      
      <span class="text-start"><h5>Other Skills Possessed by Applicant</h5></span>
      <div class="row">
        <div class="col" v-for="(chunk, index) in getChunks(otherSkills, 4)" :key="index">
          <ul>
            <li class="text-start" v-for="(skill, skillIndex) in chunk" :key="skillIndex">{{ getSkillNameById(skill) }}</li>
          </ul>
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
      employee_skills: [],
      listing_skills: [],
      applicant: [],
      applicantInfo: {},
    };
  },
  computed: {
    applicationId(){
      return this.$route.params.id;
    },
    listingName(){
      console.log(this.$route); 
      console.log(this.$route.query.listingName);
      return this.$route.query.listingName;
    },
    otherSkills() {
      if (!Array.isArray(this.employee_skills) || !Array.isArray(this.listing_skills)) {
        return [];
      }
      return this.employee_skills.filter(skill => !this.listing_skills.includes(skill));
    },
    all_skills() {
      return this.$store.state.all_skills;
    }
  },
  created() {
    this.fetchApplicationDetails();
  },
  
  methods: {
    fetchApplicationDetails() {
      axios.get(`http://127.0.0.1:5006/applications/${this.applicationId}`)
        .then(response => {
          this.application = response.data.data;
          return Promise.all([
            this.fetchEmployeeSkills(this.application["staff_id"]),
            this.fetchListingskill(this.application["listing_id"]),
            this.fetchApplicantInfo(this.application["staff_id"])
          ]);
        })
        .then(() => {
          // All fetch operations are completed
          // You can perform any other operations that rely on all data being fetched
        })
        .catch(error => {
          console.error("Error fetching application details:", error);
        });
    },
    fetchEmployeeSkills(staffId) {
      axios
        .get(`http://127.0.0.1:5004/staffs/skills/${staffId}`)
        .then((response) => {
          // Assuming the API response has a property named "skillName"
          this.employee_skills = response.data.data;
          console.log("employee skills="+this.employee_skills);
        })
        .catch((error) => {
          console.error("Error fetching applicant skill:", error);
        });
    },
    fetchListingskill(listingId) {
      axios
        .get(`http://127.0.0.1:5002/listing_skill/${listingId}`)
        .then((response) => {
          this.listing_skills = response.data.data.skill_ids;
          console.log("listing skills="+this.listing_skills);
        })
    },
    fetchApplicantInfo(staffId) {
      axios
        .get(`http://127.0.0.1:5004/staffs/${staffId}`)
        .then((response) => {
          this.applicantInfo = response.data.data;
          console.log("Applicant Info:", this.applicantInfo);
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
    skillMatchPercentage(skillsForListing) {
      if (!Array.isArray(skillsForListing) || !skillsForListing.length) return 0;
      if (!Array.isArray(this.employee_skills)) return 0;

      // let matchCount = 0;
      // skillsForListing.forEach(skill => {
      //   if (this.employee_skills.includes(skill)) {
      //     matchCount++;
      //   }
      // });
      const matchCount = skillsForListing.filter(skill => this.employee_skills.includes(skill)).length;
      let percentage = (matchCount / skillsForListing.length) * 100;
      return Math.round(percentage);
    },
    getSkillNameById(skillId) {
      const skillObj = this.all_skills.find(skill => skill.skill_id === skillId);
      return skillObj ? skillObj.skill_name : 'Unknown';
    },
  },
};
</script>