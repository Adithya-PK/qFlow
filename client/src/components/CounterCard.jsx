import { useState, useEffect } from 'react';
import { counterAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Monitor, User, Play, CheckCircle, SkipForward, ArrowRightLeft, ChevronDown, ChevronUp, Clock, Zap } from 'lucide-react';

const STATUS_CONFIG = {
  AVAILABLE: { label: 'AVAILABLE', color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/30', dot: 'bg-emerald-400' },
  CALLING: { label: 'CALLING', color: 'text-blue-400', bg: 'bg-blue-500/10 border-blue-500/30', dot: 'bg-blue-400' },
  IN_SERVICE: { label: 'IN SERVICE', color: 'text-indigo-400', bg: 'bg-indigo-500/10 border-indigo-500/30', dot: 'bg-indigo-400' },
  OFFLINE: { label: 'OFFLINE', color: 'text-gray-500', bg: 'bg-gray-500/10 border-gray-500/30', dot: 'bg-gray-500' },
};

const CounterCard = ({ 
  counter, 
  currentToken, 
  onCallNext, 
  onStart, 
  onComplete, 
  onSkip, 
  onTransfer, 
  onDeactivate,
  loading,
  queue = [],
  showAllActions = false
}) => {
  const [expanded, setExpanded] = useState(false);
  const [currentTime, setCurrentTime] = useState(Date.now());
  
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatElapsed = (startTime) => {
    if (!startTime) return '00:00';
    const diffSec = Math.max(0, Math.floor((currentTime - new Date(startTime).getTime()) / 1000));
    const mins = Math.floor(diffSec / 60);
    const secs = diffSec % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };
  
  const statusConf = STATUS_CONFIG[counter.status] || STATUS_CONFIG.OFFLINE;
  const waitingCount = queue.filter(t => t.status === 'WAITING').length;
  const canCallNext = counter.status === 'AVAILABLE' && waitingCount > 0;

  const isLoading = !!loading;
  const loadingType = typeof loading === 'string' ? loading : null;

  return (
    <div className={`card border ${statusConf.bg} flex flex-col gap-4 relative overflow-hidden`}>
      {/* Status glow line */}
      <div className={`absolute top-0 left-0 right-0 h-0.5 ${statusConf.dot}`}></div>
      
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${statusConf.bg} border`}>
            <Monitor size={18} className={statusConf.color} />
          </div>
          <div>
            <h3 className="text-white font-bold text-lg">Counter {counter.counterNumber}</h3>
            <div className="flex items-center gap-1.5">
              <div className={`w-2 h-2 rounded-full ${statusConf.dot} ${counter.status === 'IN_SERVICE' || counter.status === 'CALLING' ? 'animate-pulse' : ''}`}></div>
              <span className={`text-xs font-semibold ${statusConf.color}`}>{statusConf.label}</span>
            </div>
          </div>
        </div>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-gray-500 hover:text-gray-300 transition-colors p-1"
        >
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>

      {/* Staff */}
      <div className="flex items-center gap-2">
        <div className="w-7 h-7 bg-gray-700 rounded-full flex items-center justify-center">
          <User size={14} className="text-gray-400" />
        </div>
        <span className="text-gray-300 font-medium">{counter.staffName}</span>
      </div>

      {/* Current Token */}
      {currentToken ? (
        <div className="bg-gray-800/50 rounded-xl p-3 border border-gray-700/50">
          <p className="text-gray-500 text-xs mb-1">Now Serving</p>
          <div className="flex items-center justify-between">
            <span className="text-indigo-400 font-black text-2xl">{currentToken.tokenNumber}</span>
            <span className="text-gray-400 text-xs text-right">{currentToken.service}</span>
          </div>
          <p className="text-gray-300 text-sm mt-1">{currentToken.customerName}</p>
          <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-700/40">
            {currentToken.startedAt ? (
              <div className="flex items-center gap-1 text-emerald-400 font-mono text-xs">
                <Clock size={11} className="animate-spin" />
                <span>Elapsed: <strong>{formatElapsed(currentToken.startedAt)}</strong></span>
              </div>
            ) : currentToken.calledAt ? (
              <div className="flex items-center gap-1 text-blue-400 font-mono text-xs">
                <Clock size={11} />
                <span>Called: <strong>{formatElapsed(currentToken.calledAt)}</strong> ago</span>
              </div>
            ) : (
              <span className="text-gray-500 text-xs font-mono">{currentToken.status}</span>
            )}
            {currentToken.predictedDuration && (
              <div className="flex items-center gap-1">
                <Zap size={11} className="text-indigo-400" />
                <span className="text-gray-400 text-xs">AI: {currentToken.predictedDuration}m</span>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-gray-800/30 rounded-xl p-3 border border-gray-700/30 text-center">
          <p className="text-gray-600 text-sm">No active token</p>
        </div>
      )}

      {/* Queue stats */}
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <Clock size={12} />
        <span>{waitingCount} waiting in queue</span>
      </div>

      {/* Actions */}
      <div className="space-y-2">
        {/* Call Next */}
        {counter.status === 'AVAILABLE' && (
          <button
            onClick={onCallNext}
            disabled={!canCallNext || isLoading}
            className={`w-full py-2.5 rounded-lg font-semibold text-sm transition-all flex items-center justify-center gap-2
              ${canCallNext && !isLoading
                ? 'bg-indigo-600 hover:bg-indigo-500 text-white active:scale-95'
                : 'bg-gray-800 text-gray-600 cursor-not-allowed'
              }`}
          >
            {loadingType === 'calling' ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Play size={15} fill="currentColor" />
                {canCallNext ? 'Call Next' : 'Queue Empty'}
              </>
            )}
          </button>
        )}

        {/* Start Service */}
        {counter.status === 'CALLING' && currentToken && (
          <button
            onClick={onStart}
            disabled={isLoading}
            className="w-full py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
          >
            {loadingType === 'start' ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Play size={15} />
                Start Service
              </>
            )}
          </button>
        )}

        {/* Complete Service */}
        {counter.status === 'IN_SERVICE' && currentToken && (
          <button
            onClick={onComplete}
            disabled={isLoading}
            className="w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
          >
            {loadingType === 'complete' ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <CheckCircle size={15} />
                Complete Service
              </>
            )}
          </button>
        )}

        {/* Expanded actions */}
        {expanded && currentToken && ['CALLING', 'IN_SERVICE'].includes(counter.status) && (
          <div className="flex gap-2 pt-1">
            <button
              onClick={onSkip}
              disabled={isLoading}
              className="flex-1 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white font-medium text-xs transition-all flex items-center justify-center gap-1 disabled:opacity-50"
            >
              <SkipForward size={13} />
              Skip
            </button>
            {onTransfer && (
              <button
                onClick={onTransfer}
                disabled={isLoading}
                className="flex-1 py-2 rounded-lg bg-purple-700 hover:bg-purple-600 text-white font-medium text-xs transition-all flex items-center justify-center gap-1 disabled:opacity-50"
              >
                <ArrowRightLeft size={13} />
                Transfer
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CounterCard;
