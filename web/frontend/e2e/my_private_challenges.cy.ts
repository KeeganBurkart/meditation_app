describe("Private challenges page", () => {
  it("creates a new challenge when premium", () => {
    cy.intercept("GET", "/subscriptions/me", { tier: "premium" }).as("sub");
    cy.intercept("GET", "/users/me/private-challenges", []).as("list");
    cy.intercept("POST", "/users/me/private-challenges", {
      id: 1,
      name: "Test Challenge",
      target_minutes: 20,
      start_date: "2023-01-01",
      end_date: "2023-01-10",
    }).as("create");

    cy.visit("/my-challenges");
    cy.wait(["@sub", "@list"]);

    cy.get('input[name="name"]').type("Test Challenge");
    cy.get('input[name="target_minutes"]').clear().type("20");
    cy.get('input[name="start_date"]').type("2023-01-01");
    cy.get('input[name="end_date"]').type("2023-01-10");
    cy.contains("button", "Create").click();
    cy.wait("@create");

    cy.contains("li", "Test Challenge (20m)").should("exist");
  });
});
