import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { GraduationCap, Search, MessageSquare, Calendar, Users, Award, ArrowRight } from 'lucide-react';

const Home = ({ onOpenBecomeMentor }) => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleBecomeMentorClick = () => {
    if (!user) {
      navigate('/login');
    } else {
      onOpenBecomeMentor();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-blue-50 to-white py-16 md:py-24">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-800 text-xs sm:text-sm font-semibold px-4 py-1.5 rounded-full mb-6">
            <GraduationCap className="h-4 w-4" />
            <span>Peer-to-Peer Technical Doubt Solving</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tight mb-4">
            GyaanSetu
          </h1>

          <p className="text-xl md:text-2xl font-semibold text-blue-600 mb-6">
            "Connect. Learn. Solve."
          </p>

          <p className="text-gray-600 text-base md:text-lg max-w-2xl mx-auto mb-8 leading-relaxed">
            Find mentors, ask technical doubts and learn from other students in a structured, 1-on-1 virtual session environment.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <Link
              to="/mentors"
              className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg flex items-center justify-center space-x-2 transition shadow-md"
            >
              <Search className="h-5 w-5" />
              <span>Find a Mentor</span>
            </Link>

            <button
              onClick={handleBecomeMentorClick}
              className="w-full sm:w-auto bg-amber-500 hover:bg-amber-600 text-white font-medium px-6 py-3 rounded-lg flex items-center justify-center space-x-2 transition shadow-md"
            >
              <Award className="h-5 w-5" />
              <span>Become a Mentor</span>
            </button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 max-w-6xl mx-auto px-4">
        <h2 className="text-2xl md:text-3xl font-bold text-center text-gray-900 mb-12">
          How GyaanSetu Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition text-center">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="h-6 w-6" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Find Mentors</h3>
            <p className="text-sm text-gray-600">
              Search by technical skills like Java, React, Python, DSA, or SQL to find experienced mentors.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition text-center">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="h-6 w-6" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Ask Doubts</h3>
            <p className="text-sm text-gray-600">
              Send detailed technical doubt requests directly to your chosen mentor.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition text-center">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <Calendar className="h-6 w-6" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Schedule Sessions</h3>
            <p className="text-sm text-gray-600">
              Mentors accept requests and schedule 1-on-1 sessions at conflict-free time slots.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition text-center">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="h-6 w-6" />
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Learn Together</h3>
            <p className="text-sm text-gray-600">
              Join 1-on-1 Jitsi video calls with email alerts and clear doubt resolution.
            </p>
          </div>

        </div>
      </section>

      {/* Single Account Callout */}
      <section className="bg-blue-600 text-white py-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">
            One Account for Everything
          </h2>
          <p className="text-blue-100 text-base md:text-lg mb-6">
            Every user starts as a student. Want to share your knowledge? Click "Become a Mentor" anytime to enable mentor features on the exact same account!
          </p>
          {!user ? (
            <Link
              to="/register"
              className="inline-flex items-center space-x-2 bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg hover:bg-blue-50 transition"
            >
              <span>Get Started Now</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          ) : (
            <Link
              to="/dashboard"
              className="inline-flex items-center space-x-2 bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg hover:bg-blue-50 transition"
            >
              <span>Go to Dashboard</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          )}
        </div>
      </section>

    </div>
  );
};

export default Home;
