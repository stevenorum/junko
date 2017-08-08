#!/usr/bin/env python3

from traceback import extract_stack

LEVEL = 0

TRACE=0
DEBUG=1
INFO=2
WARN=3
ERROR=4
FATAL=5
CATACLYSM=6

LEVELS=[
    TRACE,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL,
    CATACLYSM
    ]

LEVEL_NAMES=[
    "TRACE",
    "DEBUG",
    "INFO",
    "WARN",
    "ERROR",
    "FATAL",
    "CATACLYSM"
]

def set_level(level):
    if level not in LEVELS:
        raise RuntimeError("Invalid log level {level} provided,".format(level=level))
    global LEVEL
    LEVEL = level

def _log(content, level, tag=None, trace_depth=0):
    if level < LEVEL:
        return
    tag = tag if tag else "{file}:{line}".format(file=extract_stack(limit=3+trace_depth)[0][0], line=extract_stack(limit=3+trace_depth)[0][1])
    print("[{level}] [{tag}] {content}".format(level=LEVEL_NAMES[level], tag=tag, content=content))

def trace(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=TRACE, trace_depth=trace_depth)

def debug(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=DEBUG, trace_depth=trace_depth)

def info(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=INFO, trace_depth=trace_depth)

def warn(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=WARN, trace_depth=trace_depth)

def error(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=ERROR, trace_depth=trace_depth)

def fatal(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=FATAL, trace_depth=trace_depth)

def cataclysm(content, tag=None, trace_depth=0):
    _log(content=content, tag=tag, level=CATACLYSM, trace_depth=trace_depth)

