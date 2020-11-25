#!/bin/bash

curl --data "name=$1&price=$2&availablity=$3" http://localhost:8000/food/add/