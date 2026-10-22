# 🎓 25 Simple & Punchy Viva Questions & Answers
**Department of AI & DS | Easwari Engineering College**  
**Student:** Adithya P K (310624243009) | **Project:** QFlow

---

### 1. What is the MERN stack and why did you use it?
> **Answer:**  
> MERN stands for **MongoDB, Express.js, React 19, and Node.js**. We used it because the entire project is built using **one language: JavaScript**. Data moves smoothly between the phone, server, and database as simple JSON without needing complex conversions.

### 2. Why did you choose MongoDB instead of SQL (MySQL/PostgreSQL)?
> **Answer:**  
> MongoDB stores tokens as simple JSON documents. It is super fast for saving and updating token statuses, and we don't have to join multiple complex SQL tables every time a customer moves in line.

### 3. What does Socket.IO do in your project?
> **Answer:**  
> Socket.IO creates an instant live connection between the phone and the server. Instead of the phone constantly asking the server *"Is it my turn yet?"* every 2 seconds, the server pushes the alert the exact millisecond the staff clicks "Call".

### 4. How does the customer's phone vibrate when called?
> **Answer:**  
> When the phone receives the "yourTurn" alert from Socket.IO, our React code triggers the browser's built-in **Web Vibration API** (`navigator.vibrate`), which physically pulses the phone in the customer's pocket.

### 5. What does the AI model do in your project?
> **Answer:**  
> Our AI has **two simple jobs**:
> 1. It calculates **how long the customer has to wait** based on the service type, peak hours, and people ahead.
> 2. It **recommends the best counter** by scoring open desks from 0 to 100 so customers are routed to the freest teller.

### 6. Why did you use this lightweight AI instead of Deep Learning?
> **Answer:**  
> Deep learning models are slow (taking 100ms+ to run), require expensive GPU servers, and are hard to explain. Our formula runs in less than 1 millisecond on any computer and gives clear, understandable reasons for every recommendation.

### 7. How does the AI calculate estimated waiting time?
> **Answer:**  
> It takes the base service time (like 8 mins for Account Service), adds 1.5 extra minutes if it is a busy peak hour (like 10 AM or 2 PM), adds a small buffer for people in line, and divides the total time by the number of active open counters.

### 8. How does the counter recommendation scoring work?
> **Answer:**  
> It scores every open counter from 0 to 100:
> - A free counter with no customer gets **100 points** (recommended first).
> - A counter currently calling someone gets **50 points**.
> - A busy counter currently serving someone gets **30 points** minus points for minutes left.  
> The counter with the highest score is automatically recommended.

### 9. What happens if two staff members click "Call Next" at the exact same time?
> **Answer:**  
> We use MongoDB's atomic update (`findOneAndUpdate`). It checks if the token status is `'WAITING'`. The first click claims the token and turns it to `'CALLED'`. The second click sees it is no longer waiting and safely stops. Two staff can never call the same person.

### 10. Why don't customers need to download an app or register an account?
> **Answer:**  
> Downloading an 80MB app or filling out a registration form just to get a token wastes customer time and creates lobby crowds. Customers just scan the QR code and use their normal phone browser (Safari or Chrome).

### 11. How do staff and administrators log in securely?
> **Answer:**  
> Staff log in using an email and password. Passwords are encrypted using **bcrypt**, and the server returns a signed **JWT (JSON Web Token)** that protects all staff operations.

### 12. What is React Context (`useContext`) and why did you use it?
> **Answer:**  
> React Context lets our screens share data (like user login status and the live queue list) across all pages easily, without having to pass data manually through every single component.

### 13. What is Vite and why is it better than older tools like Create React App?
> **Answer:**  
> Vite starts up almost instantly (under 300ms) and updates changes in milliseconds using modern browser modules, whereas older tools like Webpack take a long time to bundle the code.

### 14. How does the phone know your laptop's IP address when scanning the QR code?
> **Answer:**  
> Our backend automatically checks the laptop's Wi-Fi adapter using Node's `os.networkInterfaces()`, filters out virtual network adapters, and puts the real Wi-Fi IP address directly into the QR code.

### 15. What happens if the customer's phone screen turns off or sleeps?
> **Answer:**  
> When the phone screen turns off, the browser temporarily pauses the live connection. The moment the customer turns their screen back on, our code automatically reconnects and fetches the latest token status immediately.

### 16. What is the Token Transfer feature for?
> **Answer:**  
> If a customer at Counter 1 needs document verification at Counter 3, the staff can click **Transfer**. Counter 1 becomes free, Counter 3 receives the customer with priority, and the customer's phone updates without them needing to re-queue at the door.

### 17. What happens if a customer doesn't show up when called?
> **Answer:**  
> The staff clicks **"Skip Token"**. The token is marked as `SKIPPED`, the counter is freed to take the next person, and the line keeps moving without delay.

### 18. What are the 6 token statuses in your system?
> **Answer:**  
> Normal flow: `WAITING` $\rightarrow$ `CALLED` $\rightarrow$ `IN_SERVICE` $\rightarrow$ `COMPLETED`.  
> Special cases: `SKIPPED` (customer missed turn) and `TRANSFERRED` (moved to another counter).

### 19. How are the charts in the Analytics page generated?
> **Answer:**  
> MongoDB runs built-in aggregation queries that calculate the average wait time, average service duration, and hourly customer volume from completed tokens, and Recharts draws the graphs.

### 20. What is `MongoMemoryServer` and why did you include it?
> **Answer:**  
> It is an embedded, in-memory MongoDB fallback. If MongoDB is not installed or running on a presentation laptop, our server starts this temporary in-memory database automatically, ensuring our demo never fails.

### 21. How do you measure the accuracy of your AI predictions?
> **Answer:**  
> We use **MAE (Mean Absolute Error)** to check how close our predicted minutes are to the real time (our goal is within 1 to 2 minutes), and **$R^2$ score** to verify that our peak-hour adjustments follow real customer traffic patterns.

### 22. What happens if the college Wi-Fi doesn't allow cross-device connection?
> **Answer:**  
> We switch to a mobile phone hotspot, which puts the phone and laptop on the exact same private network with zero restrictions. Or, we can run the demo in a split-screen dual window on the laptop with zero Wi-Fi required.

### 23. What is the difference between an Express route and a Socket event?
> **Answer:**  
> An Express route (`POST /api/tokens`) is a one-time request sent from client to server. A Socket event (`tokenCalled`) is an instant push message sent from the server to all connected screens simultaneously.

### 24. What are the main limitations of your project today?
> **Answer:**  
> Currently, the customer's phone and laptop must be on the same local network, and turn alerts require the browser tab to remain open in the background.

### 25. What future enhancements are you planning?
> **Answer:**  
> 1. A full-screen Waiting Room TV display with spoken voice announcements (*"Token A101, please proceed to Counter 2"*).  
> 2. SMS and WhatsApp alerts so customers can receive notifications even if they close their browser.  
> 3. Cloud deployment using Docker.
