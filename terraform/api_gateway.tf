# api gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "kohiruan-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
  }
}

resource "aws_apigatewayv2_route" "main" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true
  default_route_settings {
    throttling_burst_limit = 1000
    throttling_rate_limit  = 500
  }

  stage_variables = {
    quota_limit = "100" # 1日あたりのリクエスト数
  }
}

resource "aws_apigatewayv2_integration" "main" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.main.invoke_arn
  payload_format_version = "2.0"
  integration_method     = "POST"
  connection_type        = "INTERNET"
}

resource "aws_lambda_permission" "apigateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:ap-northeast-1:${data.aws_caller_identity.current.account_id}:${aws_apigatewayv2_api.main.id}/*/*"
}