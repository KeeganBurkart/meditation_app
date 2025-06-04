import { useLocation } from "react-router-dom";

interface SessionDetailsState {
  date: string;
  time: string;
  duration: number;
  type: string;
  location: string;
  notes: string;
  photo_url?: string;
}

export default function SessionDetails() {
  const { state } = useLocation() as { state: SessionDetailsState };
  if (!state) return <p>No session data</p>;
  return (
    <main>
      <h1>Session Details</h1>
      <p>Date: {state.date}</p>
      <p>Time: {state.time}</p>
      <p>Duration: {state.duration} minutes</p>
      <p>Type: {state.type}</p>
      <p>Location: {state.location}</p>
      <p>Notes: {state.notes}</p>
      {state.photo_url && (
        <img src={state.photo_url} alt="Session" style={{ maxWidth: "100%" }} />
      )}
    </main>
  );
}
