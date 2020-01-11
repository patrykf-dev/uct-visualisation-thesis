# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# This shim has been imported from Astropy.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Mimic six package for compatibility reasons
"""
import io


file_types = (io.TextIOWrapper, io.BufferedRandom)

string_types = (str,)
text_type = str


def iteritems(d, **kw):
    return iter(d.items(**kw))