# 🎓 25 Essential Viva-Voce Questions & Master Answers
**Department of AI & DS | Easwari Engineering College**  
**Student:** Adithya P K (310624243009) | **Project:** QFlow

---

### 1. What does the MERN stack stand for and why did you choose it over Django or Spring Boot?
> **Answer:**  
> MERN stands for **MongoDB, Express.js, React 19, and Node.js**. We chose it because it is an entirely **JavaScript-driven stack**. Data travels end-to-end as native JSON without object-relational mapping impedance. Furthermore, Node.js uses an asynchronous, single-threaded event loop that handles thousands of concurrent WebSocket connections (via Socket.IO) with significantly lower memory usage than thread-per-request frameworks like Django or Spring.

### 2. Why did you use MongoDB instead of a relational database like MySQL or PostgreSQL?
> **Answer:**  
> Queue management requires high-velocity writes and status transitions (waiting $\rightarrow$ called $\rightarrow$ in-service $\rightarrow$ completed). MongoDB's WiredTiger storage engine excels at rapid in-memory writes. Moreover, tokens store dynamic arrays like `transferHistory` and AI prediction metadata, which map naturally into flexible BSON documents without expensive SQL joins.

### 3. What does Socket.IO do in your project, and how does it differ from traditional HTTP polling?
> **Answer:**  
> Socket.IO maintains a persistent, full-duplex TCP connection between clients and the server. In HTTP polling, 50 phones querying every 2 seconds generate 1,500 HTTP requests per minute, creating server congestion and draining mobile batteries. Socket.IO eliminates this by pushing updates from the server to clients in **sub-50 millisecond latency** using tiny payloads ($<100\text{ bytes}$) only when events occur.

### 4. How do Socket.IO Rooms work in QFlow?
> **Answer:**  
> Socket.IO multiplexes events into specific virtual channels:
> - **The `queue` room:** Joined by staff monitors and display screens to receive global queue events (`tokenCreated`, `counterUpdated`, `analyticsUpdated`).
> - **Private `token:{tokenId}` rooms:** When a customer receives Token A101, their mobile browser joins `token:A101`. When staff calls Token A101, the server emits `yourTurn` **only** to that room, preventing other customers from receiving false alerts.

### 5. What exact AI model is used? Is it a deep learning neural network?
> **Answer:**  
> It is **not** a deep neural network, by deliberate engineering design. Deep learning models add 100ms+ inference latency, require expensive GPU servers, and lack explainability.  
> Instead, QFlow uses a **calibrated weighted-average regression heuristic with temporal peak multipliers**, baseline-calibrated on 500 synthetic historical transactions generated via a seeded Mulberry32 pseudo-random distribution. This executes in **sub-millisecond time ($<1\text{ms}$)** and provides 100% operational transparency.

### 6. Can you state the mathematical formula for service duration prediction?
> **Answer:**  
> The predicted duration is calculated as:
> $$D_{predicted} = \max\left(1, \operatorname{round}\left(\bar{D}_{base} + \Delta_{peak} + (Q_{ahead} \times 0.05)\right)\right)$$
> Where:
> - $\bar{D}_{base}$ is the weighted average duration of historical records for that service (matching hours receive $2\times$ weight, other hours $1\times$).
> - $\Delta_{peak} = 1.5\text{ minutes}$ during peak operational hours (9–11 AM and 2–4 PM).
> - $Q_{ahead} \times 0.05$ accounts for queue length and teller fatigue.

### 7. How is the customer's live estimated waiting time derived?
> **Answer:**  
> The system sums the remaining time for all currently serving tokens plus the estimated durations of all waiting tokens ahead, and divides this aggregate facility workload by the number of active, non-offline counters ($C_{active}$):
> $$T_{wait} = \max\left(0, \operatorname{round}\left(\frac{W_{total}}{C_{active}}\right)\right)$$

### 8. How does the Dynamic Heuristic Counter Recommendation algorithm work?
> **Answer:**  
> Every open, non-offline counter receives a real-time score between 0 and 100:
> - **Available with No Token:** 100 points (highest priority)
> - **Available (general):** 80 points
> - **Calling a customer:** 50 points
> - **In-Service:** 30 points
> - **Deductions:** $-5\text{ points}$ per assigned waiting token, and $-2\text{ points}$ per minute of remaining service time.  
> The desk with the highest score is recommended with an explainable reason code.

### 9. What happens if two staff members click "Call Next" at the exact same millisecond?
> **Answer:**  
> We prevent race conditions using MongoDB's atomic document update:
> ```javascript
> const token = await Token.findOneAndUpdate(
>   { _id: req.params.id, status: 'WAITING' },
>   { status: 'CALLED', calledAt: new Date(), counterId: counter._id },
>   { new: true }
> );
> ```
> MongoDB's single-document write lock ensures only the first operation modifies the document. The second concurrent query finds zero matching documents with `status: 'WAITING'`, returns `null`, and safely responds with an HTTP 409 Conflict.

### 10. How does the customer's phone vibrate when their turn comes?
> **Answer:**  
> When the mobile browser receives the `yourTurn` socket event, it triggers the HTML5 **Web Vibration API**:
> ```javascript
> if ('vibrate' in navigator) {
>   navigator.vibrate([300, 100, 300, 100, 500]);
> }
> ```
> This vibrates the physical device while popping up an on-screen visual alert.

