const express = require('express');
const router = express.Router();
const {
  createSession,
  getMySessions,
  completeSession
} = require('../controllers/sessionController');
const { protect } = require('../middleware/authMiddleware');

// Route: Schedule a session for an accepted proposal
router.post('/', protect, createSession);

// Route: Get sessions where logged-in user is student OR mentor
router.get('/my', protect, getMySessions);

// Route: Mark session as completed
router.patch('/:id/complete', protect, completeSession);

module.exports = router;
