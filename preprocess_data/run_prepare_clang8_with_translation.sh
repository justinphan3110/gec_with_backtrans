#!/bin/bash

# Download the Lang-8 raw corpus from:
# https://docs.google.com/forms/d/17gZZsC_rnaACMXmPiab3kjqBEtRHPMz0UG9Dk-x_F0k/viewform?edit_requested=true
# and provide the directory here.
readonly LANG8_DIR='../../lang-8-20111007-2.0'

# Separate by comma for list of languages and backtrans files
export LANGUAGE_PAIRS='envi'
export TRANSLATION_FILES='../../clang/clang8_inputs_mtet_translate.txt'


# pip install absl-py spacy

# python -m spacy download en_core_web_sm
# python -m spacy download de_core_news_sm
# python -m spacy download ru_core_news_sm

#echo "Cloning google-research-dataset clang8 repo"

rm -r targets
git clone https://github.com/google-research-datasets/clang8.git
mv clang8/output_data .
mv clang8/targets .
rm -r clang8


echo "Generating the cLang-8 dataset for language pairs: ${LANGUAGE_PAIRS}"
echo "Translation files: ${TRANSLATION_FILES}"

python3 prepare_clang8_with_translation_dataset.py \
  --lang8_dir="${LANG8_DIR}" \
  --tokenize_text='True' \
  --language_pairs="${LANGUAGE_PAIRS}" \
  --translation_files="${TRANSLATION_FILES}"


echo "Cleaning up"
rm -r targets
