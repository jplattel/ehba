# Navigate into the client folder and build it
export NODE_ENV=production
cd ~/2Projects/ehba/client && yarn export dist 
export NODE_ENV=development

# Deploy to S3 bucket (named: ehba.app) --delete means delete prev version
cd ~/2Projects/ehba/client && aws s3 sync dist s3://ehba.app --acl public-read --delete --profile joostplattel

# # Activate virtual env that contains python dependencies
cd ~/.environments/ehba && source bin/activate

# # Deploy on AWS
cd ~/2Projects/ehba/server && chalice deploy --profile joostplattel

