import { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useQueue } from '../context/QueueContext';
import {
  LayoutDashboard, Users, Monitor, BarChart3, Settings,
  QrCode, LogOut, Menu, X, Wifi, WifiOff, Zap
} from 'lucide-react';
import QRModal from '../components/QRModal';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard', exact: true },
  { path: '/queue', icon: Users, label: 'Queue' },
  { path: '/counters', icon: Monitor, label: 'Counters' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/settings', icon: Settings, label: 'Settings' },
];

const StaffLayout = () => {
  const { user, logout } = useAuth();
  const { connected, waitingCount, inServiceCount } = useQueue();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [qrModalOpen, setQrModalOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:relative inset-y-0 left-0 z-30 w-64 bg-gray-900 border-r border-gray-800
        flex flex-col transition-transform duration-300
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Logo */}
        <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-800">
          <div className="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center">
            <Zap size={20} className="text-white" />
          </div>
          <div>
            <span className="text-white font-bold text-xl">QFlow</span>
            <div className="flex items-center gap-1.5">
              {connected ? (
                <>
                  <Wifi size={10} className="text-emerald-400" />
                  <span className="text-emerald-400 text-xs">Live</span>
                </>
              ) : (
                <>
                  <WifiOff size={10} className="text-red-400" />
                  <span className="text-red-400 text-xs">Offline</span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="px-4 py-4 border-b border-gray-800">
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2 text-center">
              <div className="text-amber-400 text-xl font-bold">{waitingCount}</div>
              <div className="text-gray-500 text-xs">Waiting</div>
            </div>
            <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-lg px-3 py-2 text-center">
              <div className="text-indigo-400 text-xl font-bold">{inServiceCount}</div>
              <div className="text-gray-500 text-xs">In Service</div>
            </div>
          </div>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
          {navItems.map(({ path, icon: Icon, label, exact }) => (
            <NavLink
              key={path}
              to={path}
              end={exact}
              className={({ isActive }) =>
                `sidebar-link ${isActive ? 'active' : ''}`
              }
              onClick={() => setSidebarOpen(false)}
            >
              <Icon size={18} />
              <span className="font-medium">{label}</span>
            </NavLink>
          ))}
          
          <button
            onClick={() => { setQrModalOpen(true); setSidebarOpen(false); }}
            className="sidebar-link w-full text-left"
          >
            <QrCode size={18} />
            <span className="font-medium">Customer QR</span>
          </button>
        </nav>

        {/* User */}
        <div className="px-4 py-4 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-9 h-9 bg-indigo-600/30 rounded-full flex items-center justify-center">
              <span className="text-indigo-400 font-semibold text-sm">
                {user?.name?.charAt(0)?.toUpperCase() || 'A'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-gray-200 font-medium text-sm truncate">{user?.name || 'Admin'}</p>
              <p className="text-gray-500 text-xs capitalize">{user?.role || 'admin'}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-3 py-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all text-sm"
          >
            <LogOut size={16} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar */}
        <header className="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center gap-4 lg:hidden">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-gray-400 hover:text-white p-1"
          >
            {sidebarOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center">
              <Zap size={14} className="text-white" />
            </div>
            <span className="text-white font-bold">QFlow</span>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* QR Modal */}
      <QRModal isOpen={qrModalOpen} onClose={() => setQrModalOpen(false)} />
    </div>
  );
};

export default StaffLayout;
