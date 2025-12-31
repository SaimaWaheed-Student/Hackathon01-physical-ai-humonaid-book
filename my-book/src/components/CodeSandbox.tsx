import React from 'react';
import styles from './CodeSandbox.module.css';

interface CodeSandboxProps {
  title: string;
  description?: string;
  code: string;
  language?: string;
  height?: string;
}

/**
 * CodeSandbox Component
 * Displays embedded code with syntax highlighting and copy functionality
 */
export default function CodeSandbox({
  title,
  description,
  code,
  language = 'python',
  height = '400px',
}: CodeSandboxProps): JSX.Element {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={styles.sandbox}>
      <div className={styles.header}>
        <h4 className={styles.title}>{title}</h4>
        <button
          className={styles.copyBtn}
          onClick={handleCopy}
          aria-label="Copy code"
        >
          {copied ? '✓ Copied!' : '📋 Copy'}
        </button>
      </div>
      {description && <p className={styles.description}>{description}</p>}
      <pre className={styles.codeBlock}>
        <code className={`language-${language}`}>{code}</code>
      </pre>
    </div>
  );
}
