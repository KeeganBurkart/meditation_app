// TODO: Replace with environment variable
const API_URL = 'http://localhost:8000';

function getAuthHeader() {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

export async function signup(
  email: string,
  password: string,
  displayName: string,
) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, display_name: displayName }),
  });
  return res.ok;
}

export async function login(
  email: string,
  password: string,
): Promise<string | null> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    return null;
  }
  const data = await res.json();
  // Assuming the token is stored upon successful login elsewhere, e.g., in the component calling login
  // For example: if (token) localStorage.setItem('token', token);
  return data.access_token as string;
}

export interface SessionData {
  date: string;
  time?: string; // Made optional as per backend main.py SessionInput
  duration: number;
  type: string;
  location?: string; // Made optional
  notes?: string; // Made optional
  moodBefore?: number; // Made optional
  moodAfter?: number; // Made optional
}

export async function logSession(data: SessionData) {
  await fetch(`${API_URL}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function getDashboard() {
  const res = await fetch(`${API_URL}/dashboard/me`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) {
    return null;
  }
  return res.json();
}

export async function getFeed() {
  const res = await fetch(`${API_URL}/feed`, { headers: getAuthHeader() });
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function getCommunityChallenges() {
  // This endpoint in backend main.py doesn't require authentication
  const res = await fetch(`${API_URL}/challenges`);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function joinCommunityChallenge(challengeId: number) {
  await fetch(`${API_URL}/challenges/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ challenge_id: challengeId }), // user_id is derived from token on backend
  });
}

export async function getMoodHistory() {
  const res = await fetch(`${API_URL}/moods`, { headers: getAuthHeader() }); // Assumes for current user
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function getSubscription() {
  const res = await fetch(`${API_URL}/subscriptions/me`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) {
    return null;
  }
  return res.json();
}

export async function updateSubscription(tier: string) {
  await fetch(`${API_URL}/subscriptions/me`, {
    method: 'PUT', // Backend endpoint is PUT
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ tier }),
  });
}

export async function addNotification(time: string, message: string) {
  await fetch(`${API_URL}/notifications`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ reminder_time: time, message }), // user_id is derived from token
  });
}

export async function getNotifications() {
  const res = await fetch(`${API_URL}/notifications`, { // Assumes for current user
    headers: getAuthHeader(),
  });
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function updateBio(bio: string) {
  await fetch(`${API_URL}/users/me/bio`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    body: JSON.stringify({ bio }),
  });
}

export async function uploadPhoto(file: File) {
  const res = await fetch(`${API_URL}/users/me/photo`, {
    method: 'POST',
    headers: { 'X-Filename': file.name, ...getAuthHeader() }, // Ensure Content-Type is not set by fetch for FormData/File, browser handles it.
    body: file,
  });
  if (!res.ok) {
    return null;
  }
  return res.json();
}
