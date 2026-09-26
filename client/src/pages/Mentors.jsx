import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';
import { AuthContext } from '../context/AuthContext';
import RequestDoubtModal from '../components/RequestDoubtModal';
import { Search, GraduationCap, Mail, MessageSquarePlus, Award } from 'lucide-react';

const Mentors = () => {
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [isRequestModalOpen, setIsRequestModalOpen] = useState(false);

  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchMentors();
  }, []);

  const fetchMentors = async () => {
    try {
      setLoading(true);
      const response = await API.get('/mentors');
      if (response.data.success) {
        setMentors(response.data.data);
      }
    } catch (error) {
      console.error('Failed to fetch mentors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenRequestModal = (mentor) => {
    if (!user) {
      navigate('/login');
      return;
    }
    setSelectedMentor(mentor);
    setIsRequestModalOpen(true);
  };

  // Simple search filter by mentor name or skills
  const filteredMentors = mentors.filter((mentor) => {
    const term = searchTerm.toLowerCase();
    const nameMatch = mentor.name.toLowerCase().includes(term);
    const skillMatch = mentor.skills?.some((skill) => skill.toLowerCase().includes(term));
    return nameMatch || skillMatch;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Header & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Find a Mentor</h1>
          <p className="text-gray-600 text-sm mt-1">
            Browse verified mentors by skills and send a doubt request
          </p>
        </div>

        <div className="relative max-w-xs w-full">
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search by name or skill..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Mentors Grid */}
      {loading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : filteredMentors.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-lg p-12 text-center text-gray-500">
          <GraduationCap className="h-12 w-12 mx-auto mb-3 text-gray-400" />
          <p className="text-lg font-semibold text-gray-700">No Mentors Found</p>
          <p className="text-sm mt-1">Try adjusting your search terms.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMentors.map((mentor) => {
            const isSelf = user && user._id === mentor._id;

            return (
              <div
                key={mentor._id}
                className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-bold text-lg">
                        {mentor.name.charAt(0)}
                      </div>
                      <div>
                        <h3 className="font-bold text-gray-900 text-lg">{mentor.name}</h3>
                        <p className="text-xs text-gray-500 flex items-center space-x-1">
                          <Mail className="h-3 w-3" />
                          <span>{mentor.email}</span>
                        </p>
                      </div>
                    </div>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-green-100 text-green-800">
                      <Award className="h-3 w-3 mr-1" />
                      Mentor
                    </span>
                  </div>

                  <div className="mt-4 mb-6">
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                      Technical Skills
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {mentor.skills && mentor.skills.length > 0 ? (
                        mentor.skills.map((skill, index) => (
                          <span
                            key={index}
                            className="bg-blue-50 text-blue-700 border border-blue-100 text-xs px-2.5 py-1 rounded-md font-medium"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-gray-400 italic">No skills listed</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Action button logic: Hide request button for self */}
                <div>
                  {isSelf ? (
                    <div className="w-full bg-gray-100 text-gray-500 text-xs font-medium py-2 rounded-lg text-center cursor-not-allowed">
                      This is Your Mentor Profile
                    </div>
                  ) : (
                    <button
                      onClick={() => handleOpenRequestModal(mentor)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm py-2 px-4 rounded-lg transition flex items-center justify-center space-x-2"
                    >
                      <MessageSquarePlus className="h-4 w-4" />
                      <span>Ask Doubt</span>
                    </button>
                  )}
                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* Request Modal */}
      <RequestDoubtModal
        mentor={selectedMentor}
        isOpen={isRequestModalOpen}
        onClose={() => setIsRequestModalOpen(false)}
      />

    </div>
  );
};

export default Mentors;
