terraform {
  required_version = ">= 1.5.6"
  required_providers {
    github = {
      source  = "integrations/github"
      version = "6.2.1"
    }
  }
}

provider "github" {
  owner = "org1" # Replace with the GitHub organization name
  token = var.github_token # GitHub token with permissions for org1
}

resource "github_repository" "repos" {
  for_each = local.repositories

  name        = each.key
  description = each.value.description
  visibility  = each.value.visibility

  has_issues = each.value.features.issues
  has_wiki   = each.value.features.wiki
}
