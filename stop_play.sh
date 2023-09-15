#!/bin/bash
kill -9 $(ps aux | grep '[f]fplay' | awk '{print $2}')
