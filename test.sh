# Navigate into the client folder and test it with Cypress
cd ~/2Projects/ehba/client && yarn test

# # Activate virtual env that contains python dependencies
cd ~/.environments/ehba && source bin/activate

# # Deploy on AWS
cd ~/2Projects/ehba/server && pytest