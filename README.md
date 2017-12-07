# DynamoDBToES
This project shows how to index content from a DynamoDB table to an Elasticsearch cluster

To build the project, 

 * Execute the following command `pip install -r requirements.txt -t ./` or execute `make build`
 * Then `aws cloudformation package --template template.yaml --s3-bucket {S3_BUCKET} --output-template template-export.json`
 * And `aws cloudformation deploy --template-file template-export.json --stack-name {STACK_NAME} --capabilities CAPABILITY_IAM`
 
To run it, go to AWS Step Functions and run your state machine with a json following the example provided by `input-sample.json`.
 
