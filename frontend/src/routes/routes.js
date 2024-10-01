import DashboardLayout from '@/views/Layout/DashboardLayout.vue';
import AuthLayout from '@/views/Pages/AuthLayout.vue';

import NotFound from '@/views/NotFoundPage.vue';
import CreationPlatform from '../views/CreationPlatform.vue';


const routes = [
  {
    // mode: 'history', // 使用history模式来避免URL中的#
    path: '/',
    redirect: 'culture',
    component: DashboardLayout,
    children: [
      {
        path: 'culture',
        name: 'culture',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "demo" */ '../views/CultureView.vue')
      },
      {
        path: '/profile',
        name: 'profile',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/UserProfile.vue')
      },
      {
        path: '/tables',
        name: 'tables',
        component: () => import(/* webpackChunkName: "demo" */ '../views/RegularTables.vue')
      },
      {
        path: '/ia',
        name: 'ia',
        component: () => import(/* webpackChunkName: "demo" */ '../views/InpaintingView.vue')
      },
      {
        path: '/autoia',
        name: 'autoia',
        component: () => import(/* webpackChunkName: "demo" */ '../views/AutoInpaintingView.vue')
      },
      {
        path: '/animateanyone',
        name: 'aa',
        component: () => import(/* webpackChunkName: "demo" */ '../views/AnimateAnyoneView.vue')
      },
      {
        path: '/en3d',
        name: 'en3d',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Generate3DVideo.vue')
      },
      {
        path: '/magicanimate',
        name: 'magicanimate',
        component: () => import(/* webpackChunkName: "demo" */ '../views/MagicAnimate.vue')
      },
      {
        path: '/creationplatform',
        name:'creationplatform',
        component: () => import('../views/CreationPlatform.vue'), // 指向父组件的路径
      },
      {
        path: '/threescene',
        name:'THREESCENE',
        component: () => import('../views/ThreeScene.vue'), // 指向父组件的路径
        props: (route) => ({ modelUrl: route.query.modelUrl })
      },
      {
        path: '/videodisplaypage',
        name:'videodisplaypage',
        component: () => import('../views/VideoDisplayPage.vue'), // 指向父组件的路径
        props: true // 允许组件接收路由参数作为 props
      },
      {
        path: '/timescroll',
        name:'timescroll',
        component: () => import('../views/TimeScroll.vue'), // 指向父组件的路径
      },
    ]
  },
  {
    path: '/',
    redirect: 'login',
    component: AuthLayout,
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Login.vue')
      },
      {
        path: '/register',
        name: 'register',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Register.vue')
      },
      { path: '*', component: NotFound }
    ]
  }
];

export default routes;
