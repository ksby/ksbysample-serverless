provider "aws" {
  region = "ap-northeast-1"
}

///////////////////////////////////////////////////////////////////////////////
// IAM Role
//
data "aws_iam_policy_document" "assume_role_lambda" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "lambda_role" {
  name               = "ksbysample-serverless-lambdaRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda.json
}
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:CreateLogGroup",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:ap-northeast-1:*:log-group:/aws/lambda/*:*"]
  }
}
resource "aws_iam_role_policy" "lambda_policy" {
  name   = "lambda_policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}

///////////////////////////////////////////////////////////////////////////////
// S3 Bucket
//
resource "aws_s3_bucket" "serverless_deployment_bucket" {
  bucket        = "ksbysample-serverless-deploymentbucket"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "serverless_deployment_bucket" {
  bucket = aws_s3_bucket.serverless_deployment_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
