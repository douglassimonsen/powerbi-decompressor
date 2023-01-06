resource "aws_api_gateway_deployment" "backend" {
  rest_api_id = aws_api_gateway_rest_api.backend.id
  stage_name  = "Stage"
}
resource "aws_api_gateway_rest_api" "backend" {
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
resource "aws_api_gateway_stage" "backend" {
  stage_name    = "Stage"
  rest_api_id   = aws_api_gateway_rest_api.backend.id
  deployment_id = aws_api_gateway_deployment.backend.id
}
resource "aws_lambda_function" "backend" {
  filename      = "lambda.zip"
  runtime       = "python3.9"
  function_name = "visualizer-backend"
  role          = aws_iam_role.backend.arn
  timeout       = 5
  handler       = "application.lambda_handler"
}
resource "aws_iam_role" "backend" {
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "sts:AssumeRole"
        ],
        "Effect" : "Allow",
        "Principal" : {
          "Service" : [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
}
resource "aws_lambda_permission" "backend" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:us-east-1:111263457661:${aws_api_gateway_rest_api.backend.arn}/*/*"
}