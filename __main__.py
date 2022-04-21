import pulumi,json
import pulumi_aws as aws
from pulumi import Output
import os 


    


# lambda role
lambda_role = aws.iam.Role("lambdaRole", 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
                "Action": 
                    "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
                "Effect": "Allow",
                "Sid": "",
            }]
    },))

#lambda policy
list_read_write_dynamoPolicy = aws.iam.Policy(
    resource_name = "listReadWriteDynamo",
    policy =json.dumps( {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": "*"
        }
    ]
}
))

# Attach policies to the Lambda role created above
role_policy_attachment = aws.iam.RolePolicyAttachment("lambdaRoleAttachment",
    role=lambda_role.name, 
    policy_arn=aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE)

role_policy_attachment_table = aws.iam.RolePolicyAttachment(
    "lambdaRoleAttachment--Table",
    role=lambda_role.name,
    policy_arn=list_read_write_dynamoPolicy.arn)

#Create layer
layer = aws.lambda_.LayerVersion("Slack_sdk_lambda",
layer_name = "slack_sdk",
code = pulumi.FileArchive("packages.zip"),
compatible_architectures=["x86_64", "arm64"],
compatible_runtimes = ["python3.8","python3.9"],
description = "This layer is a package for the slack sdk that i need for lambda function to run with slack"
)

# Create the lambda to execute

lambda_return = aws.lambda_.Function("lambdaFunctionReturn", 
    code=pulumi.FileArchive("./packages.zip"),
    runtime="python3.8",
    role=lambda_role.arn,
    handler="index.handler",
    layers= [layer.arn],
    environment= aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "TOKEN": os.environ("SLACK_TOKEN"),
            #old token xoxb-2895391715429-2911092400561-olwSyFBzi77lNdFYcMimVMAy
        },
    ))




# Give API Gateway permissions to invoke the Lambda
lambda_permission = aws.lambda_.Permission("lambdaPermission", 
    action="lambda:InvokeFunction",
    principal="apigateway.amazonaws.com",
    function=lambda_return)

# Set up the API Gateway
apigw = aws.apigatewayv2.Api("httpApiGateway", 
    protocol_type="HTTP",
    route_key="POST /challenge",
    target=lambda_return.invoke_arn)

#DynamoDB table for reports
dynamodbReports = aws.dynamodb.Table("dynamoDB-casey-reports",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="lastName",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="firstName",
            type="S",
        )],
    billing_mode="PAY_PER_REQUEST",
    hash_key="lastName",
    range_key="firstName",
    point_in_time_recovery= aws.dynamodb.TablePointInTimeRecoveryArgs(
        enabled= True
    )
    )
#s3 for table backup
tableS3 = aws.s3.Bucket(
    "TablePITR"
)

# Export the API endpoint for easy access
pulumi.export("endpoint", apigw.api_endpoint)
pulumi.export("layerArn",layer.arn)
pulumi.export("layerVersion", layer.version)






