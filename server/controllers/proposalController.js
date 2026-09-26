const Proposal = require('../models/Proposal');
const User = require('../models/User');

// @desc    Create a new doubt proposal request to a mentor
// @route   POST /api/proposals
// @access  Private (Any logged in user acting as student)
const createProposal = async (req, res) => {
  try {
    const { mentorId, doubt } = req.body;
    const studentId = req.user._id;

    if (!mentorId || !doubt) {
      return res.status(400).json({
        success: false,
        message: 'Mentor and doubt description are required.'
      });
    }

    // Check whether student is trying to request themselves
    if (studentId.toString() === mentorId.toString()) {
      return res.status(400).json({
        success: false,
        message: 'You cannot request yourself.'
      });
    }

    // Verify selected mentor exists and is actually registered as a mentor
    const targetMentor = await User.findById(mentorId);
    if (!targetMentor || !targetMentor.isMentor) {
      return res.status(404).json({
        success: false,
        message: 'Mentor not found.'
      });
    }

    // Check for duplicate pending requests between the same student and mentor
    const existingActiveRequest = await Proposal.findOne({
      student: studentId,
      mentor: mentorId,
      status: 'pending'
    });

    if (existingActiveRequest) {
      return res.status(400).json({
        success: false,
        message: 'An active request already exists.'
      });
    }

    // Create proposal document
    const proposal = await Proposal.create({
      student: studentId,
      mentor: mentorId,
      studentEmail: req.user.email,
      mentorEmail: targetMentor.email,
      doubt,
      status: 'pending'
    });

    const populatedProposal = await Proposal.findById(proposal._id)
      .populate('mentor', 'name email skills')
      .populate('student', 'name email');

    return res.status(201).json({
      success: true,
      message: 'Request sent successfully.',
      data: populatedProposal
    });
  } catch (error) {
    console.error('Create Proposal Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to send doubt request.'
    });
  }
};

// @desc    Get proposals sent by the logged-in user as a student
// @route   GET /api/proposals/my
// @access  Private
const getMyProposals = async (req, res) => {
  try {
    // Query proposals where current user is the student
    const proposals = await Proposal.find({ student: req.user._id })
      .populate('mentor', 'name email skills')
      .sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      data: proposals
    });
  } catch (error) {
    console.error('Get My Proposals Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to fetch student requests.'
    });
  }
};

// @desc    Get proposals received by the logged-in user as a mentor
// @route   GET /api/proposals/received
// @access  Private (Mentors)
const getReceivedProposals = async (req, res) => {
  try {
    // Query proposals where current user is the mentor
    const proposals = await Proposal.find({ mentor: req.user._id })
      .populate('student', 'name email')
      .sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      data: proposals
    });
  } catch (error) {
    console.error('Get Received Proposals Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to fetch received mentor requests.'
    });
  }
};

// @desc    Accept a doubt proposal (by receiving mentor)
// @route   PATCH /api/proposals/:id/accept
// @access  Private (Mentor who received request)
const acceptProposal = async (req, res) => {
  try {
    const proposalId = req.params.id;

    const proposal = await Proposal.findById(proposalId);
    if (!proposal) {
      return res.status(404).json({
        success: false,
        message: 'Request not found.'
      });
    }

    // Ownership check: Only the mentor who received this request can accept it
    if (proposal.mentor.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: 'Unauthorized action.'
      });
    }

    proposal.status = 'accepted';
    await proposal.save();

    const updatedProposal = await Proposal.findById(proposalId)
      .populate('student', 'name email')
      .populate('mentor', 'name email skills');

    return res.status(200).json({
      success: true,
      message: 'Request accepted successfully.',
      data: updatedProposal
    });
  } catch (error) {
    console.error('Accept Proposal Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to accept request.'
    });
  }
};

// @desc    Reject a doubt proposal (by receiving mentor)
// @route   PATCH /api/proposals/:id/reject
// @access  Private (Mentor who received request)
const rejectProposal = async (req, res) => {
  try {
    const proposalId = req.params.id;

    const proposal = await Proposal.findById(proposalId);
    if (!proposal) {
      return res.status(404).json({
        success: false,
        message: 'Request not found.'
      });
    }

    // Ownership check: Only the mentor who received this request can reject it
    if (proposal.mentor.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: 'Unauthorized action.'
      });
    }

    proposal.status = 'rejected';
    await proposal.save();

    return res.status(200).json({
      success: true,
      message: 'Request rejected.',
      data: proposal
    });
  } catch (error) {
    console.error('Reject Proposal Error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to reject request.'
    });
  }
};

module.exports = {
  createProposal,
  getMyProposals,
  getReceivedProposals,
  acceptProposal,
  rejectProposal
};
