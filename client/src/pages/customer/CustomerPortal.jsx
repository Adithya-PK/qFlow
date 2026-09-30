import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { tokenAPI, serviceAPI, counterAPI } from '../../services/api';
import { connectSocket, SOCKET_EVENTS } from '../../services/socket';
import toast from 'react-hot-toast';
import { Zap, Users, Clock, ChevronRight, Wifi, WifiOff, AlertCircle } from 'lucide-react';

const STATUS_COLORS = {
  AVAILABLE: 'text-emerald-400',
  CALLING: 'text-blue-400',
  IN_SERVICE: 'text-indigo-400',
  OFFLINE: 'text-gray-500',
};

const STATUS_BG = {
  AVAILABLE: 'bg-emerald-500/10 border-emerald-500/20',
  CALLING: 'bg-blue-500/10 border-blue-500/20',
  IN_SERVICE: 'bg-indigo-500/10 border-indigo-500/20',
  OFFLINE: 'bg-gray-500/10 border-gray-500/20',
};

const CustomerPortal = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState('landing'); // landing | form | loading | done
  const [services, setServices] = useState([]);
  const [counters, setCounters] = useState([]);
  const [queueStats, setQueueStats] = useState({ waiting: 0 });
  const [connected, setConnected] = useState(false);
  const [formData, setFormData] = useState({
    customerName: '',
    phone: '',
    service: '',
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    // Fetch services and counter data
    const fetchData = async () => {
      try {
        const [svcRes, ctrRes] = await Promise.all([
          serviceAPI.getAll(),
          counterAPI.getAll(),
        ]);
        setServices(svcRes.data.services || svcRes.data || []);
        setCounters(ctrRes.data.counters || ctrRes.data || []);
      } catch (err) {
        console.error('Failed to fetch initial data:', err);
      }
    };
    fetchData();

    // Connect to socket
    const socket = connectSocket();
    setConnected(socket.connected);

    socket.on(SOCKET_EVENTS.CONNECT, () => setConnected(true));
    socket.on(SOCKET_EVENTS.DISCONNECT, () => setConnected(false));

    // Listen for counter updates to show live status
    socket.on(SOCKET_EVENTS.COUNTER_ADDED, ({ counter }) => {
      setCounters(prev => {
        const exists = prev.find(c => c._id === counter._id);
        return exists ? prev : [...prev, counter];
      });
    });
    
    socket.on(SOCKET_EVENTS.COUNTER_UPDATED, ({ counter }) => {
      setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
    });

    socket.on(SOCKET_EVENTS.QUEUE_UPDATED, ({ stats }) => {
      if (stats) setQueueStats(stats);
    });

    socket.on(SOCKET_EVENTS.TOKEN_CREATED, () => {
      setQueueStats(prev => ({ ...prev, waiting: (prev.waiting || 0) + 1 }));
    });

    socket.on(SOCKET_EVENTS.SERVICE_COMPLETED, () => {
      setQueueStats(prev => ({ ...prev, waiting: Math.max(0, (prev.waiting || 0) - 1) }));
    });

    return () => {
      socket.off(SOCKET_EVENTS.CONNECT);
      socket.off(SOCKET_EVENTS.DISCONNECT);
      socket.off(SOCKET_EVENTS.COUNTER_ADDED);
      socket.off(SOCKET_EVENTS.COUNTER_UPDATED);
      socket.off(SOCKET_EVENTS.QUEUE_UPDATED);
      socket.off(SOCKET_EVENTS.TOKEN_CREATED);
      socket.off(SOCKET_EVENTS.SERVICE_COMPLETED);
    };
  }, []);

  const validate = () => {
    const newErrors = {};
    if (!formData.customerName.trim() || formData.customerName.trim().length < 2) {
      newErrors.customerName = 'Please enter your full name (at least 2 characters)';
    }
    if (!formData.phone.trim() || !/^\d{10}$/.test(formData.phone.trim())) {
      newErrors.phone = 'Please enter a valid 10-digit phone number';
    }
    if (!formData.service) {
      newErrors.service = 'Please select a service';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    setStep('loading');
    try {
      const response = await tokenAPI.create(formData);
      const { token } = response.data;
      toast.success(`Token ${token.tokenNumber} generated!`);
      // Navigate to token status page
      navigate(`/customer/token/${token._id}`);
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to generate token. Please try again.';
      toast.error(message);
      setStep('form');
    } finally {
      setSubmitting(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const availableCounters = counters.filter(c => c.isActive !== false);

  if (step === 'loading') {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center">
          <div className="w-20 h-20 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-white text-2xl font-bold mb-2">Generating Your Token</h2>
          <p className="text-gray-400">Please wait while we assign you a queue position...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Connection indicator */}
      <div className={`fixed top-0 left-0 right-0 z-50 flex items-center justify-center gap-2 py-1 text-xs font-medium transition-all ${
        connected ? 'bg-emerald-900/30 text-emerald-400' : 'bg-red-900/30 text-red-400'
      }`}>
        {connected ? <Wifi size={12} /> : <WifiOff size={12} />}
        {connected ? 'Connected — Live Updates Active' : 'Connecting to server...'}
      </div>

      <div className="pt-7 px-4 pb-8 max-w-lg mx-auto">
        {/* Header */}
        <div className="text-center pt-10 pb-8">
          <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-indigo-500/30">
            <Zap size={32} className="text-white" />
          </div>
          <h1 className="text-4xl font-black text-white mb-2">QFlow</h1>
          <p className="text-gray-400 text-lg">Smart Queue Management</p>
          
          {/* Live stats bar */}
          <div className="flex items-center justify-center gap-6 mt-5">
            <div className="flex items-center gap-2 text-sm">
              <Users size={15} className="text-amber-400" />
              <span className="text-gray-300">{queueStats.waiting || 0} waiting</span>
            </div>
            <div className="w-px h-4 bg-gray-700"></div>
            <div className="flex items-center gap-2 text-sm">
              <Clock size={15} className="text-indigo-400" />
              <span className="text-gray-300">Live queue</span>
            </div>
          </div>
        </div>

        {step === 'landing' && (
          <div className="animate-slide-up">
            {/* Hero Card */}
            <div className="card mb-6 text-center glow-indigo">
              <h2 className="text-2xl font-bold text-white mb-2">Skip the Queue Confusion</h2>
              <p className="text-gray-400 mb-6">
                Get your digital token, track your position in real-time, and never miss your turn.
              </p>
              <button
                onClick={() => setStep('form')}
                className="w-full btn-primary py-4 text-lg font-bold flex items-center justify-center gap-2"
              >
                Get Your Token
                <ChevronRight size={20} />
              </button>
            </div>

            {/* How it works */}
            <div className="card mb-6">
              <h3 className="text-gray-300 font-semibold mb-4 text-sm uppercase tracking-wider">How It Works</h3>
              <div className="space-y-3">
                {[
                  { num: '1', text: 'Enter your details below' },
                  { num: '2', text: 'Select your service type' },
                  { num: '3', text: 'Receive your token instantly' },
                  { num: '4', text: 'Track your position in real-time' },
                  { num: '5', text: 'Get notified when it\'s your turn' },
                ].map(({ num, text }) => (
                  <div key={num} className="flex items-center gap-3">
                    <div className="w-7 h-7 bg-indigo-600/30 border border-indigo-500/30 rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-indigo-400 text-xs font-bold">{num}</span>
                    </div>
                    <span className="text-gray-300 text-sm">{text}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Live Counter Status */}
            {availableCounters.length > 0 && (
              <div className="card">
                <h3 className="text-gray-300 font-semibold mb-4 text-sm uppercase tracking-wider">Live Counter Status</h3>
                <div className="space-y-3">
                  {availableCounters.map(counter => (
                    <div
                      key={counter._id}
                      className={`flex items-center justify-between p-3 rounded-lg border ${STATUS_BG[counter.status] || 'bg-gray-800/50 border-gray-700'}`}
                    >
                      <div>
                        <p className="text-white font-semibold text-sm">Counter {counter.counterNumber}</p>
                        <p className="text-gray-400 text-xs">{counter.staffName}</p>
                      </div>
                      <div className="text-right">
                        <span className={`text-xs font-semibold ${STATUS_COLORS[counter.status] || 'text-gray-400'}`}>
                          {counter.status?.replace('_', ' ')}
                        </span>
                        {counter.currentTokenId && (
                          <p className="text-gray-500 text-xs mt-0.5">
                            Token: {counter.currentTokenId?.tokenNumber || '—'}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {step === 'form' && (
          <div className="animate-slide-up">
            <div className="card">
              <h2 className="text-xl font-bold text-white mb-1">Get Your Token</h2>
              <p className="text-gray-400 text-sm mb-6">Fill in your details to join the queue</p>

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Name */}
                <div>
                  <label className="form-label">Full Name *</label>
                  <input
                    type="text"
                    name="customerName"
                    value={formData.customerName}
                    onChange={handleChange}
                    placeholder="Enter your full name"
                    className="form-input"
                    autoComplete="name"
                    autoFocus
                  />
                  {errors.customerName && (
                    <p className="text-red-400 text-xs mt-1.5 flex items-center gap-1">
                      <AlertCircle size={12} /> {errors.customerName}
                    </p>
                  )}
                </div>

                {/* Phone */}
                <div>
                  <label className="form-label">Phone Number *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="10-digit mobile number"
                    className="form-input"
                    inputMode="numeric"
                    maxLength={10}
                    autoComplete="tel"
                  />
                  {errors.phone && (
                    <p className="text-red-400 text-xs mt-1.5 flex items-center gap-1">
                      <AlertCircle size={12} /> {errors.phone}
                    </p>
                  )}
                </div>

                {/* Service */}
                <div>
                  <label className="form-label">Service Required *</label>
                  <select
                    name="service"
                    value={formData.service}
                    onChange={handleChange}
                    className="form-input"
                  >
                    <option value="">Select a service...</option>
                    {services.length > 0 ? (
                      services.filter(s => s.active !== false).map(s => (
                        <option key={s._id} value={s.name}>{s.name}</option>
                      ))
                    ) : (
                      <>
                        <option value="Account Service">Account Service</option>
                        <option value="Payment Service">Payment Service</option>
                        <option value="Document Verification">Document Verification</option>
                        <option value="Customer Support">Customer Support</option>
                        <option value="General Enquiry">General Enquiry</option>
                      </>
                    )}
                  </select>
                  {errors.service && (
                    <p className="text-red-400 text-xs mt-1.5 flex items-center gap-1">
                      <AlertCircle size={12} /> {errors.service}
                    </p>
                  )}
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setStep('landing')}
                    className="btn-secondary flex-1"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    {submitting ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Generating...
                      </>
                    ) : (
                      <>
                        Get Token
                        <ChevronRight size={18} />
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomerPortal;
