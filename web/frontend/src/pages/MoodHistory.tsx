import { useEffect, useState } from 'react';
import { getMoodHistory } from '../services/api';

interface Mood {
  before: number | null;
  after: number | null;
}

export default function MoodHistory() {
  const [history, setHistory] = useState<Mood[]>([]);

  useEffect(() => {
    getMoodHistory().then(setHistory);
  }, []);

  return (
    <main>
      <h1>Mood History</h1>
      <ul>
        {history.map((m, idx) => (
          <li key={idx}>{m.before} → {m.after}</li>
        ))}
      </ul>
    </main>
  );
}
