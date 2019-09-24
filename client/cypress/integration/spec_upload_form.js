describe('EHBA Client App - Form', () => {
	beforeEach(() => {
		cy.visit('/')
	});

	it('has a disabled button by default', () => {
        cy.get('input.btn-primary').should("be.disabled")
	});

	// it("should enable the submit one it has a file selected", () => {
    //     cy.get('button.btn-primary').to.be.disabled

    //     cy.get('.file-selector')

    //     cy.get('button.btn-primary').not.to.be.disabled
    // });
});



