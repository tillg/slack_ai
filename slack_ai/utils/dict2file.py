import json
import logging
import os
from typing import Dict, Optional
from slack_ai.utils.robust_jsonify import robust_jsonify
from slack_ai.utils.utils import get_logger, get_now_as_string

def write_dict_to_file(*, dictionary: Dict, full_filename: str) -> Dict:
    """Writes a dictionary to a file. Also updates the _stats element."""
    logger = get_logger(write_dict_to_file.__name__, logging.INFO)
    if not isinstance(dictionary, dict):
        raise TypeError("Expected a dictionary, but got a " +
                        str(type(dictionary)))
    # log("writeDictToFile", "Len of dict to write: ", len(dictionary), " type: ", type(dictionary))
    dictionary.setdefault("_stats", {"lastWritten": get_now_as_string()})
    dictionary["_stats"]["lastWritten"] = get_now_as_string()
    dictionary["_stats"]["counter"] = len(dictionary) - 1
    stats = dictionary["_stats"]
    del dictionary["_stats"]
    # log("writeDictToFile", "Len of dict after deleting _stats: ", len(dictionary), " type: ", type(dictionary))
    dictionary = dict(sorted(dictionary.items()))
    # log("writeDictToFile", "Len of dict after sorting: ", len(dictionary), " type: ", type(dictionary))
    sorted_dictionary = {"_stats": stats, **dictionary}
    # log("writeDictToFile", "Len of sorted dict to write: ", len(sortedDictionary), " type: ", type(dictionary))
    dict_dump = robust_jsonify(sorted_dictionary, sort_keys=False, indent=2)

    # Make sure that the directory in which we want to write exists.
    directory = os.path.dirname(os.path.abspath(full_filename))
    # log('writeDictToFile', 'Writing to dir ', directory)
    try:
        os.makedirs(directory)
    except FileExistsError:
        # directory already exists, so no need to create it - all good
        pass

    with open(full_filename, 'w') as file:
        file.write(dict_dump)
    return sorted_dictionary


def read_dict_from_file(*, full_filename: str, skip_file_not_found=True) -> Dict:
    """Reads a dictionary from a file. Checks that the dictionary read has a _stats.lastWritten entry."""
    logger = get_logger(read_dict_from_file.__name__, logging.INFO)
    data = {}
    try:
        with open(full_filename, "r+") as file:
            data = json.load(file)
            if data is None:
                return {}
            if data.get("_stats", {}).get("lastWritten") is None:
                logger.warning(
                    f"Read file {full_filename} successfully but does not contain _stats.lastWritten.")
            return data
    except IOError as e:
        if not skip_file_not_found:
            logger.error(f"Could not open file {full_filename}")
            raise e
        else:
            logger.warn(f"Could not open file {
                        full_filename} - returning empty dict.")
    return data
