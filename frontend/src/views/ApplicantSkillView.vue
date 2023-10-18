<template>

  <div>
    employee_id: 140002 <br>

    employee_skills: {{ employee_skills }}
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