import { useState, useEffect } from 'react';
import { useQueue } from '../../context/QueueContext';
import { counterAPI, tokenAPI } from '../../services/api';
import { Users, Clock, CheckCircle, RefreshCw, Monitor, History, List } from 'lucide-react';
import toast from 'react-hot-toast';
import CounterCard from '../../components/CounterCard';
import AIRecommendation from '../../components/AIRecommendation';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];

const Dashboard = () => {
  const { counters, queue, analytics, loading, refreshData } = useQueue();
  const [refreshing, setRefreshing] = useState(false);
  const [actionLoading, setActionLoading] = useState({});
  const [activeTab, setActiveTab] = useState('live'); // 'live' | 'completed'
  const [completedTokens, setCompletedTokens] = useState([]);
  const [loadingCompleted, setLoadingCompleted] = useState(false);

  const fetchCompletedTokens = async () => {
    try {
      setLoadingCompleted(true);
      const res = await tokenAPI.getAll({ status: 'COMPLETED' });
      setCompletedTokens(res.data.tokens || res.data || []);
    } catch (err) {
      console.error('Failed to fetch completed tokens:', err);
    } finally {
      setLoadingCompleted(false);
    }
  };

  useEffect(() => {
    fetchCompletedTokens();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([refreshData(), fetchCompletedTokens()]);
    setRefreshing(false);
  };

  const waitingTokens = queue.filter(t => t.status === 'WAITING');
  const calledTokens = queue.filter(t => t.status === 'CALLED');
  const inServiceTokens = queue.filter(t => t.status === 'IN_SERVICE');

  const handleCallNext = async (counterId) => {
    setActionLoading(prev => ({ ...prev, [counterId]: 'calling' }));
    try {
      const res = await counterAPI.callNext(counterId);
      toast.success(res.data.message || 'Next token called!');
      await Promise.all([refreshData(), fetchCompletedTokens()]);
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to call next token');
    } finally {
      setActionLoading(prev => ({ ...prev, [counterId]: null }));
    }
  };

  const handleTokenAction = async (action, tokenId, data = {}) => {
    setActionLoading(prev => ({ ...prev, [tokenId]: action }));
    try {
      await tokenAPI[action](tokenId, data);
      const labels = { start: 'started', complete: 'completed', skip: 'skipped' };
      toast.success(`Token ${labels[action] || 'updated'}!`);
      await Promise.all([refreshData(), fetchCompletedTokens()]);
    } catch (error) {
      toast.error(error.response?.data?.message || `Failed to ${action} token`);
    } finally {
      setActionLoading(prev => ({ ...prev, [tokenId]: null }));
    }
  };

  const stats = [
    {
      label: 'Waiting',
      value: waitingTokens.length,
      icon: Users,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20',
    },
    {
      label: 'In Service',
      value: inServiceTokens.length + calledTokens.length,
      icon: Monitor,
      color: 'text-indigo-400',
      bg: 'bg-indigo-500/10 border-indigo-500/20',
    },
    {
      label: 'Completed Today',
      value: analytics?.summary?.completed ?? analytics?.completed ?? completedTokens.length,
      icon: CheckCircle,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/20',
    },
    {
      label: 'Avg Wait Time',
      value: (analytics?.summary?.averageWaitTime ?? analytics?.averageWaitTime) != null
        ? `${Math.round(analytics?.summary?.averageWaitTime ?? analytics?.averageWaitTime)} min`
        : '—',
      icon: Clock,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/20',
    },
  ];

  const activeCounters = counters.filter(c => c.isActive !== false);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 text-sm mt-0.5">Real-time token and queue management operations</p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn-secondary flex items-center gap-2"
        >
          <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className={`stat-card border ${bg}`}>
            <div className="flex items-center justify-between">
              <span className="text-gray-400 text-sm">{label}</span>
              <div className={`w-8 h-8 rounded-lg ${bg} flex items-center justify-center`}>
                <Icon size={16} className={color} />
              </div>
            </div>
            <div className={`text-3xl font-bold ${color}`}>{value}</div>
          </div>
        ))}
      </div>

      {/* Active Counters — Main View at Top */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Monitor size={20} className="text-indigo-400" />
            Active Counters ({activeCounters.length})
          </h2>
          <span className="text-xs text-gray-400">
            {waitingTokens.length} customer{waitingTokens.length === 1 ? '' : 's'} waiting in queue
          </span>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 bg-gray-700 rounded mb-4 w-3/4"></div>
                <div className="h-8 bg-gray-700 rounded mb-2 w-1/2"></div>
                <div className="h-4 bg-gray-700 rounded w-full"></div>
              </div>
            ))}
          </div>
        ) : activeCounters.length === 0 ? (
          <div className="card text-center py-12">
            <Monitor size={40} className="text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No active counters. Please activate counters in Settings or Counters page.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            {activeCounters.map(counter => {
              const currentToken = counter.currentTokenId 
                ? (typeof counter.currentTokenId === 'object' ? counter.currentTokenId : queue.find(t => t._id === counter.currentTokenId))
                : null;
              return (
                <CounterCard
                  key={counter._id}
                  counter={counter}
                  currentToken={currentToken}
                  onCallNext={() => handleCallNext(counter._id)}
                  onStart={() => currentToken && handleTokenAction('start', currentToken._id)}
                  onComplete={() => currentToken && handleTokenAction('complete', currentToken._id)}
                  onSkip={() => currentToken && handleTokenAction('skip', currentToken._id)}
                  loading={actionLoading[counter._id] || (currentToken && actionLoading[currentToken._id])}
                  queue={queue}
                />
              );
            })}
          </div>
        )}
      </div>

      {/* AI Recommendation — Positioned Below Active Counters */}
      <AIRecommendation counters={counters} queue={queue} />

      {/* Queue Overview & History Section */}
      <div className="card">
        <div className="flex items-center justify-between pb-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('live')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-semibold transition-all ${
                activeTab === 'live'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'bg-gray-800 text-gray-400 hover:text-gray-200'
              }`}
            >
              <List size={16} />
              Live Queue ({queue.length})
            </button>
            <button
              onClick={() => { setActiveTab('completed'); fetchCompletedTokens(); }}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-semibold transition-all ${
                activeTab === 'completed'
                  ? 'bg-emerald-600 text-white shadow'
                  : 'bg-gray-800 text-gray-400 hover:text-gray-200'
              }`}
            >
              <History size={16} />
              Completed Today ({completedTokens.length})
            </button>
          </div>
          <span className="text-xs text-gray-400 hidden sm:inline">
            {activeTab === 'live' ? 'Real-time database sync' : 'Finished service log'}
          </span>
        </div>

        {/* Live Queue Tab */}
        {activeTab === 'live' && (
          <div className="overflow-x-auto pt-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-400 border-b border-gray-800/80 text-xs uppercase tracking-wider">
                  <th className="text-left pb-3 font-medium">Token</th>
                  <th className="text-left pb-3 font-medium">Customer</th>
                  <th className="text-left pb-3 font-medium hidden md:table-cell">Phone</th>
                  <th className="text-left pb-3 font-medium">Service</th>
                  <th className="text-left pb-3 font-medium">Status</th>
                  <th className="text-left pb-3 font-medium hidden lg:table-cell">Wait Time</th>
                  <th className="text-left pb-3 font-medium hidden xl:table-cell">AI Pred.</th>
                  <th className="text-left pb-3 font-medium">Counter</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {loading ? (
                  <tr>
                    <td colSpan="8" className="py-8 text-center text-gray-500">Loading queue...</td>
                  </tr>
                ) : queue.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="py-8 text-center text-gray-500">
                      No active customers in queue. Customers can scan the QR code to join.
                    </td>
                  </tr>
                ) : (
                  queue.map(token => {
                    const counter = counters.find(c => c._id === token.counterId || c._id === token.counterId?._id);
                    return (
                      <tr key={token._id} className="hover:bg-gray-800/30 transition-colors">
                        <td className="py-3 font-bold text-indigo-400 font-mono text-base">{token.tokenNumber}</td>
                        <td className="py-3 text-gray-200 font-medium">{token.customerName}</td>
                        <td className="py-3 text-gray-400 hidden md:table-cell font-mono text-xs">{token.phone}</td>
                        <td className="py-3 text-gray-300">{token.service}</td>
                        <td className="py-3">
                          <span className={`
                            px-2.5 py-0.5 rounded-full text-xs font-semibold
                            ${token.status === 'WAITING' ? 'badge-waiting' : ''}
                            ${token.status === 'CALLED' ? 'badge-called' : ''}
                            ${token.status === 'IN_SERVICE' ? 'badge-inservice' : ''}
                            ${token.status === 'COMPLETED' ? 'badge-completed' : ''}
                            ${token.status === 'SKIPPED' ? 'badge-skipped' : ''}
                          `}>
                            {token.status?.replace('_', ' ')}
                          </span>
                        </td>
                        <td className="py-3 text-gray-400 hidden lg:table-cell">
                          {token.estimatedWait != null ? `${token.estimatedWait} min` : '—'}
                        </td>
                        <td className="py-3 text-gray-400 hidden xl:table-cell">
                          {token.predictedDuration != null ? `${token.predictedDuration} min` : '—'}
                        </td>
                        <td className="py-3 text-gray-300 text-xs font-semibold">
                          {counter ? `Counter ${counter.counterNumber}` : '—'}
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        )}

        {/* Completed Today Tab */}
        {activeTab === 'completed' && (
          <div className="overflow-x-auto pt-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-400 border-b border-gray-800/80 text-xs uppercase tracking-wider">
                  <th className="text-left pb-3 font-medium">Token</th>
                  <th className="text-left pb-3 font-medium">Customer</th>
                  <th className="text-left pb-3 font-medium">Service</th>
                  <th className="text-left pb-3 font-medium">Counter Staff</th>
                  <th className="text-left pb-3 font-medium hidden sm:table-cell">Actual Duration</th>
                  <th className="text-left pb-3 font-medium hidden md:table-cell">Completed At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {loadingCompleted ? (
                  <tr>
                    <td colSpan="6" className="py-8 text-center text-gray-500">Loading history...</td>
                  </tr>
                ) : completedTokens.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="py-8 text-center text-gray-500">
                      No completed tokens for today yet.
                    </td>
                  </tr>
                ) : (
                  completedTokens.map(token => {
                    const counter = counters.find(c => c._id === token.counterId || c._id === token.counterId?._id);
                    const completedTime = token.completedAt 
                      ? new Date(token.completedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                      : '—';
                    return (
                      <tr key={token._id} className="hover:bg-gray-800/30 transition-colors">
                        <td className="py-3 font-bold text-emerald-400 font-mono">{token.tokenNumber}</td>
                        <td className="py-3 text-gray-200">{token.customerName}</td>
                        <td className="py-3 text-gray-300">{token.service}</td>
                        <td className="py-3 text-gray-400">
                          {counter ? `Counter ${counter.counterNumber} (${counter.staffName})` : '—'}
                        </td>
                        <td className="py-3 text-gray-300 font-semibold hidden sm:table-cell">
                          {token.actualDuration != null ? `${token.actualDuration} min` : '< 1 min'}
                        </td>
                        <td className="py-3 text-gray-400 font-mono text-xs hidden md:table-cell">
                          {completedTime}
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Analytics Section — Live Data Charts */}
      {analytics?.tokensByService && analytics.tokensByService.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-gray-300 font-semibold mb-4 text-sm uppercase tracking-wider">
              Tokens by Service (Today)
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={analytics.tokensByService}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="service" tick={{ fill: '#9ca3af', fontSize: 10 }}
                  tickFormatter={s => s?.split(' ')[0] || s} />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  labelStyle={{ color: '#f9fafb' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="card">
            <h3 className="text-gray-300 font-semibold mb-4 text-sm uppercase tracking-wider">
              Service Distribution
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={analytics.tokensByService}
                  dataKey="count"
                  nameKey="service"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ service, percent }) => `${service?.split(' ')[0]}: ${(percent * 100).toFixed(0)}%`}
                  labelLine={false}
                >
                  {analytics.tokensByService.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
