import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

export default function Dashboard() {
  const [stats, setStats] = useState<{
    total: number;
    sessions: number;
    streak: number;
  } | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboard()
      .then((data) => {
        if (data) setStats(data as any);
        else setError("Failed to load dashboard");
      })
      .catch(() => setError("Failed to load dashboard"));
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
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
