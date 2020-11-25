#!/bin/bash

curl --data "token=$1&menu_id=$2&food_id=$3" http://localhost:8000/menu/add/food/