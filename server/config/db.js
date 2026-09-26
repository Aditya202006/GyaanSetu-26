const mongoose = require('mongoose');
const dns = require('dns');

// Force Node.js to use Google Public DNS (8.8.8.8) to resolve MongoDB Atlas SRV records
// This fixes the "querySrv ECONNREFUSED" error caused by local ISP/router DNS restrictions.
try {
  dns.setServers(['8.8.8.8', '8.8.4.4']);
} catch (err) {
  console.warn('Could not set custom DNS servers:', err.message);
}

// Connect to MongoDB database using Mongoose.
const connectDB = async () => {
  const targetUri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/gyaansetu';
  
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
