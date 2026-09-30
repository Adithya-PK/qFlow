import { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { connectSocket, disconnectSocket, SOCKET_EVENTS } from '../services/socket';
import { counterAPI, queueAPI, analyticsAPI } from '../services/api';
import toast from 'react-hot-toast';

const QueueContext = createContext(null);

export const QueueProvider = ({ children }) => {
  const [counters, setCounters] = useState([]);
  const [queue, setQueue] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const socketRef = useRef(null);

  // Fetch initial data from REST APIs
  const fetchInitialData = useCallback(async () => {
    try {
      setLoading(true);
      const [countersRes, queueRes, analyticsRes] = await Promise.all([
        counterAPI.getAll(),
        queueAPI.getCurrent(),
        analyticsAPI.get(),
      ]);
      setCounters(countersRes.data.counters || countersRes.data || []);
      setQueue(queueRes.data.queue || queueRes.data || []);
      setAnalytics(analyticsRes.data);
    } catch (error) {
      console.error('Failed to fetch initial data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchInitialData();

    // Connect socket
    const socket = connectSocket();
    socketRef.current = socket;
    setConnected(socket.connected);

    socket.emit(SOCKET_EVENTS.JOIN_QUEUE);

    socket.on(SOCKET_EVENTS.CONNECT, () => {
      setConnected(true);
      // Re-fetch to sync after reconnect
      fetchInitialData();
    });

    socket.on(SOCKET_EVENTS.DISCONNECT, () => {
      setConnected(false);
    });

    socket.on(SOCKET_EVENTS.CONNECT_ERROR, (err) => {
      console.error('Socket connection error:', err.message);
      setConnected(false);
    });

    socket.on(SOCKET_EVENTS.TOKEN_CREATED, ({ token, queue: updatedQueue }) => {
      if (updatedQueue) {
        setQueue(updatedQueue);
      } else {
        setQueue(prev => {
          const exists = prev.find(t => t._id === token._id);
          if (exists) return prev;
          return [...prev, token];
        });
      }
      toast.success(`New token ${token.tokenNumber} created`, { id: `token-${token._id}` });
    });

    socket.on(SOCKET_EVENTS.TOKEN_CALLED, ({ token, counter, queue: updatedQueue }) => {
      if (updatedQueue) setQueue(updatedQueue);
      else {
        setQueue(prev => prev.map(t => t._id === token._id ? { ...t, ...token } : t));
      }
      if (counter) {
        setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
      }
    });

    socket.on(SOCKET_EVENTS.SERVICE_STARTED, ({ token, counter, queue: updatedQueue }) => {
      if (updatedQueue) setQueue(updatedQueue);
      else {
        setQueue(prev => prev.map(t => t._id === token._id ? { ...t, ...token } : t));
      }
      if (counter) {
        setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
      }
    });

    socket.on(SOCKET_EVENTS.SERVICE_COMPLETED, ({ token, counter, queue: updatedQueue }) => {
      if (updatedQueue) {
        setQueue(updatedQueue.filter(t => t.status !== 'COMPLETED'));
      } else {
        setQueue(prev => prev.filter(t => t._id !== token._id));
      }
      if (counter) {
        setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
      }
    });

    socket.on(SOCKET_EVENTS.TOKEN_SKIPPED, ({ token, counter, queue: updatedQueue }) => {
      if (updatedQueue) setQueue(updatedQueue);
      else {
        setQueue(prev => prev.filter(t => t._id !== token._id));
      }
      if (counter) {
        setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
      }
    });

    socket.on(SOCKET_EVENTS.TOKEN_TRANSFERRED, ({ token, queue: updatedQueue }) => {
      if (updatedQueue) setQueue(updatedQueue);
      else {
        setQueue(prev => prev.map(t => t._id === token._id ? { ...t, ...token } : t));
      }
    });

    socket.on(SOCKET_EVENTS.COUNTER_ADDED, ({ counter }) => {
      setCounters(prev => {
        const exists = prev.find(c => c._id === counter._id);
        if (exists) return prev;
        return [...prev, counter];
      });
      toast.success(`Counter ${counter.counterNumber} added!`);
    });

    socket.on(SOCKET_EVENTS.COUNTER_UPDATED, ({ counter }) => {
      setCounters(prev => prev.map(c => c._id === counter._id ? { ...c, ...counter } : c));
    });

    socket.on(SOCKET_EVENTS.QUEUE_UPDATED, ({ queue: updatedQueue }) => {
      if (updatedQueue) setQueue(updatedQueue);
    });

    socket.on(SOCKET_EVENTS.ANALYTICS_UPDATED, (data) => {
      setAnalytics(data);
    });

    return () => {
      socket.off(SOCKET_EVENTS.TOKEN_CREATED);
      socket.off(SOCKET_EVENTS.TOKEN_CALLED);
      socket.off(SOCKET_EVENTS.SERVICE_STARTED);
      socket.off(SOCKET_EVENTS.SERVICE_COMPLETED);
      socket.off(SOCKET_EVENTS.TOKEN_SKIPPED);
      socket.off(SOCKET_EVENTS.TOKEN_TRANSFERRED);
      socket.off(SOCKET_EVENTS.COUNTER_ADDED);
      socket.off(SOCKET_EVENTS.COUNTER_UPDATED);
      socket.off(SOCKET_EVENTS.QUEUE_UPDATED);
      socket.off(SOCKET_EVENTS.ANALYTICS_UPDATED);
      socket.off(SOCKET_EVENTS.CONNECT);
      socket.off(SOCKET_EVENTS.DISCONNECT);
    };
  }, [fetchInitialData]);

  const refreshData = useCallback(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  const waitingCount = queue.filter(t => t.status === 'WAITING').length;
  const inServiceCount = queue.filter(t => t.status === 'IN_SERVICE' || t.status === 'CALLED').length;

  return (
    <QueueContext.Provider value={{
      counters,
      setCounters,
      queue,
      setQueue,
      analytics,
      setAnalytics,
      connected,
      loading,
      refreshData,
      waitingCount,
      inServiceCount,
    }}>
      {children}
    </QueueContext.Provider>
  );
};

export const useQueue = () => {
  const context = useContext(QueueContext);
  if (!context) throw new Error('useQueue must be used within QueueProvider');
  return context;
};
