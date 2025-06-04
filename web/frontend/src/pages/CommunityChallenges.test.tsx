import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import CommunityChallenges from "./CommunityChallenges";
import * as api from "../services/api";

vi.mock("../services/api", () => ({
  getCommunityChallenges: () =>
    Promise.resolve([
      {
        id: 1,
        name: "Test",
        target_minutes: 100,
        start_date: "",
        end_date: "",
      },
    ]),
  joinCommunityChallenge: vi.fn(),
}));

describe("CommunityChallenges page", () => {
  it("renders list of challenges", async () => {
    render(<CommunityChallenges />);
    expect(await screen.findByText(/Test/)).toBeInTheDocument();
  });

  it("handles load failure", async () => {
    vi.spyOn(api, "getCommunityChallenges").mockResolvedValueOnce(null as any);
    render(<CommunityChallenges />);
    expect(await screen.findByText(/Failed to load/)).toBeInTheDocument();
  });
});
