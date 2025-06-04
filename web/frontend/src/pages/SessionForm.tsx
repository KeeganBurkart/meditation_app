import { useState } from "react";
import { logSession } from "../services/api";

export default function SessionForm() {
  const [form, setForm] = useState({
    date: "",
    time: "",
    duration: 10,
    type: "",
    location: "",
    notes: "",
    moodBefore: 5,
    moodAfter: 5,
  });

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await logSession({
      ...form,
      duration: Number(form.duration),
    });
    setForm({ ...form, notes: "" });
  }

  return (
    <main>
      <h1>Log Session</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Date
          <input
            type="date"
            name="date"
            value={form.date}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Time
          <input
            type="time"
            name="time"
            value={form.time}
            onChange={handleChange}
          />
        </label>
        <label>
          Duration (minutes)
          <input
            type="number"
            name="duration"
            value={form.duration}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Meditation Type
          <input
            name="type"
            value={form.type}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Location
          <input
            name="location"
            value={form.location}
            onChange={handleChange}
          />
        </label>
        <label>
          Notes
          <textarea name="notes" value={form.notes} onChange={handleChange} />
        </label>
        <label>
          Mood Before
          <input
            type="number"
            name="moodBefore"
            value={form.moodBefore}
            onChange={handleChange}
            min="1"
            max="10"
          />
        </label>
        <label>
          Mood After
          <input
            type="number"
            name="moodAfter"
            value={form.moodAfter}
            onChange={handleChange}
            min="1"
            max="10"
          />
        </label>
        <button type="submit">Save Session</button>
      </form>
    </main>
  );
}
