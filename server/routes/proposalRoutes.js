const express = require('express');
const router = express.Router();
const {
  createProposal,
  getMyProposals,
  getReceivedProposals,
  acceptProposal,
  rejectProposal
} = require('../controllers/proposalController');
const { protect } = require('../middleware/authMiddleware');

// Route: Send doubt proposal to a mentor
router.post('/', protect, createProposal);

// Route: Get requests created by logged in user as student
router.get('/my', protect, getMyProposals);

// Route: Get requests received by logged in user as mentor
router.get('/received', protect, getReceivedProposals);

// Route: Accept a doubt request
router.patch('/:id/accept', protect, acceptProposal);

// Route: Reject a doubt request
router.patch('/:id/reject', protect, rejectProposal);

module.exports = router;
