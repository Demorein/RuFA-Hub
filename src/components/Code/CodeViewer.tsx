
import React from 'react';
import { Button } from '@/components/ui/button';
import { Copy } from 'lucide-react';
import { toast } from 'sonner';

interface CodeViewerProps {
  code: string;
  language: string;
}

const CodeViewer: React.FC<CodeViewerProps> = ({ code, language }) => {
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code);
      toast.success('Код скопирован в буфер обмена');
    } catch (err) {
      toast.error('Не удалось скопировать код');
      console.error('Failed to copy code: ', err);
    }
  };

  return (
    <div className="border rounded-md bg-code">
      <div className="bg-muted px-3 py-2 border-b flex justify-between items-center">
        <span className="text-sm font-medium">{language}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={copyToClipboard}
          className="h-8 px-2"
        >
          <Copy className="h-4 w-4 mr-1" />
          <span>Копировать</span>
        </Button>
      </div>
      <pre className="p-4 overflow-x-auto text-sm font-mono text-code-foreground">
        <code>{code}</code>
      </pre>
    </div>
  );
};

export default CodeViewer;
