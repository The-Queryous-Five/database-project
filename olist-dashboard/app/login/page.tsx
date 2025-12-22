'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { LogIn, LogOut, User, Lock, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

const API_BASE = 'http://localhost:5000';

interface UserInfo {
  username: string;
  name: string;
  role: string;
  logged_in_at?: string;
}

export default function LoginPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();
  
  // Form state
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    setMounted(true);
    checkLoginStatus();
  }, []);

  const checkLoginStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/auth/me`, { withCredentials: true });
      if (res.data.logged_in) {
        setIsLoggedIn(true);
        setUser(res.data.user);
      }
    } catch (err) {
      console.error('Error checking login status:', err);
    } finally {
      setLoading(false);
    }
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!username.trim()) {
      errors.username = 'Username is required';
    }
    if (!password) {
      errors.password = 'Password is required';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setError(null);
    
    try {
      const res = await axios.post(`${API_BASE}/auth/login`, {
        username: username.trim(),
        password
      }, { withCredentials: true });
      
      setIsLoggedIn(true);
      setUser(res.data.user);
      setUsername('');
      setPassword('');
      
      // Redirect to dashboard
      setTimeout(() => router.push('/'), 1000);
    } catch (err: unknown) {
      const errorMsg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Login failed';
      setError(errorMsg);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${API_BASE}/auth/logout`, {}, { withCredentials: true });
      setIsLoggedIn(false);
      setUser(null);
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  if (!mounted || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Session Management</h1>
        <p className="text-gray-400">Login / Logout functionality with session handling</p>
      </div>

      {/* Info Box */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-2xl p-6">
        <h3 className="text-blue-400 font-semibold mb-2 flex items-center gap-2">
          <User className="w-5 h-5" />
          Demo Credentials
        </h3>
        <div className="text-gray-300 text-sm space-y-1">
          <p><strong>Admin:</strong> username: <code className="bg-white/10 px-2 py-1 rounded">admin</code> / password: <code className="bg-white/10 px-2 py-1 rounded">admin123</code></p>
          <p><strong>User:</strong> username: <code className="bg-white/10 px-2 py-1 rounded">demo</code> / password: <code className="bg-white/10 px-2 py-1 rounded">demo123</code></p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Login Form */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <LogIn className="w-6 h-6" />
            Login (SESSION)
          </h2>

          {error && (
            <div className="bg-red-500/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              {error}
            </div>
          )}

          {isLoggedIn ? (
            <div className="space-y-4">
              <div className="bg-green-500/20 border border-green-500 text-green-400 px-4 py-3 rounded-lg">
                ✓ You are logged in!
              </div>
              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </div>
          ) : (
            <form onSubmit={handleLogin} className="space-y-4">
              {/* Username (Text Box) */}
              <div>
                <label className="block text-gray-400 mb-2">Username (TEXT BOX)</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username..."
                    className="w-full bg-white/5 text-white rounded-lg pl-10 pr-4 py-3 outline-none border border-white/20 focus:border-blue-500"
                  />
                </div>
                {formErrors.username && <p className="text-red-400 text-sm mt-1">{formErrors.username}</p>}
              </div>

              {/* Password (Text Box) */}
              <div>
                <label className="block text-gray-400 mb-2">Password (TEXT BOX)</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password..."
                    className="w-full bg-white/5 text-white rounded-lg pl-10 pr-4 py-3 outline-none border border-white/20 focus:border-blue-500"
                  />
                </div>
                {formErrors.password && <p className="text-red-400 text-sm mt-1">{formErrors.password}</p>}
              </div>

              {/* Remember Me (Checkbox) */}
              <div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-5 h-5 rounded bg-white/10 border-white/30 text-blue-500 focus:ring-blue-500"
                  />
                  <span className="text-white">Remember me (CHECK BOX)</span>
                </label>
              </div>

              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg transition-colors"
              >
                <LogIn className="w-5 h-5" />
                Login
              </button>
            </form>
          )}
        </div>

        {/* Current Session Info */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <User className="w-6 h-6" />
            Session Info
          </h2>

          {isLoggedIn && user ? (
            <div className="space-y-4">
              <div className="bg-white/5 rounded-lg p-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-400 text-sm">Username</p>
                    <p className="text-white font-semibold">{user.username}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Name</p>
                    <p className="text-white font-semibold">{user.name}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Role</p>
                    <p className="text-white font-semibold">
                      <span className={`px-2 py-1 rounded text-xs ${
                        user.role === 'admin' ? 'bg-purple-500/20 text-purple-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {user.role.toUpperCase()}
                      </span>
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Logged in at</p>
                    <p className="text-white font-semibold text-sm">
                      {user.logged_in_at ? new Date(user.logged_in_at).toLocaleString('en-US') : '-'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                <p className="text-green-400 text-sm">
                  ✓ Session is active. Your authentication state is maintained server-side using Flask sessions.
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-white/5 rounded-lg p-8 text-center">
              <User className="w-16 h-16 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No active session</p>
              <p className="text-gray-500 text-sm mt-2">Please login to see session information</p>
            </div>
          )}
        </div>
      </div>

      {/* Session Features Info */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h3 className="text-xl font-bold text-white mb-4">Session Implementation Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">Backend (Flask)</h4>
            <ul className="text-gray-400 text-sm space-y-1">
              <li>• Flask session management</li>
              <li>• Secret key for encryption</li>
              <li>• CORS with credentials</li>
            </ul>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">Endpoints</h4>
            <ul className="text-gray-400 text-sm space-y-1">
              <li>• POST /auth/login</li>
              <li>• POST /auth/logout</li>
              <li>• GET /auth/me</li>
            </ul>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">UI Components Used</h4>
            <ul className="text-gray-400 text-sm space-y-1">
              <li>• Text boxes (username, password)</li>
              <li>• Checkbox (remember me)</li>
              <li>• Validation messages</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
