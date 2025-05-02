<template>
    <div>
      <h2>Create a New Event</h2>
      <input v-model="eventName" placeholder="Event Name" />
      <button @click="createEvent">Create</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        eventName: ''
      }
    },
    methods: {
      async createEvent() {
        // TEMP: Simulate backend response
        const eventId = Math.floor(Math.random() * 100000)
        // In real code, call backend to create and get ID
        this.$router.push(`/chat/${eventId}`)
      }
    }
  }
  </script>
  

  <style scoped>
.create-event-wrapper {
  background-color: #f0f0f0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.create-event-card {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 90%;
  max-width: 400px;
}

h2 {
  margin-bottom: 1.5rem;
  color: #979797;
}

input {
  padding: 0.75rem;
  font-size: 1rem;
  width: 100%;
  margin-bottom: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #646cff;
  outline: none;
}

button {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  background-color: #646cff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #4a53c4;
}
</style>