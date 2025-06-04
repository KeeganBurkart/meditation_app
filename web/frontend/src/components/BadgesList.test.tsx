import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import BadgesList from "./BadgesList";

vi.mock("../services/api", () => ({
  getBadges: () => Promise.resolve([{ name: "Beginner" }]),
}));

describe("BadgesList", () => {
  it("shows badges", async () => {
    render(<BadgesList />);
    expect(await screen.findByText("Beginner")).toBeInTheDocument();
  });
});
