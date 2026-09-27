const Session = require('../models/Session');
const Proposal = require('../models/Proposal');
const sendEmail = require('../utils/sendEmail');

// @desc    Schedule a new mentoring session for an accepted proposal
// @route   POST /api/sessions
// @access  Private (Mentor who received proposal)
const createSession = async (req, res) => {
  try {
    const { proposalId, scheduledTime } = req.body;

    if (!proposalId || !scheduledTime) {
      return res.status(400).json({
        success: false,
        message: 'Proposal ID and scheduled time are required.'
      });
    }

    const proposedDate = new Date(scheduledTime);
    if (isNaN(proposedDate.getTime())) {
      return res.status(400).json({
        success: false,
        message: 'Invalid date/time format.'
      });
    }

    // Scheduled time must be in the future
    if (proposedDate < new Date()) {
      return res.status(400).json({
        success: false,
        message: 'Scheduled time must be in the future.'
      });
    }

    // Find target proposal
    const proposal = await Proposal.findById(proposalId);
    if (!proposal) {
      return res.status(404).json({
        success: false,
        message: 'Proposal not found.'
      });
    }

    // Verify current user is the mentor for this proposal
    if (proposal.mentor.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: 'Only the assigned mentor can schedule this session.'
      });
    }

    // Verify proposal has been accepted
    if (proposal.status !== 'accepted') {
      return res.status(400).json({
        success: false,
        message: 'Proposal must be accepted before scheduling a session.'
      });
    }

    // Check for existing session on this proposal to prevent duplicate sessions
    const existingProposalSession = await Session.findOne({ proposal: proposalId });
    if (existingProposalSession) {
      return res.status(400).json({
        success: false,
        message: 'Session has already been scheduled for this request.'
      });
    }

    // Simple time conflict check for both mentor and student:
    // Check if either mentor or student has a scheduled session within a 30-minute window
    const startTimeWindow = new Date(proposedDate.getTime() - 29 * 60 * 1000);
    const endTimeWindow = new Date(proposedDate.getTime() + 29 * 60 * 1000);

    const conflict = await Session.findOne({
      status: 'scheduled',
      $or: [
        { mentor: proposal.mentor, scheduledTime: { $gte: startTimeWindow, $lte: endTimeWindow } },
        { student: proposal.student, scheduledTime: { $gte: startTimeWindow, $lte: endTimeWindow } }
      ]
    });

    if (conflict) {
      return res.status(400).json({
        success: false,
        message: 'Time slot is already occupied.'
      });
    }

    // Generate unique Jitsi Meet room link
    const roomName = `gyaansetu-${proposalId}-${Date.now().toString().slice(-6)}`;
    const meetingLink = `https://meet.jit.si/${roomName}`;

    // Create session record in database
    const session = await Session.create({
      proposal: proposalId,
      student: proposal.student,
      mentor: proposal.mentor,
      studentEmail: proposal.studentEmail,
      mentorEmail: proposal.mentorEmail,
      scheduledTime: proposedDate,
      meetingLink,
      status: 'scheduled'
    });

    const populatedSession = await Session.findById(session._id)
      .populate('student', 'name email')
      .populate('mentor', 'name email skills');

    return res.status(201).json({
      success: true,
      message: 'Session scheduled successfully.',
      data: populatedSession
    });
  } catch (error) {
    console.error('Create Session Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to schedule session.'
    });
  }
};

// @desc    Get all sessions for logged in user (where user is student OR mentor)
// @route   GET /api/sessions/my
// @access  Private
const getMySessions = async (req, res) => {
  try {
    const userId = req.user._id;

    // Fetch sessions where the current user is either the student or the mentor
    const sessions = await Session.find({
      $or: [{ student: userId }, { mentor: userId }]
    })
      .populate('student', 'name email')
      .populate('mentor', 'name email skills')
      .populate('proposal', 'doubt')
      .sort({ scheduledTime: 1 });

    return res.status(200).json({
      success: true,
      data: sessions
    });
  } catch (error) {
    console.error('Get My Sessions Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to fetch sessions.'
    });
  }
};

// @desc    Mark a scheduled session as completed
// @route   PATCH /api/sessions/:id/complete
// @access  Private (Mentor involved in session)
const completeSession = async (req, res) => {
  try {
    const sessionId = req.params.id;

    const session = await Session.findById(sessionId);
    if (!session) {
      return res.status(404).json({
        success: false,
        message: 'Session not found.'
      });
    }

    // Ownership check: Only the mentor involved in that session can mark it complete
    if (session.mentor.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: 'Unauthorized. Only the mentor can mark the session as complete.'
      });
    }

    session.status = 'completed';
    await session.save();

    const updatedSession = await Session.findById(sessionId)
      .populate('student', 'name email')
      .populate('mentor', 'name email skills');

    return res.status(200).json({
      success: true,
      message: 'Session marked as completed.',
      data: updatedSession
    });
  } catch (error) {
    console.error('Complete Session Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to complete session.'
    });
  }
};

module.exports = {
  createSession,
  getMySessions,
  completeSession
};
