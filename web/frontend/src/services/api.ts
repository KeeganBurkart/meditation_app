const API_URL = 'http://localhost:8000';

function getAuthHeader() {
  const token = localStorage.getItem('token');
  // Chose single quotes for 'token' and unquoted 'Authorization' key for consistency.
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Preferred multi-line parameter formatting for readability.
export async function signup(
  email: string,
  password: string,
  displayName: string,
) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    // Standardized to single quotes and ensured trailing comma.
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, display_name: displayName }),
  });
  return res.ok;
}

// Preferred multi-line parameter formatting.
export async function login(
  email: string,
  password: string,
): Promise<string | null> {
  const res = await fetch(`${API_URL}/auth/login`, {
    // Standardized to single quotes and ensured trailing comma.
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) return null;
  const data = await res.json();
  return data.access_token as string;
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
    // Standardized to single quotes and ensured trailing comma.
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function getDashboard() {
  // Preferred multi-line formatting for fetch options.
  const res = await fetch(`${API_URL}/dashboard/me`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function getFeed() {
  const res = await fetch(`${API_URL}/feed`, { headers: getAuthHeader() });
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
    // Standardized to single quotes and ensured trailing comma.
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ challenge_id: challengeId }),
  });
}

export async function getMoodHistory() {
  const res = await fetch(`${API_URL}/moods`, { headers: getAuthHeader() });
  if (!res.ok) return [];
  return res.json();
}

export async function getSubscription() {
  // Preferred multi-line formatting for fetch options.
  const res = await fetch(`${API_URL}/subscriptions/me`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function updateSubscription(tier: string) {
  await fetch(`${API_URL}/subscriptions/me`, {
    // Standardized to single quotes and ensured trailing comma.
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ tier }),
  });
}

export async function addNotification(time: string, message: string) {
  await fetch(`${API_URL}/notifications`, {
    // Standardized to single quotes and ensured trailing comma.
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ reminder_time: time, message }),
  });
}

export async function getNotifications() {
  // Preferred multi-line formatting for fetch options.
  const res = await fetch(`${API_URL}/notifications`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  return res.json();
}

export async function updateBio(bio: string) {
  await fetch(`${API_URL}/users/me/bio`, {
    // Standardized to single quotes and ensured trailing comma.
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ bio }),
  });
}

export async function uploadPhoto(file: File) {
  // The second conflicting part was more complete, including the fetch call closing and response handling.
  // Standardized to single quotes, ensured trailing comma, and corrected the final ')' to '}'.
  const res = await fetch(`${API_URL}/users/me/photo`, {
    method: 'POST',
    headers: { 'X-Filename': file.name, ...getAuthHeader() },
    body: file,
  });
  if (!res.ok) return null;
  return res.json();
}