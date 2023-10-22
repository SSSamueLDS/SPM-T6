<template>
    <div class="View Applicant's Skills">
    <div class="container text-center col-10 mt-5">

      <div class="col mb-3">
        <div class="card text-start">
          <div class="card-header text-bg-dark">
            <h5><strong>Software Engineer #0100 Engineering Department</strong></h5>
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
              <h6><strong>ID: 150065</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Name: Noah Goh</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Email: Noah.Goh@allinone.com.sg</strong></h6>
            </li>
            <li class="list-group-item">
              <h6><strong>Department: Engineering</strong></h6>
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
                      {{ listing_skills }}
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
            <tr>
              <th scope="row">1</th>
              <td>Node.js</td>
              <td>Yes</td>
            </tr>
            <tr>
              <th scope="row">2</th>
              <td>Javascript</td>
              <td>No</td>
            </tr>
            <tr>
              <th scope="row">3</th>
              <td>Bootstrap</td>
              <td>Yes</td>
            </tr>
            <tr>
              <th scope="row">3</th>
              <td>Java</td>
              <td>No</td>
            </tr>
          </tbody>
        </table>
      </div>
      </div>

      <!-- OTHER SKILLS POSSESSED BY THE APPLICANT -->
      <span class="text-start"><h5>Other Skills Possessed by Applicant</h5></span>
      <div class="row">
        <div class="col">
          <ul>
            <li class="text-start"> Data Analytics</li>
            <li class="text-start">Problem Management</li>
            <li class="text-start">Project Management</li>
            <li class="text-start">Product Management</li>
          </ul>
        </div>
        <div class="col">
          <ul>
            <li class="text-start">Solution Architecture</li>
            <li class="text-start">Solutions Design Thinking</li>
            <li class="text-start">Technology Application</li>
            <li class="text-start">User Interface Design</li>
          </ul>
        </div>
        <div class="col">
          <ul>
            <li class="text-start">Solution Architecture</li>
            <li class="text-start">Solutions Design Thinking</li>
            <li class="text-start">Technology Application</li>
            <li class="text-start">User Interface Design</li>
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
      employee_skills: [],
      listing_skills: {},
      employee: {},
    };
  },
  created() {
    this.fetchEmployeeSkills();
    this.fetchListingskill();
    this.fetchEmployee();
  },
  
  methods: {
    fetchEmployeeSkills() {
      axios
        .get("http://127.0.0.1:5004/staffs/skills/140002")
        .then((response) => {
          // Assuming the API response has a property named "skillName"
          this.employee_skills = response.data.data;
        })
        .catch((error) => {
          console.error("Error fetching applicant skill:", error);
        });
    },
    fetchListingskill() {
      axios
        .get("http://127.0.0.1:5002/listing_skill/1")
        .then((response) => {
          this.listing_skills = response.data.data.skill_ids;
        })
    },
    fetchEmployee() {
      axios
        .get("http://127.0.0.1:5004/staffs/skills/140002")
        .then((response) => {
          // Assuming the API response has a property named "skillName"
          this.employee_skills = response.data.data;
        })
        .catch((error) => {
          console.error("Error fetching applicant skill:", error);
        });
    },
    skillMatchPercentage(skillsForListing) {
      if (!skillsForListing || !skillsForListing.length) return 0;  // <-- Add this line

      let matchCount = 0;

      skillsForListing.forEach(skill => {
          if (this.employee_skills.includes(skill)) {
              matchCount++;
          }
      });

      let percentage = (matchCount / skillsForListing.length) * 100;
      return Math.round(percentage);  // <-- Use Math.round() here
    },
  },
};
</script>