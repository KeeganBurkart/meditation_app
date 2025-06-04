import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Timer from "./pages/Timer";
import SessionForm from "./pages/SessionForm";
import SessionDetails from "./pages/SessionDetails";
import Dashboard from "./pages/Dashboard";
import ActivityFeedPage from "./pages/ActivityFeed";
import CommunityChallenges from "./pages/CommunityChallenges";
import MoodHistory from "./pages/MoodHistory";
import Subscription from "./pages/Subscription";
import EditProfile from "./pages/EditProfile";
import CustomTypes from "./pages/CustomTypes";
import BadgesPage from "./pages/BadgesPage";
import MyPrivateChallenges from "./pages/MyPrivateChallenges";
import UserProfile from "./pages/UserProfile";
import Analytics from "./pages/Analytics";
import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/timer" element={<Timer />} />
        <Route path="/session" element={<SessionForm />} />
        <Route path="/sessions/:id" element={<SessionDetails />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/feed" element={<ActivityFeedPage />} />
        <Route path="/challenges" element={<CommunityChallenges />} />
        <Route path="/moods" element={<MoodHistory />} />
        <Route path="/subscription" element={<Subscription />} />
        <Route path="/custom-types" element={<CustomTypes />} />
        <Route path="/badges" element={<BadgesPage />} />
        <Route path="/my-challenges" element={<MyPrivateChallenges />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/profile" element={<EditProfile />} />
        <Route path="/profile/:id" element={<UserProfile />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  );
}
