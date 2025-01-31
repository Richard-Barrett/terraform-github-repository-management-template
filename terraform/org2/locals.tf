locals {
  repositories = {
    another-repo = {
      description = "This is a new repository for Java projects."
      language    = "java"
      visibility  = "public"
      features = {
        issues = false
        wiki   = true
      }
    }
  }
}