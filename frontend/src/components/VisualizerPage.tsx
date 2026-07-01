'use client';
import { useState } from 'react';

const API = 'http://localhost:8000';

interface VisStep {
  step: number;
  line: string;
  line_number: number;
  action: string;
  variables: Record<string, string>;
  changed_vars: string[];
  callstack: string[];
  output: string;
  highlight: string;
}

interface VisualizerPageProps {
  code: string;
  language: string;
}

export default function VisualizerPage({ code, language }: VisualizerPageProps) {
  const [steps, setSteps] = useState<VisStep[]>([]);
  const [current, setCurrent] = useState(0);
  const [summary, setSummary] = useState('');
  const [patterns, setPatterns] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const visualize = async () => {
    if (!code.trim()) return;
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/api/visualize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language }),
      });
      const data = await res.json();
      if (data.success) {
        setSteps(data.data.steps || []);
        setCurrent(0);
        setSummary(data.data.summary || '');
        setPatterns(data.data.key_patterns || []);
      }
    } catch {
      // silently fail
    }
    setIsLoading(false);
  };

  const step = steps[current];
  const total = steps.length;
  const activeLn = step?.line_number || 0;

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* ── LEFT: Current Line Panel ──────────────────────────────────────── */}
      <div className="w-[30%] flex flex-col border-r border-[var(--border-subtle)] overflow-hidden">
        <div className="panel-header">
          <span className="panel-dot"></span>
          📍 Current Line
        </div>

        <div className="flex-1 overflow-y-auto p-3">
          <div className="code-mirror" style={{ maxHeight: '100%' }}>
            {code.split('\n').map((line, i) => {
              const lnum = i + 1;
              const isActive = lnum === activeLn;
              return (
                <div key={i} className={isActive ? 'line-active' : 'line-inactive'}>
                  <span className={`inline-block w-6 text-right mr-2 select-none ${isActive ? 'text-[var(--violet)] font-bold' : 'text-[var(--text-muted)] opacity-40'}`}>
                    {lnum}
                  </span>
                  {isActive ? `▶ ${line}` : (line || ' ')}
                </div>
              );
            })}
          </div>
        </div>

        {/* Step counter */}
        {total > 0 && (
          <div className="p-3 border-t border-[var(--border-subtle)] flex-shrink-0">
            <div className="bg-[rgba(139,92,246,0.08)] border border-[rgba(139,92,246,0.2)] rounded-lg p-3">
              <div className="text-[10px] text-[var(--violet)] font-bold tracking-[1px] uppercase mb-1">STEP</div>
              <div className="text-[var(--text-primary)] text-2xl font-extrabold">
                {current + 1}
                <span className="text-[12px] text-[var(--text-muted)] font-normal ml-1">/ {total}</span>
              </div>
              <div className="progress-track mt-2">
                <div className="progress-fill" style={{ width: `${((current + 1) / total) * 100}%` }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── RIGHT: Visualization Panel ────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="panel-header justify-between">
          <div className="flex items-center gap-2">
            <span className="panel-dot"></span>
            🔬 {summary ? `Execution — ${summary}` : 'Visual Code Stepper'}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={visualize}
              disabled={isLoading || !code.trim()}
              className="text-[11px] font-semibold px-3 py-1.5 rounded-md text-white transition-all disabled:opacity-40"
              style={{ background: 'var(--grad-hero)' }}
            >
              {isLoading ? '⏳ Analyzing...' : '🔬 Visualize'}
            </button>
            {total > 0 && (
              <button
                onClick={() => { setSteps([]); setCurrent(0); setSummary(''); setPatterns([]); }}
                className="text-[11px] text-[var(--text-muted)] hover:text-white px-2 py-1 rounded border border-[var(--border-subtle)] transition-colors"
              >
                🗑️ Clear
              </button>
            )}
          </div>
        </div>

        {total === 0 ? (
          /* ── Empty state ──────────────────────────────────────────────── */
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div className="text-6xl mb-4 drop-shadow-[0_0_20px_rgba(139,92,246,0.4)]">🔬</div>
            <div className="text-[16px] font-semibold text-[var(--text-secondary)] mb-2">Ready to visualize</div>
            <div className="text-[13px] text-[var(--text-muted)]">Write code in the editor, then click <strong>Visualize</strong></div>
            <div className="info-box philosophy mt-6 max-w-md">
              <span>🎬</span>
              <span>Like a slow-motion replay of what the computer does. Watch variables change, loops iterate, and logic unfold — one step at a time.</span>
            </div>
          </div>
        ) : (
          /* ── Active visualization ─────────────────────────────────────── */
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Nav controls */}
            <div className="flex items-center gap-2 px-4 py-3 border-b border-[var(--border-subtle)] flex-shrink-0">
              <button onClick={() => setCurrent(0)} className="px-3 py-1.5 rounded-md bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--border-mid)] transition-all text-sm">⏮</button>
              <button onClick={() => current > 0 && setCurrent(current - 1)} className="px-3 py-1.5 rounded-md bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--border-mid)] transition-all text-sm">◀</button>
              <div className="flex-1 text-center text-[13px] text-[var(--text-secondary)]">
                Step <strong className="text-[var(--violet)]">{current + 1}</strong> of {total}
                &nbsp;·&nbsp; Line <strong className="text-[var(--cyan)]">{activeLn}</strong>
                <div className="progress-track mt-1"><div className="progress-fill" style={{ width: `${((current + 1) / total) * 100}%` }}></div></div>
              </div>
              <button onClick={() => current < total - 1 && setCurrent(current + 1)} className="px-3 py-1.5 rounded-md bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--border-mid)] transition-all text-sm">▶</button>
              <button onClick={() => setCurrent(total - 1)} className="px-3 py-1.5 rounded-md bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--border-mid)] transition-all text-sm">⏭</button>
            </div>

            {/* Step detail + variables */}
            <div className="flex-1 overflow-y-auto p-4">
              <div className="grid grid-cols-2 gap-4">
                {/* What's happening */}
                <div className="glass-card p-4">
                  <div className="text-[10px] text-[var(--violet)] font-bold tracking-[1px] uppercase mb-2">📍 LINE {activeLn}</div>
                  <div className="bg-[#0d1117] border border-[rgba(139,92,246,0.2)] border-l-[3px] border-l-[var(--violet)] rounded-r-md p-2 font-mono text-[13px] text-[var(--text-primary)] mb-3">
                    {step.line}
                  </div>
                  <div className="text-[13px] text-[var(--text-primary)] leading-relaxed mb-3">
                    <strong>What&apos;s happening:</strong><br />{step.action}
                  </div>
                  {step.highlight && (
                    <div className="info-box tip text-[12px]">
                      <span>💡</span><span>{step.highlight}</span>
                    </div>
                  )}
                  {step.output && (
                    <div className="bg-[rgba(16,185,129,0.08)] border border-[rgba(16,185,129,0.2)] rounded-lg p-3 mt-2">
                      <div className="text-[10px] text-[var(--emerald)] font-bold tracking-[1px] uppercase mb-1">📤 OUTPUT</div>
                      <code className="text-[var(--emerald)] font-mono text-[12px]">{step.output}</code>
                    </div>
                  )}
                  {step.callstack?.length > 0 && (
                    <div className="mt-3">
                      <div className="text-[10px] text-[var(--text-muted)] font-bold tracking-[1px] uppercase mb-2">📚 CALL STACK</div>
                      {[...step.callstack].reverse().map((f, i) => (
                        <div key={i} className="text-[12px] font-mono text-[var(--violet)] bg-[rgba(139,92,246,0.08)] rounded px-2 py-1 mb-1">→ {f}</div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Variable state */}
                <div className="glass-card p-4">
                  <div className="section-title mt-0">VARIABLE STATE</div>
                  {Object.keys(step.variables || {}).length > 0 ? (
                    <table className="var-table">
                      <thead>
                        <tr><th>Variable</th><th>Value</th><th>Changed</th></tr>
                      </thead>
                      <tbody>
                        {Object.entries(step.variables).map(([name, val]) => {
                          const changed = step.changed_vars?.includes(name);
                          return (
                            <tr key={name} style={changed ? { background: 'rgba(6,182,212,0.06)' } : {}}>
                              <td><code className="text-[var(--violet)]">{name}</code></td>
                              <td><code style={{ color: changed ? 'var(--cyan)' : 'var(--text-primary)' }}>{String(val)}</code></td>
                              <td className="text-[10px] font-bold text-[var(--cyan)]">{changed ? '⚡ NOW' : ''}</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  ) : (
                    <div className="text-center text-[var(--text-muted)] py-8">No variables at this step yet</div>
                  )}
                </div>
              </div>

              {/* Key patterns (last step) */}
              {patterns.length > 0 && current === total - 1 && (
                <div className="mt-4">
                  <div className="section-title">KEY PATTERNS IDENTIFIED</div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {patterns.map((p, i) => <span key={i} className="badge badge-violet">🔑 {p}</span>)}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
