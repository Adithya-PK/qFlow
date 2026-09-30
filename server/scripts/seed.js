/**
 * QFlow Seed Script
 *
 * Seeds the database with:
 *  1. Admin user
 *  2. Service types
 *  3. Counters (4 staff members)
 *  4. 15 historical completed tokens (for analytics demo)
 *
 * Safe to run multiple times — uses upsert/findOneAndUpdate to avoid duplicates.
 *
 * Usage: npm run seed
 */

const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const User = require('../src/models/User');
const Service = require('../src/models/Service');
const Counter = require('../src/models/Counter');
const Token = require('../src/models/Token');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/qflow';

// ---------------------------------------------------------------------------
// Seed data definitions
// ---------------------------------------------------------------------------
const USERS = [
  {
    name: 'Admin User',
    email: 'admin@smartqueue.com',
    password: 'admin123',
    role: 'admin',
  },
  {
    name: 'Staff User',
    email: 'staff@smartqueue.com',
    password: 'staff123',
    role: 'staff',
  },
];

const SERVICES = [
  { name: 'Account Service', code: 'AC', averageDuration: 9, description: 'Account opening, closing, and management.' },
  { name: 'Payment Service', code: 'PAY', averageDuration: 11, description: 'Bill payments, fund transfers, and remittances.' },
  { name: 'Document Verification', code: 'DOC', averageDuration: 16, description: 'KYC, identity verification, and document checks.' },
  { name: 'Customer Support', code: 'SUP', averageDuration: 8, description: 'Complaints, queries, and general assistance.' },
  { name: 'General Enquiry', code: 'GEN', averageDuration: 5, description: 'Information, directions, and quick enquiries.' },
];

const COUNTERS = [
  { counterNumber: 1, staffName: 'Arun Kumar', servicesSupported: ['AC', 'PAY', 'GEN'] },
  { counterNumber: 2, staffName: 'Priya Sharma', servicesSupported: ['DOC', 'SUP', 'GEN'] },
  { counterNumber: 3, staffName: 'Rahul Mehta', servicesSupported: ['PAY', 'AC', 'SUP'] },
  { counterNumber: 4, staffName: 'Sneha Pillai', servicesSupported: ['DOC', 'GEN', 'AC'] },
];

// ---------------------------------------------------------------------------
// Historical token generator
// ---------------------------------------------------------------------------
function buildHistoricalTokens(counters, serviceNames) {
  const tokens = [];
  const now = new Date();

  // Spread 15 tokens across different hours today
  for (let i = 0; i < 15; i++) {
    const serviceName = serviceNames[i % serviceNames.length];
    const counter = counters[i % counters.length];

    const hoursAgo = 8 - Math.floor(i * 0.5); // spread from ~8hrs ago to ~0.5hrs ago
    const createdAt = new Date(now.getTime() - hoursAgo * 60 * 60 * 1000);
    const calledAt = new Date(createdAt.getTime() + (2 + Math.floor(Math.random() * 5)) * 60 * 1000);
    const startedAt = new Date(calledAt.getTime() + 1 * 60 * 1000);
    const actualDuration = 5 + Math.floor(Math.random() * 12); // 5-17 min
    const completedAt = new Date(startedAt.getTime() + actualDuration * 60 * 1000);

    const seq = 101 + i;
    tokens.push({
      tokenNumber: `A${seq}`,
      customerName: `Customer ${seq}`,
      phone: `98765${String(43210 + i).padStart(5, '0')}`,
      service: serviceName,
      status: 'COMPLETED',
      createdAt,
      calledAt,
      startedAt,
      completedAt,
      counterId: counter._id,
      predictedDuration: actualDuration + Math.floor(Math.random() * 3) - 1,
      estimatedWait: 5 + Math.floor(Math.random() * 10),
      peopleAhead: Math.floor(Math.random() * 8),
      actualDuration,
    });
  }

  return tokens;
}

// ---------------------------------------------------------------------------
// Main seed function
// ---------------------------------------------------------------------------
async function seed() {
  const isStandalone = mongoose.connection.readyState === 0;
  try {
    if (isStandalone) {
      await mongoose.connect(MONGODB_URI);
      console.log('\n[Seed] Connected to MongoDB:', MONGODB_URI);
    } else {
      console.log('\n[Seed] Using active MongoDB connection');
    }

    // 1. Users
    console.log('\n[Seed] Seeding users...');
    for (const u of USERS) {
      const hashedPassword = await bcrypt.hash(u.password, 12);
      const user = await User.findOneAndUpdate(
        { email: u.email },
        { $setOnInsert: { name: u.name, email: u.email, password: hashedPassword, role: u.role } },
        { upsert: true, new: true, setDefaultsOnInsert: true }
      );
      console.log(`  ✓ User: ${user.email} (${user.role})`);
    }

    // 2. Services
    console.log('\n[Seed] Seeding services...');
    for (const s of SERVICES) {
      const service = await Service.findOneAndUpdate(
        { code: s.code },
        { $set: { name: s.name, averageDuration: s.averageDuration, description: s.description, active: true } },
        { upsert: true, new: true }
      );
      console.log(`  ✓ Service: ${service.name} (${service.code})`);
    }

    // 3. Counters
    console.log('\n[Seed] Seeding counters...');
    const seededCounters = [];
    for (const c of COUNTERS) {
      const counter = await Counter.findOneAndUpdate(
        { counterNumber: c.counterNumber },
        {
          $set: {
            staffName: c.staffName,
            servicesSupported: c.servicesSupported,
            status: 'AVAILABLE',
            isActive: true,
          },
        },
        { upsert: true, new: true }
      );
      seededCounters.push(counter);
      console.log(`  ✓ Counter ${counter.counterNumber}: ${counter.staffName}`);
    }

    // 4. Historical tokens — only create if fewer than 15 exist for today
    console.log('\n[Seed] Seeding historical tokens...');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const existingCount = await Token.countDocuments({ createdAt: { $gte: today } });

    if (existingCount < 15) {
      const serviceNames = SERVICES.map((s) => s.name);
      const historicalTokens = buildHistoricalTokens(seededCounters, serviceNames);

      for (const t of historicalTokens) {
        await Token.findOneAndUpdate(
          { tokenNumber: t.tokenNumber },
          { $setOnInsert: t },
          { upsert: true, new: true }
        );
        process.stdout.write(`  ✓ Token ${t.tokenNumber} `);
      }
      console.log('\n  Done.');
    } else {
      console.log(`  Skipped — ${existingCount} tokens already exist for today.`);
    }

    console.log('\n========================================');
    console.log('  QFlow Seed Completed Successfully! ✓');
    console.log('========================================');
    console.log('  Admin Login:');
    console.log('    Email:    admin@smartqueue.com');
    console.log('    Password: admin123');
    console.log('  Staff Login:');
    console.log('    Email:    staff@smartqueue.com');
    console.log('    Password: staff123');
    console.log('========================================\n');

    if (require.main === module) {
      await mongoose.disconnect();
      process.exit(0);
    }
  } catch (err) {
    console.error('\n[Seed] Error:', err.message);
    if (require.main === module) {
      await mongoose.disconnect();
      process.exit(1);
    }
    throw err;
  }
}

if (require.main === module) {
  seed();
}

module.exports = { seedDatabase: seed };
