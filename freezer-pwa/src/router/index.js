import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FreezerView from "../views/FreezerView.vue";
import CompartmentView from "../views/CompartmentView.vue";

const routes = [
  { path: "/", component: HomeView },
  {
    path: "/freezer/:id",
    component: FreezerView,
    props: (r) => ({ freezerId: Number(r.params.id) }),
  },
  {
    path: "/compartment/:id",
    component: CompartmentView,
    props: (r) => ({ compartmentId: Number(r.params.id) }),
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
