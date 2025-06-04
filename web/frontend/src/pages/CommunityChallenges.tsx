import { useEffect, useState } from "react";
import {
  getCommunityChallenges,
  joinCommunityChallenge,
} from "../services/api";

interface Challenge {
  id: number;
  name: string;
  target_minutes: number;
  start_date: string;
  end_date: string;
}

export default function CommunityChallenges() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCommunityChallenges()
      .then((data) => {
        if (data) setChallenges(data as Challenge[]);
        else setError("Failed to load challenges");
      })
      .finally(() => setLoading(false));
  }, []);

  async function handleJoin(id: number) {
    await joinCommunityChallenge(id);
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <main>
      <h1>Community Challenges</h1>
      <ul>
        {challenges.map((c) => (
          <li key={c.id}>
            {c.name} ({c.target_minutes}m)
            <button onClick={() => handleJoin(c.id)}>Join</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
