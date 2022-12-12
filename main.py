import jmespath
import json
import logging
import os
import sys

from src.api import Rpilocator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("requests.packages.urllib3")
logger.setLevel(logging.DEBUG)
logger.propagate = True


def format_items(items):
    assert len(items) > 0

    fields = ['sku', 'vendor', 'description', 'link', "last_stock.display"]
    item_fields = items[0].keys()
    fields_to_remove = set(item_fields) - set(fields)

    for item in items:
        for field in fields_to_remove:
            item.pop(field)

    return items

def get_products(res, models):
    logging.info(f"total items: {len(res['data'])}")

    base_criteria = f"data[?avail == 'Yes']"
    matching_items = jmespath.search(base_criteria, res)
    logging.info(f"total available item(s): {len(matching_items)}")

    if models:
        model_criterias = set()

        for model in models:
            model_criterias.add(f"contains(sku, '{model}')")

        # e.g: [?contains(sku, 'CM4') || contains(sku, 'RPI4')]
        model_criterias = f"[?{' || '.join(model_criterias)}]"
        matching_items = jmespath.search(model_criterias, matching_items)
        logging.info(f"total matching item(s): {len(matching_items)}")
    
    return format_items(matching_items)

def main(models):
    is_mock = os.environ.get("IS_MOCK").lower() == 'true' or True

    if is_mock:
        logging.warn(f"Running in mocking environment")

    try:
        return json.dumps(
            get_products(Rpilocator.send('us', is_mock=is_mock), models)
        )
    except AssertionError:
        print("No available products")
        sys.exit(1)

if __name__ == "__main__":
    target_models = sys.argv[1:]
    print(main(target_models))