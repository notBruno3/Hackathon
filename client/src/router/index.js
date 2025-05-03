import { createRouter, createWebHistory } from 'vue-router'
import CreateEvent from '../views/CreateEvent.vue'
import ChatView from '../views/ChatView.vue'
import JoinEvent from '../views/JoinEvent.vue'

const routes = [
  { path: '/', component: CreateEvent },
  { path: '/chat/:eventId', component: ChatView, props: true },
  { path: '/join/:eventId', component: JoinEvent, props: true }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
