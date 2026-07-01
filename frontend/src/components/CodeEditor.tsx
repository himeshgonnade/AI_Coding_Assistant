'use client';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  code: string;
  onChange: (value: string | undefined) => void;
  language?: string;
  readOnly?: boolean;
  height?: string;
}

const MONACO_LANG_MAP: Record<string, string> = {
  python: 'python',
  javascript: 'javascript',
  typescript: 'typescript',
  java: 'java',
  cpp: 'cpp',
  c: 'c',
  go: 'go',
  rust: 'rust',
  html: 'html',
  css: 'css',
  sql: 'sql',
  bash: 'shell',
  json: 'json',
  markdown: 'markdown',
};

export default function CodeEditor({ code, onChange, language = 'python', readOnly = false, height = '100%' }: CodeEditorProps) {
  const monacoLang = MONACO_LANG_MAP[language] || language;

  return (
    <div className="w-full h-full border border-[var(--border-subtle)] rounded-lg overflow-hidden bg-[#0d1117] shadow-[var(--shadow-sm)]">
      <Editor
        height={height}
        language={monacoLang}
        theme="vs-dark"
        value={code}
        onChange={readOnly ? undefined : onChange}
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "'JetBrains Mono', monospace",
          padding: { top: 16 },
          scrollBeyondLastLine: false,
          smoothScrolling: true,
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: 'on',
          renderLineHighlight: readOnly ? 'none' : 'line',
          lineNumbers: 'on',
          glyphMargin: false,
          folding: true,
          wordWrap: 'on',
        }}
      />
    </div>
  );
}
