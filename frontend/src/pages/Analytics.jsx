import { useState, useEffect } from 'react';
import { getMetrics, getRecent, getEvaluationResults, runEvaluation } from '../api/analyticsApi';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const COLORS = ['#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function Analytics() {
  const [metrics, setMetrics] = useState(null);
  const [recent, setRecent] = useState([]);
  const [evalResults, setEvalResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [evalRunning, setEvalRunning] = useState(false);

  useEffect(() => {
    fetchAll();
  }, []);

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [m, r] = await Promise.all([
        getMetrics(),
        getRecent()
      ]);
      setMetrics(m);
      setRecent(r.recent || []);

      try {
        const ev = await getEvaluationResults();
        setEvalResults(ev);
      } catch {
        // No eval results yet
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunEval = async () => {
    setEvalRunning(true);
    try {
      await runEvaluation('balanced');
      setTimeout(() => {
        fetchAll();
        setEvalRunning(false);
      }, 3000);
    } catch {
      setEvalRunning(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p style={{ color: '#64748b' }}>Loading analytics...</p>
      </div>
    );
  }

  // Prepare chart data
  const modeData = metrics?.mode_distribution
    ? Object.entries(metrics.mode_distribution).map(([k, v]) => ({
        name: k, value: v
      }))
    : [];

  const failureData = metrics?.failure_types
    ? Object.entries(metrics.failure_types).map(([k, v]) => ({
        name: k, value: v
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            Analytics Dashboard
          </h1>
          <p className="text-sm mt-1" style={{ color: '#64748b' }}>
            Live metrics from all generation runs
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={fetchAll}
            className="px-4 py-2 rounded-lg text-sm font-medium"
            style={{
              background: '#1a1a2e',
              color: '#94a3b8',
              border: '1px solid #2a2a3e'
            }}>
            🔄 Refresh
          </button>
          <button
            onClick={handleRunEval}
            disabled={evalRunning}
            className="px-4 py-2 rounded-lg text-sm font-medium"
            style={{
              background: evalRunning ? '#2a2a3e' : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: '#fff',
              cursor: evalRunning ? 'not-allowed' : 'pointer'
            }}>
            {evalRunning ? '⏳ Running...' : '🧪 Run Evaluation'}
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
        {[
          {
            label: 'Total Generations',
            value: metrics?.total_generations || 0,
            icon: '⚡',
            color: '#6366f1'
          },
          {
            label: 'Success Rate',
            value: `${metrics?.success_rate || 0}%`,
            icon: '✅',
            color: '#22c55e'
          },
          {
            label: 'Avg Latency',
            value: `${metrics?.average_latency || 0}s`,
            icon: '⏱️',
            color: '#f59e0b'
          },
          {
            label: 'Avg Retries',
            value: metrics?.average_retries || 0,
            icon: '🔁',
            color: '#8b5cf6'
          },
          {
            label: 'Avg Confidence',
            value: `${Math.round((metrics?.average_confidence || 0) * 100)}%`,
            icon: '🎯',
            color: '#ec4899'
          },
        ].map((stat, i) => (
          <div key={i} className="p-4 rounded-xl"
            style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
            <div className="flex items-center gap-2 mb-2">
              <span>{stat.icon}</span>
              <span className="text-xs" style={{ color: '#64748b' }}>
                {stat.label}
              </span>
            </div>
            <div className="text-2xl font-bold" style={{ color: stat.color }}>
              {stat.value}
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Mode Distribution */}
        <div className="p-5 rounded-xl"
          style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
          <h3 className="text-sm font-semibold mb-4" style={{ color: '#e2e8f0' }}>
            Mode Distribution
          </h3>
          {modeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={modeData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {modeData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: '#1a1a2e',
                    border: '1px solid #2a2a3e',
                    color: '#e2e8f0'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-48">
              <p className="text-sm" style={{ color: '#64748b' }}>
                No data yet — generate some apps first
              </p>
            </div>
          )}
        </div>

        {/* Failure Types */}
        <div className="p-5 rounded-xl"
          style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
          <h3 className="text-sm font-semibold mb-4" style={{ color: '#e2e8f0' }}>
            Failure Types
          </h3>
          {failureData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={failureData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    background: '#1a1a2e',
                    border: '1px solid #2a2a3e',
                    color: '#e2e8f0'
                  }}
                />
                <Bar dataKey="value" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-48">
              <p className="text-sm" style={{ color: '#22c55e' }}>
                ✅ No failures recorded
              </p>
            </div>
          )}
        </div>

      </div>

      {/* Recent Generations */}
      <div className="p-5 rounded-xl mb-6"
        style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
        <h3 className="text-sm font-semibold mb-4" style={{ color: '#e2e8f0' }}>
          Recent Generations
        </h3>

        {recent.length === 0 ? (
          <p className="text-sm" style={{ color: '#64748b' }}>
            No generations yet
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr style={{ borderBottom: '1px solid #2a2a3e' }}>
                  {['Prompt', 'Mode', 'Status', 'Confidence', 'Latency', 'Retries'].map(h => (
                    <th key={h} className="text-left pb-3 pr-4 text-xs font-medium"
                      style={{ color: '#64748b' }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {recent.map((item, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #1a1a2e' }}>
                    <td className="py-3 pr-4" style={{ color: '#94a3b8', maxWidth: '300px' }}>
                      <span className="truncate block">{item.prompt}</span>
                    </td>
                    <td className="py-3 pr-4">
                      <span className="px-2 py-1 rounded text-xs"
                        style={{
                          background: '#6366f122',
                          color: '#6366f1'
                        }}>
                        {item.mode}
                      </span>
                    </td>
                    <td className="py-3 pr-4">
                      <span className="px-2 py-1 rounded text-xs font-medium"
                        style={{
                          background: item.success ? '#22c55e22' : '#ef444422',
                          color: item.success ? '#22c55e' : '#ef4444'
                        }}>
                        {item.success ? '✅ Success' : '❌ Failed'}
                      </span>
                    </td>
                    <td className="py-3 pr-4" style={{ color: '#e2e8f0' }}>
                      {Math.round(item.confidence * 100)}%
                    </td>
                    <td className="py-3 pr-4" style={{ color: '#e2e8f0' }}>
                      {item.latency}s
                    </td>
                    <td className="py-3" style={{ color: '#e2e8f0' }}>
                      {item.retries}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Evaluation Results */}
      {evalResults && (
        <div className="p-5 rounded-xl"
          style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
          <h3 className="text-sm font-semibold mb-4" style={{ color: '#e2e8f0' }}>
            🧪 Evaluation Results
          </h3>

          {/* Summary */}
          <div className="grid grid-cols-4 gap-4 mb-4">
            {[
              { label: 'Total Prompts', value: evalResults.total_prompts, color: '#6366f1' },
              { label: 'Success Rate', value: `${evalResults.success_rate}%`, color: '#22c55e' },
              { label: 'Avg Latency', value: `${evalResults.average_latency}s`, color: '#f59e0b' },
              { label: 'Avg Retries', value: evalResults.average_retries, color: '#8b5cf6' },
            ].map((s, i) => (
              <div key={i} className="p-3 rounded-lg text-center"
                style={{ background: '#0f0f1a' }}>
                <div className="text-xl font-bold" style={{ color: s.color }}>
                  {s.value}
                </div>
                <div className="text-xs mt-1" style={{ color: '#64748b' }}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>

          {/* Individual Results */}
          <div className="flex flex-col gap-2">
            {evalResults.results?.map((r, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg"
                style={{ background: '#0f0f1a' }}>
                <div className="flex items-center gap-3">
                  <span>{r.success ? '✅' : '❌'}</span>
                  <span className="text-xs" style={{ color: '#94a3b8' }}>
                    {r.prompt?.substring(0, 60)}...
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-xs" style={{ color: '#64748b' }}>
                    {r.latency}s
                  </span>
                  <span className="text-xs" style={{ color: '#64748b' }}>
                    {Math.round(r.confidence * 100)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}