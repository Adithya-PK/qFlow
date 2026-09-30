import { useState, useEffect } from 'react';
import { serviceAPI, counterAPI } from '../../services/api';
import { Settings, Plus, RefreshCw, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { useQueue } from '../../context/QueueContext';

const SettingsPage = () => {
  const { counters, refreshData } = useQueue();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddService, setShowAddService] = useState(false);
  const [newService, setNewService] = useState({ name: '', code: '', averageDuration: 10 });
  const [savingService, setSavingService] = useState(false);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const res = await serviceAPI.getAll({ includeInactive: 'true' });
      setServices(res.data.services || res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();
  }, []);

  const handleToggleCounter = async (counter) => {
    try {
      const nextActive = counter.isActive === false;
      await counterAPI.update(counter._id, { 
        isActive: nextActive,
        status: nextActive ? 'AVAILABLE' : 'OFFLINE'
      });
      toast.success(`Counter ${counter.counterNumber} ${nextActive ? 'activated' : 'deactivated'}`);
      await refreshData();
    } catch (e) {
      toast.error('Failed to update counter');
    }
  };

  const handleToggleService = async (service) => {
    try {
      const nextActive = !service.active;
      await serviceAPI.update(service._id, { active: nextActive });
      toast.success(`Service "${service.name}" ${nextActive ? 'activated' : 'deactivated'}`);
      await fetchServices();
    } catch (e) {
      toast.error('Failed to update service');
    }
  };

  const handleCreateService = async (e) => {
    e.preventDefault();
    if (!newService.name.trim() || !newService.code.trim()) {
      toast.error('Service name and code are required');
      return;
    }
    setSavingService(true);
    try {
      await serviceAPI.create({
        name: newService.name.trim(),
        code: newService.code.trim().toUpperCase(),
        averageDuration: Number(newService.averageDuration) || 10,
      });
      toast.success(`Service "${newService.name}" created!`);
      setNewService({ name: '', code: '', averageDuration: 10 });
      setShowAddService(false);
      await fetchServices();
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to create service');
    } finally {
      setSavingService(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Settings</h1>
          <p className="text-gray-400 text-sm mt-0.5">Manage services, counters, and system configuration</p>
        </div>
        <button onClick={fetchServices} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      {/* Services Section */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Settings size={18} className="text-indigo-400" />
            Services Management ({services.length})
          </h2>
          <button
            onClick={() => setShowAddService(!showAddService)}
            className="btn-primary text-xs py-1.5 px-3 flex items-center gap-1.5"
          >
            <Plus size={14} />
            Add Service
          </button>
        </div>

        {/* Add Service Form */}
        {showAddService && (
          <form onSubmit={handleCreateService} className="mb-4 p-4 bg-gray-800/60 rounded-xl border border-indigo-500/30 grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div>
              <label className="form-label text-xs">Service Name *</label>
              <input
                type="text"
                value={newService.name}
                onChange={e => setNewService(prev => ({ ...prev, name: e.target.value }))}
                placeholder="e.g. VIP Consultation"
                className="form-input text-sm py-2"
                required
              />
            </div>
            <div>
              <label className="form-label text-xs">Short Code *</label>
              <input
                type="text"
                value={newService.code}
                onChange={e => setNewService(prev => ({ ...prev, code: e.target.value.toUpperCase() }))}
                placeholder="e.g. VIP"
                className="form-input text-sm py-2"
                maxLength={6}
                required
              />
            </div>
            <div>
              <label className="form-label text-xs">Avg Duration (min)</label>
              <input
                type="number"
                value={newService.averageDuration}
                onChange={e => setNewService(prev => ({ ...prev, averageDuration: e.target.value }))}
                min={1}
                max={120}
                className="form-input text-sm py-2"
              />
            </div>
            <div className="flex items-end gap-2">
              <button
                type="submit"
                disabled={savingService}
                className="btn-primary flex-1 py-2 text-sm flex items-center justify-center gap-1"
              >
                {savingService ? 'Saving...' : 'Save'}
              </button>
              <button
                type="button"
                onClick={() => setShowAddService(false)}
                className="btn-secondary py-2 text-sm"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {loading ? (
          <p className="text-gray-400 py-4 text-center">Loading services...</p>
        ) : (
          <div className="space-y-2">
            {services.map(service => (
              <div
                key={service._id}
                className={`flex items-center justify-between p-3.5 rounded-xl border transition-all ${
                  service.active !== false
                    ? 'bg-gray-800/50 border-gray-700/60'
                    : 'bg-gray-900/40 border-gray-800 opacity-60'
                }`}
              >
                <div>
                  <div className="flex items-center gap-2">
                    <p className="text-white font-semibold text-sm">{service.name}</p>
                    <span className="text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono">
                      {service.code}
                    </span>
                  </div>
                  <p className="text-gray-400 text-xs mt-0.5">
                    Estimated avg duration: {service.averageDuration} min
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded-full font-semibold ${
                    service.active !== false ? 'badge-available' : 'badge-skipped'
                  }`}>
                    {service.active !== false ? 'Active' : 'Inactive'}
                  </span>
                  <button
                    onClick={() => handleToggleService(service)}
                    className={`text-xs px-3 py-1.5 rounded-lg font-semibold transition-all ${
                      service.active !== false
                        ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/30'
                        : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30'
                    }`}
                  >
                    {service.active !== false ? 'Deactivate' : 'Activate'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Counter Status Management */}
      <div className="card">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Settings size={18} className="text-indigo-400" />
          Counter Status Management ({counters.length})
        </h2>
        <div className="space-y-2">
          {counters.map(counter => {
            const isCurrentlyActive = counter.isActive !== false;
            return (
              <div
                key={counter._id}
                className={`flex items-center justify-between p-3.5 rounded-xl border transition-all ${
                  isCurrentlyActive
                    ? 'bg-gray-800/50 border-gray-700/60'
                    : 'bg-gray-900/40 border-gray-800 opacity-60'
                }`}
              >
                <div>
                  <div className="flex items-center gap-2">
                    <p className="text-white font-bold text-sm">Counter {counter.counterNumber}</p>
                    <span className="text-gray-400 text-xs">({counter.staffName})</span>
                  </div>
                  <p className="text-gray-500 text-xs mt-0.5 capitalize">
                    Live Status: <span className="font-semibold text-gray-300">{counter.status?.replace('_', ' ')}</span>
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded-full font-semibold ${
                    isCurrentlyActive ? 'badge-available' : 'badge-skipped'
                  }`}>
                    {isCurrentlyActive ? 'Active' : 'Deactivated'}
                  </span>
                  <button
                    onClick={() => handleToggleCounter(counter)}
                    className={`text-xs px-3 py-1.5 rounded-lg font-semibold transition-all ${
                      isCurrentlyActive
                        ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/30'
                        : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30'
                    }`}
                  >
                    {isCurrentlyActive ? 'Deactivate' : 'Activate Counter'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* System Information */}
      <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <AlertCircle size={16} className="text-indigo-400 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-gray-400">
            <p className="font-semibold text-gray-300 mb-1">System Architecture Note</p>
            <ul className="space-y-1 text-xs">
              <li>• MongoDB is the authoritative single source of truth for all counters, services, and tokens</li>
              <li>• Socket.IO broadcasts updates in real-time across laptop staff dashboards and customer smartphones</li>
              <li>• Deactivated counters/services can be reactivated here at any time with instant live synchronization</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
