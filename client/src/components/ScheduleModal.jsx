import React, { useState } from 'react';
import API from '../services/api';
import { X, Calendar, Clock, CheckCircle } from 'lucide-react';

const ScheduleModal = ({ proposal, isOpen, onClose, onSessionScheduled }) => {
  const [scheduledTime, setScheduledTime] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen || !proposal) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');

    if (!scheduledTime) {
      setError('Please select date and time for the session.');
      return;
    }

    try {
      setLoading(true);
      const response = await API.post('/sessions', {
        proposalId: proposal._id,
        scheduledTime
      });

      if (response.data.success) {
        setSuccessMsg('Session scheduled successfully!');
        if (onSessionScheduled) onSessionScheduled(response.data.data);
        setTimeout(() => {
          setSuccessMsg('');
          onClose();
        }, 1200);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to schedule session.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="flex items-center space-x-2 text-blue-600 mb-4">
          <Calendar className="h-6 w-6" />
          <h2 className="text-xl font-bold text-gray-800">Schedule Mentoring Session</h2>
        </div>

        <div className="bg-gray-50 p-3 rounded-md mb-4 text-sm text-gray-700 space-y-1">
          <div><span className="font-semibold">Student:</span> {proposal.student?.name} ({proposal.studentEmail})</div>
          <div><span className="font-semibold">Doubt:</span> {proposal.doubt}</div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm mb-4">
            {error}
          </div>
        )}

        {successMsg && (
          <div className="bg-green-50 text-green-700 p-3 rounded-md text-sm mb-4 flex items-center space-x-2">
            <CheckCircle className="h-5 w-5" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center space-x-1">
              <Clock className="h-4 w-4 text-gray-500" />
              <span>Select Date & Time</span>
            </label>
            <input
              type="datetime-local"
              value={scheduledTime}
              onChange={(e) => setScheduledTime(e.target.value)}
              className="w-full border border-gray-300 rounded-md p-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-2 rounded-md transition disabled:opacity-50"
            >
              {loading ? 'Scheduling...' : 'Schedule & Send Email'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ScheduleModal;
