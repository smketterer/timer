import Vue from 'vue'
import Router from 'vue-router'
import Track from './views/Track.vue'
import MyTime from './views/MyTime.vue'
import Reports from './views/Reports.vue'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'Track',
    component: Track
  },{
    path: '/time',
    name: 'MyTime',
    component: MyTime
  },{
    path: '/reports',
    name: 'Reports',
    component: Reports
  }]
})
