# 💻 MERN Stack & Architecture Made Simple
**Department of AI & DS | Easwari Engineering College**  
**Student:** Adithya P K (310624243009) | **Project:** QFlow

---

## 1. The MERN Stack Explained Simply

Think of QFlow like a well-organized bank branch:

| Letter | Technology | Simple Analogy | What It Does in QFlow | Why We Used It |
| :---: | :--- | :--- | :--- | :--- |
| **M** | **MongoDB** | **The Digital Record Book** | Stores tokens, staff logins, and counters as simple JSON documents. | Super fast to save tokens. No complicated SQL tables or joins needed. |
| **E** | **Express.js** | **The Traffic Police** | Routes requests between the phone, laptop, and database. | Organizes all our API links cleanly (e.g., `/tokens`, `/counters`, `/auth`). |
| **R** | **React 19** | **The Interactive Screens** | The user interface on both the phone and laptop. | Updates the screen instantly without needing to refresh or reload the browser. |
| **N** | **Node.js** | **The Engine** | Runs the backend JavaScript server on the computer. | Handles multiple phones and laptops connected at the same time smoothly. |
| **+** | **Socket.IO** | **The Live Walkie-Talkie** | Sends instant messages between server and phone. | Pushes the turn alert to the phone immediately the millisecond staff clicks "Call". |

---

## 2. How the Whole System Connects (Simple Flow)

```
 [ Customer's Phone ]                    [ Staff Laptop ]
  (React Mobile UI)                      (React Dashboard)
          │                                      │
          │ 1. Scan QR & Get Token               │ 4. Click "Call Next"
          ▼                                      ▼
   ┌──────────────────────────────────────────────────┐
   │             EXPRESS + NODE.JS BACKEND            │
   │  - Checks who you are                            │
   │  - Runs simple AI to calculate wait time         │
   │  - Sends live alerts using Socket.IO             │
   └─────────────────────────┬────────────────────────┘
                             │
                             ▼ 2. Save Token / 3. Fetch Next
   ┌──────────────────────────────────────────────────┐
   │                 MONGODB DATABASE                 │
   │  - Stores Tokens (A101, A102...)                 │
   │  - Stores Counters (Counter 1, 2, 3...)          │
   │  - Prevents double-booking                       │
   └──────────────────────────────────────────────────┘
```

### The 4-Step Journey of a Token:
1. **Customer scans QR code:** Fills in name and service on their phone $\rightarrow$ clicks "Get Token".
2. **Backend calculates wait time:** Estimates how long it takes and saves Token **A101** into MongoDB.
3. **Staff sees token live:** Token A101 immediately appears on the staff laptop screen without reloading.
4. **Staff calls customer:** Staff clicks "Call Next" $\rightarrow$ Socket.IO instantly rings the customer's phone with a vibration and **"YOUR TURN!"** message.

---

## 3. How the AI Works (Two Simple Jobs)

Instead of a heavy, complicated neural network that slows down the computer, our AI does **two simple, smart jobs**:

```
                       ┌──────────────────────────────┐
                       │     The 2 Jobs of our AI     │
                       └──────────────┬───────────────┘
                                      │
         ┌────────────────────────────┴────────────────────────────┐
         ▼                                                         ▼
   [ JOB 1: WAIT TIME ]                                     [ JOB 2: COUNTER PICKER ]
How long will the customer wait?                        Which counter should serve them?
Base Time + Peak Traffic ÷ Open Desks                  Gives each desk a score from 0 to 100
```

### Job 1: Estimating Wait Time
1. **Base Service Time:** Each service has a normal time (e.g., General Enquiry = 5 mins, Account Service = 8 mins, Document Verification = 15 mins).
2. **Peak Hour Buffer:** If it is a busy hour (like 10 AM or 2 PM), the system adds 1.5 extra minutes.
3. **Queue Length:** Adds a tiny buffer for each person waiting ahead.
4. **The Formula:**
   $$\text{Predicted Wait Time} = \frac{\text{Total Time Needed for All Waiting Customers}}{\text{Number of Active Counters}}$$
   *Example:* If 3 people ahead need a total of 24 minutes and 3 counters are open, your estimated wait is $24 \div 3 = 8\text{ minutes}$.

---

### Job 2: Recommending the Best Counter (0 to 100 Score)
The system checks all open desks and gives them a score:
- **Free Counter (No customer):** **100 points** (Recommended first!)
- **Calling Counter (Customer walking up):** **50 points**
- **Busy Counter (Currently serving):** **30 points** minus points for minutes left to finish
- **Offline / On Break:** **0 points** (Ignored)

The counter with the highest score is automatically recommended on the staff dashboard.

---

## 4. How We Prevent Double-Calling (Concurrency Made Easy)

### The Problem:
What if Counter 1 and Counter 2 click **"Call Next"** at the exact same millisecond during a morning rush?

### Our Solution:
We use MongoDB's built-in atomic check (`findOneAndUpdate`):
```javascript
// Check for next WAITING token and change to CALLED in one single step
const token = await Token.findOneAndUpdate(
  { _id: tokenId, status: 'WAITING' },
  { status: 'CALLED', counterId: counterId },
  { new: true }
);
```
- **Click 1 wins:** The database sees the status is `'WAITING'`, changes it to `'CALLED'`, and gives the token to Counter 1.
- **Click 2 is safely blocked:** The database sees the token is no longer `'WAITING'`, so it does nothing and tells Counter 2: *"Already called by another counter."*
- **Result:** Two staff members can never accidentally call the same customer!

---

## 5. Summary for Your Review
- **Frontend:** React 19 + Vite (Fast, smooth, mobile-friendly screens).
- **Backend:** Node.js + Express (Handles requests and routes).
- **Database:** MongoDB (Saves tokens, counters, and logs).
- **Real-Time:** Socket.IO (Instant push alerts & phone vibration).
- **AI:** Lightweight duration calculator and 100-point counter recommendation.
