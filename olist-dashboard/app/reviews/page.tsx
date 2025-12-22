'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Star, MessageSquare, ThumbsUp, TrendingDown, Plus, Edit, Trash2, X } from 'lucide-react';

const API_BASE = 'http://localhost:5000';

interface ReviewStats {
  total_reviews: number;
  avg_score: number;
  score_distribution: { score: number; count: number }[];
}

interface Review {
  review_id: string;
  order_id: string;
  review_score: number;
  review_comment_title: string;
  review_comment_message: string;
  review_creation_date: string;
}

interface OrderForReview {
  order_id: string;
  order_date: string;
  customer_city: string;
  label: string;
}

export default function ReviewsPage() {
  const [stats, setStats] = useState<ReviewStats | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [ordersForReview, setOrdersForReview] = useState<OrderForReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  
  // Filter states with Checkboxes
  const [scoreFilters, setScoreFilters] = useState<number[]>([1, 2, 3, 4, 5]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showWithComments, setShowWithComments] = useState(false);
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedReview, setSelectedReview] = useState<Review | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    order_id: '',
    review_score: 5,
    review_comment_message: '',
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    setMounted(true);
    fetchReviewData();
    fetchOrdersForReview();
  }, []);

  const fetchReviewData = async () => {
    try {
      setLoading(true);
      const [statsRes, reviewsRes] = await Promise.all([
        axios.get(`${API_BASE}/reviews/stats`),
        axios.get(`${API_BASE}/reviews/recent?limit=30`)
      ]);
      setStats(statsRes.data);
      setReviews(reviewsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load review data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchOrdersForReview = async () => {
    try {
      const res = await axios.get(`${API_BASE}/reviews/orders-without-review`);
      setOrdersForReview(res.data);
    } catch (err) {
      console.error('Failed to fetch orders:', err);
    }
  };

  // Toggle score filter checkbox
  const toggleScoreFilter = (score: number) => {
    setScoreFilters(prev => 
      prev.includes(score) 
        ? prev.filter(s => s !== score)
        : [...prev, score]
    );
  };

  // Form validation
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.order_id) {
      errors.order_id = 'Please select an order';
    }
    if (!formData.review_score || formData.review_score < 1 || formData.review_score > 5) {
      errors.review_score = 'Score must be between 1 and 5';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // CREATE Review
  const handleCreate = async () => {
    if (!validateForm()) return;
    
    try {
      await axios.post(`${API_BASE}/reviews/`, formData);
      setSuccess('Review created successfully!');
      setShowCreateModal(false);
      resetForm();
      fetchReviewData();
      fetchOrdersForReview();
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMsg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to create review';
      setError(errorMsg);
    }
  };

  // UPDATE Review
  const handleUpdate = async () => {
    if (!selectedReview) return;
    
    try {
      await axios.put(`${API_BASE}/reviews/${selectedReview.review_id}`, {
        review_score: formData.review_score,
        review_comment_message: formData.review_comment_message,
      });
      setSuccess('Review updated successfully!');
      setShowEditModal(false);
      resetForm();
      fetchReviewData();
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMsg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to update review';
      setError(errorMsg);
    }
  };

  // DELETE Review
  const handleDelete = async () => {
    if (!selectedReview) return;
    
    try {
      await axios.delete(`${API_BASE}/reviews/${selectedReview.review_id}`);
      setSuccess('Review deleted successfully!');
      setShowDeleteModal(false);
      setSelectedReview(null);
      fetchReviewData();
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: unknown) {
      const errorMsg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Failed to delete review';
      setError(errorMsg);
    }
  };

  const resetForm = () => {
    setFormData({ order_id: '', review_score: 5, review_comment_message: '' });
    setFormErrors({});
    setSelectedReview(null);
  };

  const openEditModal = (review: Review) => {
    setSelectedReview(review);
    setFormData({
      order_id: review.order_id,
      review_score: review.review_score,
      review_comment_message: review.review_comment_message || '',
    });
    setShowEditModal(true);
  };

  // Filter reviews based on checkboxes
  const filteredReviews = reviews.filter(review => {
    const matchesScore = scoreFilters.includes(review.review_score);
    const matchesSearch = 
      review.order_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      review.review_comment_message?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCommentFilter = !showWithComments || (review.review_comment_message && review.review_comment_message.length > 0);
    return matchesScore && matchesSearch && matchesCommentFilter;
  });

  if (!mounted) return null;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading review data...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Reviews</h1>
          <p className="text-gray-400">Customer feedback and ratings (CRUD with TextArea & Checkboxes)</p>
        </div>
        <button
          onClick={() => { resetForm(); setShowCreateModal(true); }}
          className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-black px-4 py-2 rounded-lg transition-colors font-semibold"
        >
          <Plus className="w-5 h-5" />
          Add Review
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
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <MessageSquare className="w-8 h-8 text-blue-400" />
            <span className="text-xs text-gray-400">TOTAL</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_reviews.toLocaleString('en-US') || '0'}
          </div>
          <div className="text-sm text-gray-400">Total Reviews</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <Star className="w-8 h-8 text-yellow-400" />
            <span className="text-xs text-gray-400">AVERAGE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.avg_score.toFixed(2) || '0'}
          </div>
          <div className="text-sm text-gray-400">Avg Rating</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <ThumbsUp className="w-8 h-8 text-green-400" />
            <span className="text-xs text-gray-400">POSITIVE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.score_distribution ? 
              Math.round((stats.score_distribution.filter(d => d.score >= 4).reduce((acc, d) => acc + d.count, 0) / stats.total_reviews) * 100) : 0}%
          </div>
          <div className="text-sm text-gray-400">4-5 Stars</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <TrendingDown className="w-8 h-8 text-red-400" />
            <span className="text-xs text-gray-400">NEGATIVE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.score_distribution ? 
              Math.round((stats.score_distribution.filter(d => d.score <= 2).reduce((acc, d) => acc + d.count, 0) / stats.total_reviews) * 100) : 0}%
          </div>
          <div className="text-sm text-gray-400">1-2 Stars</div>
        </div>
      </div>

      {/* Filters with Checkboxes */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h3 className="text-white font-semibold mb-4">Filters (CHECK BOXES)</h3>
        
        <div className="flex flex-wrap gap-6">
          {/* Score Checkboxes */}
          <div>
            <label className="text-gray-400 text-sm mb-2 block">Filter by Score:</label>
            <div className="flex gap-3">
              {[5, 4, 3, 2, 1].map(score => (
                <label key={score} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={scoreFilters.includes(score)}
                    onChange={() => toggleScoreFilter(score)}
                    className="w-5 h-5 rounded bg-white/10 border-white/30 text-yellow-500 focus:ring-yellow-500"
                  />
                  <span className="text-white flex items-center gap-1">
                    {score} <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Show only with comments checkbox */}
          <div>
            <label className="text-gray-400 text-sm mb-2 block">Options:</label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={showWithComments}
                onChange={(e) => setShowWithComments(e.target.checked)}
                className="w-5 h-5 rounded bg-white/10 border-white/30 text-yellow-500 focus:ring-yellow-500"
              />
              <span className="text-white">Only show reviews with comments</span>
            </label>
          </div>

          {/* Search */}
          <div className="flex-1 min-w-[200px]">
            <label className="text-gray-400 text-sm mb-2 block">Search (TEXT BOX):</label>
            <input
              type="text"
              placeholder="Search reviews..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-white/5 text-white rounded-lg px-4 py-2 outline-none border border-white/20"
            />
          </div>
        </div>

        <p className="mt-4 text-gray-400 text-sm">
          Showing {filteredReviews.length} of {reviews.length} reviews
        </p>
      </div>

      {/* Rating Distribution */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Rating Distribution</h2>
        
        <div className="space-y-4">
          {[5, 4, 3, 2, 1].map((score) => {
            const dist = stats?.score_distribution?.find(d => d.score === score);
            const count = dist?.count || 0;
            const percentage = stats?.total_reviews ? (count / stats.total_reviews) * 100 : 0;
            
            return (
              <div key={score} className="flex items-center gap-4">
                <div className="flex items-center gap-1 w-20">
                  <span className="text-white font-semibold">{score}</span>
                  <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                </div>
                <div className="flex-1 bg-white/10 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-yellow-500 to-orange-500 h-3 rounded-full transition-all"
                    style={{ width: `${percentage}%` }}
                  />
                </div>
                <span className="text-gray-400 w-24 text-right">{count.toLocaleString('en-US')}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Reviews List */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Recent Reviews</h2>
        
        <div className="space-y-4">
          {filteredReviews.length > 0 ? (
            filteredReviews.map((review, index) => (
              <div key={index} className="bg-white/5 rounded-lg p-4 hover:bg-white/10 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-4 h-4 ${
                          i < review.review_score 
                            ? 'text-yellow-400 fill-yellow-400' 
                            : 'text-gray-600'
                        }`}
                      />
                    ))}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400 text-sm">
                      {review.review_creation_date ? new Date(review.review_creation_date).toLocaleDateString('en-US') : '-'}
                    </span>
                    <button
                      onClick={() => openEditModal(review)}
                      className="p-1 bg-blue-500/20 text-blue-400 rounded hover:bg-blue-500/30"
                      title="Edit"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => { setSelectedReview(review); setShowDeleteModal(true); }}
                      className="p-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                {review.review_comment_message && (
                  <p className="text-gray-300 text-sm mb-2">{review.review_comment_message}</p>
                )}
                <div className="text-gray-500 text-xs font-mono">
                  Order: {review.order_id.substring(0, 8)}...
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-400">
              No reviews match your filter criteria
            </div>
          )}
        </div>
      </div>

      {/* CREATE Modal with TextArea */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Add Review (CREATE)</h3>
              <button onClick={() => setShowCreateModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Order Selection (Dropdown) */}
              <div>
                <label className="block text-gray-400 mb-2">Order (SELECTION/Dropdown)</label>
                <select
                  value={formData.order_id}
                  onChange={(e) => setFormData({...formData, order_id: e.target.value})}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20"
                >
                  <option value="" className="bg-gray-800">Select a delivered order...</option>
                  {ordersForReview.map(order => (
                    <option key={order.order_id} value={order.order_id} className="bg-gray-800">
                      {order.label}
                    </option>
                  ))}
                </select>
                {formErrors.order_id && <p className="text-red-400 text-sm mt-1">{formErrors.order_id}</p>}
              </div>

              {/* Score Radio Buttons */}
              <div>
                <label className="block text-gray-400 mb-2">Rating (RADIO BOXES)</label>
                <div className="flex gap-4">
                  {[1, 2, 3, 4, 5].map(score => (
                    <label key={score} className="flex items-center gap-1 cursor-pointer">
                      <input
                        type="radio"
                        name="review_score"
                        value={score}
                        checked={formData.review_score === score}
                        onChange={() => setFormData({...formData, review_score: score})}
                        className="w-4 h-4 text-yellow-500"
                      />
                      <span className="text-white">{score}</span>
                      <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                    </label>
                  ))}
                </div>
                {formErrors.review_score && <p className="text-red-400 text-sm mt-1">{formErrors.review_score}</p>}
              </div>

              {/* Comment TextArea */}
              <div>
                <label className="block text-gray-400 mb-2">Comment (TEXT AREA)</label>
                <textarea
                  value={formData.review_comment_message}
                  onChange={(e) => setFormData({...formData, review_comment_message: e.target.value})}
                  placeholder="Write your review comment here... (optional)"
                  rows={4}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20 resize-none"
                />
                <p className="text-gray-500 text-xs mt-1">{formData.review_comment_message.length} characters</p>
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
                className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-black font-semibold py-3 rounded-lg transition-colors"
              >
                Submit Review
              </button>
            </div>
          </div>
        </div>
      )}

      {/* UPDATE Modal with TextArea */}
      {showEditModal && selectedReview && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Edit Review (UPDATE)</h3>
              <button onClick={() => setShowEditModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="mb-4 p-3 bg-white/5 rounded-lg">
              <p className="text-gray-400 text-sm">Review ID:</p>
              <p className="text-white font-mono text-sm">{selectedReview.review_id}</p>
            </div>
            
            <div className="space-y-4">
              {/* Score Radio Buttons */}
              <div>
                <label className="block text-gray-400 mb-2">Rating (RADIO BOXES)</label>
                <div className="flex gap-4">
                  {[1, 2, 3, 4, 5].map(score => (
                    <label key={score} className="flex items-center gap-1 cursor-pointer">
                      <input
                        type="radio"
                        name="edit_review_score"
                        value={score}
                        checked={formData.review_score === score}
                        onChange={() => setFormData({...formData, review_score: score})}
                        className="w-4 h-4 text-yellow-500"
                      />
                      <span className="text-white">{score}</span>
                      <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                    </label>
                  ))}
                </div>
              </div>

              {/* Comment TextArea */}
              <div>
                <label className="block text-gray-400 mb-2">Comment (TEXT AREA)</label>
                <textarea
                  value={formData.review_comment_message}
                  onChange={(e) => setFormData({...formData, review_comment_message: e.target.value})}
                  placeholder="Update your review comment..."
                  rows={4}
                  className="w-full bg-white/5 text-white rounded-lg px-4 py-3 outline-none border border-white/20 resize-none"
                />
                <p className="text-gray-500 text-xs mt-1">{formData.review_comment_message.length} characters</p>
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
                Update Review
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DELETE Modal */}
      {showDeleteModal && selectedReview && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">Delete Review (DELETE)</h3>
              <button onClick={() => setShowDeleteModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg mb-4">
              <p className="text-red-400">Are you sure you want to delete this review?</p>
            </div>
            
            <div className="p-3 bg-white/5 rounded-lg mb-6">
              <p className="text-gray-400 text-sm">Review ID:</p>
              <p className="text-white font-mono text-sm">{selectedReview.review_id}</p>
              <div className="flex items-center gap-1 mt-2">
                {[...Array(5)].map((_, i) => (
                  <Star 
                    key={i} 
                    className={`w-4 h-4 ${i < selectedReview.review_score ? 'text-yellow-400 fill-yellow-400' : 'text-gray-600'}`}
                  />
                ))}
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
                Delete Review
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
