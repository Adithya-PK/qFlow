import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { tokenAPI, counterAPI } from '../../services/api';
import { connectSocket, SOCKET_EVENTS } from '../../services/socket';
import { Zap, Clock, Users, Monitor, CheckCircle, AlertTriangle, Wifi, WifiOff, Bell, ArrowLeft, RefreshCw } from 'lucide-react';

const STATUS_CONFIG = {
  WAITING: {
    label: 'WAITING',
    sublabel: 'Please wait for your turn',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10 border-amber-500/30',
    icon: Clock,
    glow: 'glow-amber',
  },
  CALLED: {
    label: 'YOUR TURN!',
    sublabel: 'Please proceed to the counter',
    color: 'text-blue-400',
    bg: 'bg-blue-500/20 border-blue-500/50',
    icon: Bell,
    glow: 'shadow-2xl shadow-blue-500/50',
    pulse: true,
  },
  IN_SERVICE: {
    label: 'IN SERVICE',
    sublabel: 'Your service is in progress',
    color: 'text-indigo-400',
    bg: 'bg-indigo-500/10 border-indigo-500/30',
    icon: Monitor,
    glow: 'glow-indigo',
  },
  COMPLETED: {
    label: 'COMPLETED',
    sublabel: 'Thank you for visiting!',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10 border-emerald-500/30',
    icon: CheckCircle,
    glow: 'glow-green',
  },
  SKIPPED: {
    label: 'SKIPPED',
    sublabel: 'Your token was skipped. Please visit the counter.',
    color: 'text-gray-400',
    bg: 'bg-gray-500/10 border-gray-500/30',
    icon: AlertTriangle,
    glow: '',
  },
  TRANSFERRED: {
    label: 'TRANSFERRED',
    sublabel: 'Your token has been transferred to another counter',
    color: 'text-purple-400',
    bg: 'bg-purple-500/10 border-purple-500/30',
    icon: Monitor,
    glow: '',
  },
};

const COUNTER_STATUS_COLORS = {
  AVAILABLE: 'text-emerald-400',
  CALLING: 'text-blue-400',
  IN_SERVICE: 'text-indigo-400',
  OFFLINE: 'text-gray-500',
};

const COUNTER_STATUS_BG = {
  AVAILABLE: 'bg-emerald-500/10 border-emerald-500/20',
  CALLING: 'bg-blue-500/10 border-blue-500/20',
  IN_SERVICE: 'bg-indigo-500/10 border-indigo-500/20',
  OFFLINE: 'bg-gray-800/50 border-gray-700',
};

