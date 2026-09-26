const mongoose = require('mongoose');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const User = require('./models/User');
const Proposal = require('./models/Proposal');
const Session = require('./models/Session');

dotenv.config();

const clearDatabase = async () => {
  try {
    await connectDB();

    console.log('Clearing all data from MongoDB Atlas...');
    await User.deleteMany({});
    await Proposal.deleteMany({});
    await Session.deleteMany({});

    console.log('✨ All seed accounts, proposals, and sessions have been completely removed!');
    console.log('The database is now 100% clean and ready for real user registrations.');
    process.exit(0);
  } catch (error) {
    console.error('Failed to clear database:', error);
    process.exit(1);
  }
};

clearDatabase();
