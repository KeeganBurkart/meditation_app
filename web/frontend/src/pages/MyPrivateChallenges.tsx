import { useEffect, useState } from "react";
import {
  getPrivateChallenges,
  createPrivateChallenge,
  deletePrivateChallenge,
  PrivateChallenge,
  ChallengeInput,
  getSubscription,
} from "../services/api";

export default function MyPrivateChallenges() {
  const [challenges, setChallenges] = useState<PrivateChallenge[]>([]);
  const [form, setForm] = useState<ChallengeInput>({
    name: "",
    target_minutes: 10,
    start_date: "",
    end_date: "",
  });
  const [premium, setPremium] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    getSubscription().then((sub) => setPremium(sub?.tier === "premium"));
    getPrivateChallenges().then(setChallenges).finally(() => setLoaded(true));
  }, []);

  if (!loaded) return <p>Loading...</p>;
  if (!premium)
    return (
      <main>
        <h1>Private Challenges</h1>
        <p>Upgrade to premium to use private challenges.</p>
      </main>
    );

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: name === "target_minutes" ? Number(value) : value }));
  }

  async function create(e: React.FormEvent) {
    e.preventDefault();
    const c = await createPrivateChallenge(form);
    if (c) setChallenges((prev) => [...prev, c]);
    setForm({ name: "", target_minutes: 10, start_date: "", end_date: "" });
  }

  async function remove(id: number) {
    await deletePrivateChallenge(id);
    setChallenges((prev) => prev.filter((c) => c.id !== id));
  }

  return (
    <main>
      <h1>My Private Challenges</h1>
      <form onSubmit={create}>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          required
        />
        <input
          type="number"
          name="target_minutes"
          value={form.target_minutes}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="start_date"
          value={form.start_date}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="end_date"
          value={form.end_date}
          onChange={handleChange}
          required
        />
        <button type="submit">Create</button>
      </form>
      <ul>
        {challenges.map((c) => (
          <li key={c.id}>
            {c.name} ({c.target_minutes}m)
            <button onClick={() => remove(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
