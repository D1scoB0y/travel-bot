#!/bin/bash

alembic revision --autogenerate
alembic upgrade head

python -m bot
