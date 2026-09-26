const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Authentication middleware to protect endpoints.
// It verifies the JWT passed in the Authorization header (Bearer <token>).
// If valid, it attaches the authenticated user object to req.user.
const protect = async (req, res, next) => {
  let token;

  // Check if authorization header exists and starts with 'Bearer'
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    try {
      // Extract token from header string "Bearer <token>"
      token = req.headers.authorization.split(' ')[1];

      // Verify token signature using JWT secret key
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'gyaansetu_secret_key_2026_placement_project');

      // Fetch user details from database (excluding password hash)
      // and attach user info to req.user for downstream controllers
      req.user = await User.findById(decoded.userId).select('-password');

      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'User no longer exists.'
        });
      }

      return next();
    } catch (error) {
      console.error('JWT Verification Error:', error.message);
      return res.status(401).json({
        success: false,
        message: 'Unauthorized, token failed or expired.'
      });
    }
  }

  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Unauthorized, no authorization token provided.'
    });
  }
};

module.exports = { protect };
