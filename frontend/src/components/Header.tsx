'use client';
import { useState } from 'react';
import { Play, Bug, Microscope, Zap, ChevronDown } from 'lucide-react';

const TABS = [
  { id: 'compiler',   label: 'Compile & Run', icon: Play },
  { id: 'debugger',   label: 'Debugger',      icon: Bug },
  { id: 'visualizer', label: 'Visualizer',    icon: Microscope },
  { id: 'optimizer',  label: 'Optimizer',     icon: Zap },
];

const LANGUAGES = [
  { id: 'python',     icon: '🐍', label: 'Python' },
  { id: 'javascript', icon: '🟨', label: 'JavaScript' },
  { id: 'typescript', icon: '🔷', label: 'TypeScript' },
  { id: 'java',       icon: '☕', label: 'Java' },
  { id: 'cpp',        icon: '⚙️', label: 'C++' },
  { id: 'c',          icon: '⚙️', label: 'C' },
  { id: 'go',         icon: '🐹', label: 'Go' },
  { id: 'rust',       icon: '🦀', label: 'Rust' },
];

interface HeaderProps {
  activeTab: string;
  setActiveTab: (t: string) => void;
  language: string;
  setLanguage: (l: string) => void;
}

export default function Header({ activeTab, setActiveTab, language, setLanguage }: HeaderProps) {
  const [showLangMenu, setShowLangMenu] = useState(false);
  const currentLang = LANGUAGES.find(l => l.id === language) || LANGUAGES[0];

  return (
    <div className="flex flex-col w-full sticky top-0 z-50">
      {/* Top bar: Logo + language pill */}
      <header className="flex items-center h-[60px] px-6 bg-[var(--bg-secondary)] border-b border-[var(--border-subtle)] shadow-[var(--shadow-md)]">
        {/* Logo */}
        <div className="flex items-center gap-3 pr-6 border-r border-[var(--border-subtle)] mr-4 flex-shrink-0">
          <div className="w-9 h-9 rounded-lg flex items-center justify-center text-lg"
               style={{ background: 'var(--grad-hero)', boxShadow: 'var(--glow-violet)' }}>
            🧠
          </div>
          <div className="leading-tight">
            <h1 className="text-[17px] font-extrabold tracking-tight text-gradient">LogicAI</h1>
            <p className="text-[8px] font-semibold tracking-[1.5px] text-[var(--text-muted)] uppercase">Code Intelligence Platform</p>
          </div>
        </div>

        {/* Nav tabs */}
        <div className="flex items-center gap-2">
          {TABS.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                flex items-center gap-2 h-9 px-4 rounded-lg text-[13px] font-semibold transition-all duration-200 border
                ${activeTab === tab.id
                  ? 'text-white border-transparent shadow-[var(--glow-violet)]'
                  : 'bg-transparent text-[var(--text-secondary)] border-[var(--border-subtle)] hover:bg-[var(--bg-glass)] hover:text-white hover:-translate-y-[1px] hover:border-[var(--border-mid)]'
                }
              `}
              style={activeTab === tab.id ? { background: 'var(--grad-hero)' } : {}}
            >
              <tab.icon size={14} />
              {tab.label}
            </button>
          ))}
        </div>

        <div className="flex-1" />

        {/* Language selector */}
        <div className="relative">
          <button
            onClick={() => setShowLangMenu(!showLangMenu)}
            className="flex items-center gap-2 h-9 px-4 rounded-lg text-[12px] font-semibold border border-[var(--border-subtle)] bg-[var(--bg-card)] text-[var(--text-secondary)] hover:border-[var(--border-mid)] transition-all"
          >
            <span>{currentLang.icon}</span>
            <span>{currentLang.label}</span>
            <ChevronDown size={12} className={`transition-transform ${showLangMenu ? 'rotate-180' : ''}`} />
          </button>

          {showLangMenu && (
            <div className="absolute right-0 top-full mt-2 w-48 bg-[var(--bg-card)] border border-[var(--border-mid)] rounded-xl shadow-[var(--shadow-lg)] overflow-hidden z-50 animate-fade-in-up">
              {LANGUAGES.map(lang => (
                <button
                  key={lang.id}
                  onClick={() => { setLanguage(lang.id); setShowLangMenu(false); }}
                  className={`
                    w-full flex items-center gap-3 px-4 py-2.5 text-[13px] font-medium transition-all
                    ${language === lang.id
                      ? 'bg-[var(--bg-glass)] text-[var(--violet)] border-l-2 border-l-[var(--violet)]'
                      : 'text-[var(--text-secondary)] hover:bg-[var(--bg-glass)] hover:text-white'
                    }
                  `}
                >
                  <span>{lang.icon}</span>
                  <span>{lang.label}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </header>
    </div>
  );
}
