'use client';
import { useState } from 'react';
import Header from '../components/Header';
import CompilerPage from '../components/CompilerPage';
import DebuggerPage from '../components/DebuggerPage';
import VisualizerPage from '../components/VisualizerPage';
import OptimizerPage from '../components/OptimizerPage';

export default function Home() {
  const [activeTab, setActiveTab] = useState('compiler');
  const [code, setCode] = useState<string>(
    '# Welcome to LogicAI!\n# Write your code and use the AI Mentor panel on the right.\n\ndef greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("World"))\n'
  );
  const [language, setLanguage] = useState('python');

  return (
    <main className="flex h-screen w-full flex-col bg-[var(--bg-base)] overflow-hidden relative">
      {/* Background mesh glow */}
      <div className="absolute top-[-15%] left-[-10%] w-[45%] h-[45%] rounded-full bg-[var(--violet)] opacity-[0.025] blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-15%] right-[-10%] w-[45%] h-[45%] rounded-full bg-[var(--cyan)] opacity-[0.025] blur-[120px] pointer-events-none"></div>

      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        language={language}
        setLanguage={setLanguage}
      />

      <div className="flex flex-1 overflow-hidden relative z-10">
        {activeTab === 'compiler' && (
          <CompilerPage code={code} setCode={setCode} language={language} />
        )}
        {activeTab === 'debugger' && (
          <DebuggerPage code={code} language={language} />
        )}
        {activeTab === 'visualizer' && (
          <VisualizerPage code={code} language={language} />
        )}
        {activeTab === 'optimizer' && (
          <OptimizerPage code={code} language={language} />
        )}
      </div>
    </main>
  );
}
