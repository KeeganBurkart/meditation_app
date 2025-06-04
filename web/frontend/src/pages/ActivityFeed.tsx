import { useEffect, useState } from "react";
import { getFeed } from "../services/api";
import FeedItemCard, { FeedItem } from "../components/FeedItemCard";
import Advertisement from "../components/Advertisement";

export default function ActivityFeedPage() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getFeed()
      .then((data) => {
        if (data) setItems(data as FeedItem[]);
        else setError("Failed to load feed");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

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