### 11. Why do customers not need to install an app or register an account?
> **Answer:**  
> Queue tokens are transient, ephemeral tickets. Forcing visitors at a bank or hospital to download an 80MB native app and create an account creates massive friction and lobby delays. By running as a responsive web app on the mobile browser and generating a secure, token-specific URL (`/customer/status/:id`), visitors enjoy instant access with full privacy.

### 12. How does authentication and route security work for staff?
> **Answer:**  
> Staff authenticate using email and password. Passwords are encrypted using **bcrypt** with 10 salt rounds. Upon successful verification, the server issues a signed **JSON Web Token (JWT)** containing the user's ID and role (`staff` or `admin`). An Express middleware (`auth.js`) intercepts all administrative endpoints and validates the `Bearer <token>` header.

### 13. What is the role of React Context (`useContext`) in the frontend?
> **Answer:**  
> We use `AuthContext` to share user login tokens and `QueueContext` to maintain the live active queue array and WebSocket subscriptions. This makes real-time queue states available across all pages (Dashboard, Queue List, Analytics) without prop-drilling or external Redux boilerplate.

### 14. What is Vite and why is it superior to Webpack?
> **Answer:**  
> Vite leverages native browser ES Modules (ESM) and compiles modules on-demand using `esbuild` (written in Go). Unlike Webpack which bundles the entire codebase before serving, Vite starts the dev server in under 300ms and provides instant Hot Module Replacement (HMR).

### 15. How does the QR code dynamically encode the laptop's Wi-Fi IP address?
> **Answer:**  
> In `lanIP.js`, Node's `os.networkInterfaces()` inspects all network adapters, filters out loopbacks (`127.0.0.1`) and virtual subnets (VirtualBox `192.168.56.x`, WSL, VMware), and picks the active physical Wi-Fi adapter IPv4 address. This IP is automatically embedded into the generated QR code.

### 16. What happens if a customer's phone screen turns off or locks?
> **Answer:**  
> Mobile operating systems pause WebSockets when the screen sleeps. In `QueueContext.jsx`, we attached a socket `reconnect` event listener. The moment the phone wakes up and the socket reconnects, it immediately fetches the latest token state from `/api/tokens/:id`, ensuring the screen is always accurate.

### 17. What is the Token Transfer feature and why is it necessary?
> **Answer:**  
> If a customer at Counter 1 requires a different specialized department (e.g. loan document verification at Counter 3), staff click **Transfer**. Counter 1 is freed, the token is assigned to Counter 3 with priority, and the customer's phone updates instantly without forcing them to re-queue at the front door.

### 18. What happens if a customer does not show up when called?
> **Answer:**  
> Staff click **"Skip Token"**. The token's status changes to `'SKIPPED'`, recording a timestamp. The counter resets to `'AVAILABLE'`, and the next waiting customer moves up without stalling the desk.

### 19. How are the charts in the Analytics page generated?
> **Answer:**  
> MongoDB runs native aggregation pipelines (`$match`, `$group`, `$avg`) over completed tokens to compute hourly customer volume, average wait time per service category, and counter throughput. Recharts renders these aggregations into interactive SVG curves.

### 20. What is `MongoMemoryServer` and why is it included in your project?
> **Answer:**  
> It is an embedded, zero-config in-memory MongoDB instance. If local MongoDB is not installed or the service stops running during a live demonstration, QFlow automatically boots `MongoMemoryServer` and runs `seed.js`, guaranteeing 100% demo uptime without manual configuration.

### 21. What metrics would you use to evaluate your AI model's accuracy?
> **Answer:**  
> 1. **MAE (Mean Absolute Error):** Measures average absolute deviation between predicted and actual minutes (Goal: within $\pm 1.5\text{ mins}$).  
> 2. **RMSE (Root Mean Squared Error):** Penalizes large estimation errors.  
> 3. **$R^2$ Score:** Measures how well temporal peak multipliers explain real wait-time variance.  
> 4. **Counter Utilization Variance:** Measures whether workload is balanced evenly across counters.

### 22. What are the 6 possible statuses of a token in QFlow?
> **Answer:**  
> 1. `WAITING` $\rightarrow$ 2. `CALLED` $\rightarrow$ 3. `IN_SERVICE` $\rightarrow$ 4. `COMPLETED`  
> Edge statuses: `SKIPPED` (customer absent) and `TRANSFERRED` (moved to another counter).

### 23. What is the difference between a PUT and a PATCH request in your API?
> **Answer:**  
> `PUT` replaces an entire document. In QFlow, we use `PATCH` for state transitions (`/api/tokens/:id/call`, `/api/tokens/:id/start`, `/api/tokens/:id/complete`) because we are only modifying specific attributes (`status`, `calledAt`, `counterId`) without touching customer registration data.

### 24. What are the main limitations of your system today?
> **Answer:**  
> 1. Devices must be on the same local subnet unless an external tunnel or public IP is used.  
> 2. Duration modeling uses a synthetic baseline rather than months of live production data.  
> 3. Mobile browser tab must remain in memory for vibration alerts to fire.

### 25. What future enhancements are planned for QFlow?
> **Answer:**  
> 1. Public Waiting Lounge TV Monitor with multi-lingual Text-to-Speech (TTS) voice announcements.  
> 2. Cellular SMS and WhatsApp gateway notifications via Twilio for customers who leave Wi-Fi range.  
> 3. Transitioning the prediction engine to an XGBoost regressor trained on real facility data.  
> 4. Multi-tenant multi-branch cloud deployment with Docker and Kubernetes.
