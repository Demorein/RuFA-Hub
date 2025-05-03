
import React from 'react';
import { Textarea } from '@/components/ui/textarea';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange, language }) => {
  // В MVP-версии используем простую textarea
  // В реальном проекте здесь мог бы быть Monaco Editor или CodeMirror
  return (
    <div className="border rounded-md">
      <div className="bg-muted px-3 py-2 border-b">
        <span className="text-sm font-medium">{language}</span>
      </div>
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="font-mono text-sm min-h-[300px] rounded-t-none"
        placeholder={`// Введите ваш ${language} код здесь`}
      />
    </div>
  );
};

export default CodeEditor;
