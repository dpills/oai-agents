#!/bin/bash

if [[ $1 == "format" ]]
then
    uv run ruff format
elif [[ $1 == "qa" ]]
then
    uv run ruff check
    uv run ruff format --check
    uv run mypy app
elif [[ $1 == "start" ]]
then
    uv run python3 -m app.main 
else
   echo "unknown command $1"
fi
