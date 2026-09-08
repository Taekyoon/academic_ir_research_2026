#!/usr/bin/env bash
# TREC RAG 2024 qrels: the NIST human judgements and the released UMBRELA judgements over the
# same pairs. NOT vendored - the upstream data repository carries no LICENSE file, so we do not
# redistribute it. Check the TREC data terms before use.
set -euo pipefail
mkdir -p data/trec_rag && cd data/trec_rag
curl -fL -O https://trec.nist.gov/data/rag/2024-retrieval-qrels.txt
echo "UMBRELA qrels: see https://github.com/TREC-RAG/trec-rag-data (terms apply)"
