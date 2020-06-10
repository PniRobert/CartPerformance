#!/bin/bash
declare -a urls=("https://splus-wip3.pnistaging.com/services/printing/services/printing/"
    "https://splus-wip3.pnistaging.com/services/printing/whats-new"
    "https://splus-wip3.pnistaging.com/services/printing/photo-gifts/personalized-calendars"
    "https://splus-wip3.pnistaging.com/services/printing/legacy/Themes?q=1Vs6CjtwxY_VteZzh2jc1dkRmT82QfiZ5yw3oRZWjYdH6cz_FTg4bjMz9,yB,qccP"
"https://splus-wip3.pnistaging.com/services/printing/Cart")
for target in "${urls[@]}"
do
    curl -kv "$target"
done
python ./EndToEnd.py
curl https://splus-wip3.pnistaging.com/services/printing/business-cards/ | grep -o '<a .*href=.*>' | sed -e 's/<a /\n<a /g' | sed -e 's/<a .*href=['"'"'"]//' -e 's/["'"'"'].*$//' -e '/^$/ d' | grep -o '^/.*'>urls.txt
input="./urls.txt"
while IFS= read -r line
do
    echo "https://splus-wip3.pnistaging.com$line"
    curl -kv "https://splus-wip3.pnistaging.com$line"
done < "$input"
