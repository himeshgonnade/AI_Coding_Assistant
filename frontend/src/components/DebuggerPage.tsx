'use client';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const API = 'http://localhost:8000';

interface DebugMessage {
  role: 'user' | 'assistant' | 'context';
  content: string;
}

interface DebuggerPageProps {
  code: string;
  language: string;
}

export default function DebuggerPage({ code, language }: DebuggerPageProps) {
  const [started, setStarted] = useState(false);
  const [history, setHistory] = useState<DebugMessage[]>([]);
  const [bugCategory, setBugCategory] = useState('');
  const [errorInput, setErrorInput] = useState('');
  const [userResp, setUserResp] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const startSession = async () => {
    if (!code.trim() || !errorInput.trim()) return;
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/api/debug/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, error: errorInput }),
      });
      const data = await res.json();
      const d = data.data;
      setBugCategory(d.bug_category || '');
      let opening = `${d.initial_observation || ''}\n\n**${d.first_question || 'What do you think is happening?'}**`;
      if (d.hint_print_statement) {
        opening += `\n\n*Try adding this to investigate:*\n\`\`\`python\n${d.hint_print_statement}\n\`\`\``;
      }
      setHistory([
        { role: 'context', content: `**Code:**\n\`\`\`\n${code}\n\`\`\`\n\n**Error:** ${errorInput}` },
        { role: 'assistant', content: opening },
      ]);
      setStarted(true);
    } catch {
      setHistory([{ role: 'assistant', content: '⚠️ Could not connect to AI backend.' }]);
      setStarted(true);
    }
    setIsLoading(false);
  };

  const respond = async () => {
    if (!userResp.trim()) return;
    const newHistory: DebugMessage[] = [...history, { role: 'user', content: userResp }];
    setHistory(newHistory);
    setUserResp('');
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/api/debug/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userResp, history: newHistory }),
      });
      const data = await res.json();
      setHistory([...newHistory, { role: 'assistant', content: data.reply }]);
    } catch {
      setHistory([...newHistory, { role: 'assistant', content: '⚠️ Connection error.' }]);
    }
    setIsLoading(false);
  };

  const reset = () => {
    setStarted(false);
    setHistory([]);
    setBugCategory('');
    setErrorInput('');
    setUserResp('');
  };

  // Progress steps
  const histLen = history.length;
  const steps = [
    { icon: '❌', label: 'Error shown',       done: true },
    { icon: '🤔', label: 'Expectations?',     done: histLen > 2 },
    { icon: '🔍', label: 'Add print/log',     done: histLen > 4 },
    { icon: '💡', label: 'Notice difference', done: histLen > 6 },
    { icon: '✅', label: 'Bug found!',        done: histLen > 8 },
  ];

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* ── LEFT: Code Mirror ─────────────────────────────────────────────── */}
      <div className="w-[45%] flex flex-col border-r border-[var(--border-subtle)] overflow-hidden">
        <div className="panel-header">
          <span className="panel-dot"></span>
          💻 Your Code
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          <div className="code-mirror" style={{ maxHeight: '100%' }}>
            {code.split('\n').map((line, i) => (
              <div key={i} className="line-inactive">
                <span className="inline-block w-8 text-right mr-3 text-[var(--text-muted)] opacity-40 select-none">{i + 1}</span>
                {line || ' '}
              </div>
            ))}
          </div>
        </div>
        <div className="px-4 py-3 border-t border-[var(--border-subtle)] flex-shrink-0">
          <div className="info-box philosophy">
            <span>🔍</span>
            <span>I won&apos;t fix your bug. I&apos;ll ask the right questions until <em>you</em> find it.</span>
          </div>
        </div>
      </div>

      {/* ── RIGHT: Debug Session ──────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="panel-header justify-between">
          <div className="flex items-center gap-2">
            <span className="panel-dot"></span>
            🐛 Debug Session
          </div>
          {started && (
            <button onClick={reset} className="text-[10px] text-[var(--text-muted)] hover:text-white transition-colors px-2 py-1 rounded border border-[var(--border-subtle)] hover:border-[var(--border-mid)]">
              🔄 New
            </button>
          )}
        </div>

        {!started ? (
          /* ── Start Screen ──────────────────────────────────────────────── */
          <div className="flex-1 overflow-y-auto p-5">
            {code.trim() && (
              <div className="info-box tip mb-4">
                <span>📎</span>
                <span><strong>Editor code synced!</strong> Describe the error below to start debugging.</span>
              </div>
            )}

            <div className="section-title">ERROR / UNEXPECTED OUTPUT</div>
            <textarea
              value={errorInput}
              onChange={(e) => setErrorInput(e.target.value)}
              placeholder="Paste the error message OR describe unexpected behavior…"
              className="w-full bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg px-4 py-3 text-[13px] text-[var(--text-primary)] outline-none focus:border-[var(--violet)] focus:ring-1 focus:ring-[var(--violet-glow)] transition-all placeholder:text-[var(--text-muted)] resize-none h-28 font-mono"
            />

            <button
              onClick={startSession}
              disabled={isLoading || !errorInput.trim()}
              className="w-full mt-4 flex items-center justify-center gap-2 px-5 py-3 rounded-lg text-[14px] font-semibold text-white hover:shadow-[var(--glow-violet)] hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50 border border-[var(--border-accent)]"
              style={{ background: 'var(--grad-hero)' }}
            >
              🐛 {isLoading ? 'Analyzing...' : 'Start Debug Session'}
            </button>
          </div>
        ) : (
          /* ── Active Session ────────────────────────────────────────────── */
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Progress bar */}
            <div className="flex gap-1 px-4 py-3 border-b border-[var(--border-subtle)] flex-shrink-0">
              {bugCategory && (
                <span className="badge badge-amber mr-3">🏷️ {bugCategory}</span>
              )}
              {steps.map((s, i) => (
                <div key={i} className="text-center flex-1">
                  <div className="text-[14px]">{s.icon}</div>
                  <div className={`text-[9px] mt-1 ${s.done ? 'text-[var(--text-secondary)]' : 'text-[var(--text-muted)] opacity-40'}`}>{s.label}</div>
                  <div className="h-[3px] mt-1 rounded" style={{ background: s.done ? 'var(--grad-hero)' : 'rgba(255,255,255,0.05)' }}></div>
                </div>
              ))}
            </div>

            {/* Chat history */}
            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
              {history.map((msg, i) => {
                if (msg.role === 'context') {
                  return (
                    <details key={i} className="bg-[var(--bg-glass)] border border-[var(--border-subtle)] rounded-lg">
                      <summary className="px-4 py-2 text-[12px] text-[var(--text-muted)] cursor-pointer hover:text-[var(--text-secondary)]">
                        📄 View Original Code & Error
                      </summary>
                      <div className="px-4 pb-3 prose-chat text-[12px]">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    </details>
                  );
                }
                if (msg.role === 'assistant') {
                  return (
                    <div key={i} className="bg-[rgba(245,158,11,0.06)] border border-[rgba(245,158,11,0.2)] border-l-[3px] border-l-[var(--amber)] rounded-lg p-4">
                      <div className="text-[10px] font-bold tracking-[1px] uppercase text-[var(--amber)] mb-2">🧠 LogicAI</div>
                      <div className="prose-chat text-[13px] leading-relaxed text-[var(--text-primary)]">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    </div>
                  );
                }
                return (
                  <div key={i} className="bg-[rgba(255,255,255,0.02)] border border-[var(--border-subtle)] border-l-[3px] border-l-[var(--text-muted)] rounded-lg p-4">
                    <div className="text-[10px] font-bold tracking-[1px] uppercase text-[var(--text-muted)] mb-2">👤 You</div>
                    <div className="text-[13px] text-[var(--text-primary)]">{msg.content}</div>
                  </div>
                );
              })}
              {isLoading && (
                <div className="bg-[rgba(245,158,11,0.06)] border border-[rgba(245,158,11,0.2)] rounded-lg p-4">
                  <div className="flex items-center gap-1">
                    <span className="typing-dot" style={{ background: 'var(--amber)' }}></span>
                    <span className="typing-dot" style={{ background: 'var(--amber)', animationDelay: '0.15s' }}></span>
                    <span className="typing-dot" style={{ background: 'var(--amber)', animationDelay: '0.3s' }}></span>
                  </div>
                </div>
              )}
            </div>

            {/* Response input */}
            <div className="p-3 border-t border-[var(--border-subtle)] bg-[var(--bg-secondary)] flex-shrink-0">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={userResp}
                  onChange={(e) => setUserResp(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && respond()}
                  placeholder="What do you think? What did the print show?"
                  className="flex-1 bg-[var(--bg-primary)] border border-[var(--border-subtle)] rounded-lg px-4 py-2.5 text-[13px] text-[var(--text-primary)] outline-none focus:border-[var(--violet)] focus:ring-1 focus:ring-[var(--violet-glow)] transition-all placeholder:text-[var(--text-muted)]"
                />
                <button
                  onClick={respond}
                  disabled={isLoading || !userResp.trim()}
                  className="px-4 py-2.5 rounded-lg text-[13px] font-semibold text-white transition-all disabled:opacity-40"
                  style={{ background: 'var(--grad-hero)' }}
                >
                  💬 Respond
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
