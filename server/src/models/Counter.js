const mongoose = require('mongoose');

const counterSchema = new mongoose.Schema(
  {
    counterNumber: { type: Number, required: true, unique: true },
    staffName: { type: String, required: true, trim: true },
    status: {
      type: String,
      enum: ['AVAILABLE', 'CALLING', 'IN_SERVICE', 'OFFLINE'],
      default: 'AVAILABLE',
    },
    currentTokenId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Token',
      default: null,
    },
    servicesSupported: { type: [String], default: [] },
    isActive: { type: Boolean, default: true },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Counter', counterSchema);
