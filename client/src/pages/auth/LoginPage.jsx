import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Zap, Eye, EyeOff, LogIn } from 'lucide-react';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    navigate('/', { replace: true });
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await login(formData.email, formData.password);
    setLoading(false);
    if (result.success) {
      navigate('/', { replace: true });
    }
  };

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-indigo-500/30">
            <Zap size={32} className="text-white" />
          </div>
          <h1 className="text-3xl font-black text-white">QFlow</h1>
          <p className="text-gray-400 mt-1">Staff Dashboard Login</p>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-white mb-6">Sign In</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="form-label">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="admin@smartqueue.com"
                className="form-input"
                required
                autoComplete="email"
                autoFocus
              />
            </div>

            <div>
              <label className="form-label">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  className="form-input pr-11"
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-200"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center gap-2 py-3 mt-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <>
                  <LogIn size={18} />
                  Sign In
                </>
              )}
            </button>
          </form>

          {/* Demo credentials */}
          <div className="mt-6 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-lg">
            <p className="text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">Demo Credentials</p>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Email:</span>
                <span className="text-gray-200 font-mono">admin@smartqueue.com</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Password:</span>
                <span className="text-gray-200 font-mono">admin123</span>
              </div>
            </div>
            <button
              onClick={() => setFormData({ email: 'admin@smartqueue.com', password: 'admin123' })}
              className="mt-3 text-indigo-400 hover:text-indigo-300 text-xs underline"
            >
              Fill demo credentials
            </button>
          </div>
        </div>

        <p className="text-center text-gray-600 text-sm mt-6">
          Customer? <a href="/customer" className="text-indigo-400 hover:text-indigo-300">Scan QR or visit /customer</a>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
