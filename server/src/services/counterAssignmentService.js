/**
 * Counter Assignment Service for QFlow
 *
 * Recommends the best available counter for a new token using a scoring system
 * that accounts for counter status, current workload, and predicted completion time.
 */

const { predictServiceDuration } = require('./predictionService');

/**
 * Recommend the best counter for a given service request.
 *
 * Scoring:
 *  - AVAILABLE counter with no token:  100 points (best)
 *  - AVAILABLE counter (general):       80 points
 *  - CALLING counter:                   50 points (about to start service)
 *  - IN_SERVICE counter:                30 points (adjusted by remaining time)
 *  - OFFLINE counter:                    0 points (excluded)
 *
 * Deductions:
 *  - Each token assigned to the counter: -5 points
 *  - Each minute of predicted remaining service time: -2 points
 *
 * @param {string} serviceName  - service being requested
 * @param {Array}  counters     - Counter documents (populated with currentTokenId)
 * @param {Array}  tokens       - All active Token documents
 * @returns {{ recommendedCounter: object|null, reason: string, score: number }}
 */
function recommendCounter(serviceName, counters, tokens) {
  const hour = new Date().getHours();

  const active = counters.filter((c) => c.isActive && c.status !== 'OFFLINE');

  if (active.length === 0) {
    return {
      recommendedCounter: null,
      reason: 'No active counters are currently available.',
      score: 0,
    };
  }

  let best = null;
  let bestScore = -Infinity;
  let bestReason = '';

  for (const counter of active) {
    let score = 0;
    let reason = '';

    // Base score by status
    if (counter.status === 'AVAILABLE' && !counter.currentTokenId) {
      score = 100;
      reason = `Counter ${counter.counterNumber} is fully available with no active token.`;
    } else if (counter.status === 'AVAILABLE') {
      score = 80;
      reason = `Counter ${counter.counterNumber} is available.`;
    } else if (counter.status === 'CALLING') {
      score = 50;
      reason = `Counter ${counter.counterNumber} is calling a customer and will be free soon.`;
    } else if (counter.status === 'IN_SERVICE') {
      score = 30;
      reason = `Counter ${counter.counterNumber} is currently serving a customer.`;
    }

    // Count tokens assigned to this counter (WAITING/CALLED/IN_SERVICE)
    const assignedTokens = tokens.filter(
      (t) =>
        t.counterId &&
        t.counterId.toString() === counter._id.toString() &&
        ['WAITING', 'CALLED', 'IN_SERVICE'].includes(t.status)
    );
    score -= assignedTokens.length * 5;

    // Deduct for remaining service time if IN_SERVICE
    if (counter.status === 'IN_SERVICE' && counter.currentTokenId) {
      const currentToken = tokens.find(
        (t) => t._id.toString() === counter.currentTokenId.toString()
      );
      if (currentToken && currentToken.startedAt) {
        const predicted = predictServiceDuration(currentToken.service, 0, hour);
        const elapsed =
          (Date.now() - new Date(currentToken.startedAt).getTime()) / 60000;
        const remaining = Math.max(0, predicted - elapsed);
        score -= remaining * 2;

        if (remaining > 0) {
          reason = `Counter ${counter.counterNumber} will be free in ~${Math.ceil(remaining)} min.`;
        }
      }
    }

    if (score > bestScore) {
      bestScore = score;
      best = counter;
      bestReason = reason;
    }
  }

  return {
    recommendedCounter: best,
    reason: bestReason || `Counter ${best?.counterNumber} recommended based on workload.`,
    score: bestScore,
  };
}

module.exports = { recommendCounter };
