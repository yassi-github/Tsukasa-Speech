#!/bin/bash

echo "Fetching Git LFS files from Hugging Face..."
git-lfs ls-files -n | xargs -t hf download Respair/Tsukasa_Speech --local-dir ./
