const express = require('express');
const router = express.Router();
const { login, getMe, register } = require('../controllers/authController');
const { protect, adminOnly } = require('../middleware/auth');

router.post('/login', login);
router.get('/me', protect, getMe);
router.get('/verify', protect, getMe);
router.post('/register', protect, adminOnly, register);

module.exports = router;
