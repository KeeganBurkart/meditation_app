import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import UserProfile from "./UserProfile";

vi.mock("../services/api", () => ({
  getUserProfile: () =>
    Promise.resolve({
      user_id: 1,
      display_name: "Tester",
      bio: "hello",
      photo_url: "",
      is_public: true,
    }),
}));

describe("UserProfile page", () => {
  it("loads profile data", async () => {
    render(
      <MemoryRouter initialEntries={["/profile/1"]}>
        <Routes>
          <Route path="/profile/:id" element={<UserProfile />} />
        </Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText("Tester")).toBeInTheDocument();
  });
});
