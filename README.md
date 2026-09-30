# QFlow — AI-Powered Smart Token & Queue Management System

[![Node.js](https://img.shields.io/badge/Node.js-v18+-green.svg)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.x-green.svg)](https://www.mongodb.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4.x-black.svg)](https://socket.io/)

**QFlow** is a real-time, AI-powered token and queue management system built with the MERN stack. Customers scan a physical QR code with their phone, receive a digital token, and track their queue position live. Staff manage the queue through a professional dashboard with real-time updates powered by Socket.IO.

---

## ✨ Features

- 📱 **Real Phone QR Scanning** — Physical QR code opens customer portal
- 🎫 **Token Generation** — Database-backed sequential tokens (A101, A102...)
- 🔄 **Real-Time Updates** — Socket.IO synchronization between phone and dashboard
- 🤖 **AI Prediction** — Service duration prediction using synthetic historical dataset
- 📊 **Dynamic Counter Assignment** — AI-scored counter recommendation
- 👥 **Staff Dashboard** — Call, start, complete, skip, and transfer tokens
- 📈 **Analytics** — Real charts from MongoDB data
- 🏪 **Dynamic Counters** — Add Counter 5 and it appears everywhere instantly
- 🔔 **Live Customer Notifications** — Phone vibrates when it's your turn
- 🔐 **JWT Authentication** — Secure staff/admin login

---

## 🏗️ Architecture

```
Customer Phone (same Wi-Fi)
        │
        │ HTTP + Socket.IO
        ▼
React/Vite Frontend (port 5173)
        │
        │ REST API + Socket.IO
        ▼
Node/Express Backend (port 5000)
        │
        ├── Socket.IO (real-time broadcast)
        ├── JWT Auth
        ├── AI Prediction Service
        └── MongoDB (source of truth)
```

### Real-Time Flow
```
Phone scans QR → Customer Portal → POST /api/tokens
→ MongoDB stores token → Socket.IO emits 'tokenCreated'
→ Staff dashboard updates → Staff clicks 'Call Next'
→ MongoDB updates → Socket.IO emits 'tokenCalled' + 'yourTurn'
→ Customer phone shows "YOUR TURN!" + vibrates
→ Staff clicks 'Start Service' → MongoDB → Socket.IO
→ Staff clicks 'Complete' → MongoDB → Socket.IO
→ Counter becomes AVAILABLE
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Tailwind CSS, Recharts, Socket.IO Client |
| Backend | Node.js, Express.js, Socket.IO |
| Database | MongoDB, Mongoose |
| Auth | JWT, bcryptjs |
| AI/ML | Synthetic dataset + weighted regression (pure JS) |
| QR | qrcode library (PNG, SVG), qrcode.react |
| Real-time | Socket.IO (WebSocket + polling fallback) |

---

## 📁 Project Structure

```
QFlow/
├── client/                    # React/Vite frontend
│   └── src/
│       ├── components/        # CounterCard, AIRecommendation, QRModal, TransferModal
│       ├── context/           # AuthContext, QueueContext (Socket.IO + REST)
│       ├── layouts/           # StaffLayout (sidebar navigation)
│       ├── pages/
│       │   ├── auth/          # LoginPage
│       │   ├── customer/      # CustomerPortal, TokenStatus (mobile-first)
│       │   └── staff/         # Dashboard, QueuePage, CountersPage, AnalyticsPage
│       └── services/          # api.js (Axios), socket.js (Socket.IO client)
│
├── server/                    # Node/Express backend
│   ├── src/
│   │   ├── controllers/       # auth, token, counter, service, queue, analytics
│   │   ├── models/            # User, Token, Counter, Service
│   │   ├── routes/            # REST API routes
│   │   ├── services/          # predictionService.js, counterAssignmentService.js
│   │   ├── sockets/           # socketHandler.js (emit helpers)
│   │   ├── middleware/        # auth.js (JWT), errorHandler.js
│   │   ├── utils/             # lanIP.js
│   │   └── server.js
│   └── scripts/
│       ├── seed.js            # Database seeder
│       └── generateQR.js      # QR code generator
│
├── qr/                        # Generated QR files (after npm run generate-qr)
│   ├── customer-qr.png
│   ├── customer-qr.svg
│   └── customer-qr-print.png
│
├── package.json               # Root scripts (concurrently)
├── .env.example
└── README.md
```

---

## 📋 Prerequisites

1. **Node.js** v18 or higher → https://nodejs.org/
2. **MongoDB** v6 or higher (local installation)
3. Both devices (laptop + phone) on the **same Wi-Fi network**

### Install MongoDB (Windows)

1. Download from: https://www.mongodb.com/try/download/community
2. Install with default settings (includes mongod as Windows Service)
3. OR use MongoDB Atlas (cloud) and update `MONGODB_URI` in `.env`

### Find Your LAN IP (Windows)

Open Command Prompt and run:
```cmd
ipconfig
```

Look for **IPv4 Address** under your Wi-Fi adapter:
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . : 192.168.1.15   ← This is your LAN IP
```

---

## 🚀 Installation & Setup

### Step 1: Clone / Open the project
```bash
cd c:\Projects\QFlow
```

### Step 2: Install all dependencies
```bash
npm run install-all
```
This installs root, server, and client dependencies.

Or install individually:
```bash
npm install                          # root (concurrently)
npm install --prefix server          # backend
npm install --prefix client          # frontend
```

### Step 3: Configure environment
```bash
# Copy the example file
copy .env.example server\.env
```

Edit `server/.env` if needed:
```env
MONGODB_URI=mongodb://127.0.0.1:27017/qflow
PORT=5000
JWT_SECRET=your_secure_secret_here
CLIENT_URL=http://localhost:5173
NODE_ENV=development
```

### Step 4: Start MongoDB
If installed as a service, it starts automatically. Otherwise:
```cmd
mongod --dbpath C:\data\db
```

### Step 5: Seed the database
```bash
npm run seed
```

This creates:
- **Admin user**: `admin@smartqueue.com` / `admin123`
- **Staff user**: `staff@smartqueue.com` / `staff123`
- **5 Services**: Account Service, Payment Service, Document Verification, Customer Support, General Enquiry
- **4 Counters**: Counter 1 (Arun), Counter 2 (Priya), Counter 3 (Rahul), Counter 4 (Sneha)
- **15 historical tokens** for demo analytics

### Step 6: Generate QR Code
```bash
npm run generate-qr
```

This automatically detects your LAN IP and generates:
- `qr/customer-qr.png` (400×400, standard)
- `qr/customer-qr.svg` (vector, scalable)
- `qr/customer-qr-print.png` (1200×1200, printable)

Output example:
```
Customer URL: http://192.168.1.15:5173/customer
QR files saved to qr/
```

> **⚠️ Important:** If your laptop's Wi-Fi IP changes, run `npm run generate-qr` again.

### Step 7: Start the application
```bash
npm run dev
```

This starts both frontend and backend concurrently.

Terminal will show:
```
========================================
  QFLOW - AI-POWERED SMART QUEUE MGMT
========================================
  Backend:   http://localhost:5000
  Network:   http://192.168.1.15:5000
  MongoDB:   Connected ✓
  Socket.IO: Ready ✓
========================================
```

---

## 📱 LAN / Phone Setup

### On the Laptop
Both services must bind to `0.0.0.0` (not just localhost):
- ✅ Vite: configured with `server: { host: '0.0.0.0', port: 5173 }`
- ✅ Express: configured with `server.listen(PORT, '0.0.0.0')`

### On the Phone
1. Connect to the **same Wi-Fi** as the laptop
2. Scan the physical QR code (from `qr/customer-qr-print.png`)
3. The phone opens: `http://192.168.1.15:5173/customer`

### Windows Firewall
If the phone cannot reach the laptop, allow Node.js and Vite through Windows Firewall:

1. Open **Windows Defender Firewall with Advanced Security**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → TCP → Specific local ports: `5000, 5173`
4. Allow the connection → Apply to **Domain** and **Private** networks
5. Name it "QFlow"

---

## 🎮 Demo Workflow

### Full Demo Sequence

**STEP 1** — Start MongoDB service (if not auto-started)

**STEP 2** — Seed the database:
```bash
npm run seed
```

**STEP 3** — Start the app:
```bash
npm run dev
```

**STEP 4** — Generate QR:
```bash
npm run generate-qr
```
Print `qr/customer-qr-print.png` or display it on screen.

**STEP 5** — Connect phone and laptop to same Wi-Fi

**STEP 6** — Open Staff Dashboard on laptop:
- Go to `http://localhost:5173`
- Login: `admin@smartqueue.com` / `admin123`

**STEP 7** — Customer scans QR with phone:
- Phone opens `http://192.168.1.15:5173/customer`
- Customer enters: Name, Phone, Service
- Clicks **"Get Token"**

**STEP 8** — Observe real-time sync:
- Token (e.g., `A101`) appears on phone
- **Without refreshing**, the token row appears in staff dashboard queue

**STEP 9** — Staff calls the token:
- Click **"Call Next"** on Counter 1 card
- Phone immediately shows: **"YOUR TURN! → Counter 1"** and vibrates

**STEP 10** — Staff starts service:
- Click **"Start Service"**
- Phone updates to: **"IN SERVICE"**

**STEP 11** — Staff completes service:
- Click **"Complete Service"**
- Phone shows: **"COMPLETED"**
- Counter 1 becomes **AVAILABLE** again

**STEP 12** — Add Counter 5 dynamically:
- Go to Counters page → Click "Add Counter"
- Enter staff name "Karthik"
- Counter 5 appears immediately on ALL dashboards including customer phone

---

## 🔗 URLs

| URL | Description |
|-----|-------------|
| `http://localhost:5173` | Staff dashboard (laptop) |
| `http://localhost:5173/customer` | Customer portal (localhost) |
| `http://<LAN-IP>:5173/customer` | Customer portal (phone) |
| `http://localhost:5000/api/health` | Backend health check |
| `http://localhost:5173/login` | Login page |

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|---------|
| Admin | `admin@smartqueue.com` | `admin123` |
| Staff | `staff@smartqueue.com` | `staff123` |

---

## 🤖 AI/ML Component

### Prediction Model
QFlow uses a **weighted regression prediction** model implemented in pure JavaScript:

```
Predicted Duration = ServiceBaseDuration
                   + HourFactor (peak hours add 0-3 min)
                   + QueueFactor (longer queue adds 0-2 min)
```

### Synthetic Dataset
> **Academic Honesty Notice:** For prototype validation, a synthetic historical service dataset was generated programmatically. This is **not** real service center data. The model demonstrates the concept of AI-based service duration prediction.

The dataset contains 500 records with:
- `service_type` — one of 5 service categories
- `queue_length` — number of people in queue
- `hour` — hour of day (0-23)
- `historical_duration` — simulated service duration in minutes

### Service Prediction Examples

| Service | Queue | Hour | Predicted |
|---------|-------|------|-----------|
| Account Service | 3 | 10am | ~10 min |
| Document Verification | 5 | 2pm | ~20 min |
| General Enquiry | 1 | 9am | ~5 min |
| Payment Service | 2 | 11am | ~12 min |

### Counter Assignment AI
The counter recommendation scores each counter:
- **AVAILABLE** → base score 100
- **CALLING** → base score 50
- **IN_SERVICE** → base score 30 (with penalty for remaining service time)
- Deductions for queue workload

Returns: recommended counter + human-readable reason.

---

## 📡 API Reference

### Health
```
GET /api/health          → System status + LAN IP
```

### Authentication
```
POST /api/auth/login     → Login, returns JWT token
```

### Tokens
```
GET  /api/tokens         → All tokens (today's queue)
POST /api/tokens         → Create token (customer form)
GET  /api/tokens/:id     → Get token by ID
POST /api/tokens/:id/call      → Call token (staff)
POST /api/tokens/:id/start     → Start service (staff)
POST /api/tokens/:id/complete  → Complete service (staff)
POST /api/tokens/:id/skip      → Skip token (staff)
POST /api/tokens/:id/transfer  → Transfer token (staff)
```

### Counters
```
GET  /api/counters        → All active counters
POST /api/counters        → Add counter (auth required)
PUT  /api/counters/:id    → Update counter (auth required)
POST /api/counters/:id/call-next → Call next waiting token
```

### Queue & Analytics
```
GET /api/queue            → Current active queue
GET /api/analytics        → Dashboard analytics
POST /api/prediction      → AI duration prediction
GET /api/services         → All services
```

---

## 🔌 Socket.IO Events

### Server → Client Events
| Event | Room | Description |
|-------|------|-------------|
| `tokenCreated` | `queue` | New token created |
| `tokenCalled` | `queue` | Token called by staff |
| `yourTurn` | `token:{id}` | Customer's specific turn notification |
| `serviceStarted` | `queue` + `token:{id}` | Service started |
| `serviceCompleted` | `queue` + `token:{id}` | Service completed |
| `tokenSkipped` | `queue` + `token:{id}` | Token skipped |
| `tokenTransferred` | `queue` | Token transferred |
| `counterAdded` | broadcast | New counter added |
| `counterUpdated` | broadcast | Counter status changed |
| `queueUpdated` | `queue` | General queue update |

### Client → Server Events
| Event | Description |
|-------|-------------|
| `joinQueue` | Join staff queue room |
| `joinToken` | Join customer token room |

---

## 🏷️ Token State Machine

```
WAITING ──→ CALLED ──→ IN_SERVICE ──→ COMPLETED
    │           │
    └──→ SKIPPED │
         TRANSFERRED ──→ WAITING (at new counter)
```

Invalid transitions are blocked by the backend.

---

## 🔧 NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run install-all` | Install all dependencies |
| `npm run dev` | Start frontend + backend (concurrently) |
| `npm run server` | Start backend only |
| `npm run client` | Start frontend only |
| `npm run seed` | Seed MongoDB with demo data |
| `npm run generate-qr` | Generate QR codes |

---

## 🛠️ Troubleshooting

### MongoDB Connection Refused
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution:** MongoDB is not running. Start it:
- As Windows Service: `net start MongoDB`
- Manually: `mongod --dbpath C:\data\db`

### Phone Cannot Access Laptop
1. Check both devices are on the same Wi-Fi
2. Run `ipconfig` to confirm LAN IP
3. Allow ports 5000 and 5173 in Windows Firewall
4. Check antivirus isn't blocking connections

### QR Code Shows Wrong URL
The QR contains `127.0.0.1` instead of LAN IP:
```bash
npm run generate-qr
```
This auto-detects the LAN IP. If detection fails, your IP may be in a non-standard range.

### Tokens Not Appearing in Real-Time
1. Check browser console for Socket.IO errors
2. Verify backend is running on port 5000
3. The Vite proxy routes `/socket.io` to backend (works on localhost)
4. On phone via LAN: the frontend connects directly to `http://<LAN-IP>:5000`

### Port Already in Use
```bash
# Find what's using port 5000
netstat -ano | findstr :5000
# Kill process by PID
taskkill /PID <PID> /F
```

---

## 📊 Data Consistency

MongoDB is the **single source of truth**. The frontend:
1. Fetches initial state via REST API on page load
2. Receives live updates via Socket.IO
3. Re-fetches from REST after Socket.IO reconnection

Page refresh works because all data is in MongoDB — no localStorage queue.

---

## 🚧 Known Limitations (Prototype)

1. **AI Model:** Uses synthetic dataset, not real historical data
2. **No SMS:** No SMS notification (would require Twilio/etc.)
3. **Single Organization:** No multi-tenant support
4. **No Queue Display Board:** No public TV display (easily added)
5. **Phone notifications:** Uses browser vibration API; no push notifications

---

## 🔮 Future Enhancements

- [ ] Real historical data collection for better ML predictions
- [ ] Multi-organization / tenant support
- [ ] SMS/WhatsApp notifications
- [ ] Queue display board (large screen view)
- [ ] Advanced RBAC (per-counter staff roles)
- [ ] Appointment scheduling integration
- [ ] PWA for offline support
- [ ] Export reports (PDF/Excel)

---

## 📝 Academic Notes

- **Dataset:** Synthetic historical service dataset generated programmatically (500 records)
- **ML Approach:** Weighted regression with service-type averages, hour-of-day factor, and queue-length factor
- **Architecture:** Standard MERN stack with Socket.IO for real-time bidirectional communication
- **Security:** JWT authentication, bcrypt password hashing, input validation

---

*QFlow — AI-Powered Smart Token & Queue Management System*  
*Academic Full-Stack Development Project*
