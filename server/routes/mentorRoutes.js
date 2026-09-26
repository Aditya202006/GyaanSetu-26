const express = require('express');
const router = express.Router();
const { getMentors } = require('../controllers/mentorController');

// Route: Get all mentors (users where isMentor = true)
router.get('/', getMentors);

module.exports = router;
