#!/usr/bin/env bash
gunicorn expense_tracker.wsgi:application