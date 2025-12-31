import React from 'react';
import styles from './AudioPlayer.module.css';

interface AudioPlayerProps {
  title: string;
  description?: string;
  audioUrl: string;
  duration?: string;
  speaker?: string;
}

/**
 * AudioPlayer Component
 * Custom audio player for lectures, explanations, and tutorials
 */
export default function AudioPlayer({
  title,
  description,
  audioUrl,
  duration = '10:00',
  speaker = 'Instructor',
}: AudioPlayerProps): JSX.Element {
  const [isPlaying, setIsPlaying] = React.useState(false);
  const audioRef = React.useRef<HTMLAudioElement>(null);
  const [currentTime, setCurrentTime] = React.useState(0);
  const [totalDuration, setTotalDuration] = React.useState(0);

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setTotalDuration(audioRef.current.duration);
    }
  };

  const handleProgressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const formatTime = (seconds: number): string => {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const downloadAudio = () => {
    const a = document.createElement('a');
    a.href = audioUrl;
    a.download = `${title}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className={styles.audioContainer}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h4 className={styles.title}>🎙️ {title}</h4>
          <span className={styles.speaker}>by {speaker}</span>
        </div>
      </div>

      {description && <p className={styles.description}>{description}</p>}

      <audio
        ref={audioRef}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        src={audioUrl}
      />

      <div className={styles.playerContainer}>
        <button
          className={styles.playBtn}
          onClick={handlePlayPause}
          aria-label={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? '⏸' : '▶'}
        </button>

        <div className={styles.timeInfo}>
          <span className={styles.currentTime}>{formatTime(currentTime)}</span>
          <span className={styles.separator}>/</span>
          <span className={styles.totalTime}>{duration}</span>
        </div>

        <div className={styles.progressContainer}>
          <input
            type="range"
            className={styles.progressBar}
            min="0"
            max={totalDuration || 0}
            value={currentTime}
            onChange={handleProgressChange}
            step="0.1"
          />
        </div>

        <button
          className={styles.downloadBtn}
          onClick={downloadAudio}
          aria-label="Download audio"
          title="Download MP3"
        >
          ⬇️
        </button>
      </div>

      <div className={styles.info}>
        <p className={styles.infoText}>
          💡 <strong>Tip:</strong> Use playback speed controls in your browser to
          listen at 1.25x or 1.5x speed for faster learning.
        </p>
      </div>
    </div>
  );
}
