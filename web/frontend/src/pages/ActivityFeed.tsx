import { useEffect, useState } from 'react';
import { getFeed } from '../services/api';

interface FeedItem {
  item_id: number;
  user_id: number;
  item_type: string;
  message: string;
}

export default function ActivityFeedPage() {
  const [items, setItems] = useState<FeedItem[]>([]);

  useEffect(() => {
    getFeed().then(setItems);
  }, []);

  return (
    <main>
      <h1>Activity Feed</h1>
      <ul>
        {items.map(i => (
          <li key={i.item_id}>{i.message}</li>
        ))}
      </ul>
    </main>
  );
}
