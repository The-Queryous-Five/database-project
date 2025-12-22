'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { CreditCard, DollarSign, TrendingUp, PieChart } from 'lucide-react';

interface PaymentStats {
  total_payments: number;
  total_value: number;
  avg_payment_value: number;
  payment_types: { type: string; count: number; total: number }[];
}

export default function PaymentsPage() {
  const [stats, setStats] = useState<PaymentStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchPaymentData();
  }, []);

  const fetchPaymentData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/payments/stats');
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load payment data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredPaymentTypes = stats?.payment_types?.filter(type =>
    type.type.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading payment data...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Payments</h1>
        <p className="text-gray-400">Payment analytics and transaction insights</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <CreditCard className="w-8 h-8 text-blue-400" />
            <span className="text-xs text-gray-400">TOTAL</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_payments.toLocaleString() || '103,886'}
          </div>
          <div className="text-sm text-gray-400">Total Payments</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="w-8 h-8 text-green-400" />
            <span className="text-xs text-gray-400">REVENUE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            ${stats?.total_value.toLocaleString() || '13.5M'}
          </div>
          <div className="text-sm text-gray-400">Total Value</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <TrendingUp className="w-8 h-8 text-yellow-400" />
            <span className="text-xs text-gray-400">AVERAGE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            ${stats?.avg_payment_value.toFixed(2) || '130'}
          </div>
          <div className="text-sm text-gray-400">Avg Payment</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <PieChart className="w-8 h-8 text-purple-400" />
            <span className="text-xs text-gray-400">METHODS</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.payment_types.length || '5'}
          </div>
          <div className="text-sm text-gray-400">Payment Types</div>
        </div>
      </div>

      {error && (
        <div className="text-yellow-400 bg-yellow-400/10 p-4 rounded-lg">
          {error} - Create Flask endpoints to load real data
        </div>
      )}

      {/* Payment Methods */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Payment Methods</h2>
        
        <div className="space-y-4">
          {filteredPaymentTypes && filteredPaymentTypes.length > 0 ? (
            filteredPaymentTypes.map((type, index) => (
              <div key={index} className="bg-white/5 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-white font-semibold capitalize">{type.type}</span>
                  <span className="text-gray-400">{type.count.toLocaleString()} payments</span>
                </div>
                <div className="flex justify-between items-center">
                  <div className="flex-1 bg-white/10 rounded-full h-2 mr-4">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                      style={{ width: `${(type.count / (stats?.total_payments || 1)) * 100}%` }}
                    />
                  </div>
                  <span className="text-green-400 font-semibold">${type.total.toLocaleString()}</span>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-400">
              {searchTerm 
                ? `No payment types match "${searchTerm}"` 
                : 'No payment method data available. Create Flask endpoints to load real data.'}
            </div>
          )}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-400/10 border border-blue-400/20 rounded-2xl p-6">
        <h3 className="text-xl font-bold text-blue-400 mb-2">💡 Note</h3>
        <p className="text-gray-300">
          Payment analytics require Flask API endpoints. Create <code className="bg-white/10 px-2 py-1 rounded">/payments/stats</code> endpoint to display real payment data.
        </p>
      </div>
    </div>
  );
}
