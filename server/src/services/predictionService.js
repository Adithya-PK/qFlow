/**
 * Lightweight AI Prediction Service for QFlow
 *
 * Uses a weighted-average approach over a synthetically generated historical
 * dataset (500 records) to predict service durations and estimated wait times.
 * The dataset is generated once at module load and cached in memory.
 */

// ---------------------------------------------------------------------------
// Service base configurations
// ---------------------------------------------------------------------------
const SERVICE_CONFIG = {
  'Account Service':        { base: 8,  variance: 4 },
  'Payment Service':        { base: 10, variance: 5 },
  'Document Verification':  { base: 15, variance: 7 },
  'Customer Support':       { base: 7,  variance: 3 },
  'General Enquiry':        { base: 5,  variance: 2 },
};

// Peak hours add up to 3 extra minutes
const PEAK_HOURS = new Set([9, 10, 11, 14, 15, 16]);

// ---------------------------------------------------------------------------
// Seeded pseudo-random for reproducible dataset (Mulberry32)
// ---------------------------------------------------------------------------
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------------------------------------------------------------------------
// Generate 500 synthetic historical records
// ---------------------------------------------------------------------------
function generateSyntheticDataset(count = 500) {
  const rand = mulberry32(42); // fixed seed for reproducibility
  const serviceNames = Object.keys(SERVICE_CONFIG);
  const records = [];

  for (let i = 0; i < count; i++) {
    const serviceName = serviceNames[Math.floor(rand() * serviceNames.length)];
    const { base, variance } = SERVICE_CONFIG[serviceName];

    // Business hours 8-18
    const hour = 8 + Math.floor(rand() * 10);

    // Queue length between 0 and 20
    const queueLength = Math.floor(rand() * 21);

    // Hour factor: peak hours add 0-3 min
    const hourFactor = PEAK_HOURS.has(hour) ? rand() * 3 : 0;

    // Queue factor: each extra person adds ~0.05 min distraction
    const queueFactor = queueLength * 0.05;

    // Actual duration
    const duration = Math.max(
      1,
      Math.round(base + rand() * variance + hourFactor + queueFactor)
    );

    records.push({ serviceName, hour, queueLength, duration });
  }

  return records;
}

// Module-level cached dataset — generated once
const SYNTHETIC_DATA = generateSyntheticDataset(500);

// ---------------------------------------------------------------------------
// Prediction helpers
// ---------------------------------------------------------------------------

/**
 * Predict service duration in minutes.
 * @param {string} serviceName
 * @param {number} queueLength - current people ahead
 * @param {number} hour        - current hour (0-23)
 * @returns {number} predicted duration in minutes
 */
function predictServiceDuration(serviceName, queueLength, hour) {
  // Filter records for this service
  const relevant = SYNTHETIC_DATA.filter((r) => r.serviceName === serviceName);

  if (relevant.length === 0) {
    // Fallback: use base config or generic default
    const cfg = SERVICE_CONFIG[serviceName];
    return cfg ? cfg.base : 10;
  }

  // Weighted average:
  // - Records with matching hour get weight 2x
  // - All others get weight 1x
  let totalWeight = 0;
  let weightedSum = 0;

  for (const r of relevant) {
    const weight = r.hour === hour ? 2 : 1;
    weightedSum += r.duration * weight;
    totalWeight += weight;
  }

  const basePrediction = weightedSum / totalWeight;

  // Apply current context adjustments
  const hourAdj = PEAK_HOURS.has(hour) ? 1.5 : 0;
  const queueAdj = queueLength * 0.05;

  return Math.max(1, Math.round(basePrediction + hourAdj + queueAdj));
}

/**
 * Calculate estimated wait time for a new token.
 *
 * @param {string}   serviceName  - service being requested
 * @param {number}   queueLength  - tokens ahead of this new token
 * @param {number}   hour         - current hour
 * @param {Array}    counters     - active Counter documents
 * @param {Array}    tokens       - active Token documents (WAITING / CALLED / IN_SERVICE)
 * @returns {number} estimated wait in minutes
 */
function calculateEstimatedWait(serviceName, queueLength, hour, counters, tokens) {
  const activeCounters = counters.filter(
    (c) => c.isActive && c.status !== 'OFFLINE'
  );

  if (activeCounters.length === 0) {
    // No counters available — rough linear estimate
    const duration = predictServiceDuration(serviceName, queueLength, hour);
    return queueLength * duration;
  }

  // Tokens that are currently being served or about to be served
  const inProgress = tokens.filter(
    (t) => t.status === 'IN_SERVICE' || t.status === 'CALLED'
  );

  // Tokens still waiting ahead
  const waiting = tokens.filter((t) => t.status === 'WAITING');

  // Estimate remaining time for in-progress tokens
  let remainingInProgress = 0;
  for (const t of inProgress) {
    const predicted = predictServiceDuration(t.service, 0, hour);
    if (t.startedAt) {
      const elapsed = (Date.now() - new Date(t.startedAt).getTime()) / 60000;
      remainingInProgress += Math.max(0, predicted - elapsed);
    } else {
      remainingInProgress += predicted;
    }
  }

  // Estimate total duration for waiting tokens
  let waitingTotal = 0;
  for (const t of waiting) {
    waitingTotal += predictServiceDuration(t.service, 0, hour);
  }

  // Distribute load across available counters
  const totalWork = remainingInProgress + waitingTotal;
  const perCounterWork = totalWork / activeCounters.length;

  return Math.max(0, Math.round(perCounterWork));
}

module.exports = { predictServiceDuration, calculateEstimatedWait, SYNTHETIC_DATA };
