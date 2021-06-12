import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/pages/Home'
import Login from "../components/pages/Login";
import ExpressDistribute from "../components/pages/ExpressDistribute";
import ExpressDelivery from "../components/pages/ExpressDelivery";

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/distribute',
      name: 'Distribute',
      component: ExpressDistribute
    },
    {
      path: '/delivery',
      name: 'Delivery',
      component: ExpressDelivery
    },
  ]
})
