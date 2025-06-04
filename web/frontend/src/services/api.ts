const API_URL = "http://localhost:8000";

function getAuthHeader() {
  // Access tokens are stored in ``localStorage`` after login. When present we
  // send them as a ``Bearer`` token so protected endpoints authenticate the
  // current user.
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

export async function signup(
  email: string,
  password: string,
  displayName: string,
) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, display_name: displayName }),
  });
  return res.ok;
}

export async function login(
  email: string,
  password: string,
): Promise<string | null> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function getDashboard() {
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
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ challenge_id: challengeId }),
  });
}

export async function getMoodHistory() {
  const res = await fetch(`${API_URL}/moods`, { headers: getAuthHeader() });
  if (!res.ok) return [];
  return res.json();
}

export async function getSubscription() {
  const res = await fetch(`${API_URL}/subscriptions/me`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function updateSubscription(tier: string) {
  await fetch(`${API_URL}/subscriptions/me`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ tier }),
  });
}

export async function addNotification(time: string, message: string) {
  await fetch(`${API_URL}/notifications`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ reminder_time: time, message }),
  });
}

export async function getNotifications() {
  const res = await fetch(`${API_URL}/notifications`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  return res.json();
}

export async function updateBio(bio: string) {
  await fetch(`${API_URL}/users/me/bio`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ bio }),
  });
}

export async function uploadPhoto(file: File) {
  const res = await fetch(`${API_URL}/users/me/photo`, {
    method: "POST",
    headers: { "X-Filename": file.name, ...getAuthHeader() },
    body: file,
  });
  if (!res.ok) return null;
  return res.json();
}

// ---------------------- Custom Meditation Types ----------------------

export interface CustomMeditationType {
  id: number;
  type_name: string;
}

export async function createCustomType(
  typeName: string,
): Promise<CustomMeditationType | null> {
  const res = await fetch(`${API_URL}/users/me/custom-meditation-types`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ type_name: typeName }),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function getCustomTypes(): Promise<CustomMeditationType[]> {
  const res = await fetch(`${API_URL}/users/me/custom-meditation-types`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  return res.json();
}

export async function updateCustomType(
  id: number,
  typeName: string,
): Promise<void> {
  await fetch(`${API_URL}/users/me/custom-meditation-types/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ type_name: typeName }),
  });
}

export async function deleteCustomType(id: number): Promise<void> {
  await fetch(`${API_URL}/users/me/custom-meditation-types/${id}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });
}

// ------------------------------- Badges -------------------------------

export interface Badge {
  name: string;
}

export async function getBadges(): Promise<Badge[]> {
  const res = await fetch(`${API_URL}/users/me/badges`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  return res.json();
}

// --------------------------- Private Challenges ---------------------------

export interface PrivateChallenge {
  id: number;
  name: string;
  target_minutes: number;
  start_date: string;
  end_date: string;
}

export interface ChallengeInput {
  name: string;
  target_minutes: number;
  start_date: string;
  end_date: string;
}

export async function createPrivateChallenge(
  data: ChallengeInput,
): Promise<PrivateChallenge | null> {
  const res = await fetch(`${API_URL}/users/me/private-challenges`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function getPrivateChallenges(): Promise<PrivateChallenge[]> {
  const res = await fetch(`${API_URL}/users/me/private-challenges`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  return res.json();
}

export async function updatePrivateChallenge(
  id: number,
  data: ChallengeInput,
): Promise<void> {
  await fetch(`${API_URL}/users/me/private-challenges/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function deletePrivateChallenge(id: number): Promise<void> {
  await fetch(`${API_URL}/users/me/private-challenges/${id}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });
}
