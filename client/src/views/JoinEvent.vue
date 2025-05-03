<template>
    <div class="create-event-wrapper">
      <div class="create-event-card">
        <h2>Join Event</h2>
        <p class="event-id-text">Event ID: {{ eventId }}</p>
        <input v-model="userName" placeholder="Your Name" />
        <button @click="joinEvent">Join</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    inject: ['globalUid'],
    props: ['eventId'],
    data() {
      return {
        userName: ''
      }
    },
    methods: {
      async joinEvent() {
        if (!this.userName.trim()) {
          alert('Please enter your name');
          return;
        }
  
        try {
          const response = await fetch(`http://localhost:8000/event/${this.eventId}/join`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: this.userName, id: this.globalUid})
          });
  
          if (!response.ok) {
            throw new Error('Join failed');
          }
  
          this.$router.push(`/chat/${this.eventId}`);
        } catch (err) {
          console.error(err);
          alert('Could not join the event');
        }
      }
    }
  }
  </script>
  
  
  <style scoped>
  .event-id-text {
    color: #bbb;
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }
  </style>
  