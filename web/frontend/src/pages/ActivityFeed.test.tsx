import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ActivityFeedPage from "./ActivityFeed";

const addComment = vi.fn();
const addEnc = vi.fn();
const getAd = vi.fn();

vi.mock("../services/api", () => ({
  getFeed: () =>
    Promise.resolve([
      {
        item_id: 1,
        user_id: 2,
        item_type: "session",
        message: "Morning",
        comments: [
          { comment_id: 1, feed_item_id: 1, user_id: 3, text: "Nice" },
        ],
        encouragements: [],
      },
    ]),
  addFeedComment: (...args: any[]) => {
    addComment(...args);
    return Promise.resolve({
      comment_id: 2,
      feed_item_id: 1,
      user_id: 1,
      text: args[1],
    });
  },
  addFeedEncouragement: (...args: any[]) => {
    addEnc(...args);
    return Promise.resolve({
      encouragement_id: 3,
      feed_item_id: 1,
      user_id: 1,
      text: args[1],
    });
  },
  getSubscription: () => Promise.resolve({ tier: "free" }),
  getRandomAd: () => {
    getAd();
    return Promise.resolve({ ad_id: 1, text: "Buy now" });
  },
}));

describe("ActivityFeed page", () => {
  it("shows comments and allows posting", async () => {
    render(<ActivityFeedPage />);
    expect(await screen.findByText("Nice")).toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText("Add comment"), {
      target: { value: "Hello" },
    });
    fireEvent.click(screen.getByText("Comment"));
    expect(addComment).toHaveBeenCalled();
    expect(await screen.findByText("Buy now")).toBeInTheDocument();
  });
});
