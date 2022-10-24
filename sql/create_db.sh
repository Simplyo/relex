#!/bin/bash
sqlite3 relex.db <schema.sql
sqlite3 relex_test.db <schema.sql