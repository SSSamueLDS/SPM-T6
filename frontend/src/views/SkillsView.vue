<template>
  <div class="SkillsView container">
    <div class="row">
      <!-- Create New Skill Button, do later -->
      <div class="col-5 m-0 col-sm-5 col-md-6 col-lg-3 col-xl-2">
        <a
          href="add_skill.html"
          class="btn btn-dark w-100 m-2"
          style="color: greenyellow; font-weight: bold"
          >ADD NEW SKILL</a
        >
      </div>
      <!-- SEARCH BAR -->
      <div
        class="col-5 d-flex align-items-center col-sm-7 col-md-6 col-lg-9 col-xl-10"
      >
        <form class="form-inline d-flex w-100">
          <div class="input-group">
            <input
              class="form-control mr-2 flex-grow-1"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button
              class="btn btn-outline-success my-2 my-sm-0 p-2"
              type="submit"
            >
              Search
            </button>
          </div>
        </form>
      </div>
    </div>


    <!-- Table of skills -->
    <div v-if="database_error == false">
      <table class="table mt-3 table-bordered table-hover">
        <thead class="table-dark">
          <th scope="col" class="w-25">ID</th>
          <th scope="col" class="w-75">Skill Name</th>
        </thead>
        <tbody>
          <tr v-for="skill in grouped_skills[current_page - 1]">
            <td>{{ skill.skill_ID }}</td>
            <td>{{ skill.skill_name }}</td>
          </tr>
        </tbody>
      </table>
      <nav aria-label="Skill page navigation">
        <ul class="pagination">
          <li class="page-item">
            <a class="page-link text-black" @click="go_previous_page()"
              >Previous</a
            >
          </li>
          <li class="page-item" v-for="i in grouped_skills.length">
            <a class="page-link text-black" @click="go_page(i)">{{ i }}</a>
          </li>
          <li class="page-item">
            <a class="page-link text-black" @click="go_next_page()">Next</a>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Error message -->
    <div class="alert alert-danger mt-3" role="alert" v-else>
      <h4 class="alert-heading">Error!</h4>
      <p>
        There was an error loading the skills from the database. Please try
        again later.
      </p>
    </div>
  </div>
</template>

<script>
//import jquery
import $ from "jquery";

export default {
  name: "SkillsView",
  components: {},
  data() {
    return {
      skills: [],
      grouped_skills: [],
      database_error: false,
      current_page: 1,
    };
  },
  computed: {},
  methods: {
    sort_alphabetically() {
      this.skills = this.skills.sort((a, b) =>
        a.skill_name > b.skill_name ? 1 : b.skill_name > a.skill_name ? -1 : 0,
      );
      this.grouped_skills = this.group_skills();
      this.current_page = 1;
    },
    sort_by_ID() {
      this.skills = this.skills.sort((a, b) =>
        a.skill_ID > b.skill_ID ? 1 : b.skill_ID > a.skill_ID ? -1 : 0,
      );
      this.grouped_skills = this.group_skills();
      this.current_page = 1;
    },

    group_skills() {
      var grouped_skills = [];
      var group = [];
      var i = 0;
      for (i = 0; i < this.skills.length; i++) {
        if (i % 10 == 0 && i != 0) {
          grouped_skills.push(group);
          group = [];
        }
        group.push(this.skills[i]);
      }
      grouped_skills.push(group);
      console.log(grouped_skills);
      return grouped_skills;
    },
    go_page(i) {
      this.current_page = i;
    },
    go_previous_page() {
      if (this.current_page > 1) {
        this.current_page--;
      }
    },
    go_next_page() {
      if (this.current_page < this.grouped_skills.length - 1) {
        this.current_page++;
      }
    },
  },
  created() {

      this.$store.commit('setLoading', true);
    $(async () => {
      var serviceURL = "http://localhost:5005/skills";

      try {
        const response = await fetch(serviceURL, { method: "GET" });
        const result = await response.json();
        if (response.status === 200) {
          
          var skills = result.data; 
          this.skills = skills;

          var grouped_skills = [];
          var group = [];
          var i = 0;
          for (i = 0; i < this.skills.length; i++) {
            if (i % 10 == 0 && i != 0) {
              grouped_skills.push(group);
              group = [];
            }
            group.push(this.skills[i]);
          }
          grouped_skills.push(group);
          this.grouped_skills = grouped_skills;
        }
      } catch (error) {
        this.database_error = true;
      }
      finally{
        this.$store.commit('setLoading', false);
      }
    });
  },
};
</script>
