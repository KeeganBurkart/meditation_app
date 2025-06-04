import { useState, useRef } from 'react';
import { logSession } from '../services/api';

export default function Timer() {
  const [seconds, setSeconds] = useState(0);
  const [running, setRunning] = useState(false);
  const interval = useRef<number>();

  function start() {
    if (running) return;
    setRunning(true);
    interval.current = window.setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);
  }

  async function stop() {
    if (interval.current) window.clearInterval(interval.current);
    setRunning(false);
    const minutes = Math.floor(seconds / 60) || 1;
    await logSession({
      date: new Date().toISOString().slice(0, 10),
      time: new Date().toISOString().slice(11, 16),
      duration: minutes,
      type: 'Timer',
      location: '',
      notes: '',
      moodBefore: 5,
      moodAfter: 5
    });
    setSeconds(0);
  }

  return (
    <main>
      <h1>Timer</h1>
      <div style={{fontSize: '2rem'}}>{seconds}s</div>
      <button onClick={start} disabled={running}>Start</button>
      <button onClick={stop} disabled={!running}>Stop</button>
    </main>
  );
}
