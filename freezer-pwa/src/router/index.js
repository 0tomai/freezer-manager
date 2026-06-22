import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import HomeView from "../views/HomeView.vue";
import FreezerView from "../views/FreezerView.vue";
import CompartmentView from "../views/CompartmentView.vue";

const routes = [
  { path: "/login", component: LoginView },
  {
    path: "/",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/freezer/:id",
    component: FreezerView,
    props: (r) => ({ freezerId: Number(r.params.id) }),
    meta: { requiresAuth: true },
  },
  {
    path: "/compartment/:id",
    component: CompartmentView,
    props: (r) => ({ compartmentId: Number(r.params.id) }),
    meta: { requiresAuth: true },
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const token = localStorage.getItem("freezer_token");
  if (to.meta.requiresAuth && !token) return "/login";
});

export default router;
