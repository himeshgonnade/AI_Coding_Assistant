'use client';
import { useState, useRef, useCallback } from 'react';
import { Play } from 'lucide-react';
import CodeEditor from './CodeEditor';
import ChatPanel from './ChatPanel';

const API = 'http://localhost:8000';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface CompilerPageProps {
  code: string;
  setCode: (v: string) => void;
  language: string;
}

export default function CompilerPage({ code, setCode, language }: CompilerPageProps) {
  const [output, setOutput] = useState('');
  const [outputError, setOutputError] = useState('');
  const [stdin, setStdin] = useState('');
  const [showStdin, setShowStdin] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isChatLoading, setIsChatLoading] = useState(false);

  // Vertical resize state (chat vs output split on right side)
  const [chatPct, setChatPct] = useState(55);
  const rightRef = useRef<HTMLDivElement>(null);
  const isDraggingV = useRef(false);

  // Horizontal resize state (editor vs right panel)
  const [leftPct, setLeftPct] = useState(55);
  const containerRef = useRef<HTMLDivElement>(null);
  const isDraggingH = useRef(false);

  const runCode = async () => {
    setIsRunning(true);
    setOutput('');
    setOutputError('');
    try {
      const res = await fetch(`${API}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language, stdin }),
      });
      const data = await res.json();
      setOutput(data.output || '');
      setOutputError(data.error || '');
    } catch (e: unknown) {
      setOutputError(e instanceof Error ? e.message : 'Connection failed');
    }
    setIsRunning(false);
  };

  const sendChatMessage = async (message: string) => {
    const newMessages: ChatMessage[] = [...chatMessages, { role: 'user', content: message }];
    setChatMessages(newMessages);
    setIsChatLoading(true);
    try {
      const res = await fetch(`${API}/api/mentor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, code, language, history: newMessages }),
      });
      const data = await res.json();
      setChatMessages([...newMessages, { role: 'assistant', content: data.reply }]);
    } catch {
      setChatMessages([...newMessages, { role: 'assistant', content: '⚠️ Could not connect to AI backend.' }]);
    }
    setIsChatLoading(false);
  };

  // ── Horizontal drag ────────────────────────────────────────────────────────
  const startHDrag = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isDraggingH.current = true;
    const startX = e.clientX;
    const startPct = leftPct;

    const onMove = (ev: MouseEvent) => {
      if (!isDraggingH.current || !containerRef.current) return;
      const total = containerRef.current.getBoundingClientRect().width;
      const dx = ev.clientX - startX;
      const newPct = Math.max(25, Math.min(75, startPct + (dx / total) * 100));
      setLeftPct(newPct);
    };
    const onUp = () => {
      isDraggingH.current = false;
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }, [leftPct]);

  // ── Vertical drag ─────────────────────────────────────────────────────────
  const startVDrag = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isDraggingV.current = true;
    const startY = e.clientY;
    const startPct = chatPct;

    const onMove = (ev: MouseEvent) => {
      if (!isDraggingV.current || !rightRef.current) return;
      const total = rightRef.current.getBoundingClientRect().height;
      const dy = ev.clientY - startY;
      const newPct = Math.max(20, Math.min(85, startPct + (dy / total) * 100));
      setChatPct(newPct);
    };
    const onUp = () => {
      isDraggingV.current = false;
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
    document.body.style.cursor = 'row-resize';
    document.body.style.userSelect = 'none';
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }, [chatPct]);

  return (
    <div ref={containerRef} className="flex flex-1 w-full overflow-hidden">
      {/* ── LEFT: Code Editor ──────────────────────────────────────────────── */}
      <div className="flex flex-col overflow-hidden" style={{ width: `${leftPct}%` }}>
        {/* Header row */}
        <div className="flex items-center justify-between px-4 py-2 flex-shrink-0">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.15em] text-[var(--violet)]">
            <span className="panel-dot"></span>
            Code Editor
          </div>
          <button
            onClick={runCode}
            disabled={isRunning}
            className="flex items-center gap-2 px-5 py-2 rounded-lg text-[13px] font-semibold text-white hover:shadow-[var(--glow-violet)] hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:hover:scale-100 border border-[var(--border-accent)]"
            style={{ background: 'var(--grad-hero)' }}
          >
            <Play size={14} className="fill-white" />
            {isRunning ? 'Running...' : '▶ Run Code'}
          </button>
        </div>

        {/* Editor */}
        <div className="flex-1 px-4 pb-2 min-h-0 min-w-0">
          <CodeEditor code={code} onChange={(v) => setCode(v || '')} language={language} />
        </div>

        {/* Stats bar */}
        <div className="mx-4 mb-3 flex gap-5 px-4 py-2 bg-[var(--bg-glass)] border border-[var(--border-subtle)] rounded-lg text-[11px] text-[var(--text-muted)] flex-shrink-0">
          <span>📄 <strong className="text-[var(--text-secondary)]">{code.split('\n').length}</strong> lines</span>
          <span>💻 <strong className="text-[var(--text-secondary)]">{code.split('\n').filter(l => l.trim() && !l.trim().startsWith('#')).length}</strong> code</span>
          <span>📝 <strong className="text-[var(--text-secondary)]">{code.length}</strong> chars</span>
          <span>🌐 <strong className="text-[var(--cyan)]">{language.toUpperCase()}</strong></span>
        </div>
      </div>

      {/* ── HORIZONTAL DRAG HANDLE ─────────────────────────────────────────── */}
      <div className="drag-handle-h" onMouseDown={startHDrag}>
        <div className="drag-pill-h"></div>
      </div>

      {/* ── RIGHT: Chat + Output ───────────────────────────────────────────── */}
      <div ref={rightRef} className="flex flex-col overflow-hidden border-l border-[var(--border-subtle)]" style={{ width: `${100 - leftPct}%` }}>
        {/* Chat section */}
        <div className="flex flex-col overflow-hidden" style={{ height: `${chatPct}%` }}>
          <ChatPanel
            messages={chatMessages}
            onSend={sendChatMessage}
            isLoading={isChatLoading}
          />
        </div>

        {/* Vertical drag handle */}
        <div className="drag-handle-v" onMouseDown={startVDrag}>
          <div className="drag-pill-v"></div>
        </div>

        {/* Output section */}
        <div className="flex flex-col overflow-hidden bg-[var(--bg-primary)]" style={{ height: `${100 - chatPct}%` }}>
          {/* Standard Input (collapsible) */}
          <div className="flex flex-col border-b border-[var(--border-subtle)] bg-[rgba(10,15,30,0.5)] flex-shrink-0">
            <div 
              className="px-4 py-2 flex items-center justify-between cursor-pointer hover:bg-[rgba(255,255,255,0.02)] transition-colors select-none"
              onClick={() => setShowStdin(!showStdin)}
            >
              <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.1em] text-[var(--text-muted)] hover:text-[var(--text-secondary)] transition-colors">
                <span className={`text-[9px] transition-transform duration-200 ${showStdin ? 'rotate-90' : ''}`}>▶</span>
                ⌨️ Standard Input
              </div>
            </div>
            {showStdin && (
              <div className="p-3 pt-0">
                <textarea
                  value={stdin}
                  onChange={(e) => setStdin(e.target.value)}
                  placeholder="Enter input here (e.g. if code uses input())..."
                  className="w-full h-20 bg-[#060913] text-[var(--text-primary)] border border-[var(--border-subtle)] rounded p-2 text-xs font-mono focus:outline-none focus:border-[var(--violet)] focus:shadow-[var(--glow-violet)] resize-y transition-all"
                />
              </div>
            )}
          </div>

          <div className="panel-header flex-shrink-0">
            <span className="w-[6px] h-[6px] rounded-full bg-[var(--cyan)] shadow-[var(--glow-cyan)]"></span>
            📤 Output Console
          </div>
          <div className="flex-1 overflow-y-auto p-4 font-mono text-[13px]">
            {output && (
              <pre className="text-[var(--emerald)] whitespace-pre-wrap leading-relaxed">{output}</pre>
            )}
            {outputError && (
              <pre className="text-[var(--rose)] bg-[rgba(244,63,94,0.06)] border border-[rgba(244,63,94,0.2)] rounded-lg p-3 whitespace-pre-wrap">{outputError}</pre>
            )}
            {!output && !outputError && (
              <div className="text-[var(--text-muted)] font-sans italic flex items-center gap-2">
                <span>▶</span> Click <strong>Run Code</strong> to see output
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
