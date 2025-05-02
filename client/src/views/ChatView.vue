<template>
    <div class="chat-view-wrapper">
      <div class="chat-view-card">
        <div class="chat-header">
            <button class="back-button" @click="goBack">←</button>
            <h2>Event Chat — ID: {{ eventId }}</h2>
        </div>
        <deep-chat
          class="chat-component"
          :request='{
            url: "http://localhost:8000/submit",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: { user: "Alice", event_id: Number(eventId) }
          }'
        />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['eventId'],
    methods: {
      goBack() {
        this.$router.push('/') // or this.$router.back() for browser history
      }
    }
  }
  </script>


<style scoped>

    .chat-header {
        display: flex;
        align-items: center;
        gap: 1rem; /* spacing between button and title */
        width: 100%;
        justify-content: flex-start;
        margin-bottom: 1.5rem;
    }

    .back-button {
        color: #ffffff; 
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        transition: color 0.2s ease;
        padding: 0.4rem 0.6rem;
        border-radius: 4px;
        background-color: transparent;
    }

    .chat-component-wrapper {
        width: 100%;
        max-width: 66.66vw;
        margin: 0 auto;
        padding: 1rem;
        box-sizing: border-box;
    }

    .chat-view-card {
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center;
        text-align: center;
        padding: 2rem;
        width: 100%;
        max-width: 800px;
    }

    h2 {
        color: #989898;
        margin-bottom: 1.5rem;
        font-size: 1.75rem;
    }

    .chat-component {
        width: 100%; /* Full width inside wrapper */
        height: 100%;
        border-radius: 8px; 
        
    }
</style>