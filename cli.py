import click
import json
import logging
import os
from pprint import pprint

from constants import OUTPUT_TYPES
from exceptions import InvalidOutputFileType, NoDataAvailable
from parser import run_parser, write_to_json
from util import get_files_to_parse

LOGGING_CONFIG = {
    "format": "[%(asctime)s] %(filename)s:%(lineno)s %(levelname)-8s %(message)s",
    "level": "INFO",
}

logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--output-as", default="json", help="File format for output options: csv, json"
)
def parse_documents(output_as):
    file_paths = get_files_to_parse()
    parsed_sents, parsed_words = run_parser(file_paths)

    # open to extension regarding output type
    if output_as == "json":
        write_to_json(parsed_sents, "sents")
        write_to_json(parsed_words, "words")
    else:
        msg = "output_as: {} is invalid, must be one of {}".format(
            output_as, OUTPUT_TYPES
        )
        raise InvalidOutputFileType(msg)


@cli.command()
@click.argument("word")
@click.option("--words-file", default="words.json")
@click.option("--sents-file", default="sents.json")
def lookup_word(word, words_file, sents_file):

    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")
    words_file = os.path.join(output_dir, words_file)
    sents_file = os.path.join(output_dir, sents_file)

    if not (os.path.exists(words_file) and os.path.exists(sents_file)):
        msg = "No data files exist yet, it's possible you haven't run the parser"
        raise NoDataAvailable(msg)

    with open(sents_file) as sfp, open(words_file) as wfp:
        sents = json.loads(sfp.read())
        words = json.loads(wfp.read())

    word_data = words[word]
    output = {
        "word": word,
        "total_occurrences": word_data["total_occurrences"],
        "documents": word_data["documents"],
        "sentences": [
            [doc_name, sentence_num, sents[doc_name][sentence_num]]
            for doc_name, sentence_num in word_data["sentences"]
        ],
    }
    pprint(output)


if __name__ == "__main__":
    cli()
