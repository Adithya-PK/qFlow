const mongoose = require('mongoose');

const tokenSchema = new mongoose.Schema({
  tokenNumber: { type: String, unique: true, required: true },
  customerName: { type: String, required: true, trim: true },
  phone: { type: String, required: true, trim: true },
  service: { type: String, required: true },
  status: {
    type: String,
    enum: ['WAITING', 'CALLED', 'IN_SERVICE', 'COMPLETED', 'SKIPPED', 'TRANSFERRED'],
    default: 'WAITING',
  },
  createdAt: { type: Date, default: Date.now },
  calledAt: { type: Date, default: null },
  startedAt: { type: Date, default: null },
  completedAt: { type: Date, default: null },
  skippedAt: { type: Date, default: null },
  transferredAt: { type: Date, default: null },
  counterId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Counter',
    default: null,
  },
  predictedDuration: { type: Number, default: null },  // minutes
  estimatedWait: { type: Number, default: null },       // minutes
  peopleAhead: { type: Number, default: null },
  actualDuration: { type: Number, default: null },      // minutes
  transferHistory: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Counter' }],
  notes: { type: String, default: '' },
});

// Indexes for common query patterns (tokenNumber index is already created by unique: true)
tokenSchema.index({ status: 1 });
tokenSchema.index({ createdAt: -1 });
tokenSchema.index({ phone: 1 });

module.exports = mongoose.model('Token', tokenSchema);
