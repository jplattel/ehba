describe('EHBA Client App', () => {
	beforeEach(() => {
		cy.visit('/')
	});

	it('has the correct <h1>', () => {
		cy.contains('h1', 'Eerste Hulp Bij Abonnementen!')
	});

	it('navigates to /about', () => {
		cy.get('nav ul li a').contains('📜 Over').click();
		cy.url().should('include', '/about');
	});

	it('navigates to /howto', () => {
		cy.get('nav ul li a').contains('📚 Hoe werkt het?').click();
		cy.url().should('include', '/howto');
	});
});


