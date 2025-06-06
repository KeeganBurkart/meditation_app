import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  logSession,
  uploadSessionPhoto,
  getCustomTypes,
  CustomMeditationType,
} from "../services/api";

export default function SessionForm() {
  const navigate = useNavigate();
  const [photo, setPhoto] = useState<File | null>(null);
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
  const [types, setTypes] = useState<CustomMeditationType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    getCustomTypes()
      .then((data) => {
        if (data) setTypes(data);
        else setError("Failed to load types");
      })
      .finally(() => setLoading(false));
  }, []);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    const sessionId = await logSession({
      ...form,
      duration: Number(form.duration),
    });
    let photoUrl: string | undefined;
    if (sessionId && photo) {
      const resp = await uploadSessionPhoto(sessionId, photo);
      photoUrl = resp?.photo_url;
    }
    setForm({ ...form, notes: "" });
    if (sessionId) {
      navigate(`/sessions/${sessionId}`, { state: { ...form, photo_url: photoUrl } });
    }
    setSaving(false);
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

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
          <select
            name="type"
            value={form.type}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            {types.map((t) => (
              <option key={t.id} value={t.type_name}>
                {t.type_name}
              </option>
            ))}
          </select>
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
        <div className="form-row">
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
        </div>
        <label>
          Photo
          <input type="file" onChange={handleFileChange} />
        </label>
        <button type="submit" disabled={saving}>Save Session</button>
      </form>
    </main>
  );
}
