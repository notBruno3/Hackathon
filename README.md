# 🧾 Bill — Group Expense Tracker with AI

Bill is a **Vue + FastAPI** powered web app for managing shared expenses in group events. It features an AI agent that helps users log and track their spending intuitively, making cost splitting transparent, fair, and even fun.


---

## ✨ Features

- ✅ Create and join events with a unique ID
- 🧑‍🤝‍🧑 Add participants with IBANs
- 💬 Log expenses via an AI chat interface
- 🟢 Real-time event status (active/inactive)
- 📋 Participant list with a gradient design
- 🚀 Finalize events and automatically trigger Bunq API inquiries *(planned)*

---


## 🌐 API Endpoints

| Method | Endpoint                        | Description               |
|--------|---------------------------------|---------------------------|
| POST   | `/event`                        | Create new event          |
| POST   | `/event/{event_id}/join`        | Join an existing event    |
| POST   | `/event/{event_id}/finalize`    | Finalize the event        |
| GET    | `/event/{event_id}`             | Get event details         |
| GET    | `/events`                       | List all events           |
| POST   | `/event/{event_id}/message`     | AI chat expense input     |

---


## 🚀 How to Run the Project


1. Navigate to the frontend directory:

   ```bash
   cd client
   npm install
   npm run dev
   ```

2. Open a new terminal and do the same for backend (there is a run.ps1 in case you don't have the dependencies installed)

   ```bash 
   cd server
   python main.py
   ```

3. Environment
   Create a new .env file in the server root. Add you API key there. Example:
   ```
   OPENAI_API_KEY=your_api_key
   ```
   And a .env.local in the client root for the server endpoints
   ```
   VITE_API_URL=your_server_port
   ```
