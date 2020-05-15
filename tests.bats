#!/usr/bin/env bats

load test-assets/test_kubesplit

@test "--help" {
  python -m kubesplit --help
}

# kubesplit --input test-assets/source/all-in-one.yml \
#   --output test-assets/expected/all-in-one--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir
@test "all-in-one.yml, --no-quotes-preserved, --clean-output-dir" {
  kubesplit_no_quotes_preserved all-in-one
}

# kubesplit --input test-assets/source/all-in-one.yml \
#   --output test-assets/expected/all-in-one--no-quotes-preserved--no-resource-prefix \
#   --no-quotes-preserved \
#   --no-resource-prefix \
#   --clean-output-dir
@test "all-in-one.yml, --no-quotes-preserved, --no-resource-prefix, --clean-output-dir" {
  kubesplit_no_quotes_preserved_no_resource_prefix all-in-one
}

# kubesplit --input test-assets/source/mixed-content-valid-invalid-and-empty-resources.yml \
#   --output test-assets/expected/mixed-content-valid-invalid-and-empty-resources--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir
@test "mixed-content-valid-invalid-and-empty-resources.yml, --no-quotes-preserved, --clean-output-dir" {
  kubesplit_no_quotes_preserved mixed-content-valid-invalid-and-empty-resources
}

# kubesplit --input test-assets/source/mixed-content-valid-invalid-empty-and-list-resources.yml \
#   --output test-assets/expected/mixed-content-valid-invalid-empty-and-list-resources--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir
@test "mixed-content-valid-invalid-empty-and-list-resources.yml, --no-quotes-preserved, --clean-output-dir" {
  kubesplit_no_quotes_preserved mixed-content-valid-invalid-empty-and-list-resources
}
