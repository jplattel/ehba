# Navigate into the client folder and build it
# export NODE_ENV=production
# cd ~/2Projects/ehba/client && yarn export dist 

# Deploy to S3 bucket (named: ehba.jplattel.nl) --delete means delete prev version
cd ~/2Projects/ehba/client && aws s3 sync dist s3://ehba.jplattel.nl --acl public-read --delete --profile joostplattel > /dev/null

# # Clear cloudfront
# # TODO: setup cloudfront and https

# # Activate virtual env that contains python dependencies
cd ~/.environments/ehba && source bin/activate

# # Deploy on AWS
cd ~/2Projects/ehba/server && chalice deploy --profile joostplattel