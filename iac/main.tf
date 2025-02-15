module "dynamodb_table" {
  source       = "github.com/terraform-aws-modules/terraform-aws-dynamodb-table.git"
  name         = "CodexCorpData"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attributes = [
    {
      name = "PK"
      type = "S"
    },
    {
      name = "SK"
      type = "S"
    }
  ]

  global_secondary_indexes = [
    {
      name            = "GSI1"
      hash_key        = "SK"
      range_key       = "PK"
      projection_type = "ALL"
    }
  ]

  tags = var.tags
}
