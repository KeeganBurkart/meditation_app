import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Subscription from "./Subscription";

const update = vi.fn();

vi.mock("../services/api", () => ({
  getSubscription: () => Promise.resolve({ tier: "free" }),
  updateSubscription: (...args: any[]) => {
    update(...args);
    return Promise.resolve();
  },
}));

describe("Subscription page", () => {
  it("toggles tier", async () => {
    render(<Subscription />);
    const btn = await screen.findByText("Toggle");
    fireEvent.click(btn);
    expect(update).toHaveBeenCalled();
  });
});
