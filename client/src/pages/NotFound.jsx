import { Link } from 'react-router-dom';
import { Zap, Home, ArrowLeft } from 'lucide-react';

const NotFound = () => (
  <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
    <div className="text-center max-w-md">
      <div className="w-20 h-20 bg-indigo-600/20 border border-indigo-500/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <Zap size={36} className="text-indigo-400" />
      </div>
      <h1 className="text-6xl font-black text-gray-700 mb-2">404</h1>
      <h2 className="text-2xl font-bold text-white mb-3">Page Not Found</h2>
      <p className="text-gray-400 mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div className="flex gap-4 justify-center">
        <Link to="/" className="btn-primary flex items-center gap-2">
          <Home size={16} /> Staff Dashboard
        </Link>
        <Link to="/customer" className="btn-secondary flex items-center gap-2">
          <Zap size={16} /> Customer Portal
        </Link>
      </div>
    </div>
  </div>
);

export default NotFound;
