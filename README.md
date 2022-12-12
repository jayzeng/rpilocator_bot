# Rpilocator bot
PI becomes almost impossible to purchase these days, this is a tiny bot to send slack messages to notify myself to buy CM4

# Usage:
It supports multiple products
e.g: 
```
python3 main.py CM4 RPI4
```

Or you can run in "mock" mode, which will simply load the mock.json as stub content
```
IS_MOCK=True python3 main.py CM4
```

# Run in your environment
1. clone this repo
2. add a secret (Settings -> Security -> Actions -> Repository secrets) named SLACK_WEBHOOK_URL
3. paste in your slack webhook url

# How it works
1. Retrieve token from https://rpilocator.com/
2. Makes a subsequent call (see src/api.py) for implementation details

THANKS  https://rpilocator.com/! Please DO NOT USE this for commercial purpose