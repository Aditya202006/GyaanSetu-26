const express = require('express');
const router = express.Router();
const { becomeMentor, updateSkills } = require('../controllers/userController');
const { protect } = require('../middleware/authMiddleware');

// Route: Become a mentor (set isMentor = true and store skills)
router.patch('/become-mentor', protect, becomeMentor);

// Route: Update technical skills for mentor
router.patch('/update-skills', protect, updateSkills);

module.exports = router;
