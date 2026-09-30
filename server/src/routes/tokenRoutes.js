const express = require('express');
const router = express.Router();
const {
  createToken,
  getTokens,
  getToken,
  callToken,
  startService,
  completeService,
  skipToken,
  transferToken,
} = require('../controllers/tokenController');

// Token CRUD
router.post('/', createToken);
router.get('/', getTokens);
router.get('/:id', getToken);

// Token lifecycle operations
router.post('/:id/call', callToken);
router.post('/:id/start', startService);
router.post('/:id/complete', completeService);
router.post('/:id/skip', skipToken);
router.post('/:id/transfer', transferToken);

module.exports = router;
