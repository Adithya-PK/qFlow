const Counter = require('../models/Counter');
const Token = require('../models/Token');
const { emitCounterAdded, emitCounterUpdated } = require('../sockets/socketHandler');

/**
 * GET /api/counters
 * Returns all active counters with current token populated.
 */
async function getCounters(req, res, next) {
  try {
    const filter = req.query.activeOnly === 'true' ? { isActive: true } : {};
    const counters = await Counter.find(filter)
      .populate('currentTokenId', 'tokenNumber customerName service status')
      .sort({ counterNumber: 1 })
      .lean();

    return res.status(200).json({ success: true, count: counters.length, counters });
  } catch (err) {
    next(err);
  }
}

/**
 * GET /api/counters/:id
 * Returns a single counter with full token detail.
 */
async function getCounter(req, res, next) {
  try {
    const counter = await Counter.findById(req.params.id)
      .populate('currentTokenId', 'tokenNumber customerName service status startedAt')
      .lean();

    if (!counter) {
      return res.status(404).json({ success: false, message: 'Counter not found.' });
    }

    return res.status(200).json({ success: true, counter });
  } catch (err) {
    next(err);
  }
}

/**
 * POST /api/counters
 * Creates a new counter with auto-assigned counterNumber if omitted.
 */
async function createCounter(req, res, next) {
  try {
    let { counterNumber, staffName, servicesSupported } = req.body;

    if (!staffName || !staffName.trim()) {
      return res.status(400).json({
        success: false,
        message: 'staffName is required.',
      });
    }

    // Auto-assign counterNumber if not provided
    if (!counterNumber) {
      const highest = await Counter.findOne({}, { counterNumber: 1 }).sort({ counterNumber: -1 }).lean();
      counterNumber = highest ? highest.counterNumber + 1 : 1;
    }

    const existing = await Counter.findOne({ counterNumber });
    if (existing) {
      return res.status(409).json({
        success: false,
        message: `Counter number ${counterNumber} already exists.`,
      });
    }

    const counter = await Counter.create({
      counterNumber,
      staffName: staffName.trim(),
      servicesSupported: servicesSupported || [],
      status: 'AVAILABLE',
      isActive: true,
    });

    const io = req.app.get('io');
    emitCounterAdded(io, counter.toObject());

    return res.status(201).json({
      success: true,
      message: `Counter ${counterNumber} created successfully.`,
      counter,
    });
  } catch (err) {
    next(err);
  }
}

/**
 * POST /api/counters/:id/call-next
 * Finds the next waiting token in queue and calls it to this counter.
 */
async function callNext(req, res, next) {
  try {
    const counter = await Counter.findById(req.params.id);
    if (!counter) {
      return res.status(404).json({ success: false, message: 'Counter not found.' });
    }

    if (!counter.isActive || counter.status === 'OFFLINE') {
      return res.status(409).json({ success: false, message: 'Counter is offline or deactivated.' });
    }

    // Find the next WAITING token (FIFO)
    let nextToken = null;

    // First try supported services if defined
    if (counter.servicesSupported && counter.servicesSupported.length > 0) {
      nextToken = await Token.findOneAndUpdate(
        { status: 'WAITING', service: { $in: counter.servicesSupported } },
        {
          status: 'CALLED',
          calledAt: new Date(),
          counterId: counter._id,
        },
        { sort: { createdAt: 1 }, new: true }
      );
    }

    // Otherwise grab the oldest waiting token
    if (!nextToken) {
      nextToken = await Token.findOneAndUpdate(
        { status: 'WAITING' },
        {
          status: 'CALLED',
          calledAt: new Date(),
          counterId: counter._id,
        },
        { sort: { createdAt: 1 }, new: true }
      );
    }

    if (!nextToken) {
      return res.status(404).json({
        success: false,
        message: 'No customers are currently waiting in the queue.',
      });
    }

    // Update counter status
    counter.status = 'CALLING';
    counter.currentTokenId = nextToken._id;
    await counter.save();

    const populated = await Token.findById(nextToken._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const { emitTokenCalled } = require('../sockets/socketHandler');
    const io = req.app.get('io');
    emitTokenCalled(io, populated, counter.toObject());

    return res.status(200).json({
      success: true,
      message: `Called token ${nextToken.tokenNumber} to Counter ${counter.counterNumber}.`,
      token: populated,
      counter: counter.toObject(),
    });
  } catch (err) {
    next(err);
  }
}

/**
 * PUT /api/counters/:id
 * Updates counter details (staffName, servicesSupported, isActive, status).
 */
async function updateCounter(req, res, next) {
  try {
    const allowed = ['staffName', 'servicesSupported', 'isActive', 'status'];
    const updates = {};

    for (const key of allowed) {
      if (req.body[key] !== undefined) {
        updates[key] = req.body[key];
      }
    }

    if (Object.keys(updates).length === 0) {
      return res.status(400).json({ success: false, message: 'No valid fields provided for update.' });
    }

    // If reactivating, set status to AVAILABLE if was OFFLINE
    if (updates.isActive === true) {
      updates.status = updates.status || 'AVAILABLE';
    } else if (updates.isActive === false) {
      updates.status = 'OFFLINE';
      updates.currentTokenId = null;
    }

    const counter = await Counter.findByIdAndUpdate(
      req.params.id,
      { $set: updates },
      { new: true, runValidators: true }
    ).populate('currentTokenId', 'tokenNumber customerName service status');

    if (!counter) {
      return res.status(404).json({ success: false, message: 'Counter not found.' });
    }

    const io = req.app.get('io');
    emitCounterUpdated(io, counter.toObject());

    return res.status(200).json({
      success: true,
      message: 'Counter updated successfully.',
      counter,
    });
  } catch (err) {
    next(err);
  }
}

/**
 * DELETE /api/counters/:id
 * Soft-deletes a counter (sets isActive = false).
 */
async function deleteCounter(req, res, next) {
  try {
    const counter = await Counter.findById(req.params.id);
    if (!counter) {
      return res.status(404).json({ success: false, message: 'Counter not found.' });
    }

    counter.isActive = false;
    counter.status = 'OFFLINE';
    counter.currentTokenId = null;
    await counter.save();

    const io = req.app.get('io');
    emitCounterUpdated(io, counter.toObject());

    return res.status(200).json({
      success: true,
      message: `Counter ${counter.counterNumber} deactivated.`,
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  getCounters,
  getCounter,
  createCounter,
  callNext,
  updateCounter,
  deleteCounter,
};
