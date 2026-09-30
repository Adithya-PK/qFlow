# QFlow — Easy-to-Learn Review 1 Presentation & Viva Guide
**Project Title**: QFlow — AI-Powered Smart Token & Queue Management System  
**Review**: Review 1 (MERN Stack Full Stack Development)  
**Student**: Adithya P K (310624243009)  
**College**: Easwari Engineering College  
**Guide**: Ms. D S K Harshitha  
**GitHub**: `https://github.com/Adithya-PK/qFlow`

---

## 1. The Simple 30-Second Elevator Pitch
> *"Traditional token machines just print paper slips without telling customers how long they actually have to wait, causing crowded waiting rooms and stressed staff.  
> **QFlow** solves this with a modern web app. Customers simply scan a QR code with their phone to get a digital token. Our lightweight AI estimates their waiting time and tells them which counter to go to. When their turn comes, their phone vibrates and alerts them in real time—no manual refreshing needed. Everything runs smoothly on the MERN stack."*

---

## 2. How the AI Model Works (Explained in Simple Terms)

Think of our AI as having **two simple jobs**:
1. **Estimate how long a customer will take** (Service Duration & Wait Time)
2. **Pick the best counter for them** (Counter Recommendation)

```
                       ┌──────────────────────────────┐
                       │       How AI Predicts        │
                       └──────────────┬───────────────┘
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     ▼                                ▼                                ▼
[ Service Type ]              [ Time of Day ]                 [ Queue Length ]
Account: ~8 mins             Peak hours (10am/2pm)           Each person ahead
Doc Verify: ~15 mins         adds 1 to 3 mins                adds a little extra time
     │                                │                                │
     └────────────────────────────────┼────────────────────────────────┘
                                      │
                                      ▼
                        Total Estimated Service Time
                                      │
                                      ▼
                Divide by Number of Active Working Counters
                                      │
                                      ▼
                      Customer's Live Waiting Time
```

### A. How Duration is Calculated:
1. **Base Time**: Different services take different times (e.g., General Enquiry takes ~5 mins, Document Verification takes ~15 mins).
2. **Peak Hours**: If it's a busy time (like 10 AM or 2 PM), the AI adds 1.5 to 3 minutes because counters are crowded.
3. **Line Length**: If 10 people are in line, staff get slightly busier, so each person adds a tiny buffer.
4. **Formula**:  
   $$\text{Predicted Time} = \text{Base Service Time} + \text{Peak Hour Buffer} + \text{Queue Buffer}$$

### B. How Waiting Time is Calculated:
Take the total time needed for all people waiting ahead, and **divide it by the number of active counters**.  
*Example*: If 3 people ahead take a total of 24 minutes and 3 counters are open, your estimated wait is $24 / 3 = 8\text{ minutes}$.

### C. How Counter Recommendation Works:
The system gives each open counter a score from 0 to 100:
- **Free Counter (No customer)**: 100 points (Recommended first)
- **Calling a Customer**: 50 points
- **Currently Serving**: 30 points minus time left to finish
- **Offline / Break**: 0 points (Excluded)

The counter with the highest score is recommended on the staff screen automatically.

### D. Evaluation Metrics (How We Test Accuracy):
1. **MAE (Mean Absolute Error)**: Average difference between estimated time and real time in minutes (Goal: within 1 to 2 minutes).
2. **RMSE (Root Mean Squared Error)**: Checks if there are any huge estimation mistakes.
3. **$R^2$ Score**: Checks how well the AI predictions match actual customer data (Goal: 85%+ accuracy).
4. **Counter Utilization**: Checks if work is distributed fairly among all counters rather than overloading just one.

---

## 3. MERN Stack Made Simple (Why We Used Each Part)

| Letter | Technology | Simple Explanation | Why We Used It |
| :---: | :--- | :--- | :--- |
| **M** | **MongoDB** | Database (stores data as JSON documents) | Fast writes, easy to save token history, and atomic updates so two counters never grab the same token. |
| **E** | **Express.js** | Backend Web Framework | Organizes our API routes (`/tokens`, `/counters`) and checks login security cleanly. |
| **R** | **React 19 + Vite** | Frontend User Interface | Fast, smooth screens for both mobile and desktop. Updates automatically without reloading the page. |
| **N** | **Node.js** | Backend JavaScript Runtime | Runs the server and easily handles multiple phones connected at the same time. |
| **+** | **Socket.IO** | Real-Time Live Connection | Sends instant alerts to the phone (vibration + pop-up) the second staff click "Call". |

---

## 4. Easy Slide-by-Slide Script (What to Say for Slides 1 to 17)

### **Slide 01: Title Slide**
> *"Good morning respected panel and guide. Today I am presenting Review 1 of my project: **QFlow — AI-Powered Smart Token and Queue Management System**. In this review, I will show the working MERN stack implementation, our AI prediction system, and demonstrate the live app running on phone and laptop."*

