terraform {
  required_version = "0.12.26"
}

provider "aws" {
  region = "ap-northeast-1"
}

///////////////////////////////////////////////////////////////////////////////
// Route53 の Public Zone
// ※Route53 でドメインを取得したので作成済、resource ではなく data で定義する
//
data "aws_route53_zone" "dns_zone_apex" {
  name = "ksbyzero.com"
}

///////////////////////////////////////////////////////////////////////////////
// ACM で SSL証明書を作成する
//
resource "aws_acm_certificate" "dns_zone_apex" {
  domain_name               = data.aws_route53_zone.dns_zone_apex.name
  subject_alternative_names = ["*.${data.aws_route53_zone.dns_zone_apex.name}"]
  validation_method         = "DNS"

  tags = {
    Name = data.aws_route53_zone.dns_zone_apex.name
  }

  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_route53_record" "cert_validation_0" {
  name    = aws_acm_certificate.dns_zone_apex.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.dns_zone_apex.domain_validation_options.0.resource_record_type
  records = [aws_acm_certificate.dns_zone_apex.domain_validation_options.0.resource_record_value]
  zone_id = data.aws_route53_zone.dns_zone_apex.id
  ttl     = 60
}
resource "aws_acm_certificate_validation" "cert" {
  certificate_arn = aws_acm_certificate.dns_zone_apex.arn

  validation_record_fqdns = [
    aws_route53_record.cert_validation_0.fqdn,
  ]
}
