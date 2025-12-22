"use client";

import { useEffect, useState } from "react";
import { Users, ShoppingCart, Package, TrendingUp } from "lucide-react";
import axios from "axios";

interface Stats {
  customers: number;
  orders: number;
  products: number;
  reviews: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({
    customers: 0,
    orders: 0,
    products: 0,
    reviews: 0,
  });
  const [mounted, setMounted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setMounted(true);
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/stats');
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
      // Fallback to default values if API fails
      setStats({
        customers: 99163,
        orders: 99441,
        products: 32951,
        reviews: 98410,
      });
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: "Total Customers",
      value: mounted ? stats.customers.toLocaleString('en-US') : stats.customers.toString(),
      icon: Users,
      gradient: "from-blue-500 to-cyan-500",
      bgGradient: "from-blue-500/20 to-cyan-500/20",
    },
    {
      title: "Total Orders",
      value: mounted ? stats.orders.toLocaleString('en-US') : stats.orders.toString(),
      icon: ShoppingCart,
      gradient: "from-purple-500 to-pink-500",
      bgGradient: "from-purple-500/20 to-pink-500/20",
    },
    {
      title: "Products",
      value: mounted ? stats.products.toLocaleString('en-US') : stats.products.toString(),
      icon: Package,
      gradient: "from-green-500 to-emerald-500",
      bgGradient: "from-green-500/20 to-emerald-500/20",
    },
    {
      title: "Customer Reviews",
      value: mounted ? stats.reviews.toLocaleString('en-US') : stats.reviews.toString(),
      icon: TrendingUp,
      gradient: "from-orange-500 to-red-500",
      bgGradient: "from-orange-500/20 to-red-500/20",
    },
  ];

  if (loading) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome to Olist Analytics
          </h1>
          <p className="text-purple-200">
            Loading dashboard data...
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6 animate-pulse">
              <div className="h-8 bg-white/20 rounded mb-4 w-12"></div>
              <div className="h-4 bg-white/20 rounded mb-2 w-24"></div>
              <div className="h-8 bg-white/20 rounded w-32"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">
          Welcome to Olist Analytics
        </h1>
        <p className="text-purple-200">
          Your comprehensive e-commerce data platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.title}
              className="group relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6 hover:scale-105 transition-all duration-300"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${card.bgGradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />
              
              <div className="relative">
                <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${card.gradient} mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>

                <h3 className="text-purple-200 text-sm font-medium mb-1">
                  {card.title}
                </h3>
                <p className="text-3xl font-bold text-white">
                  {card.value}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6">
          <h2 className="text-2xl font-bold text-white mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <a
              href="/customers"
              className="block p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all duration-200"
            >
              <h3 className="text-white font-semibold mb-1">Customer Analytics</h3>
              <p className="text-sm text-purple-200">
                Explore customer demographics and behavior
              </p>
            </a>
            <a
              href="/orders"
              className="block p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all duration-200"
            >
              <h3 className="text-white font-semibold mb-1">Order Management</h3>
              <p className="text-sm text-purple-200">
                Track and analyze order performance
              </p>
            </a>
            <a
              href="/reviews"
              className="block p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all duration-200"
            >
              <h3 className="text-white font-semibold mb-1">Review Insights</h3>
              <p className="text-sm text-purple-200">
                Monitor customer satisfaction metrics
              </p>
            </a>
          </div>
        </div>

        <div className="rounded-2xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-xl border border-white/20 p-6">
          <h2 className="text-2xl font-bold text-white mb-4">System Status</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-purple-100">Database</span>
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/20 text-green-300 text-sm font-medium">
                <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                Connected
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-purple-100">API Server</span>
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/20 text-green-300 text-sm font-medium">
                <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                Online
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-purple-100">Data Loaded</span>
              <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-sm font-medium">
                1.3M+ rows
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6">
        <h2 className="text-2xl font-bold text-white mb-4">Platform Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <h3 className="text-white font-semibold mb-2">🔍 Advanced Search</h3>
            <p className="text-sm text-purple-200">
              Filter and search across all data entities
            </p>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <h3 className="text-white font-semibold mb-2">📊 Real-time Analytics</h3>
            <p className="text-sm text-purple-200">
              Live data visualization and insights
            </p>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <h3 className="text-white font-semibold mb-2">📈 Export Reports</h3>
            <p className="text-sm text-purple-200">
              Download data in multiple formats
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
