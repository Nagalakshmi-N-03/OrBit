const modes = [
  {
    id: 'fast',
    icon: '⚡',
    label: 'Fast',
    desc: '2 stages, quick output',
    color: '#f59e0b',
    time: '~15s'
  },
  {
    id: 'balanced',
    icon: '⚖️',
    label: 'Balanced',
    desc: 'All stages, standard validation',
    color: '#6366f1',
    time: '~30s'
  },
  {
    id: 'quality',
    icon: '🏆',
    label: 'Quality',
    desc: 'Deep repair + simulation',
    color: '#22c55e',
    time: '~60s'
  }
];

export default function ModeSelector({ selected, onChange }) {
  return (
    <div>
      <p className="text-xs font-medium mb-2" style={{ color: '#94a3b8' }}>
        GENERATION MODE
      </p>
      <div className="grid grid-cols-3 gap-2">
        {modes.map(mode => (
          <button
            key={mode.id}
            onClick={() => onChange(mode.id)}
            className="p-3 rounded-xl text-left transition-all"
            style={{
              background: selected === mode.id
                ? `${mode.color}22`
                : '#1a1a2e',
              border: selected === mode.id
                ? `1px solid ${mode.color}`
                : '1px solid #2a2a3e',
            }}
          >
            <div className="text-lg mb-1">{mode.icon}</div>
            <div className="text-sm font-semibold" style={{
              color: selected === mode.id ? mode.color : '#e2e8f0'
            }}>
              {mode.label}
            </div>
            <div className="text-xs mt-1" style={{ color: '#64748b' }}>
              {mode.desc}
            </div>
            <div className="text-xs mt-1 font-mono" style={{ color: mode.color }}>
              {mode.time}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}