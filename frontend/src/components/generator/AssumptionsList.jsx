export default function AssumptionsList({ assumptions }) {
  if (!assumptions || assumptions.length === 0) return null;

  return (
    <div className="p-4 rounded-xl"
      style={{ background: '#1a1a2e', border: '1px solid #f59e0b33' }}>

      <div className="flex items-center gap-2 mb-3">
        <span>⚠️</span>
        <span className="text-sm font-semibold" style={{ color: '#f59e0b' }}>
          Assumptions Made ({assumptions.length})
        </span>
      </div>

      <div className="flex flex-col gap-2">
        {assumptions.map((assumption, i) => (
          <div key={i} className="flex items-start gap-2">
            <span className="text-xs mt-0.5" style={{ color: '#f59e0b' }}>→</span>
            <span className="text-xs" style={{ color: '#94a3b8' }}>
              {assumption}
            </span>
          </div>
        ))}
      </div>

    </div>
  );
}