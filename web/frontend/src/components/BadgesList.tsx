import { useEffect, useState } from "react";
import { getBadges, Badge } from "../services/api";

export default function BadgesList() {
  const [badges, setBadges] = useState<Badge[]>([]);

  useEffect(() => {
    getBadges().then(setBadges);
  }, []);

  return (
    <ul>
      {badges.map((b) => (
        <li key={b.name}>{b.name}</li>
      ))}
    </ul>
  );
}
