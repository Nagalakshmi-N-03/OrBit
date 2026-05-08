import React, { useState } from 'react';
import Generator from './pages/Generator';
import Analytics from './pages/Analytics';

const tabs = [
  { id: 'generator', label: '⚡ Generator' },
  { id: 'analytics', label: '📊 Analytics' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('generator');

  return (
    <div className="min-h-screen" style={{ background: '#0f0f1a' }}>

      {/* Header */}
      <header className="border-b border-orbit-border px-6 py-4 flex items-center justify-between"
        style={{ borderColor: '#2a2a3e' }}>

        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
            <span className="text-white font-bold text-sm">O</span>
          </div>
          <span className="text-xl font-bold gradient-text">OrBit</span>
          <span className="text-xs px-2 py-1 rounded-full"
            style={{ background: '#1a1a2e', color: '#94a3b8', border: '1px solid #2a2a3e' }}>
            v1.0.0
          </span>
        </div>

        {/* Tabs */}
        <nav className="flex gap-2">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className="px-4 py-2 rounded-lg text-sm font-medium transition-all"
              style={{
                background: activeTab === tab.id ? '#6366f1' : 'transparent',
                color: activeTab === tab.id ? '#fff' : '#94a3b8',
                border: activeTab === tab.id ? 'none' : '1px solid #2a2a3e'
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        {/* Status */}
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-sm" style={{ color: '#94a3b8' }}>Live</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6">
        {activeTab === 'generator' && <Generator />}
        {activeTab === 'analytics' && <Analytics />}
      </main>

    </div>
  );
}