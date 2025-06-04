import { useEffect, useState } from "react";
import { getBadges, Badge } from "../services/api";

export default function BadgesList() {
  const [badges, setBadges] = useState<Badge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getBadges()
      .then((data) => {
        if (data) setBadges(data);
        else setError("Failed to load badges");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <ul>
      {badges.map((b) => (
        <li key={b.name}>{b.name}</li>
      ))}
    </ul>
  );
}
