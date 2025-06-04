import { useEffect, useState } from "react";
import { getFeed } from "../services/api";
import FeedItemCard, { FeedItem } from "../components/FeedItemCard";
import Advertisement from "../components/Advertisement";

export default function ActivityFeedPage() {
  const [items, setItems] = useState<FeedItem[]>([]);

  useEffect(() => {
    getFeed().then(setItems);
  }, []);

  return (
    <main>
      <h1>Activity Feed</h1>
      <ul>
        {items.map((i) => (
          <FeedItemCard key={i.item_id} item={i} />
        ))}
      </ul>
      <Advertisement />
    </main>
  );
}
