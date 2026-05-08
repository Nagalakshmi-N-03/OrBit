export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'generator', label: '⚡ Generator' },
    { id: 'analytics', label: '📊 Analytics' },
  ];

  return (
    <header className="border-b px-6 py-4 flex items-center justify-between"
      style={{ borderColor: '#2a2a3e', background: '#0f0f1a' }}>

      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
          <span className="text-white font-bold">O</span>
        </div>
        <div>
          <span className="text-xl font-bold" style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            OrBit
          </span>
          <p className="text-xs" style={{ color: '#64748b' }}>
            AI App Blueprint Generator
          </p>
        </div>
      </div>

      {/* Tabs */}
      <nav className="flex gap-2">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="px-4 py-2 rounded-lg text-sm font-medium transition-all"
            style={{
              background: activeTab === tab.id
                ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
                : 'transparent',
              color: activeTab === tab.id ? '#fff' : '#94a3b8',
              border: activeTab === tab.id ? 'none' : '1px solid #2a2a3e'
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Status */}
      <div className="flex items-center gap-2 px-3 py-1 rounded-full"
        style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
        <div className="w-2 h-2 rounded-full bg-green-500"
          style={{ animation: 'pulse 2s infinite' }} />
        <span className="text-xs" style={{ color: '#94a3b8' }}>System Live</span>
      </div>

    </header>
  );
}