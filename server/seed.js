const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const User = require('./models/User');
const Proposal = require('./models/Proposal');
const Session = require('./models/Session');

dotenv.config();

const seedData = async () => {
  try {
    // Connect using DB helper (supports Atlas, Local Mongo, and automatic In-Memory fallback)
    await connectDB();

    // Clear existing data
    await User.deleteMany({});
    await Proposal.deleteMany({});
    await Session.deleteMany({});

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash('123456', salt);

    // Create initial seed users
    const rahul = await User.create({
      name: 'Rahul Sharma',
      email: 'rahul@gmail.com',
      password: hashedPassword,
      isMentor: true,
      skills: ['Java', 'DSA', 'SQL']
    });

    const priya = await User.create({
      name: 'Priya Verma',
      email: 'priya@gmail.com',
      password: hashedPassword,
      isMentor: true,
      skills: ['React', 'Node.js', 'MongoDB']
    });

    const arjun = await User.create({
      name: 'Arjun Patel',
      email: 'arjun@gmail.com',
      password: hashedPassword,
      isMentor: true,
      skills: ['Python', 'Machine Learning']
    });

    const aditya = await User.create({
      name: 'Aditya Kumar',
      email: 'aditya@gmail.com',
      password: hashedPassword,
      isMentor: false,
      skills: []
    });

    console.log('🌱 Seed Data Population Complete!');
    console.log('------------------------------------');
    console.log('Created Users:');
    console.log('1. Rahul Sharma (Mentor)  - rahul@gmail.com / 123456 [Java, DSA, SQL]');
    console.log('2. Priya Verma  (Mentor)  - priya@gmail.com / 123456 [React, Node.js, MongoDB]');
    console.log('3. Arjun Patel  (Mentor)  - arjun@gmail.com / 123456 [Python, ML]');
    console.log('4. Aditya Kumar (Student) - aditya@gmail.com / 123456');
    console.log('------------------------------------');

    process.exit(0);
  } catch (error) {
    console.error('Seed Error:', error);
    process.exit(1);
  }
};

seedData();
