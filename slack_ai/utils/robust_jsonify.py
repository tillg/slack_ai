import json
import logging
from slack_ai.utils.utils import get_logger


def robust_jsonify(obj, *args, **kwargs):

    seen = set()

    class RobustEncoder(json.JSONEncoder):
        def default(self, o):
            """
            Default JSON serializer.
            """
            logger = get_logger(
                "robust_jsonify.RobustEncoder.default", logging.INFO)
            logger.info(f"Jsonifying {o} with type {type(o)} id: {id(o)}")

            # Take care of circular references
            if id(o) in seen:
                logger.info(f"Object in seen, returning <Circular Reference>")
                return '<Circular Reference>'
            # Otherwise, add it to the set of seen objects
            seen.add(id(o))

            try:
                # Try to get a dictionary representation of the object
                dict_representation = o.__dict__
                logger.info(f"Returning dictionary {dict_representation}")
                return dict_representation
            except AttributeError:
                logger.warning(
                    f"Failed to get dictionary representation of {o}")

                # If that fails, convert the object to a string
                str = str(o)
                logger.info(f"Returning string {str}")
                return str

        def encode(self, obj):
            logger = get_logger(
                "robust_jsonify.RobustEncoder.encode", logging.INFO)
            logger.info(f"Encoding {obj} with type {
                        type(obj)} and id {id(obj)}")
            return super().encode(obj)

        def iterencode(self, obj, _one_shot=False):
            logger = get_logger(
                "robust_jsonify.RobustEncoder.iterencode", logging.INFO)
            logger.info(f"{obj=}, {_one_shot=}")
            iter = super().iterencode(obj, _one_shot)
            logger.info(f"{iter=}")
            return iter

    logger = get_logger(robust_jsonify.__name__, logging.INFO)
    logger.info(f"{obj=}, {args=}, {kwargs=}")
    kwargs.setdefault('indent', 3)
    kwargs.setdefault('sort_keys', True)
    kwargs.setdefault('skipkeys', True)
    kwargs.setdefault('cls', RobustEncoder)
    kwargs.setdefault('check_circular', False)
    logger.info(f"{kwargs=}")

    return json.dumps(obj, *args, **kwargs)
