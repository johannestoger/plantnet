#!/usr/bin/env bash

outfname=im_$(date '+%y%m%d_%H%M%S').jpg
outdir=~/im

mkdir -p $outdir

# Get image
outfullfile=$outdir/$outfname
curl -n http://192.168.15.21/axis-cgi/jpg/image.cgi -o $outfullfile
