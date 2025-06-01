import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect:'/signup',
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
