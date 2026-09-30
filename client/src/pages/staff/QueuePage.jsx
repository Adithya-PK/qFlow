import { useState, useEffect, useCallback } from 'react';
import { useQueue } from '../../context/QueueContext';
import { tokenAPI } from '../../services/api';
import { getSocket, SOCKET_EVENTS } from '../../services/socket';
import { Users, Filter, RefreshCw, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import TransferModal from '../../components/TransferModal';

const STATUS_OPTIONS = ['ALL', 'WAITING', 'CALLED', 'IN_SERVICE', 'COMPLETED', 'SKIPPED'];

const QueuePage = () => {
  const { counters, refreshData: refreshGlobalQueue } = useQueue();
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [actionLoading, setActionLoading] = useState({});
  const [transferModal, setTransferModal] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchAllTokens = useCallback(async () => {
    try {
      const res = await tokenAPI.getAll();
      setTokens(res.data.tokens || res.data || []);
    } catch (err) {
      console.error('Failed to load tokens:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchAllTokens();

    const socket = getSocket();
    const handleTokenUpdate = ({ token }) => {
      if (!token || !token._id) return;
      setTokens(prev => {
        const exists = prev.some(t => t._id === token._id);
        if (exists) {
          return prev.map(t => (t._id === token._id ? { ...t, ...token } : t));
        }
        return [token, ...prev];
      });
    };

    socket.on(SOCKET_EVENTS.TOKEN_CREATED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.TOKEN_CALLED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.SERVICE_STARTED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.SERVICE_COMPLETED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.TOKEN_SKIPPED, handleTokenUpdate);
    socket.on(SOCKET_EVENTS.TOKEN_TRANSFERRED, handleTokenUpdate);

    return () => {
      socket.off(SOCKET_EVENTS.TOKEN_CREATED, handleTokenUpdate);
      socket.off(SOCKET_EVENTS.TOKEN_CALLED, handleTokenUpdate);
      socket.off(SOCKET_EVENTS.SERVICE_STARTED, handleTokenUpdate);
      socket.off(SOCKET_EVENTS.SERVICE_COMPLETED, handleTokenUpdate);
      socket.off(SOCKET_EVENTS.TOKEN_SKIPPED, handleTokenUpdate);
      socket.off(SOCKET_EVENTS.TOKEN_TRANSFERRED, handleTokenUpdate);
    };
  }, [fetchAllTokens]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([fetchAllTokens(), refreshGlobalQueue()]);
  };

  const handleAction = async (action, tokenId, data = {}) => {
    setActionLoading(prev => ({ ...prev, [tokenId]: action }));
    try {
      const res = await tokenAPI[action](tokenId, data);
      const updatedToken = res.data?.token;
      if (updatedToken) {
        setTokens(prev => prev.map(t => t._id === (updatedToken._id || tokenId) ? { ...t, ...updatedToken } : t));
      }
      const labels = { call: 'called', start: 'started', complete: 'completed', skip: 'skipped', transfer: 'transferred' };
      toast.success(`Token ${labels[action] || action}!`);
      await Promise.all([fetchAllTokens(), refreshGlobalQueue()]);
    } catch (error) {
      toast.error(error.response?.data?.message || `Failed to ${action}`);
      await fetchAllTokens();
    } finally {
      setActionLoading(prev => ({ ...prev, [tokenId]: null }));
    }
  };

  const filtered = tokens.filter(t => {
    const matchesFilter = filter === 'ALL' || t.status === filter;
    const matchesSearch = !search || 
      t.tokenNumber?.toLowerCase().includes(search.toLowerCase()) ||
      t.customerName?.toLowerCase().includes(search.toLowerCase()) ||
      t.phone?.includes(search) ||
      t.service?.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getCounterName = (token) => {
    if (!token.counterId) return '—';
    const counterId = typeof token.counterId === 'object' ? token.counterId._id : token.counterId;
    const counter = counters.find(c => c._id === counterId);
    return counter ? `Counter ${counter.counterNumber}` : '—';
  };

  const canAction = (token, action) => {
    const transitions = {
      call: ['WAITING'],
      start: ['CALLED'],
      complete: ['IN_SERVICE'],
      skip: ['WAITING', 'CALLED'],
      transfer: ['WAITING', 'CALLED'],
    };
    return transitions[action]?.includes(token.status);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Queue & Token History</h1>
          <p className="text-gray-400 text-sm mt-0.5">{filtered.length} tokens listed</p>
        </div>
        <button onClick={handleRefresh} disabled={refreshing} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search by token, name, phone, or service..."
            className="form-input pl-9"
          />
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <Filter size={16} className="text-gray-400" />
          {STATUS_OPTIONS.map(status => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                filter === status
                  ? 'bg-indigo-600 text-white shadow'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {status}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-400 border-b border-gray-800 text-xs uppercase tracking-wider">
              <th className="text-left pb-3 font-medium">Token</th>
              <th className="text-left pb-3 font-medium">Customer</th>
              <th className="text-left pb-3 font-medium hidden md:table-cell">Phone</th>
              <th className="text-left pb-3 font-medium">Service</th>
              <th className="text-left pb-3 font-medium">Status</th>
              <th className="text-left pb-3 font-medium hidden lg:table-cell">Wait Time</th>
              <th className="text-left pb-3 font-medium hidden xl:table-cell">AI Pred.</th>
              <th className="text-left pb-3 font-medium">Counter</th>
              <th className="text-left pb-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/50">
            {loading ? (
              <tr><td colSpan="9" className="py-8 text-center text-gray-500">Loading queue...</td></tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan="9" className="py-10 text-center">
                  <Users size={32} className="text-gray-600 mx-auto mb-2" />
                  <p className="text-gray-500">No tokens found</p>
                </td>
              </tr>
            ) : (
              filtered.map(token => (
                <tr key={token._id} className="hover:bg-gray-800/30 transition-colors">
                  <td className="py-3 font-bold text-indigo-400 font-mono">{token.tokenNumber}</td>
                  <td className="py-3 text-gray-200">{token.customerName}</td>
                  <td className="py-3 text-gray-400 hidden md:table-cell font-mono text-xs">{token.phone}</td>
                  <td className="py-3 text-gray-400 text-xs">{token.service}</td>
                  <td className="py-3">
                    <span className={`
                      px-2.5 py-0.5 rounded-full text-xs font-semibold
                      ${token.status === 'WAITING' ? 'badge-waiting' : ''}
                      ${token.status === 'CALLED' ? 'badge-called' : ''}
                      ${token.status === 'IN_SERVICE' ? 'badge-inservice' : ''}
                      ${token.status === 'COMPLETED' ? 'badge-completed' : ''}
                      ${['SKIPPED', 'TRANSFERRED'].includes(token.status) ? 'badge-skipped' : ''}
                    `}>
                      {token.status?.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-3 text-gray-400 hidden lg:table-cell text-xs">
                    {token.estimatedWait != null ? `${token.estimatedWait} min` : '—'}
                  </td>
                  <td className="py-3 text-gray-400 hidden xl:table-cell text-xs">
                    {token.predictedDuration != null ? `${token.predictedDuration} min` : '—'}
                  </td>
                  <td className="py-3 text-gray-400 text-xs">{getCounterName(token)}</td>
                  <td className="py-3">
                    <div className="flex items-center gap-1 flex-wrap">
                      {canAction(token, 'start') && (
                        <button
                          onClick={() => handleAction('start', token._id)}
                          disabled={!!actionLoading[token._id]}
                          className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded transition-colors disabled:opacity-50"
                        >
                          {actionLoading[token._id] === 'start' ? '...' : 'Start'}
                        </button>
                      )}
                      {canAction(token, 'complete') && (
                        <button
                          onClick={() => handleAction('complete', token._id)}
                          disabled={!!actionLoading[token._id]}
                          className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded transition-colors disabled:opacity-50"
                        >
                          {actionLoading[token._id] === 'complete' ? '...' : 'Complete'}
                        </button>
                      )}
                      {canAction(token, 'skip') && (
                        <button
                          onClick={() => handleAction('skip', token._id)}
                          disabled={!!actionLoading[token._id]}
                          className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition-colors disabled:opacity-50"
                        >
                          {actionLoading[token._id] === 'skip' ? '...' : 'Skip'}
                        </button>
                      )}
                      {canAction(token, 'transfer') && (
                        <button
                          onClick={() => setTransferModal(token)}
                          className="px-2 py-1 bg-purple-700 hover:bg-purple-600 text-white text-xs rounded transition-colors"
                        >
                          Transfer
                        </button>
                      )}
                      {token.status === 'COMPLETED' && (
                        <span className="text-xs text-gray-500 font-mono">
                          {token.actualDuration != null ? `${token.actualDuration}m done` : 'done'}
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Transfer Modal */}
      {transferModal && (
        <TransferModal
          token={transferModal}
          counters={counters}
          onClose={() => setTransferModal(null)}
          onTransfer={async (targetCounterId) => {
            await handleAction('transfer', transferModal._id, { targetCounterId });
            setTransferModal(null);
          }}
        />
      )}
    </div>
  );
};

export default QueuePage;
