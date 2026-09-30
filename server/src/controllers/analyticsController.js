const Token = require('../models/Token');
const Counter = require('../models/Counter');

/**
 * GET /api/analytics
 * Returns comprehensive analytics for the admin dashboard.
 */
async function getAnalytics(req, res, next) {
  try {
    // Date range — default today; allow ?date=YYYY-MM-DD for historical
    let targetDate = req.query.date ? new Date(req.query.date) : new Date();
    const start = new Date(targetDate);
    start.setHours(0, 0, 0, 0);
    const end = new Date(targetDate);
    end.setHours(23, 59, 59, 999);

    const todayFilter = { createdAt: { $gte: start, $lte: end } };

    // --- Basic counts ---
    const [totalToday, waiting, inService, completed, skipped] = await Promise.all([
      Token.countDocuments(todayFilter),
      Token.countDocuments({ ...todayFilter, status: 'WAITING' }),
      Token.countDocuments({ ...todayFilter, status: 'IN_SERVICE' }),
      Token.countDocuments({ ...todayFilter, status: 'COMPLETED' }),
      Token.countDocuments({ ...todayFilter, status: 'SKIPPED' }),
    ]);

    // --- Average wait time (createdAt → calledAt) for completed tokens ---
    const waitTimeAgg = await Token.aggregate([
      {
        $match: {
          ...todayFilter,
          status: 'COMPLETED',
          calledAt: { $exists: true, $ne: null },
        },
      },
      {
        $project: {
          waitMinutes: {
            $divide: [{ $subtract: ['$calledAt', '$createdAt'] }, 60000],
          },
        },
      },
      { $group: { _id: null, avg: { $avg: '$waitMinutes' } } },
    ]);

    const averageWaitTime = waitTimeAgg[0]
      ? Math.round(waitTimeAgg[0].avg * 10) / 10
      : 0;

    // --- Average service duration ---
    const durationAgg = await Token.aggregate([
      {
        $match: {
          ...todayFilter,
          status: 'COMPLETED',
          actualDuration: { $exists: true, $ne: null },
        },
      },
      { $group: { _id: null, avg: { $avg: '$actualDuration' } } },
    ]);

    const averageServiceDuration = durationAgg[0]
      ? Math.round(durationAgg[0].avg * 10) / 10
      : 0;

    // --- Tokens by service ---
    const tokensByService = await Token.aggregate([
      { $match: todayFilter },
      { $group: { _id: '$service', count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $project: { _id: 0, service: '$_id', count: 1 } },
    ]);

    // --- Tokens by hour of day ---
    const tokensByHour = await Token.aggregate([
      { $match: todayFilter },
      {
        $group: {
          _id: { $hour: '$createdAt' },
          count: { $sum: 1 },
        },
      },
      { $sort: { _id: 1 } },
      { $project: { _id: 0, hour: '$_id', count: 1 } },
    ]);

    // --- Counter utilization ---
    const counters = await Counter.find({ isActive: true }).lean();

    const counterUtilization = await Promise.all(
      counters.map(async (c) => {
        const counterTodayFilter = {
          ...todayFilter,
          counterId: c._id,
        };

        const [totalHandled, completedCount, avgDurAgg] = await Promise.all([
          Token.countDocuments(counterTodayFilter),
          Token.countDocuments({ ...counterTodayFilter, status: 'COMPLETED' }),
          Token.aggregate([
            {
              $match: {
                ...counterTodayFilter,
                status: 'COMPLETED',
                actualDuration: { $exists: true, $ne: null },
              },
            },
            { $group: { _id: null, avg: { $avg: '$actualDuration' } } },
          ]),
        ]);

        return {
          counterId: c._id,
          counterNumber: c.counterNumber,
          staffName: c.staffName,
          status: c.status,
          totalHandled,
          completedCount,
          avgServiceDuration: avgDurAgg[0]
            ? Math.round(avgDurAgg[0].avg * 10) / 10
            : 0,
        };
      })
    );

    // --- Status distribution for pie chart ---
    const statusDistribution = await Token.aggregate([
      { $match: todayFilter },
      { $group: { _id: '$status', count: { $sum: 1 } } },
      { $project: { _id: 0, status: '$_id', count: 1 } },
    ]);

    return res.status(200).json({
      success: true,
      date: targetDate.toISOString().split('T')[0],
      summary: {
        totalToday,
        waiting,
        inService,
        completed,
        skipped,
        averageWaitTime,
        averageServiceDuration,
      },
      tokensByService,
      tokensByHour,
      counterUtilization,
      statusDistribution,
    });
  } catch (err) {
    next(err);
  }
}

module.exports = { getAnalytics };
