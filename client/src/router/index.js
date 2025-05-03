import { createRouter, createWebHistory } from 'vue-router';
import CreateEvent from '../views/CreateEvent.vue';
import ChatView from '../views/ChatView.vue';
import JoinEvent from '../views/JoinEvent.vue';

const routes = [
  { path: '/', component: CreateEvent, meta: { title: 'Create Event | Bill' } },
  { path: '/chat/:eventId', component: ChatView, props: true, meta: { title: 'Chat | Bill' } },
  { path: '/join/:eventId', component: JoinEvent, props: true, meta: { title: 'Join Event | Bill' } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Event App';
  next();
});

export default router;
