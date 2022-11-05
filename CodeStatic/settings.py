#!/usr/bin/python
# -*- coding: utf-8 -*-

import screeninfo

monitor_width = screeninfo.get_monitors()[0].width
monitor_height = screeninfo.get_monitors()[0].height


width = monitor_width/1.92
height = monitor_height/1.08
pos_width = (monitor_width - width) // 2
pos_height = (monitor_height - height) // 2


