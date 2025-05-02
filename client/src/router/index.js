import { createRouter, createWebHistory } from 'vue-router'
import CreateEvent from '../views/CreateEvent.vue'
import ChatView from '../views/ChatView.vue'

const routes = [
  { path: '/', component: CreateEvent },
  { path: '/chat/:eventId', component: ChatView, props: true }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
