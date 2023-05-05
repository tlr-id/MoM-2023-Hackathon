#!/usr/bin/env bash

curl -d '{"refreshtoken": "G9F02Aaw0qjFedlWjMjPhr54Ke8b2Wi8GWtafS2o37aEzqLAYc83FeGYKYZTaDE1"}' \
-H "Content-Type: application/json" \
-o "token.json" \
-X POST https://api.chartmetric.com/api/token

#python3 -c "import json; f=open('token.json'); token_dict=json.load(f); print(token_dict['token']); print(token_dict['refresh_token'])"
