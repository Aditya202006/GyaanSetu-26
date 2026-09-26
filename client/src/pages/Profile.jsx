import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import API from '../services/api';
import { User, Mail, Award, CheckCircle, Edit3 } from 'lucide-react';

const Profile = ({ onOpenBecomeMentor }) => {
  const { user, updateUser } = useContext(AuthContext);

  const [skills, setSkills] = useState(user?.skills?.join(', ') || '');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleUpdateSkills = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      setLoading(true);
      const response = await API.patch('/users/update-skills', { skills });
      if (response.data.success) {
        updateUser(response.data.user);
        setMessage('Skills updated successfully.');
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update skills.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-6">
        
        <div className="flex items-center space-x-4 border-b border-gray-200 pb-6">
          <div className="w-16 h-16 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-bold text-2xl">
            {user?.name?.charAt(0)}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{user?.name}</h1>
            <p className="text-sm text-gray-500 flex items-center space-x-1 mt-1">
              <Mail className="h-4 w-4" />
              <span>{user?.email}</span>
            </p>
          </div>
        </div>

        {/* Mentor Status */}
        <div className="bg-gray-50 p-4 rounded-lg flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Award className={`h-6 w-6 ${user?.isMentor ? 'text-amber-500' : 'text-gray-400'}`} />
            <div>
              <p className="text-sm font-bold text-gray-900">Mentor Status</p>
              <p className="text-xs text-gray-500">
                {user?.isMentor
                  ? 'Active Mentor - You can receive student doubt requests'
                  : 'Student Account - Click below to register as a mentor'}
              </p>
            </div>
          </div>

          {!user?.isMentor && (
            <button
              onClick={onOpenBecomeMentor}
              className="bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold px-4 py-2 rounded-md transition shadow-sm"
            >
              Become a Mentor
            </button>
          )}
        </div>

        {/* Mentor Skills Editor (Visible if user is mentor) */}
        {user?.isMentor && (
          <div className="space-y-4 pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-2">
              <Edit3 className="h-5 w-5 text-blue-600" />
              <h2 className="text-lg font-bold text-gray-900">Manage Technical Skills</h2>
            </div>

            {message && (
              <div className="bg-green-50 text-green-700 p-3 rounded-md text-sm flex items-center space-x-2">
                <CheckCircle className="h-4 w-4" />
                <span>{message}</span>
              </div>
            )}

            {error && (
              <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleUpdateSkills} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Skills (comma-separated)
                </label>
                <input
                  type="text"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                  placeholder="e.g. Java, DSA, SQL, React"
                  className="w-full border border-gray-300 rounded-md p-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-1.5">
                  {user.skills?.map((s, idx) => (
                    <span key={idx} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-1 rounded">
                      {s}
                    </span>
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-md transition disabled:opacity-50"
                >
                  {loading ? 'Updating...' : 'Update Skills'}
                </button>
              </div>
            </form>
          </div>
        )}

      </div>
    </div>
  );
};

export default Profile;
