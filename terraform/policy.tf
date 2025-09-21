resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda に S3 への PutObject のみ許可するポリシー
resource "aws_iam_policy" "lambda_s3_write" {
  name        = "lambda-s3-write-only"
  description = "Allow Lambda to put objects in S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::kohiruan-reservation/*"
      }
    ]
  })
}

# Lambda 実行ロールにポリシーをアタッチ
resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_s3_write.arn
}