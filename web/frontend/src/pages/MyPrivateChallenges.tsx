import { useEffect, useState } from "react";
import {
  getPrivateChallenges,
  createPrivateChallenge,
  deletePrivateChallenge,
  updatePrivateChallenge,
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
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<PrivateChallenge | null>(null);

  useEffect(() => {
    async function load() {
      const sub = await getSubscription();
      setPremium(sub?.tier === "premium");
      const list = await getPrivateChallenges();
      if (list) setChallenges(list);
      else setError("Failed to load challenges");
      setLoaded(true);
    }
    load();
  }, []);

  if (!loaded) return <p>Loading...</p>;
  if (!premium)
    return (
      <main>
        <h1>Private Challenges</h1>
        <p>Upgrade to premium to use private challenges.</p>
        <a href="/subscription">View subscription options</a>
      </main>
    );

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: name === "target_minutes" ? Number(value) : value }));
  }

  async function save(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    if (editing) {
      await updatePrivateChallenge(editing.id, form);
      setChallenges((prev) =>
        prev.map((c) => (c.id === editing.id ? { ...editing, ...form } : c)),
      );
    } else {
      const c = await createPrivateChallenge(form);
      if (c) setChallenges((prev) => [...prev, c]);
      else setError("Failed to create challenge");
    }
    setForm({ name: "", target_minutes: 10, start_date: "", end_date: "" });
    setSaving(false);
    setShowForm(false);
    setEditing(null);
  }

  async function remove(id: number) {
    await deletePrivateChallenge(id);
    setChallenges((prev) => prev.filter((c) => c.id !== id));
  }

  return (
    <main>
      <h1>My Private Challenges</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button
        onClick={() => {
          setEditing(null);
          setForm({ name: "", target_minutes: 10, start_date: "", end_date: "" });
          setShowForm(true);
        }}
      >
        Add Challenge
      </button>
      <ul>
        {challenges.map((c) => (
          <li key={c.id}>
            {c.name} ({c.target_minutes}m)
            <button
              onClick={() => {
                setEditing(c);
                setForm({
                  name: c.name,
                  target_minutes: c.target_minutes,
                  start_date: c.start_date,
                  end_date: c.end_date,
                });
                setShowForm(true);
              }}
            >
              Edit
            </button>
            <button onClick={() => remove(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {showForm && (
        <div className="modal-overlay">
          <div className="modal">
            <form onSubmit={save}>
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
              <button type="submit" disabled={saving}>
                {editing ? "Update" : "Create"}
              </button>
              <button type="button" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
