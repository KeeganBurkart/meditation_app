import { useEffect, useState } from 'react';
import { getDashboard } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState<{total: number; sessions: number; streak: number} | null>(null);

  useEffect(() => {
    getDashboard().then(setStats);
  }, []);

  if (!stats) return <p>Loading...</p>;

  return (
    <main>
      <h1>Dashboard</h1>
      <div className="grid">
        <div>Total Minutes: {stats.total}</div>
        <div>Sessions: {stats.sessions}</div>
        <div>Current Streak: {stats.streak}</div>
      </div>
    </main>
  );
}
