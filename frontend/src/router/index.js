import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";

const routes = [
  { path: "/", name: "dashboard", component: DashboardView },
  {
    path: "/alerts",
    name: "alerts",
    component: () => import("../views/AlertsView.vue"),
  },
  {
    path: "/alerts/:id",
    name: "alert-detail",
    component: () => import("../views/AlertDetailView.vue"),
    props: true,
  },
  {
    path: "/mitre",
    name: "mitre",
    component: () => import("../views/MitreView.vue"),
  },
  {
    path: "/timeline",
    name: "timeline",
    component: () => import("../views/TimelineView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
