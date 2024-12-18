#!/bin/sh

if [ ! -d "essential-scripts" ]; then
  git clone https://github.com/GMDProjectL/essential-scripts
  cd essential-scripts
else
  cd essential-scripts
  git pull
fi

./install_essentials.sh