resource "aws_api_gateway_rest_api" "backend" {
  name = "visualizer-backend"
}
resource "aws_api_gateway_resource" "backend" {
  rest_api_id = "${aws_api_gateway_rest_api.backend.id}"
  parent_id   = "${aws_api_gateway_rest_api.backend.root_resource_id}"
  path_part   = "{proxy+}"
}
resource "aws_api_gateway_method" "backend" {
  rest_api_id   = "${aws_api_gateway_rest_api.backend.id}"
  resource_id   = "${aws_api_gateway_resource.backend.id}"
  http_method   = "ANY"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "backend" {
  rest_api_id = "${aws_api_gateway_rest_api.backend.id}"
  resource_id = "${aws_api_gateway_method.backend.resource_id}"
  http_method = "${aws_api_gateway_method.backend.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.backend.invoke_arn}"
}
resource "aws_api_gateway_deployment" "backend" {
  rest_api_id = aws_api_gateway_rest_api.backend.id
  stage_name  = "Stage"
  depends_on = [
    aws_api_gateway_integration.backend,
  ]
}
resource "aws_lambda_function" "backend" {
  filename      = "lambda.zip"
  runtime       = "python3.9"
  function_name = "visualizer-backend"
  role          = aws_iam_role.backend.arn
  timeout       = 5
  handler       = "application.lambda_handler"
}
resource "aws_iam_policy" "backend" {
  name = "lambda-demo"
  path = "/"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "asd",
        "Effect" : "Allow",
        "Action" : "ssm:GetParameter",
        "Resource" : ["arn:aws:ssm:us-east-1:111263457661:parameter/db"]
      },
      {
        "Sid" : "qwe",
        "Effect" : "Allow",
        "Action" : [
          "ssm:DescribeParameters"
        ],
        "Resource" : "*"
      }
    ]
  })
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
  
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", aws_iam_policy.backend.arn]
}
resource "aws_lambda_permission" "backend" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.backend.execution_arn}/*/*"
}
resource "aws_ssm_parameter" "backend_url" {
  name = "visualizer-backend"
  type = "String"
  value = aws_api_gateway_deployment.backend.invoke_url
}