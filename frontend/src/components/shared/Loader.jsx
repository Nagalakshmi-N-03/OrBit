export default function Loader({ message = "Generating..." }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">

      {/* Spinning ring */}
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-transparent"
          style={{ borderTopColor: '#6366f1', animation: 'spin 1s linear infinite' }} />
        <div className="absolute inset-2 rounded-full border-4 border-transparent"
          style={{ borderTopColor: '#8b5cf6', animation: 'spin 1.5s linear infinite reverse' }} />
        <div className="absolute inset-4 rounded-full"
          style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', animation: 'pulse 2s infinite' }} />
      </div>

      {/* Message */}
      <p className="text-sm font-medium" style={{ color: '#94a3b8' }}>
        {message}
      </p>

      {/* Stage indicators */}
      <div className="flex gap-2 mt-2">
        {['Intent', 'Design', 'Schema', 'Validate'].map((stage, i) => (
          <div key={stage} className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full"
              style={{
                background: '#6366f1',
                animation: `pulse 1s infinite ${i * 0.2}s`
              }} />
            <span className="text-xs" style={{ color: '#64748b' }}>{stage}</span>
          </div>
        ))}
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
}