#!/bin/bash

curl --data "username=$1&email=$2&password=$3&user_type=$4" http://localhost:8000/register/
