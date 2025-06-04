import { useEffect, useState } from 'react';
import { addNotification, getNotifications } from '../services/api';

interface Notification {
  notification_id: number;
  reminder_time: string;
  message: string;
}

export default function NotificationPreferences({ userId }: { userId: number }) {
  const [time, setTime] = useState('07:00');
  const [message, setMessage] = useState('Meditate');
  const [notes, setNotes] = useState<Notification[]>([]);

  useEffect(() => {
    getNotifications(userId).then(setNotes);
  }, [userId]);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    await addNotification(userId, time, message);
    getNotifications(userId).then(setNotes);
  }

  return (
    <section>
      <h2>Notifications</h2>
      <form onSubmit={handleAdd}>
        <input type="time" value={time} onChange={e => setTime(e.target.value)} />
        <input value={message} onChange={e => setMessage(e.target.value)} />
        <button type="submit">Add</button>
      </form>
      <ul>
        {notes.map(n => (
          <li key={n.notification_id}>{n.reminder_time} - {n.message}</li>
        ))}
      </ul>
    </section>
  );
}
