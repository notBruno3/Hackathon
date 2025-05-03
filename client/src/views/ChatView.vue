<template>
    <div class="chat-view-wrapper">
      <div class="chat-view-card">
        <div class="chat-header">
          <button class="back-button" @click="goBack">←</button>
          <h2>{{ eventName }}</h2>
  
          <div class="user-icon-container" @click="toggleUserPopup">
            <img
              src="https://cdn-icons-png.flaticon.com/512/8138/8138685.png"
              alt="Users"
              class="user-icon"
            />
          </div>
        </div>
  
        <deep-chat
          class="chat-component"
          :textInput="textInput"
          :messageStyles="messageStyles"
          :microphone="microphone"
          :submitButtonStyles="submitButtonStyles"
          :history="history"
          demo="true"
          :request="{
            url: `http://localhost:8000/event/${this.eventId}/message`,
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: { user: 'Alice', event_id: Number(eventId) }
          }"
        />
  
        <!--USER LIST PANEL -->
        <transition name="fade-slide">
            <div v-if="showUserPopup" class="user-list-panel">
            <h3>Linked Users</h3>
            <ul class="user-list">
                <li v-for="user in users" :key="user.iban">
                <div class="user-entry">
                    <strong>{{ user.name }}</strong><br />
                    <span class="iban">{{ user.iban }}</span>
                </div>
                </li>
            </ul>
            </div>
        </transition>

        <button class="finalize-button" @click="finalizeEvent">Finalize Event</button>

      </div>
    </div>
  </template>
  
  
  <script>
  export default {
    props: ['eventId'],
    methods: {
      goBack() {
        this.$router.push('/')
      },
      toggleUserPopup() {
            this.showUserPopup = !this.showUserPopup
        },
      finalizeEvent() {
          // Replace with actual API call
          fetch(`http://localhost:8000/${this.eventId}/finalize/`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
              event_id: this.eventId
              })
          })
              .then(res => res.json())
              .then(data => {
              console.log('Event finalized:', data)
                alert('Event finalized successfully!')
              })
              .catch(err => {
                console.error('Error finalizing event:', err)
                alert('Failed to finalize event.')
              });
          },
    async fetchEventDetails() {
      try {
        const response = await fetch(`http://localhost:8000/event/${this.eventId}`);
        const data = await response.json();
        this.eventName = data.name;
      } catch (err) {
        console.error('Failed to fetch event details:', err);
        this.eventName = 'Unknown Event';
      }
    }
  },
    data() {
      return {
        
        eventName: '',
        showUserPopup: false,

        users: [
      { name: 'Alice', iban: 'NL23BUNQ1234567890' },
      { name: 'Bob', iban: 'NL89BUNQ0987654321' }
        ],
        


        textInput: {
          styles: {
            container: {
              borderRadius: '20px',
              border: 'unset',
              width: '78%',
              marginLeft: '-15px',
              boxShadow: '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)'
            },
            text: {
              padding: '10px',
              paddingLeft: '15px',
              paddingRight: '34px'
            }
          },
          placeholder: {
            text: 'Any new expenses?',
            style: { color: '#606060' }
          }
        },
        messageStyles: {
          default: {
            shared: {
              bubble: {
                backgroundColor: 'unset',
                marginTop: '10px',
                marginBottom: '10px',
                boxShadow: '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)'
              }
            },
            user: {
              bubble: {
                background: 'linear-gradient(130deg, #2870EA 20%, #1B4AEF 77.5%)'
              }
            },
            ai: {
              bubble: {
                background: 'rgba(255,255,255,0.7)'
              }
            }
          }
        },
        microphone: {
          button: {
            default: {
              container: {
                default: {
                  bottom: '1em',
                  right: '0.6em',
                  borderRadius: '20px',
                  width: '1.9em',
                  height: '1.9em'
                }
              },
              svg: {
                styles: {
                  default: {
                    bottom: '0.35em',
                    left: '0.35em'
                  }
                }
              }
            },
            position: 'inside-right'
          }
        },
        submitButtonStyles: {
          position: 'outside-right',
          submit: {
            container: {
              default: {
                bottom: '0.8em',
                borderRadius: '25px',
                padding: '6px 5px 4px',
                backgroundColor: 'unset'
              },
              hover: {
                backgroundColor: '#b0deff4f'
              },
              click: {
                backgroundColor: '#b0deffb5'
              }
            },
            svg: {
              content:
                '<?xml version="1.0" encoding="utf-8"?><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m21.426 11.095-17-8A.999.999 0 0 0 3.03 4.242L4.969 12 3.03 19.758a.998.998 0 0 0 1.396 1.147l17-8a1 1 0 0 0 0-1.81zM5.481 18.197l.839-3.357L12 12 6.32 9.16l-.839-3.357L18.651 12l-13.17 6.197z"/></svg>',
              styles: {
                default: {
                  width: '1.5em',
                  filter:
                    'brightness(0) saturate(100%) invert(10%) sepia(86%) saturate(6044%) hue-rotate(205deg) brightness(100%) contrast(100%)'
                }
              }
            }
          },
          loading: {
            svg: {
              styles: {
                default: {
                  filter:
                    'brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)'
                }
              }
            }
          },
        
        },
        history: [
          { text: 'New event created! Add your expenses', role: 'ai' },
        ]
      } 
    }, 
    mounted() {
       this.fetchEventDetails(); // Called when component is mounted
    }
  }
  </script>
  
  <style scoped>


