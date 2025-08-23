'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  User, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged
} from 'firebase/auth';
import { auth } from '@/components/firebase';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setUser(user);
        localStorage.setItem('userData', JSON.stringify({
          uid: user.uid,
          email: user.email,
          displayName: user.displayName,
          photoURL: user.photoURL,
          loginTime: new Date().toISOString(),
        }));
      } else {
        setUser(null);
        localStorage.removeItem('userData');
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      console.log('Attempting login with Firebase Auth...');
      console.log('Auth object:', auth);
      console.log('Auth app:', auth.app);
      
      if (!auth) {
        throw new Error('Firebase Auth is not initialized');
      }
      
      await signInWithEmailAndPassword(auth, email, password);
    } catch (error: any) {
      console.error('Login error:', error);
      console.error('Error code:', error.code);
      console.error('Error message:', error.message);
      
      // Provide user-friendly error messages
      switch (error.code) {
        case 'auth/configuration-not-found':
          throw new Error('Firebase Authentication is not configured. Please contact support.');
        case 'auth/user-not-found':
          throw new Error('No account found with this email address');
        case 'auth/wrong-password':
          throw new Error('Incorrect password');
        case 'auth/invalid-email':
          throw new Error('Invalid email address');
        case 'auth/user-disabled':
          throw new Error('This account has been disabled');
        case 'auth/too-many-requests':
          throw new Error('Too many failed attempts. Please try again later');
        default:
          throw new Error(error.message || 'Login failed. Please try again');
      }
    }
  };

  const signup = async (email: string, password: string): Promise<void> => {
    try {
      console.log('Attempting signup with Firebase Auth...');
      console.log('Auth object:', auth);
      
      if (!auth) {
        throw new Error('Firebase Auth is not initialized');
      }
      
      await createUserWithEmailAndPassword(auth, email, password);
    } catch (error: any) {
      console.error('Signup error:', error);
      console.error('Error code:', error.code);
      console.error('Error message:', error.message);
      
      // Provide user-friendly error messages
      switch (error.code) {
        case 'auth/configuration-not-found':
          throw new Error('Firebase Authentication is not configured. Please contact support.');
        case 'auth/email-already-in-use':
          throw new Error('An account with this email already exists');
        case 'auth/invalid-email':
          throw new Error('Invalid email address');
        case 'auth/weak-password':
          throw new Error('Password is too weak. Please choose a stronger password');
        case 'auth/operation-not-allowed':
          throw new Error('Email/password accounts are not enabled. Please contact support');
        default:
          throw new Error(error.message || 'Signup failed. Please try again');
      }
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await signOut(auth);
      setUser(null);
      localStorage.removeItem('userData');
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
