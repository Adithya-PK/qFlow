const mongoose = require('mongoose');

const serviceSchema = new mongoose.Schema({
  name: { type: String, required: true },
  code: { type: String, required: true, unique: true, uppercase: true, trim: true },
  averageDuration: { type: Number, default: 10 }, // minutes
  active: { type: Boolean, default: true },
  description: { type: String, default: '' },
});

module.exports = mongoose.model('Service', serviceSchema);
