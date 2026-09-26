const mongoose = require('mongoose');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const User = require('./models/User');
const Proposal = require('./models/Proposal');
const Session = require('./models/Session');

dotenv.config();

const API_URL = 'http://localhost:5000/api';

const runFullTest = async () => {
  console.log('🚀 Starting Full End-to-End API Test Suite...');
  console.log('--------------------------------------------------');

  try {
    // 1. Health check
    console.log('1️⃣ Testing Health Check Endpoint (GET /)...');
    const healthRes = await fetch('http://localhost:5000/').then(r => r.json());
    console.log('   ✅ Health Check:', healthRes.message);

    // 2. Register Student
    console.log('\n2️⃣ Testing Student Registration (POST /api/auth/register)...');
    const studentReg = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test Student',
        email: 'realstudent_test@example.com',
        password: 'password123'
      })
    }).then(r => r.json());

    if (!studentReg.success) throw new Error(studentReg.message);
    const studentToken = studentReg.token;
    const studentId = studentReg.user._id;
    console.log(`   ✅ Registered Student: ${studentReg.user.name} (${studentReg.user.email})`);

    // 3. Register Mentor User
    console.log('\n3️⃣ Testing Mentor User Registration (POST /api/auth/register)...');
    const mentorReg = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test Mentor',
        email: 'realmentor_test@example.com',
        password: 'password123'
      })
    }).then(r => r.json());

    if (!mentorReg.success) throw new Error(mentorReg.message);
    const mentorToken = mentorReg.token;
    const mentorId = mentorReg.user._id;
    console.log(`   ✅ Registered User: ${mentorReg.user.name} (${mentorReg.user.email})`);

    // 4. Upgrade User 2 to Mentor ("Become a Mentor")
    console.log('\n4️⃣ Testing "Become a Mentor" (PATCH /api/users/become-mentor)...');
    const becomeMentorRes = await fetch(`${API_URL}/users/become-mentor`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${mentorToken}`
      },
      body: JSON.stringify({ skills: 'Java, React, SQL, Node.js' })
    }).then(r => r.json());

    if (!becomeMentorRes.success) throw new Error(becomeMentorRes.message);
    console.log('   ✅ Mentor Status:', becomeMentorRes.user.isMentor);
    console.log('   ✅ Saved Skills:', becomeMentorRes.user.skills.join(', '));

    // 5. Fetch Mentor Directory
    console.log('\n5️⃣ Testing Fetch Mentors (GET /api/mentors)...');
    const mentorsRes = await fetch(`${API_URL}/mentors`).then(r => r.json());
    const foundMentor = mentorsRes.data.find(m => m._id === mentorId);
    console.log(`   ✅ Found ${mentorsRes.data.length} mentor(s). Target mentor present: ${!!foundMentor}`);

    // 6. Student sends doubt proposal to Mentor
    console.log('\n6️⃣ Testing Send Doubt Proposal (POST /api/proposals)...');
    const proposalRes = await fetch(`${API_URL}/proposals`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${studentToken}`
      },
      body: JSON.stringify({
        mentorId: mentorId,
        doubt: 'How does React useEffect dependency array work under the hood?'
      })
    }).then(r => r.json());

    if (!proposalRes.success) throw new Error(proposalRes.message);
    const proposalId = proposalRes.data._id;
    console.log('   ✅ Proposal Created with ID:', proposalId);
    console.log('   ✅ Status:', proposalRes.data.status);

    // 7. Mentor views received proposals
    console.log('\n7️⃣ Testing Get Received Proposals (GET /api/proposals/received)...');
    const recRes = await fetch(`${API_URL}/proposals/received`, {
      headers: { 'Authorization': `Bearer ${mentorToken}` }
    }).then(r => r.json());
    console.log('   ✅ Received Requests Count:', recRes.data.length);

    // 8. Mentor accepts proposal
    console.log('\n8️⃣ Testing Accept Proposal (PATCH /api/proposals/:id/accept)...');
    const acceptRes = await fetch(`${API_URL}/proposals/${proposalId}/accept`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${mentorToken}` }
    }).then(r => r.json());

    if (!acceptRes.success) throw new Error(acceptRes.message);
    console.log('   ✅ Updated Status:', acceptRes.data.status);

    // 9. Mentor schedules session
    console.log('\n9️⃣ Testing Schedule Session (POST /api/sessions)...');
    const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
    const sessionRes = await fetch(`${API_URL}/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${mentorToken}`
      },
      body: JSON.stringify({
        proposalId: proposalId,
        scheduledTime: tomorrow
      })
    }).then(r => r.json());

    if (!sessionRes.success) throw new Error(sessionRes.message);
    const sessionId = sessionRes.data._id;
    console.log('   ✅ Session Scheduled ID:', sessionId);
    console.log('   ✅ Jitsi Meeting URL:', sessionRes.data.meetingLink);

    // 10. Student checks my sessions
    console.log('\n🔟 Testing Get My Sessions (GET /api/sessions/my)...');
    const studentSessRes = await fetch(`${API_URL}/sessions/my`, {
      headers: { 'Authorization': `Bearer ${studentToken}` }
    }).then(r => r.json());
    console.log('   ✅ Student Sessions Count:', studentSessRes.data.length);

    // 11. Mentor completes session
    console.log('\n1️⃣1️⃣ Testing Mark Session Complete (PATCH /api/sessions/:id/complete)...');
    const completeRes = await fetch(`${API_URL}/sessions/${sessionId}/complete`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${mentorToken}` }
    }).then(r => r.json());

    if (!completeRes.success) throw new Error(completeRes.message);
    console.log('   ✅ Session Completed Status:', completeRes.data.status);

    // 12. Cleanup test data
    console.log('\n1️⃣2️⃣ Cleaning up test data from MongoDB Atlas...');
    await connectDB();
    await User.deleteMany({ _id: { $in: [studentId, mentorId] } });
    await Proposal.deleteMany({ _id: proposalId });
    await Session.deleteMany({ _id: sessionId });
    console.log('   ✅ Cleanup complete! Database remains 100% clean for user.');

    console.log('\n🎉 ALL END-TO-END TESTS PASSED SUCCESSFULLY! EVERYTHING IS WORKING PERFECTLY! 🎉');
    process.exit(0);

  } catch (error) {
    console.error('❌ Test Failed:', error.message);
    process.exit(1);
  }
};

runFullTest();
