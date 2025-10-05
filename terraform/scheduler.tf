# =========================
# Scheduler定義
# =========================
resource "aws_scheduler_schedule" "scheduler" {
  name                         = "lambda-every-minute"
  schedule_expression_timezone = "Asia/Tokyo"
  schedule_expression          = "cron(58 20 ? * FRI,SAT *)"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.worker.arn
    role_arn = aws_iam_role.scheduler_role.arn

    retry_policy {
      maximum_retry_attempts = 0
    }
  }
}

# =========================
# Lambdaに対してScheduler実行許可
# =========================
resource "aws_lambda_permission" "allow_scheduler" {
  statement_id  = "AllowExecutionFromScheduler"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.worker.function_name
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.scheduler.arn
}
