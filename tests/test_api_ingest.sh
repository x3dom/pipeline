#!/bin/sh

http POST http://localhost:5000/api/v1/buckets \
  Content-Type:application/octet-stream \
  X-Filename:test.ply \
  < fixtures/herkules.ply
