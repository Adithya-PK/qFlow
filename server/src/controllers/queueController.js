const Token = require('../models/Token');
const Counter = require('../models/Counter');
const { predictServiceDuration } = require('../services/predictionService');

/**
 * GET /api/queue
 * Returns the current live queue: all WAITING, CALLED, IN_SERVICE tokens.
 * Includes populated counter data and real-time wait estimates.
 */
async function getQueue(req, res, next) {
  try {
    const hour = new Date().getHours();

    const queue = await Token.find({
      status: { $in: ['WAITING', 'CALLED', 'IN_SERVICE'] },
    })
      .populate('counterId', 'counterNumber staffName status')
      .sort({ createdAt: 1 })
      .lean();

    // Enrich each waiting token with live position and wait estimate
    let waitingPosition = 0;
    const enriched = queue.map((token) => {
      if (token.status === 'WAITING') {
        waitingPosition++;
        const estWait = waitingPosition * predictServiceDuration(token.service, waitingPosition, hour);
        return { ...token, livePosition: waitingPosition, liveEstimatedWait: estWait };
      }
      return { ...token, livePosition: 0, liveEstimatedWait: 0 };
    });

    return res.status(200).json({
      success: true,
      count: queue.length,
      waitingCount: queue.filter((t) => t.status === 'WAITING').length,
      calledCount: queue.filter((t) => t.status === 'CALLED').length,
      inServiceCount: queue.filter((t) => t.status === 'IN_SERVICE').length,
      queue: enriched,
    });
  } catch (err) {
    next(err);
  }
}

module.exports = { getQueue };
