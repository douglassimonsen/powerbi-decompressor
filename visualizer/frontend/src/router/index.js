import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/visuals',
      name: 'visuals',
      component: () => import('../views/VisualView.vue')
    },
    {
      path: '/dependencies',
      name: 'dependencies',
      component: () => import('../views/DependencyView.vue')
    }
  ]
})

export default router
