const API_URL = 'http://localhost:8000';

export async function signup(email: string, password: string, displayName: string) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, display_name: displayName })
  });
  return res.ok;
}

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return res.ok;
}

export interface SessionData {
  date: string;
  time: string;
  duration: number;
  type: string;
  location: string;
  notes: string;
  moodBefore: number;
  moodAfter: number;
}

export async function logSession(data: SessionData) {
  await fetch(`${API_URL}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}

export async function getDashboard() {
  const res = await fetch(`${API_URL}/dashboard/1`);
  if (!res.ok) return null;
  return res.json();
}

export async function getFeed() {
  const res = await fetch(`${API_URL}/feed/1`);
  if (!res.ok) return [];
  return res.json();
}

export async function getCommunityChallenges() {
  const res = await fetch(`${API_URL}/challenges`);
  if (!res.ok) return [];
  return res.json();
}

export async function joinCommunityChallenge(challengeId: number) {
  await fetch(`${API_URL}/challenges/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 1, challenge_id: challengeId })
  });
}

export async function getMoodHistory(userId: number) {
  const res = await fetch(`${API_URL}/moods/${userId}`);
  if (!res.ok) return [];
  return res.json();
}

export async function getSubscription(userId: number) {
  const res = await fetch(`${API_URL}/subscriptions/${userId}`);
  if (!res.ok) return null;
  return res.json();
}

export async function updateSubscription(userId: number, tier: string) {
  await fetch(`${API_URL}/subscriptions/${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tier })
  });
}

export async function addNotification(userId: number, time: string, message: string) {
  await fetch(`${API_URL}/notifications`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, reminder_time: time, message })
  });
}

export async function getNotifications(userId: number) {
  const res = await fetch(`${API_URL}/notifications/${userId}`);
  if (!res.ok) return [];
  return res.json();
}

export async function updateBio(userId: number, bio: string) {
  await fetch(`${API_URL}/users/${userId}/bio`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bio })
  });
}

export async function uploadPhoto(userId: number, file: File) {
  const res = await fetch(`${API_URL}/users/${userId}/photo`, {
    method: 'POST',
    headers: { 'X-Filename': file.name },
    body: file
  });
  if (!res.ok) return null;
  return res.json();
}
