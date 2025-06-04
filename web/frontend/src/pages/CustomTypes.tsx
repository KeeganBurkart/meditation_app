import { useEffect, useState } from "react";
import {
  getCustomTypes,
  createCustomType,
  deleteCustomType,
  CustomMeditationType,
} from "../services/api";

export default function CustomTypes() {
  const [types, setTypes] = useState<CustomMeditationType[]>([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCustomTypes()
      .then((data) => {
        if (data) setTypes(data);
        else setError("Failed to load types");
      })
      .finally(() => setLoading(false));
  }, []);

  async function addType(e: React.FormEvent) {
    e.preventDefault();
    if (!name) return;
    const t = await createCustomType(name);
    if (t) setTypes((prev) => [...prev, t]);
    setName("");
  }

  async function remove(id: number) {
    await deleteCustomType(id);
    setTypes((prev) => prev.filter((t) => t.id !== id));
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <main>
      <h1>Custom Meditation Types</h1>
      <form onSubmit={addType}>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New type"
          required
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {types.map((t) => (
          <li key={t.id}>
            {t.type_name}
            <button onClick={() => remove(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
