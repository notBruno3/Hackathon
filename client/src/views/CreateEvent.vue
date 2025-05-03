<template>
    <div class="create-event-wrapper">
      <div class="create-event-card">
        <h2>Create a New Event</h2>
        <input v-model="eventName" placeholder="Event Name" />
        <button @click="createEvent">Create</button>
  
        <div class="event-list" v-if="events.length > 0">
          <h3>Existing Events</h3>
          <ul>
            <li v-for="event in events" :key="event.id" @click="goToEvent(event.id)">
              <div class="event-name">{{ event.name }}</div>
              <div
                class="event-status-dot"
                :class="{ active: event.is_active, inactive: !event.is_active }"
                title="Status"
              ></div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    inject: ['globalUid'],
    data() {
      return {
        eventName: '',
        events: []
      }
    },
    methods: {
      async createEvent() {
      if (!this.eventName.trim()) {
        alert("Please enter an event name.");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/event", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event_name: this.eventName, admin_name: "You", admin_id:  this.globalUid})
        });

        if (!response.ok) {
          throw new Error("Failed to create event");
        }

        const data = await response.json();
        
        this.$router.push(`/chat/${data.event_id}`);
      } catch (error) {
        console.error(error);
        alert("Something went wrong while creating the event.");
      }
    },

      
    async fetchEvents() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/events/${this.globalUid}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json"
          }
        });

        const data = await response.json();
        this.events = Object.values(data);
      } catch (error) {
        console.error("Failed to load events:", error);
      }
    },

    async goToEvent(id) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/event/${id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch event status');
      }

      const event = await response.json();

      if (!event.is_active) {
        alert('This event has already been finalized and can no longer be joined.');
        return;
      }

      this.$router.push(`/chat/${id}`);
    } catch (error) {
      console.error(error);
      alert('Could not check event status. Please try again later.');
    }
  }

    },
    mounted() {
      this.fetchEvents();
    }
  }
  </script>
  
  

  <style scoped>

.event-status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 4px;
  margin-left: auto;
  margin-right: 0;
  background-color: gray; /* fallback */
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.event-status-dot.active {
  background-color: #22c55e; /* green */
}

.event-status-dot.inactive {
  background-color: #ef4444; /* red */
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
  padding-right: 0.5rem;  /* prevent scrollbar from overlapping text */
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

/* Container to hold pseudo border */
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

/* Animation for border flow */
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
  background: linear-gradient(135deg, #4a90e2, #6fb1fc); /* soft blue gradient */
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