const TokenStatus = () => {
  const { tokenId } = useParams();
  const [token, setToken] = useState(null);
  const [counters, setCounters] = useState([]);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [currentTime, setCurrentTime] = useState(Date.now());
  const prevStatusRef = useRef(null);

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

  const fetchToken = useCallback(async () => {
    try {
      const response = await tokenAPI.getById(tokenId);
      setToken(response.data.token || response.data);
      setError(null);
    } catch (err) {
      setError('Could not load token. Please check your connection.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [tokenId]);

  const fetchCounters = useCallback(async () => {
    try {
      const response = await counterAPI.getAll();
      setCounters(response.data.counters || response.data || []);
    } catch (err) {
      console.error('Failed to fetch counters:', err);
    }
  }, []);

  // Play notification sound / vibrate / popup on status change
  const notifyStatusChange = useCallback((newStatus, counter) => {
    if ('vibrate' in navigator) {
      if (newStatus === 'CALLED') {
        navigator.vibrate([200, 100, 200, 100, 200]);
      } else {
        navigator.vibrate(100);
      }
    }
    try {
      if ('Notification' in window && Notification.permission === 'granted' && newStatus === 'CALLED') {
        const counterText = counter?.counterNumber ? `Counter ${counter.counterNumber}` : 'the counter';
        new Notification('🔔 YOUR TURN! — QFlow', {
          body: `Your token has been called to ${counterText}! Please proceed immediately.`,
          requireInteraction: true,
        });
      }
    } catch (err) {
      console.warn('Browser notification skipped:', err);
    }
  }, []);

  useEffect(() => {
    // Politeness request for notification permission
    if (typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission().catch(() => {});
    }
  }, []);

  useEffect(() => {
    fetchToken();
    fetchCounters();

    const socket = connectSocket();
    setConnected(socket.connected);

    socket.on(SOCKET_EVENTS.CONNECT, () => {
      setConnected(true);
      fetchToken(); // Resync on reconnect
    });
    socket.on(SOCKET_EVENTS.DISCONNECT, () => setConnected(false));

    // Listen for this specific token's events
    socket.emit(SOCKET_EVENTS.JOIN_TOKEN, { tokenId });

    const handleTokenUpdate = (data) => {
      const updatedToken = data.token;
      if (!updatedToken || updatedToken._id !== tokenId) return;
      
      setToken(prev => {
        if (prev && prev.status !== updatedToken.status) {
          notifyStatusChange(updatedToken.status, data.counter);
        }
        return { ...prev, ...updatedToken };
      });
    };

    socket.on(SOCKET_EVENTS.TOKEN_CALLED, handleTokenUpdate);
    socket.on('yourTurn', handleTokenUpdate); // Backend also emits 'yourTurn' on token-specific room
    socket.on(SOCKET_EVENTS.SERVICE_STARTED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.SERVICE_COMPLETED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.TOKEN_SKIPPED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.TOKEN_TRANSFERRED, handleTokenUpdate);

    // Counter updates
    socket.on(SOCKET_EVENTS.COUNTER_UPDATED, ({ counter }) => {
      setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
    });
    socket.on(SOCKET_EVENTS.COUNTER_ADDED, ({ counter }) => {
      setCounters(prev => {
        const exists = prev.find(c => c._id === counter._id);
        return exists ? prev : [...prev, counter];
      });
    });

    // Queue update for people-ahead recalculation
    socket.on(SOCKET_EVENTS.QUEUE_UPDATED, () => fetchToken());
    socket.on(SOCKET_EVENTS.TOKEN_CREATED, () => fetchToken());
    socket.on(SOCKET_EVENTS.SERVICE_COMPLETED, () => {
      handleTokenUpdate({ token: { _id: tokenId } });
      fetchToken(); // Recalculate people ahead
    });

    return () => {
      socket.off(SOCKET_EVENTS.CONNECT);
      socket.off(SOCKET_EVENTS.DISCONNECT);
      socket.off(SOCKET_EVENTS.TOKEN_CALLED);
      socket.off(SOCKET_EVENTS.SERVICE_STARTED);
      socket.off(SOCKET_EVENTS.SERVICE_COMPLETED);
      socket.off(SOCKET_EVENTS.TOKEN_SKIPPED);
      socket.off(SOCKET_EVENTS.TOKEN_TRANSFERRED);
      socket.off(SOCKET_EVENTS.COUNTER_UPDATED);
      socket.off(SOCKET_EVENTS.COUNTER_ADDED);
      socket.off(SOCKET_EVENTS.QUEUE_UPDATED);
      socket.off(SOCKET_EVENTS.TOKEN_CREATED);
    };
  }, [tokenId, fetchToken, fetchCounters, notifyStatusChange]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([fetchToken(), fetchCounters()]);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading your token...</p>
        </div>
      </div>
    );
  }

  if (error || !token) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center max-w-sm">
          <AlertTriangle size={48} className="text-red-400 mx-auto mb-4" />
          <h2 className="text-white text-xl font-bold mb-2">Token Not Found</h2>
          <p className="text-gray-400 mb-6">{error || 'This token does not exist or may have expired.'}</p>
          <Link to="/customer" className="btn-primary inline-flex items-center gap-2">
            <ArrowLeft size={18} /> Get New Token
          </Link>
        </div>
      </div>
    );
  }

  const statusConfig = STATUS_CONFIG[token.status] || STATUS_CONFIG.WAITING;
  const StatusIcon = statusConfig.icon;
  const isActive = ['WAITING', 'CALLED', 'IN_SERVICE'].includes(token.status);
  const assignedCounter = counters.find(c => c._id === token.counterId || c._id === token.counterId?._id);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Connection bar */}
      <div className={`flex items-center justify-center gap-2 py-1.5 text-xs font-medium ${
        connected ? 'bg-emerald-900/20 text-emerald-400' : 'bg-red-900/20 text-red-400'
      }`}>
        {connected ? <Wifi size={11} /> : <WifiOff size={11} />}
        {connected ? 'Live — Updates in Real-Time' : 'Reconnecting...'}
      </div>

      <div className="px-4 pb-8 max-w-lg mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between py-4">
          <Link to="/customer" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <ArrowLeft size={18} />
            <span className="text-sm">Back</span>
          </Link>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center">
              <Zap size={14} className="text-white" />
            </div>
            <span className="text-white font-bold">QFlow</span>
          </div>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <RefreshCw size={18} className={refreshing ? 'animate-spin' : ''} />
          </button>
        </div>

        {/* YOUR TURN alert */}
        {token.status === 'CALLED' && (
          <div className="mb-4 animate-slide-up bg-blue-500/20 border-2 border-blue-500/70 rounded-2xl p-5 text-center shadow-2xl shadow-blue-500/30">
            <Bell size={32} className="text-blue-400 mx-auto mb-2 animate-bounce" />
            <h2 className="text-2xl font-black text-white mb-1">YOUR TURN!</h2>
            <p className="text-blue-300 font-medium">Please proceed to the counter immediately</p>
          </div>
        )}

        {/* Service Completed */}
        {token.status === 'COMPLETED' && (
          <div className="mb-4 animate-slide-up bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-5 text-center">
            <CheckCircle size={32} className="text-emerald-400 mx-auto mb-2" />
            <h2 className="text-xl font-bold text-white mb-1">Service Completed!</h2>
            <p className="text-emerald-300">Thank you for using QFlow</p>
          </div>
        )}

        {/* Token Card */}
        <div className={`card ${statusConfig.glow} mb-4 text-center animate-slide-up border-2 ${statusConfig.bg}`}>
          <p className="text-gray-400 text-sm uppercase tracking-widest mb-2">Your Token</p>
          <div className="relative inline-block">
            {statusConfig.pulse && (
              <div className="absolute -inset-4 rounded-full border-2 border-blue-400 animate-ping opacity-30"></div>
            )}
            <div className="token-number">{token.tokenNumber}</div>
          </div>
          
          <div className="flex items-center justify-center gap-2 mt-3 mb-4">
            <StatusIcon size={18} className={statusConfig.color} />
            <span className={`text-lg font-bold ${statusConfig.color}`}>{statusConfig.label}</span>
          </div>
          <p className="text-gray-400 text-sm">{statusConfig.sublabel}</p>

          {/* Live Action Timer */}
          <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-800/80 border border-gray-700/60 text-xs font-mono text-gray-300">
            <Clock size={12} className={statusConfig.color} />
            {token.status === 'WAITING' && (
              <span>Waiting: <strong className="text-white">{formatElapsed(token.createdAt)}</strong></span>
            )}
            {token.status === 'CALLED' && (
              <span>Called: <strong className="text-white">{formatElapsed(token.calledAt)}</strong> ago</span>
            )}
            {token.status === 'IN_SERVICE' && (
              <span>In Service: <strong className="text-emerald-400">{formatElapsed(token.startedAt)}</strong></span>
            )}
            {token.status === 'COMPLETED' && (
              <span>Total Service: <strong className="text-emerald-400">{token.actualDuration != null ? token.actualDuration : 1} min</strong></span>
            )}
            {['SKIPPED', 'TRANSFERRED'].includes(token.status) && (
              <span>{token.status}</span>
            )}
          </div>

          {/* Service & Customer */}
          <div className="mt-4 pt-4 border-t border-gray-700/50 grid grid-cols-2 gap-3 text-left">
            <div>
              <p className="text-gray-500 text-xs mb-1">Service</p>
              <p className="text-white font-semibold text-sm">{token.service}</p>
            </div>
            <div>
              <p className="text-gray-500 text-xs mb-1">Customer</p>
              <p className="text-white font-semibold text-sm">{token.customerName}</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        {isActive && (
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="card text-center p-4">
              <div className="flex items-center justify-center gap-1 text-amber-400 mb-1">
                <Users size={16} />
              </div>
              <div className="text-2xl font-bold text-white">{token.peopleAhead ?? '—'}</div>
              <div className="text-gray-500 text-xs mt-0.5">Ahead</div>
            </div>
            <div className="card text-center p-4">
              <div className="flex items-center justify-center gap-1 text-indigo-400 mb-1">
                <Clock size={16} />
              </div>
              <div className="text-2xl font-bold text-white">
                {token.estimatedWait != null ? `${token.estimatedWait}` : '—'}
              </div>
              <div className="text-gray-500 text-xs mt-0.5">Min wait</div>
            </div>
            <div className="card text-center p-4">
              <div className="flex items-center justify-center gap-1 text-purple-400 mb-1">
                <Zap size={16} />
              </div>
              <div className="text-2xl font-bold text-white">
                {token.predictedDuration != null ? `${token.predictedDuration}` : '—'}
              </div>
              <div className="text-gray-500 text-xs mt-0.5">AI min</div>
            </div>
          </div>
        )}

        {/* Counter Info */}
        {(assignedCounter || token.counterId) && (
          <div className="card mb-4">
            <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-3">Assigned Counter</h3>
            <div className={`flex items-center justify-between p-3 rounded-xl border ${
              COUNTER_STATUS_BG[assignedCounter?.status] || 'bg-gray-800/50 border-gray-700'
            }`}>
              <div>
                <p className="text-white font-bold text-lg">
                  Counter {assignedCounter?.counterNumber || '—'}
                </p>
                <p className="text-gray-400 text-sm">{assignedCounter?.staffName || 'Staff'}</p>
              </div>
              <div className="text-right">
                <span className={`text-sm font-semibold ${COUNTER_STATUS_COLORS[assignedCounter?.status] || 'text-gray-400'}`}>
                  {assignedCounter?.status?.replace('_', ' ') || 'Assigned'}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* AI Prediction Note */}
        {token.predictedDuration && (
          <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4 mb-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap size={14} className="text-indigo-400" />
              <span className="text-indigo-400 text-xs font-semibold uppercase tracking-wider">AI Prediction</span>
            </div>
            <p className="text-gray-400 text-xs">
              Estimated service duration: <span className="text-white font-semibold">{token.predictedDuration} minutes</span>
            </p>
            <p className="text-gray-600 text-xs mt-1">
              Based on historical synthetic service data. Actual time may vary.
            </p>
          </div>
        )}

        {/* Live Counter Cards */}
        {counters.filter(c => c.isActive !== false).length > 0 && (
          <div className="card">
            <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-3">All Counters — Live</h3>
            <div className="space-y-2">
              {counters.filter(c => c.isActive !== false).map(counter => (
                <div
                  key={counter._id}
                  className={`flex items-center justify-between p-3 rounded-lg border ${
                    COUNTER_STATUS_BG[counter.status] || 'bg-gray-800/50 border-gray-700'
                  } ${counter._id === token.counterId || counter._id === token.counterId?._id ? 'ring-2 ring-indigo-500/50' : ''}`}
                >
                  <div>
                    <p className="text-white font-semibold text-sm">Counter {counter.counterNumber}</p>
                    <p className="text-gray-400 text-xs">{counter.staffName}</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-xs font-semibold ${COUNTER_STATUS_COLORS[counter.status] || 'text-gray-400'}`}>
                      {counter.status?.replace('_', ' ')}
                    </p>
                    {counter.currentTokenId && (
                      <p className="text-gray-500 text-xs">
                        {counter.currentTokenId?.tokenNumber || '—'}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Get new token link */}
        {['COMPLETED', 'SKIPPED'].includes(token.status) && (
          <div className="mt-6 text-center">
            <Link to="/customer" className="btn-primary inline-flex items-center gap-2">
              <Zap size={16} /> Get Another Token
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default TokenStatus;
