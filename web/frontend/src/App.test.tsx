import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { MemoryRouter } from "react-router-dom";
import App from "./App";

describe("App", () => {
  it("renders dashboard page", () => {
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });
});