### **Slide 02: Agenda**
> *"Here is the agenda. We will cover the system requirements, architecture, database design, technology stack, frontend and backend development, live screenshots, challenges we solved, and the final demo."*

### **Slide 03: Requirements**
> *"Our functional goals are simple: customers scan a QR code to join the queue on their phone, pick a service, and get a digital token with live estimated wait time. Staff can call next, start, complete, skip, or transfer tokens.*  
> *Non-functionally, the app works on any phone browser over Wi-Fi without installing anything, updates in real time, and keeps data safe with JWT login."*

### **Slide 04: System Architecture**
> *"This slide shows how data travels. The customer phone sends a request to our Express backend. The AI estimates the time, and the token is saved into MongoDB.  
> Only after MongoDB saves the record does Socket.IO send live updates: staff get updates on the global queue, while the customer gets updates directly in their private token room."*

### **Slide 05: Use Case Diagram**
> *"We have three users in our system:*  
> *1. **Customer**: Scans QR, registers, tracks wait time, and gets turn alerts.*  
> *2. **Staff Operator**: Calls tokens in order, starts and completes service.*  
> *3. **Administrator**: Adds counters, manages service types, and views analytics."*

### **Slide 06: ER Diagram / Database Design**
> *"We have four simple MongoDB collections:*  
> *- **User**: Staff and admin logins with hashed passwords.*  
> *- **Counter**: Counter number, staff name, and active status.*  
> *- **Token**: Customer details, token number, timings, and assigned counter.*  
> *- **Service**: Service categories and standard times.*  
> *Tokens link to Counters, and all data is updated cleanly without race conditions."*

### **Slide 07: Module Description**
> *"We broke QFlow into seven clear modules: Customer Mobile, Token Management, Counter Operations, AI Prediction, Real-Time Sync, Security/Login, and Analytics. Each handles one specific responsibility."*

### **Slide 08: Technology Stack**
> *"We built this using the MERN stack: React 19 and Tailwind CSS for the frontend, Node.js and Express for the API server, MongoDB with Mongoose for the database, Socket.IO for instant live updates, and Recharts for dashboard graphs."*

### **Slide 09: UI Design**
> *"Our user interface is clean and dark-themed. The customer phone screen shows a large token number, live progress, and vibrates when called. The staff screen gives a clear dashboard with counter cards and AI suggestions."*

### **Slide 10: Frontend Development**
> *"On the frontend, we use React 19 with Vite for fast loading. We use React Context so login state and queue updates are shared easily across all pages without needing complex state libraries."*

### **Slide 11: Backend Development**
> *"The backend uses Node.js and Express. It handles all token actions—creating tokens, calling next, starting, completing, and transferring. It includes central error handling and ensures data is saved in MongoDB before any socket alert is sent."*

### **Slide 12: Database Integration**
> *"We connect to MongoDB using Mongoose. We have built-in demo data with an admin account, 5 services, 4 counters, and 15 completed records so the charts show realistic data immediately on startup."*

### **Slide 13: API Development**
> *"We created 14 clean REST API endpoints for logging in, generating tokens, changing token status, managing counters, and fetching analytics."*

### **Slide 14: Implementation Status**
> *"All 11 planned subsystems for Review 1 are 100% completed and working on real devices."*

### **Slide 15: Screenshots**
> *"Here are actual screenshots of the system: the Staff Dashboard with active counters, the Login screen, and the Customer QR code poster."*

### **Slide 16: Challenges Faced & Solutions**
> *"We solved five real engineering challenges:*  
> *1. **Mobile Access**: Configured Vite proxy so phones on the Wi-Fi can talk to the backend.*  
> *2. **Network IP**: Filtered out virtual network adapters to pick the real Wi-Fi IP for the QR code.*  
> *3. **Concurrency**: Used atomic database updates so two staff clicking at once never call the same customer.*  
> *4. **Sequence Numbers**: Generated unique tokens like A101, A102 reliably.*  
> *5. **Reconnects**: Made the phone automatically refresh when reconnecting to Wi-Fi."*

### **Slide 17: Remaining Work & References**
> *"For Review 2, we will add a full-screen TV display with voice announcements, automated tests, Docker packaging, and SMS alerts. Thank you! I am ready for the demo and questions."*

---

## 5. Top 20 Simple Viva Questions & Easy Answers

#### **Q1: What does MERN stand for and why is it useful?**
> **Answer**: MongoDB, Express, React, and Node.js. It lets us write both frontend and backend in JavaScript, making data transfer seamless using JSON without converting back and forth.

#### **Q2: Why did you use MongoDB instead of SQL?**
> **Answer**: MongoDB is fast, handles lots of simultaneous writes easily, and stores tokens as simple JSON documents. It also allows atomic updates so two counters never accidentally call the same token.

