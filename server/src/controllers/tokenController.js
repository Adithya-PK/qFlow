const mongoose = require('mongoose');
const Token = require('../models/Token');
const Counter = require('../models/Counter');
const { predictServiceDuration, calculateEstimatedWait } = require('../services/predictionService');
const { recommendCounter } = require('../services/counterAssignmentService');
const {
  emitTokenCreated,
  emitTokenCalled,
  emitServiceStarted,
  emitServiceCompleted,
  emitTokenSkipped,
  emitTokenTransferred,
  emitQueueUpdated,
} = require('../sockets/socketHandler');

// ---------------------------------------------------------------------------
// Helper: get today's date range (midnight to midnight)
// ---------------------------------------------------------------------------
function getTodayRange() {
  const start = new Date();
  start.setHours(0, 0, 0, 0);
  const end = new Date();
  end.setHours(23, 59, 59, 999);
  return { start, end };
}

// ---------------------------------------------------------------------------
// Helper: generate atomic token number (A101, A102, ...)
// ---------------------------------------------------------------------------
async function generateTokenNumber() {
  // Find highest numerical token sequence in DB to guarantee unique sequential token
  const allTokens = await Token.find({}, { tokenNumber: 1 }).lean();
  let maxSeq = 100;
  for (const t of allTokens) {
    const match = t.tokenNumber && t.tokenNumber.match(/^[A-Z](\d+)$/);
    if (match) {
      const seq = parseInt(match[1], 10);
      if (seq > maxSeq) maxSeq = seq;
    }
  }
  return `A${maxSeq + 1}`;
}

// ---------------------------------------------------------------------------
// Helper: build current active queue snapshot
// ---------------------------------------------------------------------------
async function getActiveQueue() {
  return Token.find({ status: { $in: ['WAITING', 'CALLED', 'IN_SERVICE'] } })
    .populate('counterId', 'counterNumber staffName status')
    .sort({ createdAt: 1 })
    .lean();
}

