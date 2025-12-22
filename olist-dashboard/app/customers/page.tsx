"use client";

import { useState } from "react";
import { Search, MapPin } from "lucide-react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000";

interface Customer {
  customer_id: string;
  customer_city: string;
  customer_state: string;
}

interface TopCity {
  customer_city: string;
  customer_count: number;
}

export default function CustomersPage() {
  const [state, setState] = useState("SP");
  const [limit, setLimit] = useState(10);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [topCities, setTopCities] = useState<TopCity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchByState = async () => {
    setLoading(true);
    setError("");
    setTopCities([]);
    try {
      const response = await axios.get(
        `${API_BASE}/customers/by-state/${state}?limit=${limit}`
      );
      setCustomers(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to fetch customers");
      setCustomers([]);
    } finally {
      setLoading(false);
    }
  };

  const getTopCities = async () => {
    setLoading(true);
    setError("");
    setCustomers([]);
    try {
      const response = await axios.get(
        `${API_BASE}/customers/top-cities?limit=${limit}`
      );
      setTopCities(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to fetch top cities");
      setTopCities([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Customer Analytics</h1>
        <p className="text-purple-200">Explore customer demographics and distribution</p>
      </div>

      {/* Filters */}
      <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">
              State Code
            </label>
            <input
              type="text"
              value={state}
              onChange={(e) => setState(e.target.value.toUpperCase())}
              placeholder="e.g., SP"
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">
              Results Limit
            </label>
            <input
              type="number"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value))}
              min="1"
              max="100"
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <div className="flex items-end gap-2">
            <button
              onClick={searchByState}
              disabled={loading}
              className="flex-1 px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <Search className="w-4 h-4" />
              Search by State
            </button>
            <button
              onClick={getTopCities}
              disabled={loading}
              className="flex-1 px-6 py-2 bg-white/10 border border-white/20 text-white rounded-lg font-medium hover:bg-white/20 transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <MapPin className="w-4 h-4" />
              Top Cities
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-500/20 border border-red-500/50 text-red-200">
            {error}
          </div>
        )}
      </div>

      {/* Results */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        </div>
      ) : customers.length > 0 ? (
        <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gradient-to-r from-purple-500 to-pink-500">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Customer ID
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    City
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    State
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {customers.map((customer, index) => (
                  <tr
                    key={customer.customer_id}
                    className="hover:bg-white/5 transition-colors duration-150"
                  >
                    <td className="px-6 py-4 text-sm text-white font-mono">
                      {customer.customer_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-purple-100">
                      {customer.customer_city}
                    </td>
                    <td className="px-6 py-4 text-sm text-purple-100">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-500/20 text-purple-200">
                        {customer.customer_state}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : topCities.length > 0 ? (
        <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gradient-to-r from-purple-500 to-pink-500">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    City
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-white uppercase tracking-wider">
                    Customer Count
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {topCities.map((city, index) => (
                  <tr
                    key={city.customer_city}
                    className="hover:bg-white/5 transition-colors duration-150"
                  >
                    <td className="px-6 py-4 text-sm text-white font-bold">
                      #{index + 1}
                    </td>
                    <td className="px-6 py-4 text-sm text-purple-100 font-medium">
                      {city.customer_city}
                    </td>
                    <td className="px-6 py-4 text-sm text-white">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-300">
                        {city.customer_count.toLocaleString()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-12 text-center">
          <p className="text-purple-200">
            Select a query above to view customer data
          </p>
        </div>
      )}
    </div>
  );
}
