const mongoose = require('mongoose');
const Token = require('../src/models/Token');
const Counter = require('../src/models/Counter');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/qflow';

async function run() {
  await mongoose.connect(MONGODB_URI);
  const tokens = await Token.find().sort({ createdAt: 1 }).lean();
  console.log(`Total tokens in DB: ${tokens.length}`);
  tokens.forEach((t) => {
    console.log(`- ${t.tokenNumber} | ${t.customerName} | Status: ${t.status} | Service: ${t.service}`);
  });
  await mongoose.disconnect();
}

run().catch(console.error);
