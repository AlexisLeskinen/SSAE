// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
// 用于和后台交互，发送请求
import axios from 'axios';
axios.defaults.headers.post['Content-Type'] = 'application/json';
Vue.prototype.$axios = axios;
Vue.prototype.api = "http://127.0.0.1:8000/api/";

Vue.use(Element)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
