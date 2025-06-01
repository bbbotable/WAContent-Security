import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect:'/signup',
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/manage',
      name: 'manage',
      component: () => import('../views/Manage.vue'),
      meta: {requireAuth : true}
    },
    {
      path: '/signup',
      name: 'sign',
      component: () => import('../views/FaceSign.vue'),
    },
  ],
})
router.beforeEach((to,from,next)=>{
  const token = localStorage.getItem('token')
  if(to.meta.requireAuth && !token){
    next('/login');
  }else{
    next();
  }
})
export default router