#### **Q3: What does Socket.IO do in your project?**
> **Answer**: It creates a live connection between server and phone. Instead of the phone constantly asking *"Is it my turn yet?"* every 2 seconds, the server pushes the alert the exact millisecond the staff clicks "Call".

#### **Q4: How does the phone alert the customer when their turn comes?**
> **Answer**: It triggers three things at once:
> 1. A big on-screen alert: *"YOUR TURN! Proceed to Counter 1"*.
> 2. A native browser pop-up notification.
> 3. Haptic vibration pulses on the phone.

#### **Q5: How does the AI estimate waiting time?**
> **Answer**: It checks the service type base time, adds extra minutes if it's peak hour (like 10 AM) or a long line, sums up all people ahead, and divides by the number of active counters.

#### **Q6: How does the AI pick the recommended counter?**
> **Answer**: It checks which counters are open. Free counters get highest priority (100 points). If all counters are busy, it picks the one closest to finishing their current customer.

#### **Q7: What happens if two staff members click "Call Next" at the exact same time?**
> **Answer**: We use MongoDB's atomic `findOneAndUpdate` with `status: 'WAITING'`. The database lets the first click change status to `CALLED`. The second click finds 0 waiting tokens and safely fails with a conflict message without double-calling.

#### **Q8: Why does the customer not need to download an app or log in?**
> **Answer**: We designed it to be frictionless. Customers just scan the QR code and use the mobile browser. Each token gets a unique secure URL so only that customer can see their progress.

#### **Q9: How do staff and admins log in securely?**
> **Answer**: They log in with email and password. Passwords are encrypted with bcrypt, and the server returns a signed JWT token that protects all staff operations.

#### **Q10: What does the Transfer feature do?**
> **Answer**: If a customer at Counter 1 needs a different service, the staff can transfer them to Counter 2. Counter 1 becomes free, Counter 2 gets the token, and the customer's phone updates immediately.

#### **Q11: What happens if a customer doesn't show up?**
> **Answer**: Staff click the "Skip" button. The token is marked as `SKIPPED`, the counter is freed, and the next person in line moves up.

#### **Q12: How are analytics generated?**
> **Answer**: MongoDB runs built-in aggregation queries that calculate average wait times, average service duration, and hourly traffic directly from completed tokens.

#### **Q13: How did you connect the phone and laptop on local Wi-Fi?**
> **Answer**: The server detects the laptop's Wi-Fi IP (like `192.168.1.4`) and puts it inside the QR code. The Vite server listens on `0.0.0.0` and proxies API calls to port 5000 so the phone connects smoothly.

#### **Q14: What is React Context and why did you use it?**
> **Answer**: React Context lets components share data (like user login or live queue tokens) across the whole app without having to pass props through every single component manually.

#### **Q15: What is Vite and why is it better than Webpack?**
> **Answer**: Vite starts up instantly and updates changes in milliseconds using modern browser ES modules, whereas older tools like Create React App take much longer to bundle.

#### **Q16: How do you measure the AI model's performance?**
> **Answer**: We use MAE (Mean Absolute Error) to measure how close predicted minutes are to actual service minutes, and $R^2$ to see if predictions accurately follow peak and quiet hours.

#### **Q17: What are the 6 token statuses in your system?**
> **Answer**: `WAITING` $\rightarrow$ `CALLED` $\rightarrow$ `IN_SERVICE` $\rightarrow$ `COMPLETED` (or `SKIPPED` / `TRANSFERRED`).

#### **Q18: What happens if the phone loses internet or screen sleeps?**
> **Answer**: When the phone wakes up and reconnects to the socket, it automatically fetches the latest token state from the server so the screen is never out of date.

#### **Q19: What is planned for Review 2?**
> **Answer**: A public TV screen display with text-to-speech voice announcements, Docker containerization, and SMS alerts.

#### **Q20: What is the main achievement of Review 1?**
> **Answer**: A complete, working full-stack system where physical phones scan a QR code, receive AI-predicted tokens, and communicate in real time with the staff dashboard over Wi-Fi.

---

## 6. 1-Minute Live Demo Checklist

1. **Open Laptop Dashboard**: `http://localhost:5173/` (Login: `admin@smartqueue.com` / `admin123`)
2. **Show Active Counters**: 4 counters open and ready.
3. **Show QR Code**: Click "Customer QR" in sidebar.
4. **Scan with Phone**: Open `http://<LAN_IP>:5173/customer` on phone.
5. **Register**: Enter name *"Aditya"*, service *"Account Service"*, click *"Get Token"*.
6. **Show Live Sync**: Token **A101** appears on phone with AI wait time, and instantly shows on laptop queue.
7. **Click Call Next**: On Counter 1 $\rightarrow$ phone vibrates and flashes *"YOUR TURN!"*.
8. **Start & Complete**: Click Start Service then Complete Service $\rightarrow$ counter becomes available again and duration is logged to analytics!
