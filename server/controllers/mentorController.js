const User = require('../models/User');

// @desc    Get all users who have registered as mentors (isMentor = true)
// @route   GET /api/mentors
// @access  Public / Private
const getMentors = async (req, res) => {
  try {
    // Query MongoDB for all users where isMentor is true.
    // Exclude password hashes for security.
    const mentors = await User.find({ isMentor: true })
      .select('-password')
      .sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      data: mentors
    });
  } catch (error) {
    console.error('Get Mentors Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to fetch mentors.'
    });
  }
};

module.exports = { getMentors };
