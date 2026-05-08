export default function ConfidenceScore({ score }) {
  const percent = Math.round(score * 100);

  const color = percent >= 80
    ? '#22c55e'
    : percent >= 60
    ? '#f59e0b'
    : '#ef4444';

  const label = percent >= 80
    ? 'High Confidence'
    : percent >= 60
    ? 'Medium Confidence'
    : 'Low Confidence';

  return (
    <div className="p-4 rounded-xl"
      style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>

      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium" style={{ color: '#94a3b8' }}>
          Confidence Score
        </span>
        <span className="text-sm font-bold" style={{ color }}>
          {label}
        </span>
      </div>

      {/* Bar */}
      <div className="w-full rounded-full h-2"
        style={{ background: '#2a2a3e' }}>
        <div
          className="h-2 rounded-full transition-all duration-1000"
          style={{ width: `${percent}%`, background: color }}
        />
      </div>

      <div className="flex justify-between mt-2">
        <span className="text-xs" style={{ color: '#64748b' }}>0%</span>
        <span className="text-lg font-bold" style={{ color }}>
          {percent}%
        </span>
        <span className="text-xs" style={{ color: '#64748b' }}>100%</span>
      </div>

    </div>
  );
}