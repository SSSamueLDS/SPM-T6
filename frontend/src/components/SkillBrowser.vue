<template>
  <div class="w-50 mt-5 mx-auto">
    <!-- <div>
      <label for="search"
        ><h4 style="font-weight: bold" class="mb-3">SEARCH SKILLS</h4></label
      >
      <input
        v-model="searchTerm"
        id="search"
        type="text"
        class="form-control mb-3"
        placeholder="Search skills..."
      />
    </div> -->

    <form @submit.prevent="submitForm">
      <label for="skills"
        ><h4 style="font-weight: bold" class="mb-3">
          SELECT REQUIRED SKILLS
        </h4></label
      >
      <select
        v-model="selectedSkills"
        name="skills"
        id="selectedSkills"
        multiple
      >
        <option
          v-for="skill in skills"
          :value="skill.skill_ID"
          :key="skill.skill_ID"
        >
          {{ skill.skill_name }}
        </option>
      </select>
      <div style="text-align: right" class="mt-3">
        <a href="/Role/templates/role_listing.html" class="btn btn-outline-dark"
          >Go Back</a
        >
        <button type="button" class="btn btn-dark ml-2" @click="submitForm">
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      skills: [],
      searchTerm: "",
      selectedSkills: [],
    };
  },
  computed: {
    filteredSkills() {
      if (!this.searchTerm) return this.skills;
      return this.skills.filter((skill) =>
        skill.name.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    },
  },
  methods: {
    submitForm() {
      // Handle the form submission
      // For instance, emit the selected skills or perform an API call
      this.$emit("skills-selected", this.selectedSkills);
    },
  },
  mounted() {
    // Fetch the skills when the component is mounted
    //setLoadingstate
      this.$store.commit('setLoading', true);
    axios
      .get("http://localhost:5003/skills")
      .then((response) => {
        if (response.data.code === 200) {
          this.skills = response.data.data;
          console.log(this.skills);
          console.log(this.skills[0].skill_ID);
        } else {
          console.error("Error fetching skills:", response.data.message);
        }
      })
      .catch((error) => {
        console.error("Error fetching skills:", error);
      })
      .finally(()=>{
              this.$store.commit('setLoading', false);
      });

    new window.MultiSelectTag("selectedSkills");
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
