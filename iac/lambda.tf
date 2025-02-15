provider "aws" {
  region = var.aws_region
}

module "dynamodb_lambda_function" {
  source             = "github.com/terraform-aws-modules/terraform-aws-lambda.git"
  function_name      = "dynamodb-crud"
  description        = "dynamodb crud"
  source_path        = "../src/dynamodb-crud"
  handler            = "lambda_function.lambda_handler"
  runtime            = "python3.12"
  layers             = ["arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:78"]
  memory_size        = 128
  timeout            = 10
  publish            = true
  role_name          = "dynamodb_crud_role"
  role_description   = "dynamodb_crud_role"
  attach_policy_json = true
  policy_json        = <<-EOT
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:*"
                ],
                "Resource": ["*"]
            }
        ]
    }
  EOT
  environment_variables = {
    DYNAMODB_TABLE          = module.dynamodb_table.dynamodb_table_id
    POWERTOOLS_SERVICE_NAME = "DynamoDbCRUD"
    LOG_LEVEL               = "DEBUG"

  }
  tags = var.tags
}
