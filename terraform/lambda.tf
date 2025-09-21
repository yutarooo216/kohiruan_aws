resource "aws_lambda_function" "main" {
  function_name    = "kohiruan-lambda"
  role             = aws_iam_role.lambda_exec.arn
  runtime          = "python3.11"
  filename         = "lambda/main.zip"
  source_code_hash = filebase64sha256("lambda/main.zip")
  handler          = "main.lambda_handler"
}

