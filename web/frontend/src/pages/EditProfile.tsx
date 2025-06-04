import { useState } from "react";
import {
  updateBio,
  uploadPhoto,
  updateProfileVisibility,
} from "../services/api";

export default function EditProfile() {
  const [bio, setBio] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isPublic, setIsPublic] = useState(true);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await updateBio(bio);
    if (file) {
      await uploadPhoto(file);
    }
    alert("Profile updated");
  }

  return (
    <main>
      <h1>Edit Profile</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Bio
          <textarea value={bio} onChange={(e) => setBio(e.target.value)} />
        </label>
        <label>
          Photo
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </label>
        <label>
          Profile is Public
          <input
            type="checkbox"
            checked={isPublic}
            onChange={async (e) => {
              const value = e.target.checked;
              setIsPublic(value);
              await updateProfileVisibility(value);
            }}
          />
        </label>
        <button type="submit">Save</button>
      </form>
    </main>
  );
}
