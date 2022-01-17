import pulumi
import json
import pulumi_aws as aws

# lambda role
lambda_role = aws.iam.Role("lambdaRole", 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
                "Effect": "Allow",
                "Sid": "",
            }]
    }))

# Attach fullaccess policy to the Lambda role created above
role_policy_attachment = aws.iam.RolePolicyAttachment("lambdaRoleAttachment",
    role=lambda_role,
    policy_arn=aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE)

# Create the lambda to execute
lambda_return = aws.lambda_.Function("lambdaFunctionReturn", 
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./function"),
    }),
    runtime="python3.9",
    role=lambda_role.arn,
    handler="index.handler")

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

# Export the API endpoint for easy access
pulumi.export("endpoint", apigw.api_endpoint)
