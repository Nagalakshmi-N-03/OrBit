export default function ValidationReport({ report }) {
  if (!report) return null;

  const { errors_found, errors_fixed, status, errors } = report;

  const statusColor = status === 'clean'
    ? '#22c55e'
    : status === 'repaired'
    ? '#f59e0b'
    : '#ef4444';

  const statusIcon = status === 'clean'
    ? '✅'
    : status === 'repaired'
    ? '🔧'
    : '❌';

  return (
    <div className="p-4 rounded-xl"
      style={{ background: '#1a1a2e', border: `1px solid ${statusColor}33` }}>

      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span>{statusIcon}</span>
          <span className="text-sm font-semibold" style={{ color: statusColor }}>
            Validation Report
          </span>
        </div>
        <span className="text-xs px-2 py-1 rounded-full font-medium"
          style={{ background: `${statusColor}22`, color: statusColor }}>
          {status.toUpperCase()}
        </span>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="p-3 rounded-lg text-center"
          style={{ background: '#0f0f1a' }}>
          <div className="text-xl font-bold" style={{ color: '#ef4444' }}>
            {errors_found}
          </div>
          <div className="text-xs" style={{ color: '#64748b' }}>
            Errors Found
          </div>
        </div>
        <div className="p-3 rounded-lg text-center"
          style={{ background: '#0f0f1a' }}>
          <div className="text-xl font-bold" style={{ color: '#22c55e' }}>
            {errors_fixed}
          </div>
          <div className="text-xs" style={{ color: '#64748b' }}>
            Errors Fixed
          </div>
        </div>
      </div>

      {/* Error List */}
      {errors && errors.length > 0 && (
        <div className="flex flex-col gap-2 mt-3">
          {errors.map((err, i) => (
            <div key={i} className="flex items-start gap-2 p-2 rounded-lg"
              style={{ background: '#0f0f1a' }}>
              <span className="text-xs mt-0.5">
                {err.fixed ? '✅' : '❌'}
              </span>
              <div>
                <span className="text-xs font-medium"
                  style={{ color: err.fixed ? '#22c55e' : '#ef4444' }}>
                  [{err.layer}]
                </span>
                <span className="text-xs ml-1" style={{ color: '#94a3b8' }}>
                  {err.description}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}