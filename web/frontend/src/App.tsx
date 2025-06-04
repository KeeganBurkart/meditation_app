import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Timer from "./pages/Timer";
import SessionForm from "./pages/SessionForm";
import Dashboard from "./pages/Dashboard";
import ActivityFeedPage from "./pages/ActivityFeed";
import CommunityChallenges from "./pages/CommunityChallenges";
import MoodHistory from "./pages/MoodHistory";
import Subscription from "./pages/Subscription";
import EditProfile from "./pages/EditProfile";
import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/timer" element={<Timer />} />
        <Route path="/session" element={<SessionForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/feed" element={<ActivityFeedPage />} />
        <Route path="/challenges" element={<CommunityChallenges />} />
        <Route path="/moods" element={<MoodHistory />} />
        <Route path="/subscription" element={<Subscription />} />
        <Route path="/profile" element={<EditProfile />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
