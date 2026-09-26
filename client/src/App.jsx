import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import BecomeMentorModal from './components/BecomeMentorModal';
import ProtectedRoute from './components/ProtectedRoute';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Mentors from './pages/Mentors';
import Dashboard from './pages/Dashboard';
import Sessions from './pages/Sessions';
import Profile from './pages/Profile';

function App() {
  const [isBecomeMentorModalOpen, setIsBecomeMentorModalOpen] = useState(false);

  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-gray-50 text-gray-800">
          <Navbar onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />

          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/mentors" element={<Mentors />} />

              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/sessions"
                element={
                  <ProtectedRoute>
                    <Sessions />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <Profile onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>

          {/* Become Mentor Modal available globally across pages */}
          <BecomeMentorModal
            isOpen={isBecomeMentorModalOpen}
            onClose={() => setIsBecomeMentorModalOpen(false)}
          />

          <footer className="bg-white border-t border-gray-200 py-6 text-center text-xs text-gray-500">
            <p>GyaanSetu – Mentor-Student Doubt Solving Platform</p>
          </footer>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
