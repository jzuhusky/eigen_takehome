import csv
from collections import defaultdict
import json
import logging
import os
from typing import Dict, Tuple

from exceptions import SentenceProcessingError
from tqdm import tqdm
from util import preprocess_text, make_dir_if_not_exists

logger = logging.getLogger(__name__)


def write_to_json(output_dict: Dict, filename: str) -> None:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    output_loc = os.path.join(current_dir, "output")
    filename = filename + ".json"

    output_file_dest = os.path.join(output_loc, filename)

    # make necessary dirs to successfully write output file
    make_dir_if_not_exists(output_file_dest)

    with open(output_file_dest, "w") as fp:
        logger.info("Outputting dict to '%s'", filename)
        fp.write(json.dumps(output_dict))


def run_parser(file_paths) -> Tuple[Dict, Dict]:
    """Parse documents and return 2 dicts with info about words in those documents

    Args:
        file_paths: List[str], a list of absolute-file-paths of documents to be parsed

    Returns:
        a 2-tuple of dicts. The first contains a mapping:
            (document name, sentence number) -> list of strings, sentence contents (tokenized / processed)

        The second mapping is:
            word -> {
                documents found in,
                number of total occurances,
                list of (doc name, sentence numbers), to resolve sentence contents if needed
            }
    """
    sentences = defaultdict(list)
    words = {}

    logger.info("Parsing %d files/documents", len(file_paths))
    for file_name in tqdm(file_paths):

        with open(file_name) as fp:
            text = fp.read()

        processed_text = preprocess_text(text)
        document_name = os.path.basename(file_name)

        for sentence_num, sentence_text in enumerate(processed_text):
            if (document_name, sentence_num) in sentences:
                msg = "Sentence # {}, in doc: {} has already been processed".format(
                    sentence_num, document_name
                )
                raise SentenceProcessingError(msg)

            # Store sentence data for later use and / or lookups
            sentences[document_name].append(sentence_text)

            # for each word, record the document it appeared in, and
            # what sentences it was seen in.
            for word in sentence_text:
                if word not in words:
                    words[word] = {
                        "documents": set(),
                        "sentences": [],
                        "total_occurrences": 0,
                    }
                words[word]["documents"].add(document_name)
                words[word]["sentences"].append([document_name, sentence_num])
                words[word]["total_occurrences"] += 1

    # TODO: find a different approach here, this is a bit of a hack
    # sets aren't JSON serializable, so we need to listify them.
    for word in words:
        words[word]["documents"] = list(words[word]["documents"])

    return sentences, words
