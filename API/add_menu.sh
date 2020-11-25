#!/bin/bash

curl --data "token=$1&name=$2" http://localhost:8000/menu/add/