import React from 'react';
import styles from './URDFViewer.module.css';

interface URDFViewerProps {
  title: string;
  description?: string;
  urdfContent: string;
  height?: string;
}

/**
 * URDFViewer Component
 * Displays URDF (robot description) with syntax highlighting
 * Note: For full 3D visualization, integrate with three.js or Babylon.js
 */
export default function URDFViewer({
  title,
  description,
  urdfContent,
  height = '500px',
}: URDFViewerProps): JSX.Element {
  const [copied, setCopied] = React.useState(false);
  const [expanded, setExpanded] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(urdfContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Count elements in URDF
  const linkCount = (urdfContent.match(/<link/g) || []).length;
  const jointCount = (urdfContent.match(/<joint/g) || []).length;

  return (
    <div className={styles.viewer}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h4 className={styles.title}>{title}</h4>
          <p className={styles.stats}>
            🦴 {linkCount} links • 🔗 {jointCount} joints
          </p>
        </div>
        <button
          className={styles.copyBtn}
          onClick={handleCopy}
          aria-label="Copy URDF"
        >
          {copied ? '✓ Copied!' : '📋 Copy'}
        </button>
      </div>

      {description && <p className={styles.description}>{description}</p>}

      <div className={styles.previewContainer}>
        <div className={styles.previewHeader}>
          <span className={styles.previewLabel}>📄 URDF Structure</span>
          <button
            className={styles.expandBtn}
            onClick={() => setExpanded(!expanded)}
            aria-label="Toggle expand"
          >
            {expanded ? '▼ Collapse' : '▶ Expand'}
          </button>
        </div>

        <pre className={`${styles.urdfBlock} ${expanded ? styles.expanded : ''}`}>
          <code>{urdfContent}</code>
        </pre>
      </div>

      <div className={styles.info}>
        <p className={styles.infoText}>
          💡 <strong>Tip:</strong> To visualize this robot in 3D, load this URDF
          file in Rviz2 or use a URDF viewer tool.
        </p>
      </div>
    </div>
  );
}
