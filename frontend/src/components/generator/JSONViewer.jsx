import { useState } from 'react';

const tabs = [
  { id: 'ui_schema', label: '🖥️ UI', key: 'ui_schema' },
  { id: 'api_schema', label: '🔌 API', key: 'api_schema' },
  { id: 'db_schema', label: '🗄️ Database', key: 'db_schema' },
  { id: 'auth_schema', label: '🔐 Auth', key: 'auth_schema' },
  { id: 'business_logic', label: '⚙️ Logic', key: 'business_logic' },
];

export default function JSONViewer({ data }) {
  const [activeTab, setActiveTab] = useState('ui_schema');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const content = data[activeTab];
    navigator.clipboard.writeText(JSON.stringify(content, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob(
      [JSON.stringify(data, null, 2)],
      { type: 'application/json' }
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.app_name || 'orbit'}-blueprint.json`;
    a.click();
  };

  return (
    <div className="flex flex-col h-full">

      {/* App name + actions */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold" style={{ color: '#e2e8f0' }}>
            {data.app_name}
          </h2>
          <p className="text-xs" style={{ color: '#64748b' }}>
            Generated in {data.latency_seconds}s
            · {data.retries_used} retries
            · Mode: {data.mode}
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
            style={{
              background: copied ? '#22c55e22' : '#1a1a2e',
              color: copied ? '#22c55e' : '#94a3b8',
              border: '1px solid #2a2a3e'
            }}>
            {copied ? '✅ Copied' : '📋 Copy'}
          </button>
          <button
            onClick={handleDownload}
            className="px-3 py-1.5 rounded-lg text-xs font-medium"
            style={{
              background: '#6366f122',
              color: '#6366f1',
              border: '1px solid #6366f133'
            }}>
            ⬇️ Download
          </button>
        </div>
      </div>

      {/* Schema Tabs */}
      <div className="flex gap-1 mb-3 flex-wrap">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
            style={{
              background: activeTab === tab.id ? '#6366f1' : '#1a1a2e',
              color: activeTab === tab.id ? '#fff' : '#94a3b8',
              border: activeTab === tab.id ? 'none' : '1px solid #2a2a3e'
            }}>
            {tab.label}
          </button>
        ))}
      </div>

      {/* JSON Content */}
      <div className="flex-1 rounded-xl overflow-auto"
        style={{
          background: '#0d0d1a',
          border: '1px solid #2a2a3e',
          maxHeight: '500px'
        }}>
        <pre className="p-4 text-xs leading-relaxed"
          style={{
            color: '#e2e8f0',
            fontFamily: 'JetBrains Mono, monospace',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word'
          }}>
          {JSON.stringify(data[activeTab], null, 2)}
        </pre>
      </div>

    </div>
  );
}