'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, TrendingUp, DollarSign, Clock, Plus, Edit, Trash2, X, Search } from 'lucide-react';

const API_BASE = 'http://localhost:5000';

interface OrderStats {
  total_orders: number;
  total_items: number;
  avg_items_per_order: number;
  total_revenue: number;
}

interface RecentOrder {
  order_id: string;
  customer_id: string;
  order_status: string;
  order_purchase_timestamp: string;
  order_estimated_delivery_date: string | null;
  payment_type?: string;
  payment_value?: number;
}

interface Customer {
  customer_id: string;
  customer_city: string;
  customer_state: string;
  label: string;
}

// Order Status Options
const ORDER_STATUSES = [
  { value: 'processing', label: 'Processing' },
  { value: 'shipped', label: 'Shipped' },
  { value: 'delivered', label: 'Delivered' },
  { value: 'canceled', label: 'Canceled' },
];

// Payment Type Options (Radio buttons)
const PAYMENT_TYPES = [
  { value: 'credit_card', label: 'Credit Card' },
  { value: 'boleto', label: 'Boleto' },
  { value: 'voucher', label: 'Voucher' },
  { value: 'debit_card', label: 'Debit Card' },
];

export default function OrdersPage() {
  const [stats, setStats] = useState<OrderStats | null>(null);
  const [recentOrders, setRecentOrders] = useState<RecentOrder[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [mounted, setMounted] = useState(false);
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<RecentOrder | null>(null);
  
  // Form states
  const [formData, setFormData] = useState({
    customer_id: '',
    order_status: 'processing',
    payment_type: 'credit_card',
    payment_value: '',
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    setMounted(true);
    fetchOrderData();
    fetchCustomers();
  }, []);

  const fetchOrderData = async () => {
    try {
      setLoading(true);
      const [statsRes, ordersRes] = await Promise.all([
        axios.get(`${API_BASE}/orders/stats`),
        axios.get(`${API_BASE}/orders/recent?limit=20`)
      ]);
      setStats(statsRes.data);
      setRecentOrders(ordersRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load order data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCustomers = async () => {
    try {
      const res = await axios.get(`${API_BASE}/orders/customers/list`);
      setCustomers(res.data);
    } catch (err) {
      console.error('Failed to fetch customers:', err);
    }
  };

  // Form Validation
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.customer_id) {
      errors.customer_id = 'Please select a customer';
    }
    
    if (!formData.payment_value || parseFloat(formData.payment_value) <= 0) {
      errors.payment_value = 'Payment value must be greater than 0';
    }
    
    if (!formData.order_status) {
      errors.order_status = 'Please select an order status';
    }
    
    if (!formData.payment_type) {
      errors.payment_type = 'Please select a payment type';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // CREATE Order
  const handleCreate = async () => {
    if (!validateForm()) return;
    
    try {
      const res = await axios.post(`${API_BASE}/orders/`, {
        customer_id: formData.customer_id,
        order_status: formData.order_status,
        payment_type: formData.payment_type,
        payment_value: parseFloat(formData.payment_value),
      });
      
      setSuccess(`Order created successfully! ID: ${res.data.order_id.substring(0, 8)}...`);
      setShowCreateModal(false);
      resetForm();
      fetchOrderData();
      
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 
        (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to create order';
      setError(errorMessage);
    }
  };

  // UPDATE Order
  const handleUpdate = async () => {
    if (!selectedOrder) return;
    
    try {
      await axios.put(`${API_BASE}/orders/${selectedOrder.order_id}`, {
        order_status: formData.order_status,
        payment_type: formData.payment_type,
        payment_value: formData.payment_value ? parseFloat(formData.payment_value) : undefined,
      });
      
      setSuccess('Order updated successfully!');
      setShowEditModal(false);
      resetForm();
      fetchOrderData();
      
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 
        (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to update order';
      setError(errorMessage);
    }
  };

  // DELETE Order
  const handleDelete = async () => {
    if (!selectedOrder) return;
    
    try {
      await axios.delete(`${API_BASE}/orders/${selectedOrder.order_id}`);
      
      setSuccess('Order deleted successfully!');
      setShowDeleteModal(false);
      setSelectedOrder(null);
      fetchOrderData();
      
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 
        (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to delete order';
      setError(errorMessage);
    }
  };

  const resetForm = () => {
    setFormData({
      customer_id: '',
      order_status: 'processing',
      payment_type: 'credit_card',
      payment_value: '',
    });
    setFormErrors({});
    setSelectedOrder(null);
  };

  const openEditModal = async (order: RecentOrder) => {
    try {
      // Fetch full order details
      const res = await axios.get(`${API_BASE}/orders/${order.order_id}`);
      const fullOrder = res.data;
      
      setSelectedOrder(fullOrder);
      setFormData({
        customer_id: fullOrder.customer_id,
        order_status: fullOrder.order_status,
        payment_type: fullOrder.payment_type || 'credit_card',
        payment_value: fullOrder.payment_value?.toString() || '',
      });
      setShowEditModal(true);
    } catch (err) {
      setError('Failed to load order details');
    }
  };

  const openDeleteModal = (order: RecentOrder) => {
    setSelectedOrder(order);
    setShowDeleteModal(true);
  };

  const filteredOrders = recentOrders.filter(order => {
    const matchesSearch = 
      order.order_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.customer_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.order_status.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || order.order_status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  if (!mounted) return null;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading order data...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Orders</h1>
          <p className="text-gray-400">Manage and analyze order data (CRUD Operations)</p>
        </div>
        <button
          onClick={() => { resetForm(); setShowCreateModal(true); }}
          className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
          Create New Order
        </button>
      </div>

      {/* Success/Error Messages */}
      {success && (
        <div className="bg-green-500/20 border border-green-500 text-green-400 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}
      {error && (
        <div className="bg-red-500/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg flex justify-between">
          {error}
          <button onClick={() => setError(null)}><X className="w-5 h-5" /></button>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <Package className="w-8 h-8 text-blue-400" />
            <span className="text-xs text-gray-400">TOTAL</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_orders.toLocaleString('en-US') || '0'}
          </div>
          <div className="text-sm text-gray-400">Total Orders</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <TrendingUp className="w-8 h-8 text-green-400" />
            <span className="text-xs text-gray-400">ITEMS</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_items.toLocaleString('en-US') || '0'}
          </div>
          <div className="text-sm text-gray-400">Order Items</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="w-8 h-8 text-yellow-400" />
            <span className="text-xs text-gray-400">REVENUE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            ${(stats?.total_revenue ? stats.total_revenue / 1000000 : 0).toFixed(1)}M
          </div>
          <div className="text-sm text-gray-400">Total Revenue</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <Clock className="w-8 h-8 text-purple-400" />
            <span className="text-xs text-gray-400">AVG</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.avg_items_per_order?.toFixed(2) || '0'}
          </div>
          <div className="text-sm text-gray-400">Items per Order</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Textbox - Search Input */}
          <div className="flex-1 flex items-center gap-4 bg-white/5 rounded-lg px-4 py-3">
            <Search className="w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by Order ID, Customer ID, or Status..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none"
            />
          </div>
          
          {/* Dropdown - Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20 hover:bg-white/10 transition-colors"
          >
            <option value="all" className="bg-gray-800">All Status</option>
            {ORDER_STATUSES.map(status => (
              <option key={status.value} value={status.value} className="bg-gray-800">
                {status.label}
              </option>
            ))}
          </select>
        </div>
        {searchTerm && (
          <p className="mt-3 text-gray-400 text-sm">
            Found {filteredOrders.length} orders matching &quot;{searchTerm}&quot;
          </p>
        )}
      </div>

      {/* Orders Table */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Recent Orders (READ)</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/20">
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Order ID</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Customer ID</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Status</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Purchase Date</th>
                <th className="text-left py-3 px-4 text-gray-400 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrders.length > 0 ? (
                filteredOrders.map((order, index) => (
                  <tr key={index} className="border-b border-white/10 hover:bg-white/5 transition-colors">
                    <td className="py-3 px-4 text-white font-mono text-sm">
                      {order.order_id.substring(0, 8)}...
                    </td>
                    <td className="py-3 px-4 text-gray-300 font-mono text-sm">
                      {order.customer_id.substring(0, 8)}...
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        order.order_status === 'delivered' ? 'bg-green-400/20 text-green-400' :
                        order.order_status === 'shipped' ? 'bg-blue-400/20 text-blue-400' :
                        order.order_status === 'canceled' ? 'bg-red-400/20 text-red-400' :
                        'bg-yellow-400/20 text-yellow-400'
                      }`}>
                        {order.order_status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-300 text-sm">
                      {order.order_purchase_timestamp 
                        ? new Date(order.order_purchase_timestamp).toLocaleDateString('en-US')
                        : '-'}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => openEditModal(order)}
                          className="p-2 bg-blue-500/20 text-blue-400 rounded-lg hover:bg-blue-500/30 transition-colors"
                          title="Edit Order (UPDATE)"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => openDeleteModal(order)}
                          className="p-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
                          title="Delete Order (DELETE)"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-gray-400">
                    {searchTerm || statusFilter !== 'all' 
                      ? 'No orders match your search criteria' 
                      : 'No order data available'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* CREATE Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Create New Order (CREATE)</h3>
              <button onClick={() => setShowCreateModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Customer Dropdown */}
              <div>
                <label className="block text-gray-400 mb-2">Customer (Dropdown)</label>
                <select
                  value={formData.customer_id}
                  onChange={(e) => setFormData({...formData, customer_id: e.target.value})}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                >
                  <option value="" className="bg-gray-800">Select a customer...</option>
                  {customers.map(customer => (
                    <option key={customer.customer_id} value={customer.customer_id} className="bg-gray-800">
                      {customer.label}
                    </option>
                  ))}
                </select>
                {formErrors.customer_id && (
                  <p className="text-red-400 text-sm mt-1">{formErrors.customer_id}</p>
                )}
              </div>

              {/* Order Status Dropdown */}
              <div>
                <label className="block text-gray-400 mb-2">Order Status (Dropdown)</label>
                <select
                  value={formData.order_status}
                  onChange={(e) => setFormData({...formData, order_status: e.target.value})}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                >
                  {ORDER_STATUSES.map(status => (
                    <option key={status.value} value={status.value} className="bg-gray-800">
                      {status.label}
                    </option>
                  ))}
                </select>
                {formErrors.order_status && (
                  <p className="text-red-400 text-sm mt-1">{formErrors.order_status}</p>
                )}
              </div>

              {/* Payment Type Radio Buttons */}
              <div>
                <label className="block text-gray-400 mb-2">Payment Type (Radio Buttons)</label>
                <div className="grid grid-cols-2 gap-2">
                  {PAYMENT_TYPES.map(type => (
                    <label key={type.value} className="flex items-center gap-2 cursor-pointer p-2 rounded-lg hover:bg-white/5">
                      <input
                        type="radio"
                        name="payment_type"
                        value={type.value}
                        checked={formData.payment_type === type.value}
                        onChange={(e) => setFormData({...formData, payment_type: e.target.value})}
                        className="w-4 h-4 text-blue-500"
                      />
                      <span className="text-white text-sm">{type.label}</span>
                    </label>
                  ))}
                </div>
                {formErrors.payment_type && (
                  <p className="text-red-400 text-sm mt-1">{formErrors.payment_type}</p>
                )}
              </div>

              {/* Payment Value Textbox */}
              <div>
                <label className="block text-gray-400 mb-2">Payment Value (Textbox)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.payment_value}
                  onChange={(e) => setFormData({...formData, payment_value: e.target.value})}
                  placeholder="Enter payment amount..."
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                />
                {formErrors.payment_value && (
                  <p className="text-red-400 text-sm mt-1">{formErrors.payment_value}</p>
                )}
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg transition-colors"
              >
                Create Order
              </button>
            </div>
          </div>
        </div>
      )}

      {/* UPDATE Modal */}
      {showEditModal && selectedOrder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Update Order (UPDATE)</h3>
              <button onClick={() => setShowEditModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="mb-4 p-3 bg-white/5 rounded-lg">
              <p className="text-gray-400 text-sm">Order ID:</p>
              <p className="text-white font-mono">{selectedOrder.order_id}</p>
            </div>
            
            <div className="space-y-4">
              {/* Order Status Dropdown */}
              <div>
                <label className="block text-gray-400 mb-2">Order Status (Dropdown)</label>
                <select
                  value={formData.order_status}
                  onChange={(e) => setFormData({...formData, order_status: e.target.value})}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                >
                  {ORDER_STATUSES.map(status => (
                    <option key={status.value} value={status.value} className="bg-gray-800">
                      {status.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Payment Type Radio Buttons */}
              <div>
                <label className="block text-gray-400 mb-2">Payment Type (Radio Buttons)</label>
                <div className="grid grid-cols-2 gap-2">
                  {PAYMENT_TYPES.map(type => (
                    <label key={type.value} className="flex items-center gap-2 cursor-pointer p-2 rounded-lg hover:bg-white/5">
                      <input
                        type="radio"
                        name="payment_type_edit"
                        value={type.value}
                        checked={formData.payment_type === type.value}
                        onChange={(e) => setFormData({...formData, payment_type: e.target.value})}
                        className="w-4 h-4 text-blue-500"
                      />
                      <span className="text-white text-sm">{type.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Payment Value Textbox */}
              <div>
                <label className="block text-gray-400 mb-2">Payment Value (Textbox)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.payment_value}
                  onChange={(e) => setFormData({...formData, payment_value: e.target.value})}
                  placeholder="Enter new payment amount..."
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                />
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowEditModal(false)}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUpdate}
                className="flex-1 bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg transition-colors"
              >
                Update Order
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DELETE Confirmation Modal */}
      {showDeleteModal && selectedOrder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Delete Order (DELETE)</h3>
              <button onClick={() => setShowDeleteModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="mb-6">
              <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg mb-4">
                <p className="text-red-400">Are you sure you want to delete this order? This action cannot be undone.</p>
              </div>
              <div className="p-3 bg-white/5 rounded-lg">
                <p className="text-gray-400 text-sm">Order ID:</p>
                <p className="text-white font-mono">{selectedOrder.order_id}</p>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg transition-colors"
              >
                Delete Order
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
