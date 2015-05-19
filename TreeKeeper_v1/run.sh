#!/bin/bash

cd ./iotkit-agent/ && ./start-agent.sh && cd ..
cd ./sensor_monitor/ && ./run.sh && cd ..
cd ./tree_monitor/ && ./run.sh && cd ..
#cd ./camera_sensor/bin/ && ./do_ffmpeg.sh && cd ../../

