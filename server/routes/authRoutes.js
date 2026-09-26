const express = require('express');
const router = express.Router();
const { registerUser, loginUser, getMe } = require('../controllers/authController');
const { protect } = require('../middleware/authMiddleware');

// Route: User Registration
router.post('/register', registerUser);

// Route: User Login
router.post('/login', loginUser);

// Route: Get current user profile (requires valid JWT token)
router.get('/me', protect, getMe);

module.exports = router;
