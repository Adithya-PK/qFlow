import { useState } from 'react';
import { useQueue } from '../../context/QueueContext';
import { counterAPI, tokenAPI } from '../../services/api';
import { Plus, Monitor, RefreshCw, AlertCircle, Power } from 'lucide-react';
import toast from 'react-hot-toast';
import CounterCard from '../../components/CounterCard';
import TransferModal from '../../components/TransferModal';

const CountersPage = () => {
  const { counters, queue, loading, refreshData } = useQueue();
  const [showAddForm, setShowAddForm] = useState(false);
  const [newCounter, setNewCounter] = useState({ staffName: '', servicesSupported: [] });
  const [adding, setAdding] = useState(false);
  const [actionLoading, setActionLoading] = useState({});
  const [transferModal, setTransferModal] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await refreshData();
    setRefreshing(false);
  };

  const handleAddCounter = async (e) => {
    e.preventDefault();
    if (!newCounter.staffName.trim()) {
      toast.error('Staff name is required');
      return;
    }
    setAdding(true);
    try {
      const response = await counterAPI.create({
        staffName: newCounter.staffName.trim(),
        servicesSupported: newCounter.servicesSupported,
      });
      const counter = response.data.counter || response.data;
      toast.success(`Counter ${counter.counterNumber} created!`);
      setNewCounter({ staffName: '', servicesSupported: [] });
      setShowAddForm(false);
      await refreshData();
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to add counter');
    } finally {
      setAdding(false);
    }
  };

  const handleCallNext = async (counterId) => {
    setActionLoading(prev => ({ ...prev, [counterId]: 'calling' }));
    try {
      const res = await counterAPI.callNext(counterId);
      toast.success(res.data.message || 'Next token called!');
      await refreshData();
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
      await refreshData();
    } catch (error) {
      toast.error(error.response?.data?.message || `Failed to ${action}`);
    } finally {
      setActionLoading(prev => ({ ...prev, [tokenId]: null }));
    }
  };

  const handleToggleCounter = async (counter) => {
    try {
      const nextActive = counter.isActive === false;
      await counterAPI.update(counter._id, { 
        isActive: nextActive,
        status: nextActive ? 'AVAILABLE' : 'OFFLINE'
      });
      toast.success(`Counter ${counter.counterNumber} ${nextActive ? 'activated' : 'deactivated'}`);
      await refreshData();
    } catch (error) {
      toast.error('Failed to update counter status');
    }
  };

  const activeCounters = counters.filter(c => c.isActive !== false);
  const inactiveCounters = counters.filter(c => c.isActive === false);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Counters</h1>
          <p className="text-gray-400 text-sm mt-0.5">
            {activeCounters.length} active counter{activeCounters.length === 1 ? '' : 's'} online
          </p>
        </div>
        <div className="flex gap-3">
          <button onClick={handleRefresh} disabled={refreshing} className="btn-secondary flex items-center gap-2">
            <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
          </button>
          <button onClick={() => setShowAddForm(!showAddForm)} className="btn-primary flex items-center gap-2">
            <Plus size={16} />
            Add Counter
          </button>
        </div>
      </div>

      {/* Add Counter Form */}
      {showAddForm && (
        <div className="card animate-slide-up border border-indigo-500/30">
          <h2 className="text-lg font-bold text-white mb-4">Add New Counter</h2>
          <form onSubmit={handleAddCounter} className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label className="form-label">Staff Name *</label>
              <input
                type="text"
                value={newCounter.staffName}
                onChange={e => setNewCounter(prev => ({ ...prev, staffName: e.target.value }))}
                placeholder="e.g. Karthik"
                className="form-input"
                autoFocus
              />
            </div>
            <div className="flex items-end gap-3">
              <button type="submit" disabled={adding} className="btn-primary flex items-center gap-2 whitespace-nowrap">
                {adding ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <Plus size={16} />
                )}
                {adding ? 'Creating...' : 'Create Counter'}
              </button>
              <button type="button" onClick={() => setShowAddForm(false)} className="btn-secondary whitespace-nowrap">
                Cancel
              </button>
            </div>
          </form>
          <p className="text-gray-500 text-xs mt-3 flex items-center gap-1">
            <AlertCircle size={12} />
            The counter number will be auto-assigned. It will sync immediately across staff and customer screens.
          </p>
        </div>
      )}

      {/* Active Counter Cards */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-4 bg-gray-700 rounded mb-4 w-3/4"></div>
              <div className="h-8 bg-gray-700 rounded mb-2"></div>
              <div className="h-4 bg-gray-700 rounded w-full"></div>
            </div>
          ))}
        </div>
      ) : activeCounters.length === 0 ? (
        <div className="card text-center py-16">
          <Monitor size={48} className="text-gray-600 mx-auto mb-4" />
          <h3 className="text-gray-300 font-semibold mb-2">No Active Counters</h3>
          <p className="text-gray-500 text-sm mb-6">Create a counter above or reactivate an existing counter below.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
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
                onTransfer={() => currentToken && setTransferModal(currentToken)}
                onDeactivate={() => handleToggleCounter(counter)}
                loading={actionLoading[counter._id] || (currentToken && actionLoading[currentToken._id])}
                queue={queue}
                showAllActions
              />
            );
          })}
        </div>
      )}

      {/* Deactivated Counters Section */}
      {inactiveCounters.length > 0 && (
        <div className="card border-dashed border-gray-800">
          <h3 className="text-gray-400 font-semibold text-sm mb-3 uppercase tracking-wider flex items-center gap-2">
            <Power size={14} className="text-gray-500" />
            Deactivated Counters ({inactiveCounters.length})
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {inactiveCounters.map(counter => (
              <div key={counter._id} className="p-3.5 bg-gray-800/40 rounded-xl border border-gray-800 flex items-center justify-between">
                <div>
                  <p className="text-gray-300 font-semibold text-sm">Counter {counter.counterNumber}</p>
                  <p className="text-gray-500 text-xs">{counter.staffName}</p>
                </div>
                <button
                  onClick={() => handleToggleCounter(counter)}
                  className="px-3 py-1.5 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 border border-emerald-500/30 rounded-lg text-xs font-semibold transition-all"
                >
                  Activate
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Transfer Modal */}
      {transferModal && (
        <TransferModal
          token={transferModal}
          counters={counters}
          onClose={() => setTransferModal(null)}
          onTransfer={async (targetCounterId) => {
            await handleTokenAction('transfer', transferModal._id, { targetCounterId });
            setTransferModal(null);
          }}
        />
      )}
    </div>
  );
};

export default CountersPage;
