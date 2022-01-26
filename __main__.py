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
        ),
        # aws.dynamodb.TableAttributeArgs(
        #     name="dateCreated",
        #     type="N",
        # ),
        # aws.dynamodb.TableAttributeArgs(
        #     name="reportFinished",
        #     type="N",
        # ),
        # aws.dynamodb.TableAttributeArgs(
        #     name="dateReportFinished",
        #     type="N",
        # ),
    ],
    billing_mode="PAY_PER_REQUEST",
    hash_key="lastName",
    range_key="firstName",
    # global_secondary_indexes=[aws.dynamodb.TableGlobalSecondaryIndexArgs(
    #     hash_key="reportFinished",
    #     range_key="dateCreated",
    #     name="reportFinishedIndex",
    #     non_key_attributes=["lastName","firstName","dateReportFinished"],
    #     projection_type="INCLUDE"
    # )],
    )

# Export the API endpoint for easy access
pulumi.export("endpoint", apigw.api_endpoint)
