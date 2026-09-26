import React, { useState } from 'react';
import API from '../services/api';
import { X, HelpCircle, CheckCircle } from 'lucide-react';

const RequestDoubtModal = ({ mentor, isOpen, onClose, onRequestSent }) => {
  const [doubt, setDoubt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen || !mentor) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');

    if (!doubt.trim()) {
      setError('Please describe your technical doubt.');
      return;
    }

    try {
      setLoading(true);
      const response = await API.post('/proposals', {
        mentorId: mentor._id,
        doubt
      });

      if (response.data.success) {
        setSuccessMsg('Request sent successfully!');
        setDoubt('');
        if (onRequestSent) onRequestSent(response.data.data);
        setTimeout(() => {
          setSuccessMsg('');
          onClose();
        }, 1200);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to send doubt request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="flex items-center space-x-2 text-blue-600 mb-2">
          <HelpCircle className="h-6 w-6" />
          <h2 className="text-xl font-bold text-gray-800">Ask a Doubt</h2>
        </div>

        <div className="bg-blue-50 p-3 rounded-md mb-4 text-sm text-blue-800">
          <span className="font-semibold">Mentor:</span> {mentor.name} ({mentor.email})
          <div className="flex flex-wrap gap-1 mt-1">
            {mentor.skills?.map((skill, idx) => (
              <span key={idx} className="bg-blue-200 text-blue-900 text-xs px-2 py-0.5 rounded">
                {skill}
              </span>
            ))}
          </div>
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
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Describe your technical doubt
            </label>
            <textarea
              rows="4"
              placeholder="e.g. I am confused about binary search recursion and how to handle low and high pointers..."
              value={doubt}
              onChange={(e) => setDoubt(e.target.value)}
              className="w-full border border-gray-300 rounded-md p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            ></textarea>
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
              {loading ? 'Sending...' : 'Send Request'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RequestDoubtModal;
