import { useEffect, useState } from 'react';
import { getCommunityChallenges, joinCommunityChallenge } from '../services/api';

interface Challenge {
  id: number;
  name: string;
  target_minutes: number;
  start_date: string;
  end_date: string;
}

export default function CommunityChallenges() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);

  useEffect(() => {
    getCommunityChallenges().then(setChallenges);
  }, []);

  async function handleJoin(id: number) {
    await joinCommunityChallenge(id);
  }

  return (
    <main>
      <h1>Community Challenges</h1>
      <ul>
        {challenges.map(c => (
          <li key={c.id}>
            {c.name} ({c.target_minutes}m)
            <button onClick={() => handleJoin(c.id)}>Join</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
