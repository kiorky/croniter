#!/usr/bin/env bash
set -ex
. venv/bin/activate
fullrelease
git push taichino && git push taichino --tags
# vim:set et sts=4 ts=4 tw=80:
