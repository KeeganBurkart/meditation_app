import { useEffect, useState } from "react";
import { Ad, getRandomAd, getSubscription } from "../services/api";

export default function Advertisement() {
  const [ad, setAd] = useState<Ad | null>(null);

  useEffect(() => {
    async function loadAd() {
      const sub = await getSubscription();
      if (sub && sub.tier === "free") {
        const a = await getRandomAd();
        if (a) setAd(a);
      }
    }
    loadAd();
  }, []);

  if (!ad) return null;

  return (
    <aside className="ad">
      <p>{ad.text}</p>
    </aside>
  );
}

