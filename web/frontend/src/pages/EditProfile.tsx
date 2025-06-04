import { useState } from "react";
import { updateBio, uploadPhoto } from "../services/api";

export default function EditProfile() {
  const [bio, setBio] = useState("");
  const [file, setFile] = useState<File | null>(null);

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
        <button type="submit">Save</button>
      </form>
    </main>
  );
}
