from datasets import Dataset
from tqdm import tqdm

from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM, 
    DataCollatorForSeq2Seq, 
    Seq2SeqTrainer, 
    TrainingArguments, 
    Seq2SeqTrainingArguments
)

import numpy as np
import argparse
import json
import logging


parser = argparse.ArgumentParser(description='Predicting')
parser.add_argument('-model_path', dest='model_path', type=str, help='HuggingFace Model Path for Prediction', required=True)
parser.add_argument('-input_file', dest='input_file', type=str, help='Txt file for input', required=True)
parser.add_argument('-backtranslate_file', dest='backtranslate_file', type=str, help='BackTranslate file', required=True)
parser.add_argument('-translate_file', dest='translate_file', type=str, help='Output file', required=True)
parser.add_argument('-batch_size', dest='batch_size', type=int, help='Predict Batch Size', default=32)
parser.add_argument('-max_length', dest='max_length', type=int, help='Sequence Input/Output Length', default=512)
parser.add_argument('-padding', dest='padding', type=str, help='Padding for Tokenizer', default='max_length')
parser.add_argument('-fp16', dest='fp16', type=bool, help='FP16', default=True)

args = parser.parse_args()

model_path = args.model_path
input_file = args.input_file
backtranslate_file = args.backtranslate_file
translate_file = args.translate_file
batch_size = args.batch_size
max_seq_length = args.max_length
fp16 = args.fp16
padding = args.padding

logger = logging.getLogger()
logger.setLevel(logging.INFO if args.logging else logging.NOTSET)


logger.info(f"==== Init model from Hugging Face's {model_path} ====")
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, pad_to_multiple_of=8 if fp16 else None, return_tensors="pt")
model.to("cuda")

logger.info(f"==== Constructing dataset for {input_file} ====")

inputs = []
with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        inputs.append(f'en: {line}')

input_dataset = Dataset.from_dict({'inputs': inputs})
input_dataset = input_dataset.map()

