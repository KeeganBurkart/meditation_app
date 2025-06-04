import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getUserProfile, UserProfile as Profile } from "../services/api";

export default function UserProfile() {
  const { id } = useParams();
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    if (id) {
      getUserProfile(id).then(setProfile);
    }
  }, [id]);

  if (!profile) {
    return <main>Loading...</main>;
  }

  return (
    <main>
      <h1>{profile.display_name}</h1>
      {profile.photo_url && (
        <img src={profile.photo_url} alt="profile" width={150} />
      )}
      <p>{profile.bio}</p>
      <section>
        <h2>Stats</h2>
        <p>Total Minutes: {profile.total_minutes}</p>
        <p>Sessions: {profile.session_count}</p>
      </section>
      {/* Recent activity will be added in a future update */}
    </main>
  );
}
