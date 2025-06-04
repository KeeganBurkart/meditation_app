import { useEffect, useState } from "react";
import { getMoodHistory } from "../services/api";

interface Mood {
  before: number | null;
  after: number | null;
}

export default function MoodHistory() {
  const [history, setHistory] = useState<Mood[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getMoodHistory()
      .then((data) => {
        if (data) setHistory(data as Mood[]);
        else setError("Failed to load mood history");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <main>
      <h1>Mood History</h1>
      <ul>
        {history.map((m, idx) => (
          <li key={idx}>
            {m.before} → {m.after}
          </li>
        ))}
      </ul>
    </main>
  );
}
