const User = require('../models/User');

// @desc    Upgrade logged in user to mentor role and set skills
// @route   PATCH /api/users/become-mentor
// @access  Private
const becomeMentor = async (req, res) => {
  try {
    const { skills } = req.body;

    if (!skills || (Array.isArray(skills) && skills.length === 0)) {
      return res.status(400).json({
        success: false,
        message: 'Please provide at least one technical skill.'
      });
    }

    // Process skills into a clean array of strings (supporting comma-separated string input)
    let parsedSkills = [];
    if (typeof skills === 'string') {
      parsedSkills = skills
        .split(',')
        .map(skill => skill.trim())
        .filter(skill => skill.length > 0);
    } else if (Array.isArray(skills)) {
      parsedSkills = skills.map(s => s.trim()).filter(Boolean);
    }

    if (parsedSkills.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Skills required.'
      });
    }

    // Update current user document: set isMentor = true and store skills
    const user = await User.findById(req.user._id);
    user.isMentor = true;
    user.skills = parsedSkills;
    await user.save();

    return res.status(200).json({
      success: true,
      message: 'Congratulations! You are now registered as a mentor.',
      user: {
        _id: user._id,
        name: user.name,
        email: user.email,
        isMentor: user.isMentor,
        skills: user.skills
      }
    });
  } catch (error) {
    console.error('Become Mentor Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to update mentor profile.'
    });
  }
};

// @desc    Update skills for an existing mentor
// @route   PATCH /api/users/update-skills
// @access  Private
const updateSkills = async (req, res) => {
  try {
    const { skills } = req.body;

    let parsedSkills = [];
    if (typeof skills === 'string') {
      parsedSkills = skills
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);
    } else if (Array.isArray(skills)) {
      parsedSkills = skills.map(s => s.trim()).filter(Boolean);
    }

    const user = await User.findById(req.user._id);
    user.skills = parsedSkills;
    await user.save();

    return res.status(200).json({
      success: true,
      message: 'Skills updated successfully.',
      user: {
        _id: user._id,
        name: user.name,
        email: user.email,
        isMentor: user.isMentor,
        skills: user.skills
      }
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      message: 'Failed to update skills.'
    });
  }
};

module.exports = {
  becomeMentor,
  updateSkills
};
