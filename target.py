"""
Target module for managing shooting targets.

This module contains:
- Target class for moving zombie objects
- GameState class for tracking player statistics
"""

import random
import numpy as np
from OpenGL.GL import *

from config import (
    BOUNDARY_X_MIN,
    BOUNDARY_X_MAX,
    BOUNDARY_Y_MIN,
    BOUNDARY_Y_MAX,
    BOUNDARY_Z_MIN,
    BOUNDARY_Z_MAX,
)

from zombie import draw_zombie


# ============================================================
# ZOMBIE HITBOX
# ============================================================

# The zombie model is scaled by 0.5 inside Target.draw().
#
# Original approximate dimensions:
# X: -1.2 to +1.2
# Y: -2.4 to +2.0
# Z: -0.7 to +0.7
#
# After scaling:
# X: -0.6 to +0.6
# Y: -1.2 to +1.0
# Z: -0.35 to +0.35
#
# Slightly enlarged for easier hit detection.

HITBOX_MIN = np.array([-0.70, -1.30, -0.50])
HITBOX_MAX = np.array([0.70, 1.10, 0.50])


# ============================================================
# TARGET CLASS
# ============================================================

class Target:
    """Represents a moving zombie target."""

    def __init__(self, target_id):
        self.id = target_id
        self.respawn()

    # ========================================================
    # RESPAWN
    # ========================================================

    def respawn(self):
        """Spawn the zombie at a random position."""

        self.position = np.array([
            random.uniform(BOUNDARY_X_MIN, BOUNDARY_X_MAX),
            random.uniform(BOUNDARY_Y_MIN, BOUNDARY_Y_MAX),
            random.uniform(BOUNDARY_Z_MIN, BOUNDARY_Z_MAX)
        ], dtype=float)

        self.velocity = np.array([
            random.uniform(-0.02, 0.02),
            random.uniform(-0.02, 0.02),
            random.uniform(-0.01, 0.01)
        ], dtype=float)

        self.active = True

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):
        """Move the zombie and bounce at world boundaries."""

        if not self.active:
            return

        self.position += self.velocity

        # X boundary
        if self.position[0] < BOUNDARY_X_MIN or self.position[0] > BOUNDARY_X_MAX:
            self.velocity[0] *= -1
            self.position[0] = np.clip(
                self.position[0],
                BOUNDARY_X_MIN,
                BOUNDARY_X_MAX,
            )

        # Y boundary
        if self.position[1] < BOUNDARY_Y_MIN or self.position[1] > BOUNDARY_Y_MAX:
            self.velocity[1] *= -1
            self.position[1] = np.clip(
                self.position[1],
                BOUNDARY_Y_MIN,
                BOUNDARY_Y_MAX,
            )

        # Z boundary
        if self.position[2] < BOUNDARY_Z_MIN or self.position[2] > BOUNDARY_Z_MAX:
            self.velocity[2] *= -1
            self.position[2] = np.clip(
                self.position[2],
                BOUNDARY_Z_MIN,
                BOUNDARY_Z_MAX,
            )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):
        """Render the zombie."""

        if not self.active:
            return

        glPushMatrix()

        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2]
        )

        glScalef(0.5, 0.5, 0.5)

        draw_zombie()

        glPopMatrix()

    # ========================================================
    # HIT DETECTION
    # ========================================================

    def check_hit(self, ray_origin, ray_direction):
        """
        Check whether the shooting ray intersects the zombie's
        axis-aligned bounding box (AABB).
        """

        if not self.active:
            return False

        ray_origin = np.asarray(ray_origin, dtype=float)
        ray_direction = np.asarray(ray_direction, dtype=float)

        epsilon = 1e-8

        box_min = self.position + HITBOX_MIN
        box_max = self.position + HITBOX_MAX

        # X axis
        if abs(ray_direction[0]) < epsilon:
            if ray_origin[0] < box_min[0] or ray_origin[0] > box_max[0]:
                return False
            t_min_x, t_max_x = -np.inf, np.inf
        else:
            t1 = (box_min[0] - ray_origin[0]) / ray_direction[0]
            t2 = (box_max[0] - ray_origin[0]) / ray_direction[0]
            t_min_x = min(t1, t2)
            t_max_x = max(t1, t2)

        # Y axis
        if abs(ray_direction[1]) < epsilon:
            if ray_origin[1] < box_min[1] or ray_origin[1] > box_max[1]:
                return False
            t_min_y, t_max_y = -np.inf, np.inf
        else:
            t1 = (box_min[1] - ray_origin[1]) / ray_direction[1]
            t2 = (box_max[1] - ray_origin[1]) / ray_direction[1]
            t_min_y = min(t1, t2)
            t_max_y = max(t1, t2)

        # Z axis
        if abs(ray_direction[2]) < epsilon:
            if ray_origin[2] < box_min[2] or ray_origin[2] > box_max[2]:
                return False
            t_min_z, t_max_z = -np.inf, np.inf
        else:
            t1 = (box_min[2] - ray_origin[2]) / ray_direction[2]
            t2 = (box_max[2] - ray_origin[2]) / ray_direction[2]
            t_min_z = min(t1, t2)
            t_max_z = max(t1, t2)

        # Find overlapping intersection interval
        t_min = max(t_min_x, t_min_y, t_min_z)
        t_max = min(t_max_x, t_max_y, t_max_z)

        if t_max < 0:
            return False

        if t_min > t_max:
            return False

        return True


# ============================================================
# GAME STATE
# ============================================================

class GameState:
    """Stores player statistics."""

    def __init__(self):
        self.shots_fired = 0
        self.hits = 0
        self.score = 0

    def get_accuracy(self):
        """Return shooting accuracy as a percentage."""

        if self.shots_fired == 0:
            return 0.0

        return (self.hits / self.shots_fired) * 100