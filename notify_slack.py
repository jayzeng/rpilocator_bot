import json
import sys

def make_slack_payload_file(output_file, items):
    subject = f"{len(items)} available!"
    body = []

    for item in items:
        body.append(f"- {item['description']}, ${item['price']['display']} {item['price']['currency']} ({item['vendor']}), {item['link']}")

    slack_payload = {
        "text": subject,
        "blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": '\n'.join(body)
            }
        }]
    }

    with open(output_file, 'w') as fw:
        json.dump(slack_payload, fw)

def main(items_file, payload_output):
    with open(items_file) as fr:
        items = json.load(fr)
        make_slack_payload_file(payload_output, items)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])