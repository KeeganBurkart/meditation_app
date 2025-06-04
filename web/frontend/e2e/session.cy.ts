describe('Log meditation session', () => {
  it('saves a new session', () => {
    cy.intercept('POST', '/sessions', { statusCode: 200 }).as('log');
    cy.visit('http://localhost:5173/session');
    const today = new Date().toISOString().split('T')[0];
    cy.get('input[name="date"]').type(today);
    cy.get('input[name="duration"]').clear().type('15');
    cy.get('input[name="type"]').type('Mindfulness');
    cy.contains('button', 'Save Session').click();
    cy.wait('@log');
  });
});
