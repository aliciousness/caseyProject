import pulumi,json
import pulumi_aws as aws
import slack
from slack_sdk import WebClient

#call slack message
config = pulumi.Config()
SLACK = WebClient(token=config.require('SLACK_ACCESS_TOKEN'))
HELLO = 'hello'

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
                "dynamodb:DescribeContributorInsights",
                "dynamodb:RestoreTableToPointInTime",
                "dynamodb:UpdateGlobalTable",
                "dynamodb:UpdateTableReplicaAutoScaling",
                "dynamodb:DescribeTable",
                "dynamodb:PartiQLInsert",
                "dynamodb:GetItem",
                "dynamodb:DescribeContinuousBackups",
                "dynamodb:DescribeExport",
                "dynamodb:EnableKinesisStreamingDestination",
                "dynamodb:BatchGetItem",
                "dynamodb:DisableKinesisStreamingDestination",
                "dynamodb:UpdateTimeToLive",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:PartiQLUpdate",
                "dynamodb:Scan",
                "dynamodb:StartAwsBackupJob",
                "dynamodb:UpdateItem",
                "dynamodb:UpdateGlobalTableSettings",
                "dynamodb:CreateTable",
                "dynamodb:RestoreTableFromAwsBackup",
                "dynamodb:GetShardIterator",
                "dynamodb:DescribeReservedCapacity",
                "dynamodb:ExportTableToPointInTime",
                "dynamodb:DescribeBackup",
                "dynamodb:UpdateTable",
                "dynamodb:GetRecords",
                "dynamodb:DescribeTableReplicaAutoScaling",
                "dynamodb:ListTables",
                "dynamodb:PurchaseReservedCapacityOfferings",
                "dynamodb:CreateTableReplica",
                "dynamodb:ListTagsOfResource",
                "dynamodb:UpdateContributorInsights",
                "dynamodb:CreateBackup",
                "dynamodb:UpdateContinuousBackups",
                "dynamodb:DescribeReservedCapacityOfferings",
                "dynamodb:PartiQLSelect",
                "dynamodb:CreateGlobalTable",
                "dynamodb:DescribeKinesisStreamingDestination",
                "dynamodb:DescribeLimits",
                "dynamodb:ListExports",
                "dynamodb:ConditionCheckItem",
                "dynamodb:ListBackups",
                "dynamodb:Query",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTimeToLive",
                "dynamodb:ListStreams",
                "dynamodb:ListContributorInsights",
                "dynamodb:DescribeGlobalTableSettings",
                "dynamodb:ListGlobalTables",
                "dynamodb:DescribeGlobalTable",
                "dynamodb:RestoreTableFromBackup",
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

# Create the lambda to execute
lambda_return = aws.lambda_.Function("lambdaFunctionReturn", 
    code=pulumi.AssetArchive({
        "index.py": pulumi.FileAsset("./index.py"),
        "__main__.py":pulumi.FileAsset("./__main__.py")
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
        )],
    billing_mode="PAY_PER_REQUEST",
    hash_key="lastName",
    range_key="firstName",
    )

# Export the API endpoint for easy access
pulumi.export("endpoint", apigw.api_endpoint)






