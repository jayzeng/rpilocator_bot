import jmespath
import sys
import json
from src.api import Rpilocator


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
    base_criteria = f"data[?avail == 'Yes']"
    matching_items = jmespath.search(base_criteria, res)

    if models:
        model_criterias = set()

        for model in models:
            model_criterias.add(f"contains(sku, '{model}')")

        # e.g: [?contains(sku, 'CM4') || contains(sku, 'RPI4')]
        model_criterias = f"[?{' || '.join(model_criterias)}]"
        matching_items = jmespath.search(model_criterias, matching_items)
    
    return format_items(matching_items)

def main(models):
    return json.dumps(
        get_products(Rpilocator.send('us', is_mock=True), models)
    )

if __name__ == "__main__":
    target_models = sys.argv[1:]
    print(main(target_models))