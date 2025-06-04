import { useEffect, useState } from "react";
import { addNotification, getNotifications } from "../services/api";

interface Notification {
  notification_id: number;
  reminder_time: string;
  message: string;
}

export default function NotificationPreferences() {
  const [time, setTime] = useState("07:00");
  const [message, setMessage] = useState("Meditate");
  const [notes, setNotes] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getNotifications()
      .then((data) => {
        if (data) setNotes(data as Notification[]);
        else setError("Failed to load notifications");
      })
      .finally(() => setLoading(false));
  }, []);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await addNotification(time, message);
    getNotifications().then((data) => data && setNotes(data as Notification[]));
  }

  if (loading) return <section>Loading...</section>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <section>
      <h2>Notifications</h2>
      <form onSubmit={handleAdd}>
        <input
          type="time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
        />
        <input value={message} onChange={(e) => setMessage(e.target.value)} />
        <button type="submit">Add</button>
      </form>
      <ul>
        {notes.map((n) => (
          <li key={n.notification_id}>
            {n.reminder_time} - {n.message}
          </li>
        ))}
      </ul>
    </section>
  );
}
