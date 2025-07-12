#!/bin/bash

pytest --nbmake notebooks/ --nbmake-timeout=600 --maxfail=3 -x