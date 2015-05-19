#!/bin/bash
node tree_monitor.js 84:dd:20:f0:8e:e0 1 > tree1.log &
node tree_monitor.js 84:dd:20:f0:8e:6a 2 > tree2.log &
node tree_monitor.js 84:dd:20:f0:8e:fe 3 > tree3.log &
