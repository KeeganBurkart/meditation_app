const API_URL = "http://localhost:8000";

async function fetchJson<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T | null> {
  try {
    const res = await fetch(input, init);
    if (!res.ok) throw new Error(`Request failed with ${res.status}`);
    return (await res.json()) as T;
  } catch (err) {
    console.error("API error", err);
    return null;
  }
}

async function fetchOk(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<boolean> {
  try {
    const res = await fetch(input, init);
    return res.ok;
  } catch (err) {
    console.error("API error", err);
    return false;
  }
}

function getAuthHeader() {
  // Access tokens are stored in ``localStorage`` after login. When present we
  // send them as a ``Bearer`` token so protected endpoints authenticate the
  // current user.
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function signup(
  email: string,
  password: string,
  displayName: string,
) {
  return fetchOk(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, display_name: displayName }),
  });
}

export async function login(
  email: string,
  password: string,
): Promise<string | null> {
  const res = await fetchJson<{ access_token: string }>(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return res ? res.access_token : null;
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

export interface FeedComment {
  comment_id: number;
  feed_item_id: number;
  user_id: number;
  text: string;
}

export interface FeedEncouragement {
  encouragement_id: number;
  feed_item_id: number;
  user_id: number;
  text: string;
}

export interface Ad {
  ad_id: number;
  text: string;
}

export async function logSession(
  data: SessionData,
): Promise<number | null> {
  const res = await fetchJson<{ session_id: number }>(`${API_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
  return res ? res.session_id : null;
}

export async function getDashboard() {
  return fetchJson(`${API_URL}/dashboard/me`, {
    headers: getAuthHeader(),
  });
}

export async function getFeed(): Promise<any[] | null> {
  return fetchJson<any[]>(`${API_URL}/feed`, { headers: getAuthHeader() });
}

export async function getCommunityChallenges(): Promise<any[] | null> {
  return fetchJson<any[]>(`${API_URL}/challenges`);
}

export async function joinCommunityChallenge(challengeId: number) {
  await fetchOk(`${API_URL}/challenges/join`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ challenge_id: challengeId }),
  });
}

export async function getMoodHistory(): Promise<any[] | null> {
  return fetchJson<any[]>(`${API_URL}/moods`, { headers: getAuthHeader() });
}

export async function getSubscription() {
  return fetchJson(`${API_URL}/subscriptions/me`, {
    headers: getAuthHeader(),
  });
}

export async function updateSubscription(tier: string) {
  await fetchOk(`${API_URL}/subscriptions/me`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ tier }),
  });
}

export async function addNotification(time: string, message: string) {
  await fetchOk(`${API_URL}/notifications`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ reminder_time: time, message }),
  });
}

export async function getNotifications(): Promise<any[] | null> {
  return fetchJson<any[]>(`${API_URL}/notifications`, {
    headers: getAuthHeader(),
  });
}

export async function updateBio(bio: string) {
  await fetchOk(`${API_URL}/users/me/bio`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ bio }),
  });
}

export async function uploadPhoto(file: File) {
  return fetchJson(`${API_URL}/users/me/photo`, {
    method: "POST",
    headers: { "X-Filename": file.name, ...getAuthHeader() },
    body: file,
  });
}

export async function addFeedComment(
  feedItemId: number,
  text: string,
): Promise<FeedComment | null> {
  return fetchJson<FeedComment>(`${API_URL}/feed/${feedItemId}/comment`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ text }),
  });
}

export async function addFeedEncouragement(
  feedItemId: number,
  text: string,
): Promise<FeedEncouragement | null> {
  return fetchJson<FeedEncouragement>(`${API_URL}/feed/${feedItemId}/encourage`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ text }),
  });
}

  return fetchJson<Ad>(`${API_URL}/ads/random`, { headers: getAuthHeader() });
}

  
// ---------------------- Custom Meditation Types ----------------------

export interface CustomMeditationType {
  id: number;
  type_name: string;
}

export async function createCustomType(
  typeName: string,
): Promise<CustomMeditationType | null> {
  return fetchJson<CustomMeditationType>(
    `${API_URL}/users/me/custom-meditation-types`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json", ...getAuthHeader() },
      body: JSON.stringify({ type_name: typeName }),
    },
  );
}

export async function getCustomTypes(): Promise<CustomMeditationType[] | null> {
  return fetchJson<CustomMeditationType[]>(
    `${API_URL}/users/me/custom-meditation-types`,
    { headers: getAuthHeader() },
  );
}

export async function updateCustomType(
  id: number,
  typeName: string,
): Promise<void> {
  await fetchOk(`${API_URL}/users/me/custom-meditation-types/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ type_name: typeName }),
  });
}

export async function deleteCustomType(id: number): Promise<void> {
  await fetchOk(`${API_URL}/users/me/custom-meditation-types/${id}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });
}

// ------------------------------- Badges -------------------------------

export interface Badge {
  name: string;
}

export async function getBadges(): Promise<Badge[] | null> {
  return fetchJson<Badge[]>(`${API_URL}/users/me/badges`, {
    headers: getAuthHeader(),
  });
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
  return fetchJson<PrivateChallenge>(`${API_URL}/users/me/private-challenges`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function getPrivateChallenges(): Promise<PrivateChallenge[] | null> {
  return fetchJson<PrivateChallenge[]>(`${API_URL}/users/me/private-challenges`, {
    headers: getAuthHeader(),
  });
}

export async function updatePrivateChallenge(
  id: number,
  data: ChallengeInput,
): Promise<void> {
  await fetchOk(`${API_URL}/users/me/private-challenges/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify(data),
  });
}

export async function deletePrivateChallenge(id: number): Promise<void> {
  await fetchOk(`${API_URL}/users/me/private-challenges/${id}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });

// --- Mocked Social & Profile APIs ---

export async function socialLogin(
  provider: string,
  token: string,
): Promise<string | null> {
  // Simulate a network delay then resolve a fake token
  return new Promise((resolve) => {
    setTimeout(() => resolve("mock_access_token"), 300);
  });
}

export async function updateProfileVisibility(isPublic: boolean) {
  // Placeholder mock implementation
  return new Promise((resolve) => setTimeout(resolve, 200));
}

export interface UserProfile {
  user_id: number;
  display_name: string;
  bio: string;
  photo_url: string;
  is_public: boolean;
  total_minutes: number;
  session_count: number;
  recent_activity: string[];
}

export async function getUserProfile(
  userId: string,
): Promise<UserProfile | null> {
  // Return mock profile data
  return new Promise((resolve) =>
    setTimeout(
      () =>
        resolve({
          user_id: Number(userId),
          display_name: "Mock User",
          bio: "This is a mock profile.",
          photo_url: "",
          is_public: true,
          total_minutes: 123,
          session_count: 45,
          recent_activity: ["Meditated for 10 minutes", "Completed challenge"],
        }),
      200,
    ),
  );
}
