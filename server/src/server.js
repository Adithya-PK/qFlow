const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const { getLanIP } = require('./utils/lanIP');
const { initializeSockets } = require('./sockets/socketHandler');

const authRoutes = require('./routes/authRoutes');
const tokenRoutes = require('./routes/tokenRoutes');
const counterRoutes = require('./routes/counterRoutes');
const serviceRoutes = require('./routes/serviceRoutes');
const queueRoutes = require('./routes/queueRoutes');
const analyticsRoutes = require('./routes/analyticsRoutes');
const errorHandler = require('./middleware/errorHandler');

// ---------------------------------------------------------------------------
// App & Server setup
// ---------------------------------------------------------------------------
const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    credentials: true,
  },
  transports: ['websocket', 'polling'],
});

// Make io instance available to all controllers via req.app.get('io')
app.set('io', io);

// ---------------------------------------------------------------------------
// Middleware
// ---------------------------------------------------------------------------
app.use(cors({ origin: '*', credentials: true }));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logger (development)
if (process.env.NODE_ENV === 'development') {
  app.use((req, _res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
    next();
  });
}

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------
app.use('/api/auth', authRoutes);
app.use('/api/tokens', tokenRoutes);
app.use('/api/counters', counterRoutes);
app.use('/api/services', serviceRoutes);
app.use('/api/queue', queueRoutes);
app.use('/api/analytics', analyticsRoutes);

app.get('/api/health', (_req, res) => {
  const lanIP = getLanIP();
  res.json({
    status: 'OK',
    timestamp: new Date(),
    uptime: Math.floor(process.uptime()),
    environment: process.env.NODE_ENV || 'development',
    lanIP,
    customerURL: `http://${lanIP}:5173/customer`,
  });
});

// Catch-all 404
app.use((_req, res) => {
  res.status(404).json({ success: false, message: 'Route not found.' });
});

// Global error handler — must be last
app.use(errorHandler);

// ---------------------------------------------------------------------------
// Socket.IO
// ---------------------------------------------------------------------------
initializeSockets(io);

const { seedDatabase } = require('../scripts/seed');

const PORT = parseInt(process.env.PORT, 10) || 5000;

async function connectDB() {
  const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/qflow';
  
  try {
    // Attempt local/configured MongoDB connection with a short timeout
    await mongoose.connect(MONGODB_URI, { serverSelectionTimeoutMS: 2000 });
    return { mode: 'Local / Configured MongoDB (' + MONGODB_URI + ')' };
  } catch (err) {
    console.log('[MongoDB] Local MongoDB server not found (' + err.message + ').');
    console.log('[MongoDB] Starting zero-config embedded MongoDB instance...');
    
    try {
      const { MongoMemoryServer } = require('mongodb-memory-server');
      const mongod = await MongoMemoryServer.create();
      const uri = mongod.getUri();
      await mongoose.connect(uri);
      
      // Auto-seed initial demo data into the embedded instance
      console.log('[MongoDB] Auto-seeding initial demo data...');
      await seedDatabase();
      
      return { mode: 'Embedded MongoDB (Zero-Config Active)', mongod };
    } catch (memErr) {
      console.error('[FATAL] Failed to initialize embedded MongoDB:', memErr.message);
      throw err;
    }
  }
}

connectDB()
  .then(({ mode }) => {
    const lanIP = getLanIP();

    server.listen(PORT, '0.0.0.0', () => {
      console.log('');
      console.log('========================================');
      console.log('QFLOW');
      console.log('AI-POWERED SMART QUEUE MANAGEMENT');
      console.log('========================================');
      console.log('');
      console.log(`Backend:         http://localhost:${PORT}`);
      console.log(`Frontend:        http://localhost:5173`);
      console.log(`Network:         http://${lanIP}:5173`);
      console.log(`Customer Portal: http://${lanIP}:5173/customer`);
      console.log(`Staff Dashboard: http://${lanIP}:5173/`);
      console.log(`Customer QR:     qr/customer-qr.png`);
      console.log(`MongoDB:         Connected [${mode}]`);
      console.log(`Socket.IO:       Ready`);
      console.log('');
      console.log('========================================');
      console.log('');
    });
  })
  .catch((err) => {
    console.error('[FATAL] Database connection failed:', err.message);
    process.exit(1);
  });

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[INFO] SIGTERM received. Closing server...');
  server.close(() => {
    mongoose.connection.close(false, () => {
      console.log('[INFO] Server and MongoDB closed. Exiting.');
      process.exit(0);
    });
  });
});

module.exports = { app, server };
