import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import { QueueProvider } from './context/QueueContext';

// Pages
import CustomerPortal from './pages/customer/CustomerPortal';
import TokenStatus from './pages/customer/TokenStatus';
import LoginPage from './pages/auth/LoginPage';
import Dashboard from './pages/staff/Dashboard';
import QueuePage from './pages/staff/QueuePage';
import CountersPage from './pages/staff/CountersPage';
import AnalyticsPage from './pages/staff/AnalyticsPage';
import SettingsPage from './pages/staff/SettingsPage';
import NotFound from './pages/NotFound';

// Layouts
import StaffLayout from './layouts/StaffLayout';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-gray-400">Loading QFlow...</p>
      </div>
    </div>
  );
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: '#1f2937',
              color: '#f9fafb',
              border: '1px solid #374151',
              borderRadius: '10px',
            },
            success: {
              iconTheme: { primary: '#10b981', secondary: '#fff' },
            },
            error: {
              iconTheme: { primary: '#ef4444', secondary: '#fff' },
            },
          }}
        />
        <Routes>
          {/* Customer Routes - No auth required */}
          <Route path="/customer" element={<CustomerPortal />} />
          <Route path="/customer/token/:tokenId" element={<TokenStatus />} />
          
          {/* Auth Routes */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Staff Routes - Auth required */}
          <Route path="/" element={
            <ProtectedRoute>
              <QueueProvider>
                <StaffLayout />
              </QueueProvider>
            </ProtectedRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="queue" element={<QueuePage />} />
            <Route path="counters" element={<CountersPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
          
          {/* Redirect /staff to / */}
          <Route path="/staff" element={<Navigate to="/" replace />} />
          
          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
