import React, { useState, useEffect, useContext } from 'react';
import API from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { Calendar, Video, CheckCircle, Clock, ExternalLink } from 'lucide-react';

const Sessions = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [completingId, setCompletingId] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      setLoading(true);
      const response = await API.get('/sessions/my');
      if (response.data.success) {
        setSessions(response.data.data);
      }
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteSession = async (sessionId) => {
    try {
      setCompletingId(sessionId);
      const response = await API.patch(`/sessions/${sessionId}/complete`);
      if (response.data.success) {
        fetchSessions();
      }
    } catch (error) {
      console.error('Failed to complete session:', error);
    } finally {
      setCompletingId(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Mentoring Sessions</h1>
        <p className="text-gray-600 text-sm mt-1">
          View scheduled 1-on-1 sessions, join virtual Jitsi meetings, and track session status
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : sessions.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-lg p-12 text-center text-gray-500">
          <Calendar className="h-12 w-12 mx-auto mb-3 text-gray-400" />
          <p className="text-lg font-semibold text-gray-700">No Sessions Found</p>
          <p className="text-sm mt-1">You don't have any scheduled or completed sessions yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sessions.map((session) => {
            const isMentor = session.mentor?._id === user?._id;
            const isCompleted = session.status === 'completed';

            return (
              <div
                key={session._id}
                className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <span
                      className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                        isCompleted
                          ? 'bg-gray-100 text-gray-700'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {isCompleted ? '✓ Completed' : '🗓️ Scheduled'}
                    </span>
                    <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                      Role: {isMentor ? 'Mentor' : 'Student'}
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <h3 className="font-bold text-gray-900 text-lg">
                      {session.proposal?.doubt ? `"${session.proposal.doubt}"` : 'Mentoring Session'}
                    </h3>
                    
                    <div className="text-sm text-gray-700 space-y-1">
                      <p><span className="font-semibold">Mentor:</span> {session.mentor?.name} ({session.mentorEmail})</p>
                      <p><span className="font-semibold">Student:</span> {session.student?.name} ({session.studentEmail})</p>
                      <p className="flex items-center space-x-1 text-gray-600 text-xs">
                        <Clock className="h-3.5 w-3.5" />
                        <span>Scheduled: {new Date(session.scheduledTime).toLocaleString()}</span>
                      </p>
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-gray-100 flex flex-wrap items-center justify-between gap-3">
                  {/* Jitsi Meeting Link button */}
                  <a
                    href={session.meetingLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs px-4 py-2 rounded-lg transition flex items-center space-x-1.5"
                  >
                    <Video className="h-4 w-4" />
                    <span>Join Meeting</span>
                    <ExternalLink className="h-3 w-3 ml-0.5" />
                  </a>

                  {/* Mark Complete button (Visible only to mentor when status is 'scheduled') */}
                  {isMentor && !isCompleted && (
                    <button
                      onClick={() => handleCompleteSession(session._id)}
                      disabled={completingId === session._id}
                      className="bg-green-600 hover:bg-green-700 text-white font-medium text-xs px-3.5 py-2 rounded-lg transition flex items-center space-x-1 disabled:opacity-50"
                    >
                      <CheckCircle className="h-4 w-4" />
                      <span>{completingId === session._id ? 'Completing...' : 'Mark Complete'}</span>
                    </button>
                  )}
                </div>

              </div>
            );
          })}
        </div>
      )}

    </div>
  );
};

export default Sessions;
