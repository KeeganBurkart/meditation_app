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
  // Authentication is disabled; no headers are required.
  return {};
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
  const res = await fetch(`${API_URL}/auth/social-login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, token }),
  });
  if (!res.ok) return null;
  const data = await res.json();
  return data.access_token as string;
}

export async function updateProfileVisibility(isPublic: boolean) {
  await fetch(`${API_URL}/users/me/profile-visibility`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ is_public: isPublic }),
  });
}

export interface UserProfile {
  user_id: number;
  display_name: string | null;
  bio: string | null;
  photo_url: string | null;
  total_minutes: number;
  session_count: number;
}

export async function getUserProfile(
  userId: string,
): Promise<UserProfile | null> {
  const res = await fetch(`${API_URL}/users/${userId}/profile`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return null;
  return res.json();
}

// ----------------------------- Analytics -----------------------------

export interface DateValuePoint {
  date_str: string;
  value: number;
}

export interface ConsistencyDataResponse {
  points: DateValuePoint[];
}

export interface MoodCorrelationPoint {
  mood_before: number;
  mood_after: number;
}

export interface MoodCorrelationResponse {
  points: MoodCorrelationPoint[];
}

export interface HourValuePoint {
  hour: number;
  value: number;
}

export interface TimeOfDayResponse {
  points: HourValuePoint[];
}

export interface StringValuePoint {
  name: string;
  value: number;
}

export interface LocationFrequencyResponse {
  points: StringValuePoint[];
}

export async function getConsistencyData(): Promise<DateValuePoint[]> {
  const res = await fetch(`${API_URL}/analytics/me/consistency`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  const data = (await res.json()) as ConsistencyDataResponse;
  return data.points;
}

export async function getMoodCorrelationData(): Promise<MoodCorrelationPoint[]> {
  const res = await fetch(`${API_URL}/analytics/me/mood-correlation`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  const data = (await res.json()) as MoodCorrelationResponse;
  return data.points;
}

export async function getTimeOfDayData(): Promise<HourValuePoint[]> {
  const res = await fetch(`${API_URL}/analytics/me/time-of-day`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  const data = (await res.json()) as TimeOfDayResponse;
  return data.points;
}

export async function getLocationFrequencyData(): Promise<StringValuePoint[]> {
  const res = await fetch(`${API_URL}/analytics/me/location-frequency`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) return [];
  const data = (await res.json()) as LocationFrequencyResponse;
  return data.points;
}
