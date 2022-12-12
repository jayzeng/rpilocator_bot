#!/usr/bin/env bash
output_file=$1
joboutput=$(python main.py CM4)
numEntries=$(echo $joboutput | jq -r '. | length')

if [ "$numEntries" -le 0 ]; then
	echo "no file"
	exit 0
fi

items=$(echo $joboutput | jq -r '.[] | "- \(.description) by \(.vendor) \(.link)"')
items=$(printf "%s\n" "$items")
cat << EOF > $output_file
{
  "text": "rpilocator has updates",
  "blocks": [
  	{
  		"type": "section",
  		"text": {
			"type": "mrkdwn",
			"text": $items
  		}
  	}
  ]
}
EOF