describe("Login flow", () => {
  it("allows a user to log in", () => {
    cy.intercept("POST", "/auth/login", { statusCode: 200 }).as("login");
    cy.visit("http://localhost:5173/login");
    cy.get("input").first().type("user@example.com");
    cy.get('input[type="password"]').type("password");
    cy.contains("button", "Login").click();
    cy.wait("@login");
    cy.url().should("include", "/dashboard");
  });
});
