import { useState } from 'react';
import ModeSelector from './ModeSelector';

const examples = [
  "Build a project management tool with kanban board, tasks, deadlines, team roles, and notifications",
  "Build a CRM with contacts, deals, pipeline stages, role-based access, and admin analytics",
  "Create an e-commerce store with products, cart, checkout, payments, and inventory management",
  "Build a food delivery app with restaurants, menus, orders, delivery tracking, and payments",
];

export default function PromptInput({ onGenerate, isLoading }) {
  const [prompt, setPrompt] = useState('');
  const [mode, setMode] = useState('balanced');

  const handleSubmit = () => {
    if (!prompt.trim() || isLoading) return;
    onGenerate(prompt, mode);
  };

  return (
    <div className="flex flex-col gap-5">

      {/* Header */}
      <div>
        <h2 className="text-lg font-bold" style={{ color: '#e2e8f0' }}>
          Describe Your App
        </h2>
        <p className="text-sm mt-1" style={{ color: '#64748b' }}>
          Type what you want to build in plain English
        </p>
      </div>

      {/* Text Area */}
      <div className="relative">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Build a project management tool with kanban board, tasks, deadlines, team roles, and notifications..."
          rows={5}
          className="w-full rounded-xl p-4 text-sm resize-none outline-none transition-all"
          style={{
            background: '#1a1a2e',
            border: prompt ? '1px solid #6366f1' : '1px solid #2a2a3e',
            color: '#e2e8f0',
            lineHeight: '1.6'
          }}
        />
        {/* Char count */}
        <span className="absolute bottom-3 right-3 text-xs"
          style={{ color: prompt.length > 1800 ? '#ef4444' : '#64748b' }}>
          {prompt.length}/2000
        </span>
      </div>

      {/* Examples */}
      <div>
        <p className="text-xs font-medium mb-2" style={{ color: '#64748b' }}>
          QUICK EXAMPLES
        </p>
        <div className="flex flex-col gap-2">
          {examples.map((ex, i) => (
            <button
              key={i}
              onClick={() => setPrompt(ex)}
              className="text-left text-xs px-3 py-2 rounded-lg transition-all"
              style={{
                background: '#1a1a2e',
                border: '1px solid #2a2a3e',
                color: '#94a3b8'
              }}
              onMouseEnter={e => e.target.style.borderColor = '#6366f1'}
              onMouseLeave={e => e.target.style.borderColor = '#2a2a3e'}
            >
              {ex.substring(0, 70)}...
            </button>
          ))}
        </div>
      </div>

      {/* Mode Selector */}
      <ModeSelector selected={mode} onChange={setMode} />

      {/* Generate Button */}
      <button
        onClick={handleSubmit}
        disabled={!prompt.trim() || isLoading}
        className="w-full py-4 rounded-xl font-semibold text-white transition-all"
        style={{
          background: !prompt.trim() || isLoading
            ? '#2a2a3e'
            : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
          cursor: !prompt.trim() || isLoading ? 'not-allowed' : 'pointer',
          opacity: !prompt.trim() || isLoading ? 0.5 : 1
        }}
      >
        {isLoading ? '⏳ Generating...' : '⚡ Generate Blueprint'}
      </button>

    </div>
  );
}