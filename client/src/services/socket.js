import { io } from 'socket.io-client';
import { SOCKET_URL } from './api';

let socket = null;

export const getSocket = () => {
  if (!socket) {
    socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      autoConnect: false,
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
    });
  }
  return socket;
};

export const connectSocket = () => {
  const s = getSocket();
  if (!s.connected) {
    s.connect();
  }
  return s;
};

export const disconnectSocket = () => {
  if (socket && socket.connected) {
    socket.disconnect();
  }
};

// Socket event names - centralized
export const SOCKET_EVENTS = {
  TOKEN_CREATED: 'tokenCreated',
  TOKEN_CALLED: 'tokenCalled',
  SERVICE_STARTED: 'serviceStarted',
  SERVICE_COMPLETED: 'serviceCompleted',
  TOKEN_SKIPPED: 'tokenSkipped',
  TOKEN_TRANSFERRED: 'tokenTransferred',
  COUNTER_ADDED: 'counterAdded',
  COUNTER_UPDATED: 'counterUpdated',
  QUEUE_UPDATED: 'queueUpdated',
  ANALYTICS_UPDATED: 'analyticsUpdated',
  JOIN_QUEUE: 'joinQueue',
  JOIN_TOKEN: 'joinToken',
  CONNECT: 'connect',
  DISCONNECT: 'disconnect',
  CONNECT_ERROR: 'connect_error',
  RECONNECT: 'reconnect',
};

export default getSocket;