.finalize-button {
  margin-top: 2rem;
  align-self: center;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #4a90e2, #0071bc);
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.finalize-button:hover {
  background: linear-gradient(
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
  background-size: 200% 200%;
  animation: bunqPulse 2s ease-in-out forwards;
  transform: scale(1.05);
}

@keyframes bunqPulse {
  0% {
    background-position: left;
  }
  100% {
    background-position: right;
  }
}


/* Entering */
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* Leaving */
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}


.user-list-panel {
  position: absolute;
  top: 2rem;
  right: -280px;
  background: linear-gradient(135deg, #D0E0F7, #ffffff 100%);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.5);
  color: #1a1a1a;
  width: 260px;
  z-index: 10;
  text-align: left;

  max-height: 382px;       /* Or any height limit you prefer */
  overflow-y: auto;
  scrollbar-width: thin;   /* Firefox */
  scrollbar-color: #aaa transparent;
}

.user-list-panel h3 {
  margin-top: 0;
  font-size: 1.2rem;
  color: #1a1a1a;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.user-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-list li {
  background: linear-gradient(135deg, #3b82f6, #2563eb); /* light blue to deep blue */
  margin-bottom: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  color: #ffffff;
  font-weight: 500;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-list li:hover {
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

.iban {
  font-size: 0.85rem;
  color: #bbbbbb;
}


.user-icon-container {
  margin-left: auto;
  cursor: pointer;
}

.user-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  filter: brightness(70%) invert(1) saturate(0%) contrast(10%);
  transition: transform 0.2s;
}

.user-icon:hover {
  transform: scale(1.1);
  filter: brightness(1000%) invert(1) saturate(0%) contrast(10000%);
}





  .chat-view-wrapper {
    background-color: #242424;
    min-height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }
  
  .chat-view-card {
  position: relative; /* This anchors the popup to this box */
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
  
  .chat-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .back-button {
    background-color: transparent;
    color: #979797;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.4rem 0.6rem;
    border-radius: 4px;
    transition: background-color 0.2s;
  }
  .back-button:hover {
    background-color: #e0e0e0;
  }
  
  h2 {
    color: #9d9d9d;
    margin: 0;
    font-size: 1.5rem;
  }
  
  .chat-component {
    border-radius: 10px;
    border: 1px solid #e4e4e4;
    background: linear-gradient(
        90deg,
        rgb(239, 242, 247) 0%,
        rgb(237, 240, 249) 15.2%,
        rgb(235, 239, 248) 28.9%,
        rgb(231, 237, 249) 47.6%,
        rgb(228, 236, 249) 57.6%,
        rgb(222, 234, 250) 72.1%,
        rgb(213, 228, 249) 89.4%,
        rgb(208, 224, 247) 100%
    );
    width: 100%;
    overflow: hidden;
    
  }
  </style>
  