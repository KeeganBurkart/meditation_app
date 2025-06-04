describe("Edit profile flow", () => {
  it("updates bio and photo", () => {
    cy.intercept("PUT", "/users/me/bio", { statusCode: 200 }).as("bio");
    cy.intercept("POST", "/users/me/photo", { statusCode: 200 }).as("photo");
    cy.intercept("PUT", "/users/me/profile-visibility", { statusCode: 200 }).as(
      "visibility",
    );

    cy.visit("/profile");

    cy.get("textarea").type("Meditation is awesome");
    cy.get('input[type="file"]').selectFile({
      contents: "image", // dummy content
      fileName: "photo.png",
    });
    cy.get('input[type="checkbox"]').uncheck();
    cy.wait("@visibility");

    cy.contains("button", "Save").click();
    cy.wait("@bio");
    cy.wait("@photo");

    cy.on("window:alert", (text) => {
      expect(text).to.equal("Profile updated");
    });
  });
});
