import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import CustomTypes from "./CustomTypes";

const create = vi.fn();

vi.mock("../services/api", () => ({
  getCustomTypes: () => Promise.resolve([{ id: 1, type_name: "Calm" }]),
  createCustomType: (...args: any[]) => {
    create(...args);
    return Promise.resolve({ id: 2, type_name: "Focus" });
  },
  deleteCustomType: vi.fn(),
}));

describe("CustomTypes page", () => {
  it("renders and adds type", async () => {
    render(<CustomTypes />);
    expect(await screen.findByText("Calm")).toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText("New type"), {
      target: { value: "Focus" },
    });
    fireEvent.click(screen.getByText("Add"));
    expect(create).toHaveBeenCalled();
  });
});
