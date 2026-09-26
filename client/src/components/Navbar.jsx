import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { GraduationCap, User, LogOut, Award, Calendar, Home, Users, LayoutDashboard } from 'lucide-react';

const Navbar = ({ onOpenBecomeMentor }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          
          {/* Brand Logo & Main Nav */}
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2 text-blue-600 font-bold text-xl">
              <GraduationCap className="h-7 w-7 text-blue-600" />
              <span>GyaanSetu</span>
            </Link>

            <div className="hidden md:flex space-x-4 text-sm font-medium text-gray-700">
              <Link to="/" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:text-blue-600 hover:bg-gray-50">
                <Home className="h-4 w-4" />
                <span>Home</span>
              </Link>
              <Link to="/mentors" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:text-blue-600 hover:bg-gray-50">
                <Users className="h-4 w-4" />
                <span>Mentors</span>
              </Link>
              {user && (
                <>
                  <Link to="/dashboard" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:text-blue-600 hover:bg-gray-50">
                    <LayoutDashboard className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                  <Link to="/sessions" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:text-blue-600 hover:bg-gray-50">
                    <Calendar className="h-4 w-4" />
                    <span>Sessions</span>
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Right Action Items */}
          <div className="flex items-center space-x-3">
            {user ? (
              <>
                {/* Mentor Status or Become Mentor Action */}
                {!user.isMentor ? (
                  <button
                    onClick={onOpenBecomeMentor}
                    className="flex items-center space-x-1 bg-amber-500 hover:bg-amber-600 text-white text-xs sm:text-sm font-medium px-3 py-1.5 rounded-md transition shadow-sm"
                  >
                    <Award className="h-4 w-4" />
                    <span>Become a Mentor</span>
                  </button>
                ) : (
                  <span className="hidden sm:inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                    <Award className="h-3.5 w-3.5 mr-1" />
                    Mentor Account
                  </span>
                )}

                <Link
                  to="/profile"
                  className="flex items-center space-x-1 text-sm font-medium text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md"
                >
                  <User className="h-4 w-4" />
                  <span className="hidden sm:inline">{user.name}</span>
                </Link>

                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-sm text-red-600 hover:text-red-700 px-3 py-2 rounded-md hover:bg-red-50"
                  title="Logout"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-sm font-medium text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-md transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
