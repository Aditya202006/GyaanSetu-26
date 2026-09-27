const mongoose = require('mongoose');
const dns = require('dns');

// Force Node.js to use Google Public DNS (8.8.8.8) to resolve MongoDB Atlas SRV records
try {
  dns.setServers(['8.8.8.8', '8.8.4.4']);
} catch (err) {
  console.warn('Could not set custom DNS servers:', err.message);
}

// Connect to MongoDB database using Mongoose.
const connectDB = async () => {
  const targetUri = process.env.MONGO_URI || 'mongodb+srv://23pa1a05a2_db_user:5WM2PWWnYSMpWLt4@cluster0.tadnbiz.mongodb.net/gyaansetu?retryWrites=true&w=majority';
  
  try {
    console.log(`Connecting to MongoDB...`);
    const conn = await mongoose.connect(targetUri);
    console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`❌ MongoDB Connection Error: ${error.message}`);
    throw error;
  }
};

module.exports = connectDB;
