import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/pages/Home'
import UserManager from "../components/pages/UserManager";

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
      path: '/usermanager',
      name: 'UserManager',
      component: UserManager
    },
  ]
})
