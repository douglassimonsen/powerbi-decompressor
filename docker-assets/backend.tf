resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = "Stage2"
}
resource "aws_api_gateway_rest_api" "main" {
  name = "visualizer-backend"
  body = jsonencode({
    "info" : {
      "version" : "1.0",
      "title" : "visualizer-backend"
    },
    "paths" : {
      "/{proxy+}" : {
        "x-amazon-apigateway-any-method" : {
          "x-amazon-apigateway-integration" : {
            "httpMethod" : "ANY",
            "type" : "aws_proxy",
            "uri" : "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:111263457661:function:sam-app2-LambdaFunctionOverHttp-M4mBgJtmTNzx/invocations"
          },

          "responses" : {}
        }
      }
    },
    "swagger" : "2.0"
  })
}
resource "aws_api_gateway_stage" "main" {
  stage_name    = "Stage"
  rest_api_id   = aws_api_gateway_rest_api.main.id
  deployment_id = aws_api_gateway_deployment.main.id
}
resource "aws_lambda_function" "name" {
  filename = ""
  runtime = "python3.9"
  function_name = "visualizer-backend"
  role = aws_iam_role.backend
  handler = "application.lambda_handler"
}
resource "aws_iam_role" "backend" {
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "sts:AssumeRole"
        ],
        "Effect": "Allow",
        "Principal": {
          "Service": [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })
}
# resource "aws_lambda_permission" "backend" {
#   action = "lambda:InvokeFunction"
#   function_name = "TODO"
#   principal = "apigateway.amazonaws.com"
#   source_arn = "arn:aws:execute-api:us-east-1:111263457661:TODO/*/*$default"
# }