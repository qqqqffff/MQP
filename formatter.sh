#!/usr/bin/env bash

configuration=$1

project=MQP-Wrist-Apollo-Rowe-2024-01-14-3d
cd "$project"/calibration_images || exit

side_index=0
top_index=0

for entry in "$(pwd)"/*; do
  substring="$(echo "$entry" | awk -F "/calibration_images/" '{print $2}')"
  if echo "$substring" | grep -q "side"; then
    ((side_index++))
  elif echo "$substring" | grep -q "top"; then
    ((top_index++))
  fi
  echo "$substring"
done


if [[ "$configuration" == "top" ]]; then
  echo "Starting top index = $top_index"
else
  echo "Starting side index = $side_index"
fi


for entry in "$(pwd)"/*; do
  substring="$(echo "$entry" | awk -F "/calibration_images/" '{print $2}')"
  if echo "$substring" | grep -q "top" || echo "$substring" | grep -q "side"; then
    continue
  else
    if [[ "$configuration" == "top" ]]; then
      mv "$entry" "top-$top_index.png"
      ((top_index++))
    else
      mv "$entry" "side-$side_index.png"
      ((side_index++))
    fi
  fi
done