import { useState } from 'react';
import PromptInput from '../components/generator/PromptInput';
import JSONViewer from '../components/generator/JSONViewer';
import ConfidenceScore from '../components/generator/ConfidenceScore';
import AssumptionsList from '../components/generator/AssumptionsList';
import ValidationReport from '../components/generator/ValidationReport';
import Loader from '../components/shared/Loader';
import { generateApp } from '../api/generatorApi';

export default function Generator() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async (prompt, mode) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await generateApp(prompt, mode);
      setResult(data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (detail?.error === 'prompt_too_vague') {
        setError({
          type: 'vague',
          message: detail.message,
          question: detail.question
        });
      } else {
        setError({
          type: 'error',
          message: detail?.message || 'Something went wrong'
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto">

      {/* Page Title */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold" style={{
          background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          App Blueprint Generator
        </h1>
        <p className="text-sm mt-1" style={{ color: '#64748b' }}>
          Describe any app in plain English → Get complete technical blueprint
        </p>
      </div>

      {/* Two Panel Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Left Panel — Input */}
        <div className="p-6 rounded-2xl"
          style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>
          <PromptInput
            onGenerate={handleGenerate}
            isLoading={isLoading}
          />
        </div>

        {/* Right Panel — Output */}
        <div className="p-6 rounded-2xl"
          style={{ background: '#1a1a2e', border: '1px solid #2a2a3e' }}>

          {/* Loading */}
          {isLoading && (
            <Loader message="Running pipeline stages..." />
          )}

          {/* Error */}
          {error && !isLoading && (
            <div className="p-4 rounded-xl"
              style={{ background: '#ef444422', border: '1px solid #ef444433' }}>
              <p className="text-sm font-semibold" style={{ color: '#ef4444' }}>
                {error.type === 'vague' ? '❓ Prompt Too Vague' : '❌ Error'}
              </p>
              <p className="text-sm mt-2" style={{ color: '#94a3b8' }}>
                {error.message}
              </p>
              {error.question && (
                <p className="text-sm mt-2 font-medium" style={{ color: '#f59e0b' }}>
                  → {error.question}
                </p>
              )}
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !result && !error && (
            <div className="flex flex-col items-center justify-center h-full py-16 gap-4">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center"
                style={{ background: '#6366f122' }}>
                <span className="text-3xl">⚡</span>
              </div>
              <p className="text-sm font-medium" style={{ color: '#64748b' }}>
                Your blueprint will appear here
              </p>
              <p className="text-xs text-center" style={{ color: '#475569' }}>
                Type a prompt and click Generate Blueprint
              </p>
            </div>
          )}

          {/* Result */}
          {result && !isLoading && (
            <div className="flex flex-col gap-4">
              <ConfidenceScore score={result.confidence} />
              <JSONViewer data={result} />
              <AssumptionsList assumptions={result.assumptions} />
              <ValidationReport report={result.validation_report} />
            </div>
          )}

        </div>
      </div>
    </div>
  );
}