#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)