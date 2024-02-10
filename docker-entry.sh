#!/usr/bin/env bash
cd /app
python setup.py develop >/dev/null 2>&1
exec bash $@
# vim:set et sts=4 ts=4 tw=80:
