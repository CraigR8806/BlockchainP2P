#!/bin/bash

ps aux | grep "[i]ndex.js" | awk '{print $2}' | xargs kill -9
