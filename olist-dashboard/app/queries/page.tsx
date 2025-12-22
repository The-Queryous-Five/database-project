'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, Code, Play, ChevronDown, ChevronUp, Table, Layers } from 'lucide-react';

const API_BASE = 'http://localhost:5000';

interface QueryResult {
  query_name: string;
  description: string;
  sql: string;
  results: Record<string, unknown>[];
  tables_used?: string[];
  avg_payment?: number;
  customers_without_orders?: number;
}

interface QueryInfo {
  id: string;
  name: string;
  description: string;
  endpoint: string;
}

export default function QueriesPage() {
  const [queries, setQueries] = useState<QueryInfo[]>([]);
  const [selectedQuery, setSelectedQuery] = useState<string | null>(null);
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSql, setShowSql] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchQueries();
  }, []);

  const fetchQueries = async () => {
    try {
      const res = await axios.get(`${API_BASE}/queries/all`);
      setQueries(res.data.queries);
    } catch (err) {
      console.error('Failed to fetch queries:', err);
    }
  };

  const executeQuery = async (queryId: string) => {
    setLoading(true);
    setSelectedQuery(queryId);
    try {
      const res = await axios.get(`${API_BASE}/queries/${queryId}`);
      setQueryResult(res.data);
    } catch (err) {
      console.error('Failed to execute query:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!mounted) return null;

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Complex SQL Queries</h1>
        <p className="text-gray-400">
          Zor SQL Sorguları - Nested Query, 4+ Table JOIN, GROUP BY, OUTER JOIN
        </p>
      </div>

      {/* Info Box */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-2xl p-6">
        <h3 className="text-blue-400 font-semibold mb-2 flex items-center gap-2">
          <Database className="w-5 h-5" />
          Bu Sayfa Hakkında
        </h3>
        <p className="text-gray-300 text-sm">
          Bu sayfa, proje gereksinimlerindeki &quot;Zor SQL Sorguları&quot; maddesini karşılamak için oluşturulmuştur.
          Her sorgu doğrudan veritabanında çalıştırılır ve sonuçlar ekranda gösterilir.
          <strong className="text-white"> ORM kullanılmamıştır - tüm sorgular raw SQL ile yapılmaktadır.</strong>
        </p>
      </div>

      {/* Query Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {queries.map((query) => (
          <div
            key={query.id}
            className={`bg-white/10 backdrop-blur-md rounded-2xl p-6 border transition-all cursor-pointer hover:bg-white/15 ${
              selectedQuery === query.id ? 'border-blue-500' : 'border-white/20'
            }`}
            onClick={() => executeQuery(query.id)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${
                  query.id === 'nested' ? 'bg-purple-500/20 text-purple-400' :
                  query.id === 'multi-join' ? 'bg-blue-500/20 text-blue-400' :
                  query.id === 'group-by' ? 'bg-green-500/20 text-green-400' :
                  'bg-yellow-500/20 text-yellow-400'
                }`}>
                  {query.id === 'nested' ? <Layers className="w-5 h-5" /> :
                   query.id === 'multi-join' ? <Table className="w-5 h-5" /> :
                   <Database className="w-5 h-5" />}
                </div>
                <div>
                  <h3 className="text-white font-semibold">{query.name}</h3>
                  <p className="text-gray-400 text-sm">{query.description}</p>
                </div>
              </div>
              <button
                className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-lg text-sm transition-colors"
                onClick={(e) => { e.stopPropagation(); executeQuery(query.id); }}
              >
                <Play className="w-4 h-4" />
                Run
              </button>
            </div>
            
            {/* Query Type Badge */}
            <div className="flex gap-2">
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                query.id === 'nested' ? 'bg-purple-500/20 text-purple-400' :
                query.id === 'multi-join' ? 'bg-blue-500/20 text-blue-400' :
                query.id === 'group-by' ? 'bg-green-500/20 text-green-400' :
                'bg-yellow-500/20 text-yellow-400'
              }`}>
                {query.id === 'nested' ? 'SUBQUERY' :
                 query.id === 'multi-join' ? '5 TABLE JOIN' :
                 query.id === 'group-by' ? 'GROUP BY + AGGREGATION' :
                 'LEFT OUTER JOIN'}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Query Results */}
      {loading && (
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 text-center">
          <div className="text-white text-xl">Sorgu çalıştırılıyor...</div>
        </div>
      )}

      {queryResult && !loading && (
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 space-y-6">
          {/* Query Info */}
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">{queryResult.query_name}</h2>
            <p className="text-gray-400">{queryResult.description}</p>
            
            {/* Tables Used */}
            {queryResult.tables_used && (
              <div className="mt-3 flex items-center gap-2">
                <span className="text-gray-500 text-sm">Tablolar:</span>
                {queryResult.tables_used.map((table, i) => (
                  <span key={i} className="px-2 py-1 bg-white/10 text-white text-xs rounded">
                    {table}
                  </span>
                ))}
              </div>
            )}
            
            {/* Extra Info */}
            {queryResult.avg_payment && (
              <div className="mt-2 text-sm text-gray-400">
                Ortalama Ödeme: <span className="text-green-400 font-semibold">${queryResult.avg_payment.toFixed(2)}</span>
              </div>
            )}
            {queryResult.customers_without_orders !== undefined && (
              <div className="mt-2 text-sm text-gray-400">
                Siparişi Olmayan Müşteri Sayısı: <span className="text-yellow-400 font-semibold">{queryResult.customers_without_orders}</span>
              </div>
            )}
          </div>

          {/* SQL Code */}
          <div className="border border-white/20 rounded-xl overflow-hidden">
            <button
              onClick={() => setShowSql(!showSql)}
              className="w-full flex items-center justify-between p-4 bg-white/5 hover:bg-white/10 transition-colors"
            >
              <div className="flex items-center gap-2 text-gray-300">
                <Code className="w-5 h-5" />
                <span className="font-semibold">SQL Sorgusu</span>
              </div>
              {showSql ? <ChevronUp className="w-5 h-5 text-gray-400" /> : <ChevronDown className="w-5 h-5 text-gray-400" />}
            </button>
            {showSql && (
              <pre className="p-4 bg-black/30 text-green-400 font-mono text-sm overflow-x-auto whitespace-pre-wrap">
                {queryResult.sql}
              </pre>
            )}
          </div>

          {/* Results Table */}
          <div>
            <h3 className="text-xl font-semibold text-white mb-4">
              Sonuçlar ({queryResult.results.length} kayıt)
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/20">
                    {queryResult.results.length > 0 && 
                      Object.keys(queryResult.results[0]).map((key) => (
                        <th key={key} className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">
                          {key.replace(/_/g, ' ').toUpperCase()}
                        </th>
                      ))
                    }
                  </tr>
                </thead>
                <tbody>
                  {queryResult.results.map((row, i) => (
                    <tr key={i} className="border-b border-white/10 hover:bg-white/5 transition-colors">
                      {Object.entries(row).map(([key, value], j) => (
                        <td key={j} className="py-3 px-4 text-white text-sm">
                          {key.includes('value') || key.includes('price') || key.includes('revenue') || key.includes('freight') || key.includes('spent')
                            ? `$${(typeof value === 'number' ? value : 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                            : key.includes('pct') || key.includes('avg_price')
                            ? `${(typeof value === 'number' ? value : 0).toFixed(2)}`
                            : typeof value === 'boolean'
                            ? (value ? <span className="text-green-400">✓ Evet</span> : <span className="text-red-400">✗ Hayır</span>)
                            : String(value ?? '-')
                          }
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* No Query Selected */}
      {!queryResult && !loading && (
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-12 border border-white/20 text-center">
          <Database className="w-16 h-16 text-gray-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Sorgu Seçin</h3>
          <p className="text-gray-400">Yukarıdaki kartlardan bir sorgu seçerek sonuçları görüntüleyin</p>
        </div>
      )}
    </div>
  );
}
