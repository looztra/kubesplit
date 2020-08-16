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

# kubesplit --input test-assets/source/k8s-deployment-with-comments-1.yml \
#   --output test-assets/expected/k8s-deployment-with-comments-1--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir
@test "k8s-deployment-with-comments-1.yml, --no-quotes-preserved, --clean-output-dir" {
  kubesplit_no_quotes_preserved k8s-deployment-with-comments-1
}

# kubesplit --input test-assets/source/k8s-deployment-with-comments-1.yml \
#   --output test-assets/expected/k8s-deployment-with-comments-1--no-quotes-preserved--no-resource-prefix--spaces-before-comment_1 \
#   --no-quotes-preserved \
#   --no-resource-prefix \
#   --spaces-before-comment 1 \
#   --clean-output-dir
@test "k8s-deployment-with-comments-1.yml, --no-quotes-preserved, --no-resource-prefix, --spaces-before-comment 1, --clean-output-dir" {
  kubesplit_no_quotes_preserved_no_resource_prefix_spaces_before_comment_1 k8s-deployment-with-comments-1
}

#  kubesplit \
#   --output test-assets/expected/all-in-one--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir < test-assets/source/all-in-one.yml
@test "all-in-one.yml, --no-quotes-preserved, --clean-output-dir, input not specified" {
  kubesplit_no_quotes_preserved_stdin_not_specified all-in-one
}

#  kubesplit \
#   --input - \
#   --output test-assets/expected/all-in-one--no-quotes-preserved \
#   --no-quotes-preserved \
#   --clean-output-dir < test-assets/source/all-in-one.yml
@test "all-in-one.yml, --no-quotes-preserved, --clean-output-dir, input is -" {
  kubesplit_no_quotes_preserved_stdin_is_dash all-in-one
}
