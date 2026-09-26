const mongoose = require('mongoose');

// User schema representing both students and mentors.
// Every account starts with isMentor = false.
// When a user clicks "Become a Mentor", isMentor is set to true and skills are saved.
const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  isMentor: {
    type: Boolean,
    default: false
  },
  skills: {
    type: [String],
    default: []
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('User', userSchema);
