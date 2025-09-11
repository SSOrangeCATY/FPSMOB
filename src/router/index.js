import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import ConfigView from '../views/ConfigView.vue'
import LiveView from '../views/LiveView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'config',
      component: ConfigView
    },
    {
      path: '/live',
      name: 'live',
      component: LiveView
    }
  ]
})

export default router