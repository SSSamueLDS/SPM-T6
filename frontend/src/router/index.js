import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/AboutView.vue");
    },
  },
  {
    path: "/posting",
    name: "CreatedPosting",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/CreatedPostingView.vue"
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
    path: "/edit-posting",
    name: "EditPosting",
    component: function () {
      return import(
        /* webpackChunkName: "about" */ "../views/EditPostingView.vue"
      );
    },
  },
  {
    path: "/skills",
    name: "skills",
  },
  {
    path: "/employees",
    name: "employees",
  },
  {
    path: "/logout",
    name: "logout",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;