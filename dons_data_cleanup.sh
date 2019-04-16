#!/bin/bash

DIRECTORY=$1

echo "Directory: " $DIRECTORY

for d in $DIRECTORY/logs_proto/* ; do
  echo "$d"
  rm -rf $d/processed/fusion_mesh.ply
  rm -rf $d/processed/fusion_pointcloud.ply
  rm -rf $d/processed/tsdf.bin
  rm -rf $d/processed/image_masks/*visible*
  rm -rf $d/processed/images/*depth*
  rm -rf $d/processed/rendered_images/*cropped*
done
