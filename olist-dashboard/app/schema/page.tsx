'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, Key, Link, Table, ChevronDown, ChevronUp, FileCode } from 'lucide-react';

const API_BASE = 'http://localhost:5000';

interface ForeignKey {
  column: string;
  references: string;
}

interface TableInfo {
  name: string;
  description: string;
  columns: string[];
  pk: string;
  fk: ForeignKey[];
}

interface SchemaData {
  tables: TableInfo[];
  relationships: string[];
}

export default function SchemaPage() {
  const [schema, setSchema] = useState<SchemaData | null>(null);
  const [expandedTable, setExpandedTable] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchSchema();
  }, []);

  const fetchSchema = async () => {
    try {
      const res = await axios.get(`${API_BASE}/schema`);
      setSchema(res.data);
    } catch (err) {
      console.error('Failed to fetch schema:', err);
    }
  };

  const toggleTable = (tableName: string) => {
    setExpandedTable(expandedTable === tableName ? null : tableName);
  };

  if (!mounted) return null;

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Database Schema</h1>
        <p className="text-gray-400">
          Veritabanı Tasarımı - Tüm tablolar, Primary Key ve Foreign Key ilişkileri
        </p>
      </div>

      {/* Info Box */}
      <div className="bg-green-500/10 border border-green-500/30 rounded-2xl p-6">
        <h3 className="text-green-400 font-semibold mb-2 flex items-center gap-2">
          <Database className="w-5 h-5" />
          Veritabanı Tasarımı Özeti
        </h3>
        <ul className="text-gray-300 text-sm space-y-1">
          <li>✓ Tüm tablolarda <strong className="text-white">Primary Key (PK)</strong> tanımlı</li>
          <li>✓ İlişkili tablolar arasında <strong className="text-white">Foreign Key (FK)</strong> tanımlı</li>
          <li>✓ <strong className="text-white">ORM kullanılmamıştır</strong> - Tüm sorgular raw SQL</li>
          <li>✓ İlişki tablosu mevcut: <strong className="text-white">order_items</strong> (çoktan-çoğa ilişki)</li>
        </ul>
      </div>

      {/* ERD Diagram Placeholder */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <Link className="w-6 h-6" />
          Entity Relationship Diagram
        </h2>
        
        {/* Visual ERD */}
        <div className="bg-black/30 rounded-xl p-6 overflow-x-auto">
          <div className="min-w-[800px]">
            {/* Row 1 */}
            <div className="flex justify-around mb-8">
              <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-blue-400 font-bold mb-2">customers</div>
                <div className="text-xs text-gray-400">PK: customer_id</div>
              </div>
              <div className="bg-purple-500/20 border border-purple-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-purple-400 font-bold mb-2">sellers</div>
                <div className="text-xs text-gray-400">PK: seller_id</div>
              </div>
              <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-green-400 font-bold mb-2">products</div>
                <div className="text-xs text-gray-400">PK: product_id</div>
              </div>
            </div>
            
            {/* Connection Lines (visual) */}
            <div className="flex justify-center mb-4">
              <div className="text-gray-500 text-sm">│</div>
            </div>
            <div className="flex justify-center mb-4">
              <div className="text-gray-400 text-xs px-4">FK: customer_id</div>
            </div>
            <div className="flex justify-center mb-4">
              <div className="text-gray-500 text-sm">▼</div>
            </div>
            
            {/* Row 2 */}
            <div className="flex justify-center mb-8">
              <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-yellow-400 font-bold mb-2">orders</div>
                <div className="text-xs text-gray-400">PK: order_id</div>
                <div className="text-xs text-yellow-500">FK: customer_id</div>
              </div>
            </div>
            
            {/* Connection Lines */}
            <div className="flex justify-around mb-4">
              <div className="text-gray-500 text-sm">│</div>
              <div className="text-gray-500 text-sm">│</div>
              <div className="text-gray-500 text-sm">│</div>
            </div>
            <div className="flex justify-around mb-4">
              <div className="text-gray-500 text-sm">▼</div>
              <div className="text-gray-500 text-sm">▼</div>
              <div className="text-gray-500 text-sm">▼</div>
            </div>
            
            {/* Row 3 */}
            <div className="flex justify-around">
              <div className="bg-orange-500/20 border border-orange-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-orange-400 font-bold mb-2">order_payments</div>
                <div className="text-xs text-gray-400">PK: order_id + seq</div>
                <div className="text-xs text-orange-500">FK: order_id</div>
              </div>
              <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-red-400 font-bold mb-2">order_items</div>
                <div className="text-xs text-gray-400">PK: order_id + item_id</div>
                <div className="text-xs text-red-500">FK: order_id, product_id, seller_id</div>
              </div>
              <div className="bg-pink-500/20 border border-pink-500/50 rounded-lg p-4 w-48 text-center">
                <div className="text-pink-400 font-bold mb-2">order_reviews</div>
                <div className="text-xs text-gray-400">PK: review_id</div>
                <div className="text-xs text-pink-500">FK: customer_id</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Table List */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Table className="w-6 h-6" />
          Tablolar ve İlişkiler
        </h2>

        <div className="space-y-4">
          {schema?.tables.map((table) => (
            <div key={table.name} className="border border-white/20 rounded-xl overflow-hidden">
              <button
                onClick={() => toggleTable(table.name)}
                className="w-full flex items-center justify-between p-4 bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className={`p-2 rounded-lg ${
                    table.fk.length === 0 ? 'bg-blue-500/20 text-blue-400' :
                    table.fk.length >= 2 ? 'bg-red-500/20 text-red-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    <Database className="w-5 h-5" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-white font-semibold">{table.name}</h3>
                    <p className="text-gray-400 text-sm">{table.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex gap-2">
                    <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded">
                      PK: {table.pk}
                    </span>
                    {table.fk.length > 0 && (
                      <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded">
                        {table.fk.length} FK
                      </span>
                    )}
                  </div>
                  {expandedTable === table.name ? 
                    <ChevronUp className="w-5 h-5 text-gray-400" /> : 
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  }
                </div>
              </button>
              
              {expandedTable === table.name && (
                <div className="p-4 bg-black/20 border-t border-white/10">
                  {/* Columns */}
                  <div className="mb-4">
                    <h4 className="text-gray-400 text-sm mb-2 flex items-center gap-2">
                      <FileCode className="w-4 h-4" /> Columns
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {table.columns.map((col, i) => (
                        <span 
                          key={i} 
                          className={`px-3 py-1 rounded text-sm ${
                            col.includes('PK') ? 'bg-green-500/20 text-green-400 border border-green-500/50' :
                            col.includes('FK') ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50' :
                            'bg-white/10 text-gray-300'
                          }`}
                        >
                          {col.includes('PK') && <Key className="w-3 h-3 inline mr-1" />}
                          {col.includes('FK') && <Link className="w-3 h-3 inline mr-1" />}
                          {col}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  {/* Foreign Keys Detail */}
                  {table.fk.length > 0 && (
                    <div>
                      <h4 className="text-gray-400 text-sm mb-2 flex items-center gap-2">
                        <Link className="w-4 h-4" /> Foreign Key İlişkileri
                      </h4>
                      <div className="space-y-2">
                        {table.fk.map((fk, i) => (
                          <div key={i} className="flex items-center gap-2 text-sm">
                            <span className="text-yellow-400">{fk.column}</span>
                            <span className="text-gray-500">→</span>
                            <span className="text-blue-400">{fk.references}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Relationships */}
      {schema?.relationships && (
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <Link className="w-6 h-6" />
            İlişki Özeti
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {schema.relationships.map((rel, i) => (
              <div key={i} className="bg-white/5 rounded-lg p-4 flex items-center gap-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span className="text-gray-300 font-mono text-sm">{rel}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* DDL Info */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <FileCode className="w-6 h-6" />
          DDL Dosyaları
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">000_base.sql</h4>
            <p className="text-gray-400 text-sm">Ana tabloların CREATE TABLE tanımları (PK dahil)</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">030_fk_v2_1.sql</h4>
            <p className="text-gray-400 text-sm">Foreign Key constraint tanımları (ALTER TABLE)</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">040_indexes.sql</h4>
            <p className="text-gray-400 text-sm">Performans için index tanımları</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2">010_categories.sql & 020_geo_zip.sql</h4>
            <p className="text-gray-400 text-sm">Dimension tabloları (kategori, coğrafi veri)</p>
          </div>
        </div>
      </div>
    </div>
  );
}
