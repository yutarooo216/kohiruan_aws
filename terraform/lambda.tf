# api gatewayから呼び出しを受けるlambda
resource "aws_lambda_function" "main" {
  function_name    = "kohiruan-lambda"
  role             = aws_iam_role.lambda_exec.arn
  runtime          = "python3.11"
  filename         = "lambda/main.zip"
  source_code_hash = filebase64sha256("lambda/main.zip")
  handler          = "main.lambda_handler"
}

# =========================
# Lambda本体
# =========================
resource "aws_lambda_function" "worker" {
  function_name = "scheduler-test-worker"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "event_bridge.lambda_handler"
  runtime       = "python3.12"
  filename      = "lambda/event_bridge.zip"
}