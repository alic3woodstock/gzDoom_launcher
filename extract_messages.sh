#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install babel
pybabel extract *.py -o locale/messages.pot --msgid-bugs-address='awxdeveloper@yahoo.com' \
	--copyright-holder='Alice Woodstock' --project='GZDoom_launcher' --version='2.02.00' \
	--last-translator='Alice Woodstock <awxdeveloper@yahoo.com>' --no-location
