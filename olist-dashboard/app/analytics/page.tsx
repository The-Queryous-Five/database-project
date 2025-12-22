'use client';

import { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, Package, DollarSign, Star } from 'lucide-react';
import axios from 'axios';

interface SalesTrendData {
  month: string;
  orders: number;
  revenue: number;
}

interface SatisfactionData {
  avg_score: number;
  positive_pct: number;
  neutral_pct: number;
  negative_pct: number;
  total_reviews: number;
}

export default function AnalyticsPage() {
  const [salesTrend, setSalesTrend] = useState<SalesTrendData[]>([]);
  const [satisfaction, setSatisfaction] = useState<SatisfactionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      console.log('Fetching analytics data...');
      const [trendRes, satisfactionRes] = await Promise.all([
        axios.get('http://localhost:5000/analytics/sales-trend'),
        axios.get('http://localhost:5000/analytics/satisfaction')
      ]);
      console.log('Sales trend data:', trendRes.data);
      console.log('Satisfaction data:', satisfactionRes.data);
      setSalesTrend(trendRes.data);
      setSatisfaction(satisfactionRes.data);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate max revenue for chart scaling
  const maxRevenue = Math.max(...salesTrend.map(d => d.revenue), 1);

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Analytics</h1>
        <p className="text-gray-400">Advanced insights and data visualization from your database</p>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Trend */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Sales Trend (Last 12 Months)</h2>
            <TrendingUp className="w-6 h-6 text-green-400" />
          </div>
          
          {/* Debug Info */}
          <div className="mb-2 text-xs text-gray-500">
            Loading: {loading ? 'Yes' : 'No'} | Data count: {salesTrend.length} | Max revenue: {maxRevenue.toFixed(0)}
          </div>
          
          {loading ? (
            <div className="h-64 flex items-center justify-center">
              <div className="text-gray-400">Loading chart data...</div>
            </div>
          ) : salesTrend.length > 0 ? (
            <div className="h-64 flex items-end justify-around gap-2 bg-white/5 rounded-lg p-4">
              {salesTrend.map((data, i) => {
                const heightPercent = Math.max((data.revenue / maxRevenue) * 100, 5); // Minimum 5% height
                const monthLabel = data.month.split('-')[1]; // Get month number
                return (
                  <div key={i} className="flex-1 flex flex-col items-center gap-2 group relative">
                    <div 
                      className="w-full bg-gradient-to-t from-blue-500 to-purple-500 rounded-t-lg transition-all hover:opacity-80 cursor-pointer min-h-[20px]"
                      style={{ height: `${heightPercent}%` }}
                      title={`${data.month}\nOrders: ${data.orders.toLocaleString()}\nRevenue: $${(data.revenue / 1000000).toFixed(2)}M`}
                    >
                      <div className="w-full h-full"></div>
                    </div>
                    <span className="text-xs text-gray-400">{monthLabel}</span>
                    {/* Tooltip on hover */}
                    <div className="absolute bottom-full mb-2 hidden group-hover:block bg-black/90 text-white text-xs rounded px-2 py-1 whitespace-nowrap z-10">
                      {data.month}<br/>
                      Orders: {data.orders.toLocaleString()}<br/>
                      Revenue: ${(data.revenue / 1000000).toFixed(2)}M
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center">
              <div className="text-gray-400">No data available</div>
            </div>
          )}
        </div>

        {/* Category Performance */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Top Categories</h2>
            <BarChart3 className="w-6 h-6 text-yellow-400" />
          </div>
          <div className="space-y-4">
            {[
              { name: 'Electronics', value: 85, color: 'from-blue-500 to-blue-600' },
              { name: 'Fashion', value: 72, color: 'from-purple-500 to-purple-600' },
              { name: 'Home & Garden', value: 68, color: 'from-green-500 to-green-600' },
              { name: 'Sports', value: 54, color: 'from-yellow-500 to-yellow-600' },
              { name: 'Beauty', value: 45, color: 'from-pink-500 to-pink-600' },
            ].map((category, i) => (
              <div key={i}>
                <div className="flex justify-between mb-1">
                  <span className="text-white">{category.name}</span>
                  <span className="text-gray-400">{category.value}%</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className={`bg-gradient-to-r ${category.color} h-2 rounded-full transition-all`}
                    style={{ width: `${category.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Customer Satisfaction */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Customer Satisfaction</h2>
          <Star className="w-6 h-6 text-yellow-400 fill-yellow-400" />
        </div>
        
        {loading ? (
          <div className="text-center text-gray-400 py-8">Loading satisfaction data...</div>
        ) : satisfaction ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-5xl font-bold text-white mb-2">{satisfaction.avg_score.toFixed(2)}</div>
              <div className="text-gray-400">Average Rating</div>
              <div className="flex justify-center mt-2">
                {[...Array(5)].map((_, i) => (
                  <Star 
                    key={i} 
                    className={`w-5 h-5 ${i < Math.round(satisfaction.avg_score) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-600'}`}
                  />
                ))}
              </div>
            </div>
            
            <div className="text-center">
              <div className="text-5xl font-bold text-green-400 mb-2">{satisfaction.positive_pct.toFixed(1)}%</div>
              <div className="text-gray-400">Positive Reviews</div>
              <div className="text-sm text-gray-500 mt-2">4-5 stars</div>
            </div>
            
            <div className="text-center">
              <div className="text-5xl font-bold text-yellow-400 mb-2">{satisfaction.neutral_pct.toFixed(1)}%</div>
              <div className="text-gray-400">Neutral Reviews</div>
              <div className="text-sm text-gray-500 mt-2">3 stars</div>
            </div>
            
            <div className="text-center">
              <div className="text-5xl font-bold text-red-400 mb-2">{satisfaction.negative_pct.toFixed(1)}%</div>
              <div className="text-gray-400">Negative Reviews</div>
              <div className="text-sm text-gray-500 mt-2">1-2 stars</div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-400 py-8">No satisfaction data available</div>
        )}
      </div>

      {/* Geographic Distribution */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Geographic Distribution</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { state: 'SP', customers: 41746, percentage: 42 },
            { state: 'RJ', customers: 12852, percentage: 13 },
            { state: 'MG', customers: 11635, percentage: 12 },
            { state: 'RS', customers: 5466, percentage: 5.5 },
            { state: 'PR', customers: 5045, percentage: 5.1 },
            { state: 'SC', customers: 3637, percentage: 3.7 },
          ].map((region, i) => (
            <div key={i} className="bg-white/5 rounded-lg p-4 hover:bg-white/10 transition-colors">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xl font-bold text-white">{region.state}</span>
                <span className="text-2xl font-bold text-blue-400">{region.percentage}%</span>
              </div>
              <div className="text-gray-400 text-sm mb-2">
                {mounted ? region.customers.toLocaleString('en-US') : region.customers} customers
              </div>
              <div className="w-full bg-white/10 rounded-full h-1.5">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-1.5 rounded-full"
                  style={{ width: `${region.percentage * 2}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-gradient-to-r from-purple-400/10 to-pink-400/10 border border-purple-400/20 rounded-2xl p-6">
        <h3 className="text-xl font-bold text-purple-400 mb-2">📊 Real-Time Analytics</h3>
        <p className="text-gray-300">
          This page displays real analytics from your Olist MySQL database. 
          The sales trend chart shows actual monthly revenue and customer satisfaction metrics are calculated from real reviews.
        </p>
      </div>
    </div>
  );
}
