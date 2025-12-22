'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, Tag, BarChart3, Search } from 'lucide-react';

interface ProductStats {
  total_products: number;
  total_categories: number;
}

interface Product {
  product_id: string;
  product_category_name: string;
  product_name_length: number;
  product_description_length: number;
  product_photos_qty: number;
  product_weight_g: number;
  product_length_cm: number;
  product_width_cm: number;
  product_height_cm: number;
}

export default function ProductsPage() {
  const [stats, setStats] = useState<ProductStats | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchProductData();
  }, []);

  const fetchProductData = async () => {
    try {
      setLoading(true);
      const statsResponse = await axios.get('http://localhost:5000/products/stats');
      setStats(statsResponse.data);
      
      const productsResponse = await axios.get('http://localhost:5000/products?limit=50');
      setProducts(productsResponse.data);
      
      setError(null);
    } catch (err) {
      setError('Failed to load product data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = products.filter(p => 
    p.product_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.product_category_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading product data...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Products</h1>
        <p className="text-gray-400">Browse and analyze product catalog</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <Package className="w-8 h-8 text-blue-400" />
            <span className="text-xs text-gray-400">TOTAL</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_products.toLocaleString() || '32,951'}
          </div>
          <div className="text-sm text-gray-400">Total Products</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <Tag className="w-8 h-8 text-green-400" />
            <span className="text-xs text-gray-400">CATEGORIES</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_categories || '71'}
          </div>
          <div className="text-sm text-gray-400">Categories</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <BarChart3 className="w-8 h-8 text-purple-400" />
            <span className="text-xs text-gray-400">AVG</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">464</div>
          <div className="text-sm text-gray-400">Products/Category</div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <div className="flex flex-col md:flex-row items-center gap-4">
          <div className="flex-1 flex items-center gap-4 bg-white/5 rounded-lg px-4 py-3 w-full">
            <Search className="w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by product ID or category..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none"
            />
          </div>
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="px-4 py-3 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-colors border border-white/20"
            >
              Clear Search
            </button>
          )}
        </div>
        {searchTerm && (
          <p className="mt-3 text-gray-400 text-sm">
            Found {filteredProducts.length} products matching "{searchTerm}"
          </p>
        )}
      </div>

      {error && (
        <div className="text-yellow-400 bg-yellow-400/10 p-4 rounded-lg">
          {error} - Create Flask endpoints to load real data
        </div>
      )}

      {/* Products Table */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Product Catalog</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/20">
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Product ID</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Category</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Photos</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Weight (g)</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Dimensions (cm)</th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.length > 0 ? (
                filteredProducts.slice(0, 20).map((product, index) => (
                  <tr key={index} className="border-b border-white/10 hover:bg-white/5 transition-colors">
                    <td className="py-3 px-4 text-white font-mono text-sm">
                      {product.product_id.substring(0, 8)}...
                    </td>
                    <td className="py-3 px-4 text-gray-300">
                      {product.product_category_name || 'N/A'}
                    </td>
                    <td className="py-3 px-4 text-gray-300">{product.product_photos_qty}</td>
                    <td className="py-3 px-4 text-gray-300">
                      {product.product_weight_g?.toLocaleString() || '-'}
                    </td>
                    <td className="py-3 px-4 text-gray-300">
                      {product.product_length_cm && product.product_width_cm && product.product_height_cm
                        ? `${product.product_length_cm}×${product.product_width_cm}×${product.product_height_cm}`
                        : '-'}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-gray-400">
                    {searchTerm ? `No products match "${searchTerm}"` : 'No product data available'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
