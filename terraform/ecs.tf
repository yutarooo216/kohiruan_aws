# cluster
resource "aws_ecs_cluster" "playwright" {
  name = "playwright-cluster"

  # Container Insights 有効化（任意）
  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "playwright-cluster"
  }
}

# Task Definition
resource "aws_ecs_task_definition" "playwright" {
  family                   = "playwright-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "playwright-container"
      image     = "980921727789.dkr.ecr.ap-northeast-1.amazonaws.com/my-lambda-app:latest"
      essential = true

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.playwright.name,
          "awslogs-region"        = "ap-northeast-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      environment = [
        {
          name  = "S3_JSON_PATH"
          value = "s3://bucket/path.json"
        }
      ]
    }
  ])
}

# log group
resource "aws_cloudwatch_log_group" "playwright" {
  name              = "/ecs/playwright"
  retention_in_days = 7
}