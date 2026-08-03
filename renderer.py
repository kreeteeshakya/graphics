"""
Renderer module for drawing game elements.

This module handles:
- HUD
- Ground grid
- Crosshair
"""

import pygame
from OpenGL.GL import *
from config import WINDOW_WIDTH, WINDOW_HEIGHT


# ============================================================
# CROSSHAIR
# ============================================================

def draw_crosshair():
    """Draw a crosshair at the center of the screen."""

    # Switch to 2D projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable depth testing so the crosshair stays visible
    glDisable(GL_DEPTH_TEST)

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)

    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
    size = 15

    glBegin(GL_LINES)

    # Horizontal line
    glVertex2f(cx - size, cy)
    glVertex2f(cx + size, cy)

    # Vertical line
    glVertex2f(cx, cy - size)
    glVertex2f(cx, cy + size)

    glEnd()

    glEnable(GL_DEPTH_TEST)

    # Restore matrices
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)


# ============================================================
# GROUND
# ============================================================

def draw_ground():
    """Draw a large ground grid."""

    glColor3f(0.2, 0.2, 0.2)

    grid_x_min = -100
    grid_x_max = 101

    grid_z_min = -100
    grid_z_max = 101

    grid_y = -3.0
    grid_spacing = 2

    glBegin(GL_LINES)

    # Lines parallel to Z-axis
    for x in range(grid_x_min, grid_x_max, grid_spacing):
        glVertex3f(x, grid_y, grid_z_min)
        glVertex3f(x, grid_y, grid_z_max)

    # Lines parallel to X-axis
    for z in range(grid_z_min, grid_z_max, grid_spacing):
        glVertex3f(grid_x_min, grid_y, z)
        glVertex3f(grid_x_max, grid_y, z)

    glEnd()


# ============================================================
# HUD
# ============================================================

def draw_hud(game_state, font, screen):
    """Draw score, hits, shots, and accuracy."""

    stats_text = [
        f"Score: {game_state.score}",
        f"Hits: {game_state.hits}",
        f"Shots: {game_state.shots_fired}",
        f"Accuracy: {game_state.get_accuracy():.1f}%"
    ]

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    def avg_luminance(px, py, sw=4, sh=4):
        """Calculate the average background brightness."""

        try:
            sw = max(1, int(sw))
            sh = max(1, int(sh))

            data = glReadPixels(
                int(px),
                int(py),
                sw,
                sh,
                GL_RGB,
                GL_UNSIGNED_BYTE
            )

            if not data:
                return 0.0

            total = 0
            count = 0

            for i in range(0, len(data), 3):
                r = data[i]
                g = data[i + 1]
                b = data[i + 2]

                luminance = (
                    0.2126 * r +
                    0.7152 * g +
                    0.0722 * b
                ) / 255.0

                total += luminance
                count += 1

            return total / max(1, count)

        except Exception:
            return 0.0

    # Draw each HUD line
    y_offset = 20

    for text in stats_text:

        width, height = font.size(text)

        pos_x = 20
        pos_y = WINDOW_HEIGHT - y_offset - height

        # Sample a small portion of the background
        sample_w = min(8, max(1, width // 4))
        sample_h = min(8, max(1, height // 4))

        luminance = avg_luminance(
            pos_x,
            pos_y,
            sample_w,
            sample_h
        )

        # Choose text color based on background brightness
        fg = (255, 255, 255) if luminance < 0.5 else (0, 0, 0)

        # Render text
        text_surface = font.render(text, True, fg)

        text_data = pygame.image.tostring(
            text_surface,
            "RGBA",
            True
        )

        width, height = text_surface.get_size()

        glWindowPos2d(pos_x, pos_y)

        glDrawPixels(
            width,
            height,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            text_data
        )

        y_offset += 35