'use client';
import { useState } from 'react';
import ChatPanel from './ChatPanel';

const API = 'http://localhost:8000';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface OptResult {
  user_approach: {
    description: string;
    time_complexity: string;
    space_complexity: string;
    readability: string;
    works_well_for: string;
    strength: string;
  };
  optimized: {
    approach_name: string;
    description: string;
    time_complexity: string;
    space_complexity: string;
    key_insight: string;
    optimized_code: string;
  };
  scale_comparison: Array<{
    input_size: string;
    user_time: string;
    optimized_time: string;
  }>;
  encouragement: string;
}

interface OptimizerPageProps {
  code: string;
  language: string;
}

const COMPLEXITY_PCT: Record<string, number> = {
  'O(1)': 4, 'O(log n)': 10, 'O(n)': 22, 'O(n log n)': 38,
  'O(n²)': 72, 'O(n³)': 88, 'O(2^n)': 97, 'O(n!)': 100,
};

function cpxToPct(tc: string): number {
  for (const [k, v] of Object.entries(COMPLEXITY_PCT)) {
    if (tc.includes(k)) return v;
  }
  return 50;
}

export default function OptimizerPage({ code, language }: OptimizerPageProps) {
  const [result, setResult] = useState<OptResult | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const analyze = async () => {
    if (!code.trim()) return;
    setIsAnalyzing(true);
    try {
      const res = await fetch(`${API}/api/optimize/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language }),
      });
      const data = await res.json();
      if (data.success) {
        setResult(data.data);
        if (data.data.encouragement) {
          setChatMessages([{
            role: 'assistant',
            content: `✅ **${data.data.encouragement}**\n\nAsk me anything about the difference between your approach and the optimised one!`
          }]);
        }
      }
    } catch {
      // silently fail
    }
    setIsAnalyzing(false);
  };

  const sendChatMessage = async (message: string) => {
    const newMessages: ChatMessage[] = [...chatMessages, { role: 'user', content: message }];
    setChatMessages(newMessages);
    setIsChatLoading(true);
    try {
      let analysisContext = '';
      if (result) {
        analysisContext = `User's code:\n\`\`\`\n${code}\n\`\`\`\nUser approach: ${result.user_approach.time_complexity} — ${result.user_approach.description}\nOptimised (${result.optimized.approach_name}): ${result.optimized.time_complexity} — ${result.optimized.description}\nKey insight: ${result.optimized.key_insight}`;
      }
      const res = await fetch(`${API}/api/optimize/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, code, analysis_context: analysisContext, history: newMessages }),
      });
      const data = await res.json();
      setChatMessages([...newMessages, { role: 'assistant', content: data.reply }]);
    } catch {
      setChatMessages([...newMessages, { role: 'assistant', content: '⚠️ Connection error.' }]);
    }
    setIsChatLoading(false);
  };

  const reset = () => {
    setResult(null);
    setChatMessages([]);
  };

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* ── LEFT: User Code + Optimized Code ─────────────────────────────── */}
      <div className="w-[50%] flex flex-col border-r border-[var(--border-subtle)] overflow-y-auto">
        {/* User Code */}
        <div className="panel-header">
          <span className="panel-dot"></span>
          📝 Your Code
        </div>

        <div className="p-4">
          <div className="code-mirror text-[12px]" style={{ maxHeight: '200px' }}>
            {code.split('\n').map((line, i) => (
              <div key={i} className="line-inactive">
                <span className="inline-block w-6 text-right mr-2 text-[var(--text-muted)] opacity-40 select-none">{i + 1}</span>
                {line || ' '}
              </div>
            ))}
          </div>
        </div>

        {/* User approach analysis */}
        {result && (
          <div className="px-4 pb-2">
            <div className="glass-card p-4">
              <h3 className="text-[14px] font-bold text-[var(--amber)] mb-2">📊 Your Approach</h3>
              <p className="text-[12px] text-[var(--text-secondary)] mb-3 leading-relaxed">{result.user_approach.description}</p>
              <div className="flex flex-col gap-2 text-[12px]">
                <div className="flex justify-between"><span className="text-[var(--text-muted)]">⏱ Time</span><span className="font-mono text-[var(--amber)]">{result.user_approach.time_complexity}</span></div>
                <div className="progress-track"><div className="progress-fill" style={{ width: `${cpxToPct(result.user_approach.time_complexity)}%`, background: cpxToPct(result.user_approach.time_complexity) > 40 ? 'linear-gradient(90deg, var(--rose), var(--amber))' : 'var(--grad-hero)' }}></div></div>
                <div className="flex justify-between"><span className="text-[var(--text-muted)]">💾 Space</span><span className="font-mono">{result.user_approach.space_complexity}</span></div>
                <div className="flex justify-between"><span className="text-[var(--text-muted)]">Readability</span><span>{result.user_approach.readability}</span></div>
                <div className="text-[var(--emerald)] mt-1">✅ {result.user_approach.strength}</div>
              </div>
            </div>
          </div>
        )}

        {/* Divider */}
        <div className="mx-4 h-[3px] rounded bg-[rgba(139,92,246,0.15)]"></div>

        {/* Optimized Code */}
        <div className="panel-header mt-2">
          <span className="panel-dot"></span>
          🚀 Optimized Code
        </div>

        {result ? (
          <div className="p-4">
            <div className="code-mirror text-[12px] mb-3" style={{ maxHeight: '200px' }}>
              {result.optimized.optimized_code.split('\n').map((line, i) => (
                <div key={i} className="line-inactive">
                  <span className="inline-block w-6 text-right mr-2 text-[var(--text-muted)] opacity-40 select-none">{i + 1}</span>
                  {line || ' '}
                </div>
              ))}
            </div>

            <div className="glass-card p-4" style={{ borderColor: 'rgba(139,92,246,0.35)' }}>
              <h3 className="text-[14px] font-bold text-[var(--violet)] mb-2">🚀 {result.optimized.approach_name}</h3>
              <p className="text-[12px] text-[var(--text-secondary)] mb-3 leading-relaxed">{result.optimized.description}</p>
              <div className="flex flex-col gap-2 text-[12px]">
                <div className="flex justify-between"><span className="text-[var(--text-muted)]">⏱ Time</span><span className="font-mono text-[var(--emerald)]">{result.optimized.time_complexity}</span></div>
                <div className="progress-track"><div className="progress-fill" style={{ width: `${cpxToPct(result.optimized.time_complexity)}%` }}></div></div>
                <div className="flex justify-between"><span className="text-[var(--text-muted)]">💾 Space</span><span className="font-mono">{result.optimized.space_complexity}</span></div>
                <div className="text-[var(--cyan)] mt-1">💡 {result.optimized.key_insight}</div>
              </div>
            </div>

            {/* Scale comparison */}
            {result.scale_comparison?.length > 0 && (
              <div className="mt-3">
                <div className="section-title">PERFORMANCE AT SCALE</div>
                <div className="glass-card p-3 overflow-x-auto">
                  <table className="var-table w-full">
                    <thead>
                      <tr>
                        <th>Input Size</th>
                        <th style={{ color: 'var(--amber)' }}>📝 Yours</th>
                        <th style={{ color: 'var(--emerald)' }}>🚀 Optimised</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.scale_comparison.map((r, i) => (
                        <tr key={i}>
                          <td><strong>{r.input_size}</strong></td>
                          <td style={{ color: 'var(--amber)' }}>{r.user_time}</td>
                          <td style={{ color: 'var(--emerald)' }}>{r.optimized_time}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="p-4">
            <button
              onClick={analyze}
              disabled={isAnalyzing || !code.trim()}
              className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-lg text-[14px] font-semibold text-white hover:shadow-[var(--glow-violet)] hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50 border border-[var(--border-accent)]"
              style={{ background: 'var(--grad-hero)' }}
            >
              ⚡ {isAnalyzing ? 'Analyzing...' : 'Analyse & Optimise'}
            </button>
            <div className="text-center py-10 text-[var(--text-muted)]">
              <div className="text-5xl mb-3 drop-shadow-[0_0_16px_rgba(139,92,246,0.4)]">⚡</div>
              <div className="text-[14px] font-semibold text-[var(--text-secondary)] mb-1">No analysis yet</div>
              <div className="text-[12px]">Click <strong>Analyse & Optimise</strong> to see the optimised version</div>
            </div>
          </div>
        )}

        {result && (
          <div className="px-4 pb-4">
            <button
              onClick={reset}
              className="w-full text-center text-[12px] text-[var(--text-muted)] hover:text-white py-2 rounded-lg border border-[var(--border-subtle)] hover:border-[var(--border-mid)] transition-all"
            >
              🔄 Reset Analysis
            </button>
          </div>
        )}
      </div>

      {/* ── RIGHT: AI Chatbot ─────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatPanel
          messages={chatMessages}
          onSend={sendChatMessage}
          isLoading={isChatLoading}
          title="AI Optimisation Tutor"
          icon="⚡"
          subtitle="I help you understand the difference — not just copy the optimised code."
          placeholder="Ask about the optimisation difference…"
          emptyIcon="⚡"
          emptyTitle="Optimisation Tutor"
          emptySubtitle='After analysis, ask me: "Why is a hash map faster here?" or "When does O(n²) matter?"'
        />
      </div>
    </div>
  );
}
