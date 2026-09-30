import { useState } from 'react';
import { X, ArrowRightLeft } from 'lucide-react';

const TransferModal = ({ token, counters, onClose, onTransfer }) => {
  const [targetCounterId, setTargetCounterId] = useState('');
  const [loading, setLoading] = useState(false);

  const availableCounters = counters.filter(c => 
    c.isActive !== false && 
    c._id !== token.counterId && 
    c._id !== token.counterId?._id &&
    c.status !== 'OFFLINE'
  );

  const handleTransfer = async () => {
    if (!targetCounterId) return;
    setLoading(true);
    try {
      await onTransfer(targetCounterId);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center px-4" onClick={onClose}>
      <div
        className="card w-full max-w-md animate-slide-up"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ArrowRightLeft size={20} className="text-purple-400" />
            Transfer Token
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        <div className="mb-4 p-3 bg-gray-800/50 rounded-xl border border-gray-700">
          <p className="text-gray-400 text-xs mb-1">Transferring</p>
          <p className="text-indigo-400 font-black text-2xl">{token.tokenNumber}</p>
          <p className="text-gray-300 text-sm">{token.customerName} — {token.service}</p>
        </div>

        <div className="mb-5">
          <label className="form-label">Transfer to Counter</label>
          <select
            value={targetCounterId}
            onChange={e => setTargetCounterId(e.target.value)}
            className="form-input"
          >
            <option value="">Select target counter...</option>
            {availableCounters.map(counter => (
              <option key={counter._id} value={counter._id}>
                Counter {counter.counterNumber} — {counter.staffName} ({counter.status})
              </option>
            ))}
          </select>
          {availableCounters.length === 0 && (
            <p className="text-red-400 text-xs mt-1">No available counters to transfer to.</p>
          )}
        </div>

        <div className="flex gap-3">
          <button onClick={onClose} className="btn-secondary flex-1">Cancel</button>
          <button
            onClick={handleTransfer}
            disabled={!targetCounterId || loading || availableCounters.length === 0}
            className="btn-primary flex-1 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <ArrowRightLeft size={16} />
                Transfer
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransferModal;
