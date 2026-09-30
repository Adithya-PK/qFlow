/**
 * Socket.IO Handler for QFlow
 *
 * Manages real-time rooms and exposes emit helpers used by controllers.
 * Rooms:
 *   - 'queue'           → staff dashboard, admin, display boards
 *   - 'token:{tokenId}' → customer-specific updates
 *   - 'counters'        → counter management screens
 */

/**
 * Initialize Socket.IO event listeners.
 * @param {import('socket.io').Server} io
 */
function initializeSockets(io) {
  io.on('connection', (socket) => {
    console.log(`[Socket] Client connected: ${socket.id}`);

    /**
     * Staff / admin joins the 'queue' room to receive all queue events.
     */
    socket.on('joinQueue', (data) => {
      socket.join('queue');
      console.log(`[Socket] ${socket.id} joined room: queue`);
      socket.emit('joinedQueue', { message: 'Joined queue room successfully.' });
    });

    /**
     * Customer joins their personal token room for status updates.
     */
    socket.on('joinToken', ({ tokenId }) => {
      if (!tokenId) return;
      const room = `token:${tokenId}`;
      socket.join(room);
      console.log(`[Socket] ${socket.id} joined room: ${room}`);
      socket.emit('joinedToken', { tokenId, message: 'Subscribed to token updates.' });
    });

    /**
     * Counter display joins the 'counters' room.
     */
    socket.on('joinCounters', () => {
      socket.join('counters');
      console.log(`[Socket] ${socket.id} joined room: counters`);
    });

    socket.on('disconnect', (reason) => {
      console.log(`[Socket] Client disconnected: ${socket.id} (${reason})`);
    });

    socket.on('error', (err) => {
      console.error(`[Socket] Error from ${socket.id}:`, err);
    });
  });
}

// ---------------------------------------------------------------------------
// Emit helpers — used by controllers after successful DB operations
// ---------------------------------------------------------------------------

/**
 * Emitted when a new token is created.
 * @param {import('socket.io').Server} io
 * @param {object} token
 * @param {Array}  queue - current queue snapshot
 */
function emitTokenCreated(io, token, queue) {
  io.to('queue').emit('tokenCreated', { token, queue, timestamp: new Date() });
  io.to('counters').emit('queueUpdated', { queue, timestamp: new Date() });
}

/**
 * Emitted when a counter calls a token.
 */
function emitTokenCalled(io, token, counter) {
  io.to('queue').emit('tokenCalled', { token, counter, timestamp: new Date() });
  io.to(`token:${token._id}`).emit('yourTurn', { token, counter, timestamp: new Date() });
  io.to('counters').emit('tokenCalled', { token, counter, timestamp: new Date() });
}

/**
 * Emitted when service starts (IN_SERVICE).
 */
function emitServiceStarted(io, token, counter) {
  io.to('queue').emit('serviceStarted', { token, counter, timestamp: new Date() });
  io.to(`token:${token._id}`).emit('serviceStarted', { token, counter, timestamp: new Date() });
}

/**
 * Emitted when service completes.
 */
function emitServiceCompleted(io, token, counter) {
  io.to('queue').emit('serviceCompleted', { token, counter, timestamp: new Date() });
  io.to(`token:${token._id}`).emit('serviceCompleted', { token, counter, timestamp: new Date() });
  io.to('counters').emit('counterAvailable', { counter, timestamp: new Date() });
}

/**
 * Emitted when a token is skipped.
 */
function emitTokenSkipped(io, token) {
  io.to('queue').emit('tokenSkipped', { token, timestamp: new Date() });
  io.to(`token:${token._id}`).emit('tokenSkipped', { token, timestamp: new Date() });
}

/**
 * Emitted when a token is transferred between counters.
 */
function emitTokenTransferred(io, token, oldCounter, newCounter) {
  io.to('queue').emit('tokenTransferred', { token, oldCounter, newCounter, timestamp: new Date() });
  io.to(`token:${token._id}`).emit('tokenTransferred', { token, newCounter, timestamp: new Date() });
  io.to('counters').emit('tokenTransferred', { token, oldCounter, newCounter, timestamp: new Date() });
}

/**
 * Emitted when a new counter is added.
 */
function emitCounterAdded(io, counter) {
  io.to('queue').emit('counterAdded', { counter, timestamp: new Date() });
  io.to('counters').emit('counterAdded', { counter, timestamp: new Date() });
}

/**
 * Emitted when a counter's details or status are updated.
 */
function emitCounterUpdated(io, counter) {
  io.to('queue').emit('counterUpdated', { counter, timestamp: new Date() });
  io.to('counters').emit('counterUpdated', { counter, timestamp: new Date() });
}

/**
 * Generic queue snapshot broadcast.
 */
function emitQueueUpdated(io, queue) {
  io.to('queue').emit('queueUpdated', { queue, timestamp: new Date() });
  io.to('counters').emit('queueUpdated', { queue, timestamp: new Date() });
}

module.exports = {
  initializeSockets,
  emitTokenCreated,
  emitTokenCalled,
  emitServiceStarted,
  emitServiceCompleted,
  emitTokenSkipped,
  emitTokenTransferred,
  emitCounterAdded,
  emitCounterUpdated,
  emitQueueUpdated,
};
