import 'cypress-file-upload';

const fileName = '../../../server/tests/data/joost_2019_ns.csv';

describe('EHBA Client App - Form', () => {
	beforeEach(() => {
		cy.visit('/')
	});

	it('has a disabled button by default', () => {
        cy.get('input.btn-primary').should("be.disabled")
	});

	it("should enable the submit one it has a file selected", () => {
		cy.get('input.btn-primary').should("be.disabled")
		

		cy.fixture(fileName).then(fileContent => {
			cy.get('input#file-selector').upload({ fileContent, fileName, mimeType: 'application/json' });
		});

        cy.get('button.btn-primary').should("not.be.disabled")
	});
	
	it("should have post a JSON payload the /parse after pressing submit", () => {
		cy.fixture(fileName).then(fileContent => {
			cy.get('input#file-selector').upload({ fileContent, fileName, mimeType: 'application/json' });
		});

		cy.get("input.btn-primary").click()
		
		cy.wait(300)

		cy.get('.container').contains("Let's work it")

		cy.wait(5000)

		cy.get('h1').contains("De resultaten!")
	})


});



