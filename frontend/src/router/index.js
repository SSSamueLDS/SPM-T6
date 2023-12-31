import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/logout",
    name: "logout",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/LogoutView.vue");
    },
  },
  {
    path: "/login",
    name: "login",
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/LoginView.vue");
    },
  },
  {
    path: "/posting",
    name: "CreatedPostings",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/CreatedPostingView.vue"
      );
    },
  },
  {
    path: "/apply-role",
    name: "ApplyRole",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/ApplyRoleView.vue"
      );
    },
  },
  {
    path: "/create-posting",
    name: "CreatePosting",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/CreatePosting.vue"
      );
      },
    },
  {
    path: "/browse-skill",

    name: "BrowseSkill",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/SkillBrowserView.vue"
      );
    },
  },
  {
    path: "/edit-posting/:roleID",
    name: "EditPosting",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/EditPostingView.vue"
      );
    },
    props: true
  },
  {
    path: "/view-applicant-skill/:id",
    name: "ViewApplicantSkill",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/ApplicantSkillView.vue"
      );
    },
  },
  {
    path: "/apply-role",

    name: "ApplyRole",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/ApplyRoleView.vue"
      );
    },
  },
  {
    path: "/logout",
    name: "logout",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/LogoutView.vue"
      );
    },
  },
  {
    path: "/employees",
    name: "employess",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/EmployeeList.vue"
      );
    },
  },
  {
    path: "/employees/:id",
    name: "ViewStaffSkill",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/EmployeeSkill.vue"
      );
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
