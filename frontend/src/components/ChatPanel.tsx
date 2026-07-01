'use client';
import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatPanelProps {
  messages: ChatMessage[];
  onSend: (message: string) => void;
  isLoading: boolean;
  title?: string;
  icon?: string;
  subtitle?: string;
  placeholder?: string;
  emptyIcon?: string;
  emptyTitle?: string;
  emptySubtitle?: string;
}

export default function ChatPanel({
  messages,
  onSend,
  isLoading,
  title = 'AI Logic Mentor',
  icon = '🧠',
  subtitle = "I guide your thinking — I won't write the code for you.",
  placeholder = 'Ask about logic, approach, or algorithm...',
  emptyIcon = '🧠',
  emptyTitle = 'Ask me about your code logic, algorithms, or approach!',
  emptySubtitle = "I guide your thinking — I won't write the code for you.",
}: ChatPanelProps) {
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSend(input.trim());
    setInput('');
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="panel-header">
        <span className="panel-dot"></span>
        {icon} {title}
      </div>

      {/* Subtitle */}
      <div className="px-4 py-2 text-[11px] text-[var(--text-muted)] border-b border-[var(--border-subtle)] flex-shrink-0">
        ✨ {subtitle}
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 min-h-0">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center opacity-70">
            <div className="text-4xl mb-4 drop-shadow-lg">{emptyIcon}</div>
            <p className="text-[13px] text-[var(--text-secondary)] font-medium">{emptyTitle}</p>
            <p className="text-[10px] text-[var(--text-muted)] mt-2">{emptySubtitle}</p>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}>
              {msg.role === 'assistant' && (
                <div className="ai-label">{icon} LogicAI</div>
              )}
              <div className="prose-chat">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="chat-bubble-ai">
            <div className="ai-label">{icon} LogicAI</div>
            <div className="flex items-center gap-1 h-5">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-[var(--border-subtle)] bg-[var(--bg-secondary)] flex-shrink-0">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder={placeholder}
            className="flex-1 bg-[var(--bg-primary)] border border-[var(--border-subtle)] rounded-lg px-4 py-2.5 text-[13px] text-[var(--text-primary)] outline-none focus:border-[var(--violet)] focus:ring-1 focus:ring-[var(--violet-glow)] transition-all placeholder:text-[var(--text-muted)]"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="w-10 h-10 rounded-lg flex items-center justify-center border border-[var(--border-mid)] text-[var(--text-secondary)] hover:text-white hover:border-transparent transition-all duration-200 disabled:opacity-40 disabled:hover:bg-[var(--bg-card)]"
            style={{ background: !isLoading && input.trim() ? 'var(--grad-hero)' : 'var(--bg-card)' }}
          >
            <Send size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}