// ---------------------------------------------------------------------------
// POST /api/tokens
// ---------------------------------------------------------------------------
async function createToken(req, res, next) {
  try {
    const { customerName, phone, service, notes } = req.body;

    if (!customerName || !phone || !service) {
      return res.status(400).json({
        success: false,
        message: 'customerName, phone, and service are required.',
      });
    }

    const hour = new Date().getHours();

    // Fetch active counters and current queue
    const counters = await Counter.find({ isActive: true }).lean();
    const activeTokens = await Token.find({
      status: { $in: ['WAITING', 'CALLED', 'IN_SERVICE'] },
    }).lean();

    const peopleAhead = activeTokens.filter((t) => t.status === 'WAITING').length;

    // AI predictions
    const predictedDuration = predictServiceDuration(service, peopleAhead, hour);
    const estimatedWait = calculateEstimatedWait(service, peopleAhead, hour, counters, activeTokens);

    // Counter recommendation
    const { recommendedCounter, reason } = recommendCounter(service, counters, activeTokens);

    // Generate unique token number (atomic within same process — race condition window is negligible)
    const tokenNumber = await generateTokenNumber();

    const token = await Token.create({
      tokenNumber,
      customerName,
      phone,
      service,
      status: 'WAITING',
      predictedDuration,
      estimatedWait,
      peopleAhead,
      counterId: recommendedCounter ? recommendedCounter._id : null,
      notes: notes || '',
    });

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    // Emit socket event with updated queue
    const io = req.app.get('io');
    const updatedQueue = await getActiveQueue();
    emitTokenCreated(io, populated, updatedQueue);

    return res.status(201).json({
      success: true,
      message: 'Token created successfully.',
      token: populated,
      recommendation: {
        counter: recommendedCounter
          ? { counterNumber: recommendedCounter.counterNumber, staffName: recommendedCounter.staffName }
          : null,
        reason,
      },
    });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// GET /api/tokens
// ---------------------------------------------------------------------------
async function getTokens(req, res, next) {
  try {
    const { start, end } = getTodayRange();
    const { status } = req.query;

    const filter = { createdAt: { $gte: start, $lte: end } };
    if (status) filter.status = status;

    const tokens = await Token.find(filter)
      .populate('counterId', 'counterNumber staffName status')
      .sort({ createdAt: -1 })
      .lean();

    return res.status(200).json({ success: true, count: tokens.length, tokens });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// GET /api/tokens/:id
// ---------------------------------------------------------------------------
async function getToken(req, res, next) {
  try {
    const token = await Token.findById(req.params.id)
      .populate('counterId', 'counterNumber staffName status')
      .populate('transferHistory', 'counterNumber staffName')
      .lean();

    if (!token) {
      return res.status(404).json({ success: false, message: 'Token not found.' });
    }

    return res.status(200).json({ success: true, token });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// POST /api/tokens/:id/call
// ---------------------------------------------------------------------------
async function callToken(req, res, next) {
  try {
    const { counterId } = req.body;

    if (!counterId) {
      return res.status(400).json({ success: false, message: 'counterId is required.' });
    }

    const counter = await Counter.findById(counterId);
    if (!counter) {
      return res.status(404).json({ success: false, message: 'Counter not found.' });
    }

    if (!counter.isActive || counter.status === 'OFFLINE') {
      return res.status(409).json({ success: false, message: 'Counter is offline or inactive.' });
    }

    // Atomically claim the token only if it is in WAITING status (concurrency safe)
    const token = await Token.findOneAndUpdate(
      { _id: req.params.id, status: 'WAITING' },
      {
        status: 'CALLED',
        calledAt: new Date(),
        counterId: counter._id,
      },
      { new: true }
    );

    if (!token) {
      const existingToken = await Token.findById(req.params.id);
      if (!existingToken) {
        return res.status(404).json({ success: false, message: 'Token not found.' });
      }
      return res.status(409).json({
        success: false,
        message: `Token is currently ${existingToken.status} — cannot call it again.`,
      });
    }

    // Update counter
    counter.status = 'CALLING';
    counter.currentTokenId = token._id;
    await counter.save();

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const io = req.app.get('io');
    emitTokenCalled(io, populated, counter.toObject());

    return res.status(200).json({
      success: true,
      message: `Token ${token.tokenNumber} called to Counter ${counter.counterNumber}.`,
      token: populated,
      counter: counter.toObject(),
    });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// POST /api/tokens/:id/start
// ---------------------------------------------------------------------------
async function startService(req, res, next) {
  try {
    const token = await Token.findById(req.params.id);
    if (!token) {
      return res.status(404).json({ success: false, message: 'Token not found.' });
    }

    if (token.status !== 'CALLED') {
      return res.status(409).json({
        success: false,
        message: `Token must be in CALLED status to start service. Current: ${token.status}`,
      });
    }

    token.status = 'IN_SERVICE';
    token.startedAt = new Date();
    await token.save();

    // Update counter status
    if (token.counterId) {
      await Counter.findByIdAndUpdate(token.counterId, { status: 'IN_SERVICE' });
    }

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const counter = token.counterId
      ? await Counter.findById(token.counterId).lean()
      : null;

    const io = req.app.get('io');
    emitServiceStarted(io, populated, counter);

    return res.status(200).json({
      success: true,
      message: `Service started for token ${token.tokenNumber}.`,
      token: populated,
    });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// POST /api/tokens/:id/complete
// ---------------------------------------------------------------------------
async function completeService(req, res, next) {
  try {
    const token = await Token.findById(req.params.id);
    if (!token) {
      return res.status(404).json({ success: false, message: 'Token not found.' });
    }

    if (token.status !== 'IN_SERVICE') {
      return res.status(409).json({
        success: false,
        message: `Token must be IN_SERVICE to complete. Current: ${token.status}`,
      });
    }

    const completedAt = new Date();
    const startTime = token.startedAt ? new Date(token.startedAt) : (token.calledAt ? new Date(token.calledAt) : new Date(token.createdAt));
    const elapsedMinutes = Math.max(1, Math.round(((completedAt - startTime) / 60000) * 10) / 10);

    token.status = 'COMPLETED';
    token.completedAt = completedAt;
    token.actualDuration = elapsedMinutes;
    await token.save();

    // Free the counter
    let counter = null;
    if (token.counterId) {
      counter = await Counter.findByIdAndUpdate(
        token.counterId,
        { status: 'AVAILABLE', currentTokenId: null },
        { new: true }
      ).lean();
    }

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const io = req.app.get('io');
    emitServiceCompleted(io, populated, counter);

    const updatedQueue = await getActiveQueue();
    emitQueueUpdated(io, updatedQueue);

    return res.status(200).json({
      success: true,
      message: `Token ${token.tokenNumber} completed. Duration: ${elapsedMinutes} min.`,
      token: populated,
    });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// POST /api/tokens/:id/skip
// ---------------------------------------------------------------------------
async function skipToken(req, res, next) {
  try {
    const token = await Token.findById(req.params.id);
    if (!token) {
      return res.status(404).json({ success: false, message: 'Token not found.' });
    }

    if (!['WAITING', 'CALLED'].includes(token.status)) {
      return res.status(409).json({
        success: false,
        message: `Cannot skip token with status ${token.status}.`,
      });
    }

    // Free counter if assigned
    if (token.counterId) {
      await Counter.findByIdAndUpdate(token.counterId, {
        status: 'AVAILABLE',
        currentTokenId: null,
      });
    }

    token.status = 'SKIPPED';
    token.skippedAt = new Date();
    await token.save();

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const io = req.app.get('io');
    emitTokenSkipped(io, populated);

    const updatedQueue = await getActiveQueue();
    emitQueueUpdated(io, updatedQueue);

    return res.status(200).json({
      success: true,
      message: `Token ${token.tokenNumber} has been skipped.`,
      token: populated,
    });
  } catch (err) {
    next(err);
  }
}

// ---------------------------------------------------------------------------
// POST /api/tokens/:id/transfer
// ---------------------------------------------------------------------------
async function transferToken(req, res, next) {
  try {
    const { targetCounterId } = req.body;

    if (!targetCounterId) {
      return res.status(400).json({ success: false, message: 'targetCounterId is required.' });
    }

    const token = await Token.findById(req.params.id);
    if (!token) {
      return res.status(404).json({ success: false, message: 'Token not found.' });
    }

    if (!['WAITING', 'CALLED'].includes(token.status)) {
      return res.status(409).json({
        success: false,
        message: `Cannot transfer token with status ${token.status}.`,
      });
    }

    const targetCounter = await Counter.findById(targetCounterId);
    if (!targetCounter) {
      return res.status(404).json({ success: false, message: 'Target counter not found.' });
    }

    if (!targetCounter.isActive || targetCounter.status === 'OFFLINE') {
      return res.status(409).json({
        success: false,
        message: 'Target counter is offline or inactive.',
      });
    }

    // Free old counter
    let oldCounter = null;
    if (token.counterId) {
      oldCounter = await Counter.findByIdAndUpdate(
        token.counterId,
        { status: 'AVAILABLE', currentTokenId: null },
        { new: true }
      ).lean();

      // Track transfer history
      token.transferHistory.push(token.counterId);
    }

    token.transferredAt = new Date();

    // If token was CALLED, keep it CALLED on the new counter; otherwise WAITING
    if (token.status === 'CALLED') {
      targetCounter.status = 'CALLING';
      targetCounter.currentTokenId = token._id;
      token.status = 'CALLED';
      token.calledAt = new Date();
    }

    token.counterId = targetCounter._id;
    await token.save();
    await targetCounter.save();

    const populated = await Token.findById(token._id)
      .populate('counterId', 'counterNumber staffName status')
      .lean();

    const io = req.app.get('io');
    emitTokenTransferred(io, populated, oldCounter, targetCounter.toObject());

    return res.status(200).json({
      success: true,
      message: `Token ${token.tokenNumber} transferred to Counter ${targetCounter.counterNumber}.`,
      token: populated,
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  createToken,
  getTokens,
  getToken,
  callToken,
  startService,
  completeService,
  skipToken,
  transferToken,
};
