const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const connectDB = require('../server/config/db');

// Load environment variables
dotenv.config();

// Connect to MongoDB Atlas
connectDB();

const app = express();

app.use(cors());
app.use(express.json());

// Import backend routes
const authRoutes = require('../server/routes/authRoutes');
const userRoutes = require('../server/routes/userRoutes');
const mentorRoutes = require('../server/routes/mentorRoutes');
const proposalRoutes = require('../server/routes/proposalRoutes');
const sessionRoutes = require('../server/routes/sessionRoutes');

// Mount routes with dual prefix support (/api/ and direct)
app.use('/api/auth', authRoutes);
app.use('/auth', authRoutes);

app.use('/api/users', userRoutes);
app.use('/users', userRoutes);

app.use('/api/mentors', mentorRoutes);
app.use('/mentors', mentorRoutes);

app.use('/api/proposals', proposalRoutes);
app.use('/proposals', proposalRoutes);

app.use('/api/sessions', sessionRoutes);
app.use('/sessions', sessionRoutes);

app.get('/api', (req, res) => {
  res.json({ success: true, message: 'GyaanSetu Backend API is running on Vercel Serverless.' });
});

app.use((req, res) => {
  res.status(404).json({ success: false, message: 'Route not found on Vercel API server.' });
});

module.exports = app;
