import { Zap, Monitor, Clock, Users } from 'lucide-react';

const AIRecommendation = ({ counters, queue }) => {
  const waitingTokens = queue.filter(t => t.status === 'WAITING');
  
  if (waitingTokens.length === 0) return null;

  const nextToken = waitingTokens[0]; // FIFO

  // Find best counter using simple scoring
  const availableCounters = counters.filter(c => c.isActive !== false && c.status === 'AVAILABLE');
  const callingCounters = counters.filter(c => c.isActive !== false && c.status === 'CALLING');
  const inServiceCounters = counters.filter(c => c.isActive !== false && c.status === 'IN_SERVICE');

  let recommendation = null;
  let reason = '';
  let confidence = 'high';

  if (availableCounters.length > 0) {
    // Pick available counter with fewest recent tokens (simple heuristic)
    recommendation = availableCounters[0];
    reason = `Counter ${recommendation.counterNumber} is currently available with no active service — optimal choice for immediate service.`;
    confidence = 'high';
  } else if (callingCounters.length === 0 && inServiceCounters.length > 0) {
    // All counters in service - suggest one that will finish soon
    const counterWithToken = inServiceCounters.find(c => c.currentTokenId?.predictedDuration);
    recommendation = counterWithToken || inServiceCounters[0];
    reason = `All counters are busy. Counter ${recommendation?.counterNumber} is estimated to complete soon based on predicted service duration.`;
    confidence = 'medium';
  } else {
    recommendation = counters.find(c => c.isActive !== false);
    reason = 'All counters are currently busy. The next available counter will be recommended automatically.';
    confidence = 'low';
  }

  const confidenceColor = {
    high: 'text-emerald-400',
    medium: 'text-amber-400',
    low: 'text-red-400',
  }[confidence];

  return (
    <div className="bg-indigo-500/5 border border-indigo-500/30 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-7 h-7 bg-indigo-600/30 rounded-lg flex items-center justify-center">
          <Zap size={14} className="text-indigo-400" />
        </div>
        <span className="text-indigo-400 font-semibold text-sm uppercase tracking-wider">AI Counter Recommendation</span>
        <span className={`ml-auto text-xs font-semibold ${confidenceColor} uppercase`}>
          {confidence} confidence
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Next Token */}
        <div className="bg-gray-800/50 rounded-xl p-3 border border-gray-700/50">
          <p className="text-gray-500 text-xs mb-1 flex items-center gap-1">
            <Users size={11} />
            Next Token
          </p>
          <p className="text-indigo-400 font-black text-xl">{nextToken?.tokenNumber}</p>
          <p className="text-gray-400 text-xs">{nextToken?.customerName}</p>
          <p className="text-gray-500 text-xs">{nextToken?.service}</p>
        </div>

        {/* Recommended Counter */}
        <div className="bg-gray-800/50 rounded-xl p-3 border border-gray-700/50">
          <p className="text-gray-500 text-xs mb-1 flex items-center gap-1">
            <Monitor size={11} />
            Recommended Counter
          </p>
          {recommendation ? (
            <>
              <p className="text-white font-bold text-xl">Counter {recommendation.counterNumber}</p>
              <p className="text-gray-400 text-xs">{recommendation.staffName}</p>
              <span className={`text-xs font-semibold ${recommendation.status === 'AVAILABLE' ? 'text-emerald-400' : 'text-amber-400'}`}>
                {recommendation.status?.replace('_', ' ')}
              </span>
            </>
          ) : (
            <p className="text-gray-500 text-sm">No counters available</p>
          )}
        </div>

        {/* Prediction */}
        <div className="bg-gray-800/50 rounded-xl p-3 border border-gray-700/50">
          <p className="text-gray-500 text-xs mb-1 flex items-center gap-1">
            <Clock size={11} />
            AI Prediction
          </p>
          <p className="text-purple-400 font-bold text-xl">
            {nextToken?.predictedDuration != null ? `${nextToken.predictedDuration} min` : '—'}
          </p>
          <p className="text-gray-500 text-xs">Predicted service duration</p>
          {nextToken?.estimatedWait != null && (
            <p className="text-gray-400 text-xs mt-1">
              Est. wait: {nextToken.estimatedWait} min
            </p>
          )}
        </div>
      </div>

      {/* Reason */}
      <div className="mt-3 p-3 bg-gray-800/30 rounded-lg">
        <p className="text-gray-400 text-xs">
          <span className="text-indigo-400 font-semibold">Reason: </span>
          {reason}
        </p>
      </div>

      <p className="text-gray-600 text-xs mt-2">
        ⚡ AI recommendation based on counter availability, queue workload, and predicted service duration.
        Prototype uses synthetic historical data.
      </p>
    </div>
  );
};

export default AIRecommendation;
