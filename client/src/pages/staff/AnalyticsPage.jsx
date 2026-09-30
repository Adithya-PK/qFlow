import { useState, useEffect } from 'react';
import { analyticsAPI } from '../../services/api';
import { BarChart3, RefreshCw, TrendingUp, Clock, Users, CheckCircle } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, Legend
} from 'recharts';

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'];

const AnalyticsPage = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchAnalytics = async () => {
    try {
      const response = await analyticsAPI.get();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { fetchAnalytics(); }, []);

  const handleRefresh = () => { setRefreshing(true); fetchAnalytics(); };

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading analytics...</p>
        </div>
      </div>
    );
  }

  const topStats = [
    { label: 'Total Today', value: analytics?.summary?.totalToday || analytics?.totalToday || 0, icon: Users, color: 'text-indigo-400', bg: 'bg-indigo-500/10 border-indigo-500/20' },
    { label: 'Completed', value: analytics?.summary?.completed || analytics?.completed || 0, icon: CheckCircle, color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/20' },
    { label: 'Avg Wait', value: (analytics?.summary?.averageWaitTime ?? analytics?.averageWaitTime) != null ? `${Math.round(analytics?.summary?.averageWaitTime ?? analytics?.averageWaitTime)} min` : '—', icon: Clock, color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/20' },
    { label: 'Avg Service', value: (analytics?.summary?.averageServiceDuration ?? analytics?.averageServiceDuration) != null ? `${Math.round(analytics?.summary?.averageServiceDuration ?? analytics?.averageServiceDuration)} min` : '—', icon: TrendingUp, color: 'text-purple-400', bg: 'bg-purple-500/10 border-purple-500/20' },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Analytics</h1>
          <p className="text-gray-400 text-sm mt-0.5">Real-time performance metrics</p>
        </div>
        <button onClick={handleRefresh} disabled={refreshing} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {topStats.map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className={`stat-card border ${bg}`}>
            <div className="flex items-center justify-between">
              <span className="text-gray-400 text-sm">{label}</span>
              <Icon size={16} className={color} />
            </div>
            <div className={`text-3xl font-bold ${color}`}>{value}</div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Tokens by Hour */}
        {analytics?.tokensByHour && analytics.tokensByHour.length > 0 && (
          <div className="card lg:col-span-2">
            <h3 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
              <BarChart3 size={16} className="text-indigo-400" />
              Token Volume by Hour
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={analytics.tokensByHour}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="hour"
                  tick={{ fill: '#9ca3af', fontSize: 11 }}
                  tickFormatter={h => `${h}:00`}
                />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  labelFormatter={h => `Hour: ${h}:00`}
                  labelStyle={{ color: '#f9fafb' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} name="Tokens" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Tokens by Service */}
        {analytics?.tokensByService && analytics.tokensByService.length > 0 && (
          <div className="card">
            <h3 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
              <Users size={16} className="text-purple-400" />
              Tokens by Service
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={analytics.tokensByService} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis dataKey="service" type="category" tick={{ fill: '#9ca3af', fontSize: 10 }} width={110} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  labelStyle={{ color: '#f9fafb' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]} name="Tokens" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Service Distribution Pie */}
        {analytics?.tokensByService && analytics.tokensByService.length > 0 && (
          <div className="card">
            <h3 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
              <TrendingUp size={16} className="text-emerald-400" />
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
                  outerRadius={85}
                >
                  {analytics.tokensByService.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                />
                <Legend 
                  formatter={(value) => <span style={{ color: '#9ca3af', fontSize: 11 }}>{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Counter Utilization */}
      {analytics?.counterUtilization && analytics.counterUtilization.length > 0 && (
        <div className="card">
          <h3 className="text-gray-300 font-semibold mb-4">Counter Utilization</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-400 border-b border-gray-800">
                  <th className="text-left pb-3">Counter</th>
                  <th className="text-left pb-3">Staff</th>
                  <th className="text-left pb-3">Completed</th>
                  <th className="text-left pb-3">Avg Duration</th>
                  <th className="text-left pb-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {analytics.counterUtilization.map((c, i) => (
                  <tr key={i} className="hover:bg-gray-800/30">
                    <td className="py-2 font-semibold text-indigo-400">Counter {c.counterNumber}</td>
                    <td className="py-2 text-gray-300">{c.staffName}</td>
                    <td className="py-2 text-gray-400">{c.completedCount || 0}</td>
                    <td className="py-2 text-gray-400">
                      {c.avgServiceDuration != null ? `${Math.round(c.avgServiceDuration)} min` : (c.avgDuration != null ? `${Math.round(c.avgDuration)} min` : '—')}
                    </td>
                    <td className="py-2">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                        c.status === 'AVAILABLE' ? 'badge-available' :
                        c.status === 'IN_SERVICE' ? 'badge-inservice' : 'badge-skipped'
                      }`}>
                        {c.status?.replace('_', ' ')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Data Note */}
      <div className="bg-gray-800/30 border border-gray-700/50 rounded-xl p-4">
        <p className="text-gray-500 text-xs">
          📊 Analytics data is sourced directly from MongoDB. The AI prediction model uses a synthetically generated
          historical service-duration dataset for prototype validation. Actual historical service data would improve 
          prediction accuracy in production.
        </p>
      </div>
    </div>
  );
};

export default AnalyticsPage;
