#!/usr/bin/env bash
# CLEF eHealth TAR 2017/2018/2019 - topics, qrels and participant runs.
# Source repository is MIT licensed (Leif Azzopardi), so these are redistributable with
# attribution; they are fetched rather than vendored so the provenance stays visible.
set -euo pipefail
mkdir -p data/clef && cd data/clef
git clone --depth 1 https://github.com/CLEF-TAR/tar.git
echo "qrels:"; ls tar/2017-TAR/testing/
echo "participant runs:"; ls tar/2017-TAR/participant-runs/ | head
