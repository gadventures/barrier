#!/usr/bin/env bash
set -euo pipefail
export IFS="\n\t"

echo "Writing configuration file..."
barrier-config
echo "Running WSGI service..."
barrier-wsgi
