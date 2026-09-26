import React, { useState, useContext } from 'react';
import API from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { X, Award, CheckCircle } from 'lucide-react';

const BecomeMentorModal = ({ isOpen, onClose }) => {
  const { user, updateUser } = useContext(AuthContext);
  const [skills, setSkills] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');

    if (!skills.trim()) {
      setError('Please enter at least one technical skill.');
      return;
    }

    try {
      setLoading(true);
      const response = await API.patch('/users/become-mentor', { skills });
      if (response.data.success) {
        updateUser(response.data.user);
        setSuccessMsg('Awesome! You are now a registered mentor.');
        setTimeout(() => {
          setSuccessMsg('');
          onClose();
        }, 1200);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to upgrade to mentor.');
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
          <Award className="h-6 w-6" />
          <h2 className="text-xl font-bold text-gray-800">Become a Mentor</h2>
        </div>

        <p className="text-sm text-gray-600 mb-4">
          Share your knowledge with fellow students! Add your technical skills below to get started. You can still use all student features.
        </p>

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
              Your Name
            </label>
            <input
              type="text"
              disabled
              value={user?.name || ''}
              className="w-full bg-gray-100 border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-600 cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Technical Skills (comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. Java, DSA, SQL, React, Node.js"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Example: Java, DSA, SQL
            </p>
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
              {loading ? 'Updating...' : 'Register as Mentor'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BecomeMentorModal;
