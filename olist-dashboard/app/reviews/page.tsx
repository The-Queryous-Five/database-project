'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Star, MessageSquare, ThumbsUp, TrendingDown } from 'lucide-react';

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

export default function ReviewsPage() {
  const [stats, setStats] = useState<ReviewStats | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [scoreFilter, setScoreFilter] = useState<number | 'all'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchReviewData();
  }, []);

  const fetchReviewData = async () => {
    try {
      setLoading(true);
      const statsResponse = await axios.get('http://localhost:5000/reviews/stats');
      setStats(statsResponse.data);
      
      const reviewsResponse = await axios.get('http://localhost:5000/reviews/recent?limit=20');
      setReviews(reviewsResponse.data);
      
      setError(null);
    } catch (err) {
      setError('Failed to load review data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredReviews = reviews.filter(review => {
    const matchesScore = scoreFilter === 'all' || review.review_score === scoreFilter;
    const matchesSearch = 
      review.order_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      review.review_comment_message?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesScore && matchesSearch;
  });

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
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Reviews</h1>
        <p className="text-gray-400">Customer feedback and ratings</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <MessageSquare className="w-8 h-8 text-blue-400" />
            <span className="text-xs text-gray-400">TOTAL</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.total_reviews.toLocaleString() || '98,410'}
          </div>
          <div className="text-sm text-gray-400">Total Reviews</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <Star className="w-8 h-8 text-yellow-400" />
            <span className="text-xs text-gray-400">AVERAGE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {stats?.avg_score.toFixed(2) || '4.09'}
          </div>
          <div className="text-sm text-gray-400">Avg Rating</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <ThumbsUp className="w-8 h-8 text-green-400" />
            <span className="text-xs text-gray-400">POSITIVE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">76%</div>
          <div className="text-sm text-gray-400">4-5 Stars</div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all">
          <div className="flex items-center justify-between mb-4">
            <TrendingDown className="w-8 h-8 text-red-400" />
            <span className="text-xs text-gray-400">NEGATIVE</span>
          </div>
          <div className="text-3xl font-bold text-white mb-1">11%</div>
          <div className="text-sm text-gray-400">1-2 Stars</div>
        </div>
      </div>

      {error && (
        <div className="text-yellow-400 bg-yellow-400/10 p-4 rounded-lg">
          {error} - Create Flask endpoints to load real data
        </div>
      )}

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
                <span className="text-gray-400 w-20 text-right">{count.toLocaleString()}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Reviews */}
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
                  <span className="text-gray-400 text-sm">
                    {new Date(review.review_creation_date).toLocaleDateString()}
                  </span>
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
              {searchTerm || scoreFilter !== 'all'
                ? 'No reviews match your search criteria'
                : 'No review data available. Create Flask endpoints to load real reviews.'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
