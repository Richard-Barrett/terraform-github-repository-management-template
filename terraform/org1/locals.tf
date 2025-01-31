locals {
  repositories = {
    my-new-repo = {
      description = "This is a new repository for Python projects."
      language    = "python"
      visibility  = "private"
      features = {
        issues = true
        wiki   = false
      }
    }
  }
}