#!/usr/bin/env bash

cd nunif || exit
. ./venv/Scripts/activate

current_directory=$(pwd)
search_dir="$current_directory"/tmp/images
out_dir="$current_directory"/tmp/out

if [ -d "$out_dir" ]; then
  echo "Output directory detected clearing space..."
  rm -rf "$out_dir"
  mkdir "$out_dir"
  mkdir "$out_dir/n-0"
  mkdir "$out_dir/n-1"
  mkdir "$out_dir/n-2"
  mkdir "$out_dir/n-3"
else
  echo "Making output directories at $out_dir"
  mkdir "$out_dir"
  mkdir "$out_dir/n-0"
  mkdir "$out_dir/n-1"
  mkdir "$out_dir/n-2"
  mkdir "$out_dir/n-3"
fi

if [ -d "$search_dir" ]; then
  for entry in "${search_dir}"/*; do
    substring="$(echo "$entry" | awk -F "/images/" '{print $2}')"

    output_directory="$out_dir/n-0/$substring"
    mkdir "$output_directory"
    echo "Upscaling 4x $substring directory noise param = 0"
    python -m waifu2x.cli --style photo -m noise_scale -n 0 -i "$entry" -o "$output_directory"

#    output_directory="$out_dir/n-1/$substring"
#    mkdir "$output_directory"
#    echo "Upscaling 4x $substring directory noise param = 1"
#    python -m waifu2x.cli --style photo -m noise_scale4x -n 1 -i "$entry" -o "$output_directory"
#
#    output_directory="$out_dir/n-2/$substring"
#    mkdir "$output_directory"
#    echo "Upscaling 4x $substring directory noise param = 2"
#    python -m waifu2x.cli --style photo -m noise_scale4x -n 2 -i "$entry" -o "$output_directory"
#
#    output_directory="$out_dir/n-3/$substring"
#    mkdir "$output_directory"
#    echo "Upscaling 4x $substring directory noise param = 3"
#    python -m waifu2x.cli --style photo -m noise_scale4x -n 3 -i "$entry" -o "$output_directory"
  done
else
  echo "Directory not found: $search_dir"
fi