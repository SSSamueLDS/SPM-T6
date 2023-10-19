<template>
    <div class="View Applicant's Skills">
    <div class="container text-center col-10 mt-5">

      <!-- ROLE DETAILS CARD GROUP -->
      <div class="card-group mb-3">
          <div class="card border-2 border-dark">
            <div class="card-body">
              <h6><strong>Role ID: #0100</strong></h6>
            </div>
          </div>
          <div class="card border-2 border-dark">
            <div class="card-body">
              <h6><strong>Role Name: Software Engineer</strong></h6>
            </div>
          </div>
          <div class="card border-2 border-dark">
            <div class="card-body">
              <h6><strong>Department: Engineering</strong></h6>
            </div>
          </div>
      </div>


      <div class="row mb-3">
        <!-- APPLICANT'S DETAILS -->
        <div class="col-9">
        <div class="card text-start">
          <div class="card-header text-bg-dark">
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
          <div class="card-header text-bg-dark">
            <h5><strong>Percentage Skill Match</strong></h5>
          </div>
          <div class="card-body d-flex align-items-center justify-content-center">
            <h1><strong>50%</strong></h1>
          </div>
        </div> 
        </div>
      </div>

      <!-- APPLICANT'S SKILLS VS REQUIRED SKILLS TABLE -->
      <div class="row">
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Skill</th>
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
          </tbody>
        </table>
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
    };
  },
  created() {
    this.fetchSkills();
  },
  
  methods: {
    fetchSkills() {
      axios
        .get("http://127.0.0.1:5004/staffs/skills/140002")
        .then((response) => {
          // Assuming the API response has a property named "skillName"
          this.employee_skills = response.data.data
        })
        .catch((error) => {
          console.error("Error fetching applicant skill:", error);
        });
    },
  },
};
</script>