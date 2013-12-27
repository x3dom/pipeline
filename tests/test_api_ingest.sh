#!/bin/sh

http POST http://localhost:5000/api/v1/payload \
  Content-Type:application/octet-stream \
  X-Filename:test.ply \
  < fixtures/herkules.ply
