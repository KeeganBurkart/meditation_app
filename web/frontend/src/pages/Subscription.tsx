import { useEffect, useState } from 'react';
import { getSubscription, updateSubscription } from '../services/api';

interface Sub {
  tier: string;
}

export default function Subscription() {
  const [sub, setSub] = useState<Sub | null>(null);

  useEffect(() => {
    getSubscription(1).then(setSub);
  }, []);

  async function toggle() {
    if (!sub) return;
    const next = sub.tier === 'premium' ? 'free' : 'premium';
    await updateSubscription(1, next);
    setSub({ tier: next });
  }

  if (!sub) return <p>Loading...</p>;

  return (
    <main>
      <h1>Subscription</h1>
      <p>Current tier: {sub.tier}</p>
      <button onClick={toggle}>Toggle</button>
    </main>
  );
}
