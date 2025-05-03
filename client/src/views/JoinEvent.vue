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
const baseURL = import.meta.env.VITE_API_URL;

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
          const response = await fetch(`${baseURL}/event/${this.eventId}/join`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: this.userName, id: this.globalUid })
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
  /* Include only additional class not already in the large CSS */
  .event-id-text {
    color: #bbbbbb;
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }
  
  /* Insert the full CSS you provided above here (or import it in the parent component) */
  
  .event-status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-top: 4px;
    margin-left: auto;
    margin-right: 0;
    background-color: gray;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }
  
  .event-status-dot.active {
    background-color: #22c55e;
  }
  
  .event-status-dot.inactive {
    background-color: #ef4444;
  }
  
  .event-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
  }
  
  .event-id {
    font-size: 0.8rem;
    color: #bbbbbb;
  }
  
  .event-list {
    margin-top: 2rem;
    text-align: left;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 0.5rem;
  }
  
  .event-list::-webkit-scrollbar {
    width: 6px;
  }
  
  .event-list::-webkit-scrollbar-thumb {
    background-color: #444;
    border-radius: 4px;
  }
  
  .event-list h3 {
    margin-bottom: 0.75rem;
    color: #ffffff;
    font-size: 1.25rem;
    border-bottom: 1px solid #444;
    padding-bottom: 0.5rem;
  }
  
  .event-list ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .event-list li {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    background-color: #1a1a1a;
    color: #e2e2e2;
    cursor: pointer;
    margin-bottom: 0.75rem;
    transition: background-color 0.3s, transform 0.2s;
    border-left: 6px solid transparent;
  }
  
  .event-list li:hover {
    background-color: #2c2c2c;
    transform: scale(1.01);
    border-left: 6px solid;
    border-image: linear-gradient(
      180deg,
      #0B9344,
      #66BB46,
      #A5CD39,
      #33C1B1,
      #1E90F0,
      #0071BC,
      #A73439,
      #EF3E3E,
      #F7941E,
      #FFD200
    ) 1;
  }
  
  .create-event-wrapper {
    background-color: #242424;
    min-height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .create-event-card {
    background-color: #242424;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    width: 90%;
    max-width: 400px;
  }
  
  h2 {
    margin-bottom: 1.5rem;
    color: #e2e2e2;
    font-size: 2rem; /* increased from default */
    }
  
  input {
    position: relative;
    padding: 0.75rem;
    font-size: 1rem;
    width: 100%;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    background-color: #1a1a1a;
    color: white;
    animation: bunqInputBorder 8s ease-in-out infinite;
    z-index: 1;
  }
  
  input:focus {
    outline: none;
    border-color: transparent;
    background-image:
      linear-gradient(#1a1a1a, #1a1a1a),
      linear-gradient(
        90deg,
        #0B9344,
        #66BB46,
        #A5CD39,
        #33C1B1,
        #1E90F0,
        #0071BC,
        #A73439,
        #EF3E3E,
        #F7941E,
        #FFD200
      );
    background-origin: border-box;
    background-clip: padding-box, border-box;
    animation: bunqInputBorder 3s linear infinite;
    background-size: 300% 300%;
  }
  
  @keyframes bunqInputBorder {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
  
  button {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    color: white;
    background: linear-gradient(135deg, #4a90e2, #6fb1fc);
    cursor: pointer;
    transition: background 0.6s ease, transform 0.3s ease;
    background-size: 200% 200%;
    background-position: center;
  }
  
  button:hover {
    background: linear-gradient(
      90deg,
      #0B9344 0%,
      #66BB46 10%,
      #A5CD39 20%,
      #33C1B1 30%,
      #1E90F0 40%,
      #0071BC 50%,
      #A73439 60%,
      #EF3E3E 70%,
      #F7941E 80%,
      #FFD200 90%
    );
    background-size: 200% 200%;
    animation: bunqPulse 2s ease-out forwards;
    transform: scale(1.02);
  }
  
  @keyframes bunqPulse {
    0% {
      background-position: left;
    }
    100% {
      background-position: right;
    }
  }
  </style>
  