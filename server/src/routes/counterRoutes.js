const express = require('express');
const router = express.Router();
const {
  getCounters,
  getCounter,
  createCounter,
  callNext,
  updateCounter,
  deleteCounter,
} = require('../controllers/counterController');

router.get('/', getCounters);
router.get('/:id', getCounter);
router.post('/', createCounter);
router.post('/:id/call-next', callNext);
router.put('/:id', updateCounter);
router.delete('/:id', deleteCounter);

module.exports = router;
