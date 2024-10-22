import json
import logging
from pathlib import Path

from src.estimator.loader import XmlLoader
from src.estimator.remove_prefix import RemovePrefix

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

DATA_DIR = Path() / "data" / "sample"
SCHEMA_PATH = Path() / "data" / "data_schema.json"

FLAG = "BUILD"  # "BUILD" or "VALIDATE"

if FLAG == "VALIDATE":
    from genson import SchemaBuilder

    filenames = [file.name for file in DATA_DIR.glob("*.html")]

    random_file = filenames[2]  # random.choice(filenames)
    logger.info(random_file)
    xml_path = DATA_DIR / random_file
    loder = XmlLoader.from_path(xml_path)
    documents = RemovePrefix().transform(loder.document)

    # Function to generate JSON schema

    builder = SchemaBuilder()
    builder.add_object(documents)

    # Generate schema from the dictionary
    schema = builder.to_schema()

    with open(SCHEMA_PATH, "w") as f:
        json.dump(schema, f, indent=4)
else:
    from jsonschema import validate

    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)
    counter = 1
    for file_path in DATA_DIR.glob("*.html"):
        loder = XmlLoader.from_path(file_path)
        documents = RemovePrefix().transform(loder.document)
        try:
            validate(
                instance=documents,
                schema=schema,
            )
        except Exception:
            logger.info(f"{counter}: Validation Error in file: {file_path}")
            # print(str(e))
        else:
            logger.info(f"{counter} Validation successful in file: {file_path}")
        finally:
            counter += 1
