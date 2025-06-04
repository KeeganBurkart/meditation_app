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

  useEffect(() => {
    getCustomTypes().then(setTypes);
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
