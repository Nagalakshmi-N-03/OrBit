import { useState } from 'react';
import Navbar from './components/shared/Navbar';
import Generator from './pages/Generator';
import Analytics from './pages/Analytics';

export default function App() {
  const [activeTab, setActiveTab] = useState('generator');

  return (
    <div style={{ minHeight: '100vh', background: '#0f0f1a' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="p-6">
        {activeTab === 'generator' && <Generator />}
        {activeTab === 'analytics' && <Analytics />}
      </main>
    </div>
  );
}