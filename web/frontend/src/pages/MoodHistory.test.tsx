import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import MoodHistory from "./MoodHistory";
import * as api from "../services/api";

vi.mock("../services/api", () => ({
  getMoodHistory: () => Promise.resolve([{ before: 3, after: 7 }]),
}));

describe("MoodHistory page", () => {
  it("shows mood entries", async () => {
    render(<MoodHistory />);
    expect(await screen.findByText("3 → 7")).toBeInTheDocument();
  });

  it("handles load failure", async () => {
    vi.spyOn(api, "getMoodHistory").mockResolvedValueOnce(null as any);
    render(<MoodHistory />);
    expect(await screen.findByText(/Failed to load mood history/)).toBeInTheDocument();
  });
});
