import React, { createContext, useState, useEffect } from 'react';
import API from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('gyaansetu_token') || null);
  const [loading, setLoading] = useState(true);

  // Sync user details on mount if token exists
  useEffect(() => {
    const checkLoggedInUser = async () => {
      if (token) {
        try {
          const response = await API.get('/auth/me');
          if (response.data.success) {
            setUser(response.data.user);
          }
        } catch (error) {
          console.error('Failed to sync current user:', error);
          logout();
        }
      }
      setLoading(false);
    };

    checkLoggedInUser();
  }, [token]);

  // Login handler
  const login = (userData, userToken) => {
    localStorage.setItem('gyaansetu_token', userToken);
    localStorage.setItem('gyaansetu_user', JSON.stringify(userData));
    setToken(userToken);
    setUser(userData);
  };

  // Register handler
  const register = (userData, userToken) => {
    localStorage.setItem('gyaansetu_token', userToken);
    localStorage.setItem('gyaansetu_user', JSON.stringify(userData));
    setToken(userToken);
    setUser(userData);
  };

  // Logout handler
  const logout = () => {
    localStorage.removeItem('gyaansetu_token');
    localStorage.removeItem('gyaansetu_user');
    setToken(null);
    setUser(null);
  };

  // Update user state when user becomes a mentor or updates skills
  const updateUser = (updatedUser) => {
    setUser(updatedUser);
    localStorage.setItem('gyaansetu_user', JSON.stringify(updatedUser));
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};
