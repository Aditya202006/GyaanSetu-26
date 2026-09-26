import React, { useState, useEffect, useContext } from 'react';
import API from '../services/api';
import { AuthContext } from '../context/AuthContext';
import ScheduleModal from '../components/ScheduleModal';
import { LayoutDashboard, Award, Clock, CheckCircle2, XCircle, Calendar, Video, ArrowUpRight, HelpCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = ({ onOpenBecomeMentor }) => {
  const { user } = useContext(AuthContext);

  const [myProposals, setMyProposals] = useState([]);
  const [receivedProposals, setReceivedProposals] = useState([]);
  const [sessions, setSessions] = useState([]);

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState({});
  const [message, setMessage] = useState('');

  const [selectedProposalForSchedule, setSelectedProposalForSchedule] = useState(null);
  const [isScheduleModalOpen, setIsScheduleModalOpen] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // 1. Fetch student requests sent by current user
      const myRes = await API.get('/proposals/my');
      if (myRes.data.success) {
        setMyProposals(myRes.data.data);
      }

      // 2. Fetch sessions for current user (student or mentor)
      const sessRes = await API.get('/sessions/my');
      if (sessRes.data.success) {
        setSessions(sessRes.data.data);
      }

      // 3. If user is mentor, fetch incoming requests
      if (user?.isMentor) {
        const recRes = await API.get('/proposals/received');
        if (recRes.data.success) {
          setReceivedProposals(recRes.data.data);
        }
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptProposal = async (proposalId) => {
    try {
      setActionLoading((prev) => ({ ...prev, [proposalId]: true }));
      const response = await API.patch(`/proposals/${proposalId}/accept`);
      if (response.data.success) {
        setMessage('Request accepted successfully!');
        fetchDashboardData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (error) {
      console.error('Accept error:', error);
    } finally {
      setActionLoading((prev) => ({ ...prev, [proposalId]: false }));
    }
  };

  const handleRejectProposal = async (proposalId) => {
    try {
      setActionLoading((prev) => ({ ...prev, [proposalId]: true }));
      const response = await API.patch(`/proposals/${proposalId}/reject`);
      if (response.data.success) {
        setMessage('Request rejected.');
        fetchDashboardData();
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (error) {
      console.error('Reject error:', error);
    } finally {
      setActionLoading((prev) => ({ ...prev, [proposalId]: false }));
    }
  };

  const handleOpenScheduleModal = (proposal) => {
    setSelectedProposalForSchedule(proposal);
    setIsScheduleModalOpen(true);
  };

  // Status Badge Component
  const getStatusBadge = (status) => {
    if (status === 'accepted') {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          <CheckCircle2 className="h-3 w-3 mr-1" /> Accepted
        </span>
      );
    }
    if (status === 'rejected') {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
          <XCircle className="h-3 w-3 mr-1" /> Rejected
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
        <Clock className="h-3 w-3 mr-1" /> Pending
      </span>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Welcome Banner */}
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
            Welcome, {user?.name}!
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Manage your student doubt requests and mentoring sessions from one central dashboard.
          </p>
        </div>

        {/* Mentor CTA banner if isMentor is false */}
        {!user?.isMentor ? (
          <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-bold text-amber-800">Want to help other students?</p>
              <p className="text-xs text-amber-700">Become a mentor on this same account!</p>
            </div>
            <button
              onClick={onOpenBecomeMentor}
              className="bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold px-3 py-2 rounded-md transition whitespace-nowrap"
            >
              Become a Mentor
            </button>
          </div>
        ) : (
          <div className="bg-blue-50 border border-blue-200 px-4 py-2 rounded-lg flex items-center space-x-2 text-blue-800 text-sm font-semibold">
            <Award className="h-5 w-5 text-blue-600" />
            <span>Active Mentor Account</span>
          </div>
        )}
      </div>

      {message && (
        <div className="bg-green-50 text-green-700 p-3 rounded-md text-sm">
          {message}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="space-y-8">
          
          {/* ========================================= */}
          {/* STUDENT SECTION (Available to ALL Users)  */}
          {/* ========================================= */}
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-6">
            <div className="flex items-center space-x-2 border-b border-gray-200 pb-3">
              <HelpCircle className="h-5 w-5 text-blue-600" />
              <h2 className="text-xl font-bold text-gray-900">Student Section - My Doubt Requests</h2>
            </div>

            {myProposals.length === 0 ? (
              <div className="text-center py-8 text-gray-500 text-sm">
                You haven't sent any doubt requests yet.{' '}
                <Link to="/mentors" className="text-blue-600 font-medium hover:underline">
                  Find a mentor to ask a doubt!
                </Link>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {myProposals.map((prop) => (
                  <div key={prop._id} className="py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-1 max-w-2xl">
                      <div className="flex items-center space-x-3">
                        <span className="font-bold text-gray-900">Mentor: {prop.mentor?.name}</span>
                        <span className="text-xs text-gray-500">({prop.mentorEmail})</span>
                        {getStatusBadge(prop.status)}
                      </div>
                      <p className="text-sm text-gray-700 font-medium">Doubt: "{prop.doubt}"</p>
                      <p className="text-xs text-gray-400">Sent on: {new Date(prop.createdAt).toLocaleDateString()}</p>
                    </div>

                    {prop.status === 'accepted' && (
                      <div className="text-xs text-green-700 bg-green-50 px-3 py-1.5 rounded-md border border-green-200">
                        Request accepted! Check <Link to="/sessions" className="font-semibold underline">Sessions</Link> for meeting link.
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ========================================= */}
          {/* MENTOR SECTION (Visible if isMentor === true) */}
          {/* ========================================= */}
          {user?.isMentor && (
            <div className="bg-blue-50/50 border border-blue-200 rounded-xl p-6 shadow-sm space-y-6">
              <div className="flex items-center space-x-2 border-b border-blue-200 pb-3 text-blue-900">
                <Award className="h-6 w-6 text-blue-600" />
                <h2 className="text-xl font-bold">Mentor Section - Incoming Student Requests</h2>
              </div>

              {receivedProposals.length === 0 ? (
                <div className="text-center py-8 text-gray-500 text-sm">
                  No incoming student requests received yet.
                </div>
              ) : (
                <div className="space-y-4">
                  {receivedProposals.map((prop) => (
                    <div key={prop._id} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="space-y-1">
                        <div className="flex items-center space-x-3">
                          <span className="font-bold text-gray-900">Student: {prop.student?.name}</span>
                          <span className="text-xs text-gray-500">({prop.studentEmail})</span>
                          {getStatusBadge(prop.status)}
                        </div>
                        <p className="text-sm text-gray-800">Doubt: "{prop.doubt}"</p>
                        <p className="text-xs text-gray-400">Received on: {new Date(prop.createdAt).toLocaleDateString()}</p>
                      </div>

                      {/* Action buttons for receiving mentor */}
                      <div className="flex items-center space-x-2">
                        {prop.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleAcceptProposal(prop._id)}
                              disabled={actionLoading[prop._id]}
                              className="bg-green-600 hover:bg-green-700 text-white text-xs font-semibold px-3 py-1.5 rounded-md transition"
                            >
                              {actionLoading[prop._id] ? 'Processing...' : 'Accept'}
                            </button>
                            <button
                              onClick={() => handleRejectProposal(prop._id)}
                              disabled={actionLoading[prop._id]}
                              className="bg-red-600 hover:bg-red-700 text-white text-xs font-semibold px-3 py-1.5 rounded-md transition"
                            >
                              Reject
                            </button>
                          </>
                        )}

                        {prop.status === 'accepted' && (
                          <button
                            onClick={() => handleOpenScheduleModal(prop)}
                            className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-3 py-1.5 rounded-md transition flex items-center space-x-1"
                          >
                            <Calendar className="h-3.5 w-3.5" />
                            <span>Schedule Session</span>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* ========================================= */}
          {/* UPCOMING SESSIONS SUMMARY                 */}
          {/* ========================================= */}
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-gray-200 pb-3">
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5 text-blue-600" />
                <h2 className="text-xl font-bold text-gray-900">Upcoming & Scheduled Sessions</h2>
              </div>
              <Link to="/sessions" className="text-xs text-blue-600 font-semibold hover:underline flex items-center space-x-1">
                <span>View All Sessions</span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </Link>
            </div>

            {sessions.filter(s => s.status === 'scheduled').length === 0 ? (
              <div className="text-center py-6 text-gray-500 text-sm">
                No scheduled upcoming sessions found.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {sessions.filter(s => s.status === 'scheduled').map((sess) => (
                  <div key={sess._id} className="border border-blue-100 bg-blue-50/30 rounded-lg p-4 space-y-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="text-xs font-semibold text-blue-800 uppercase tracking-wider">
                          {sess.mentor?._id === user?._id ? 'Mentoring Student' : 'Session with Mentor'}
                        </p>
                        <h4 className="font-bold text-gray-900 text-base">
                          {sess.mentor?._id === user?._id ? sess.student?.name : sess.mentor?.name}
                        </h4>
                      </div>
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded font-semibold">
                        Scheduled
                      </span>
                    </div>

                    <p className="text-xs text-gray-600">
                      📅 {new Date(sess.scheduledTime).toLocaleString()}
                    </p>

                    <a
                      href={sess.meetingLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium px-3 py-1.5 rounded transition mt-2"
                    >
                      <Video className="h-3.5 w-3.5" />
                      <span>Join Jitsi Meeting</span>
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}

      {/* Schedule Modal */}
      <ScheduleModal
        proposal={selectedProposalForSchedule}
        isOpen={isScheduleModalOpen}
        onClose={() => setIsScheduleModalOpen(false)}
        onSessionScheduled={fetchDashboardData}
      />

    </div>
  );
};

export default Dashboard;
