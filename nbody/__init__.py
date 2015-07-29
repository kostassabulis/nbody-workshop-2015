"""N-body simulation project."""

import snapshots

import bodies
import constants
import diag
import euler
import icc
import leapfrog
import leapfrog_adaptive

try:
    import leapfrog_gpu
except ImportError:
    pass
    