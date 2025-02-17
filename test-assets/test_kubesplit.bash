function diff_result_vs_expected() {
  local f_input=$1
  local config=$2

  [ -d "$BATS_TMPDIR/result" ]
  [ -d "$BATS_TEST_DIRNAME/test-assets/expected/${f_input}--${config}" ]
  diff -q -r "$BATS_TEST_DIRNAME/test-assets/expected/${f_input}--${config}/" "$BATS_TMPDIR/result/"
}

function kubesplit_no_quotes_preserved() {
  local f_input=$1
  uv run kubesplit \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result" \
    --no-quotes-preserved \
    --clean-output-dir
  diff_result_vs_expected "${f_input}" no-quotes-preserved
}

function kubesplit_no_quotes_preserved_stdin_not_specified() {
  local f_input=$1
  uv run kubesplit \
    --output "$BATS_TMPDIR/result" \
    --no-quotes-preserved \
    --clean-output-dir <"$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml"
  diff_result_vs_expected "${f_input}" no-quotes-preserved
}

function kubesplit_no_quotes_preserved_stdin_is_dash() {
  local f_input=$1
  uv run kubesplit \
    --input - \
    --output "$BATS_TMPDIR/result" \
    --no-quotes-preserved \
    --clean-output-dir <"$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml"
  diff_result_vs_expected "${f_input}" no-quotes-preserved
}

function kubesplit_no_quotes_preserved_no_resource_prefix() {
  local f_input=$1
  uv run kubesplit \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result" \
    --no-quotes-preserved \
    --no-resource-prefix \
    --clean-output-dir
  diff_result_vs_expected "${f_input}" no-quotes-preserved--no-resource-prefix
}

function kubesplit_no_quotes_preserved_no_resource_prefix_spaces_before_comment_1() {
  local f_input=$1
  uv run kubesplit \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result" \
    --no-quotes-preserved \
    --no-resource-prefix \
    --spaces-before-comment 1 \
    --clean-output-dir
  diff_result_vs_expected "${f_input}" no-quotes-preserved--no-resource-prefix--spaces-before-comment_1
}
