#!/bin/bash

echo "No turning back, deleting the database"

rm db.sqlite3

echo "Cleaning Migrations"

rm ./budget/Migrations/*