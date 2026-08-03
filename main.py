"""
Main entry point for FPS Training Simulation.
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FOV,
    TARGET_COUNT
)

from camera import Camera

from target import (
    Target,
    GameState
)

from renderer import (
    draw_crosshair,
    draw_ground,
    draw_hud
)


def main():

    # ========================================================
    # INITIALIZE PYGAME
    # ========================================================

    pygame.init()


    screen = pygame.display.set_mode(
        (
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        ),
        DOUBLEBUF | OPENGL
    )


    pygame.display.set_caption(
        "FPS Zombie Training Simulation"
    )


    pygame.mouse.set_visible(False)

    pygame.event.set_grab(True)


    # ========================================================
    # OPENGL SETUP
    # ========================================================

    glEnable(GL_DEPTH_TEST)


    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(
        FOV,
        WINDOW_WIDTH / WINDOW_HEIGHT,
        1.0,
        500.0
    )


    glMatrixMode(GL_MODELVIEW)


    # ========================================================
    # CREATE GAME OBJECTS
    # ========================================================

    camera = Camera()


    targets = [
        Target(i)
        for i in range(TARGET_COUNT)
    ]


    game_state = GameState()


    font = pygame.font.Font(
        None,
        36
    )


    clock = pygame.time.Clock()


    running = True


    # ========================================================
    # CONTROLS
    # ========================================================

    print(
        "=== FPS Zombie Training Simulation ==="
    )

    print("Controls:")

    print("  Mouse: Look around")

    print("  Left Click: Shoot")

    print("  ESC: Exit")

    print(
        "======================================"
    )


    # ========================================================
    # MAIN GAME LOOP
    # ========================================================

    while running:


        # ----------------------------------------------------
        # EVENT PROCESSING
        # ----------------------------------------------------

        for event in pygame.event.get():


            # Window close
            if event.type == QUIT:

                running = False


            # Keyboard
            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:

                    running = False


            # Mouse movement
            elif event.type == MOUSEMOTION:

                dx, dy = event.rel

                camera.process_mouse(
                    dx,
                    dy
                )


            # Mouse click
            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:

                    # Register shot
                    game_state.shots_fired += 1


                    # Shooting ray
                    ray_origin = camera.position

                    ray_direction = camera.forward


                    hit_any = False


                    # Check every zombie
                    for target in targets:

                        if target.check_hit(
                            ray_origin,
                            ray_direction
                        ):

                            # Successful hit
                            game_state.hits += 1

                            game_state.score += 10


                            # Respawn zombie
                            target.respawn()


                            hit_any = True


                            break


                    # Display hit information
                    if hit_any:

                        print(
                            f"HIT! "
                            f"Score: {game_state.score} | "
                            f"Accuracy: "
                            f"{game_state.get_accuracy():.1f}%"
                        )


        # ----------------------------------------------------
        # UPDATE ZOMBIES
        # ----------------------------------------------------

        for target in targets:

            target.update()


        # ----------------------------------------------------
        # CLEAR SCREEN
        # ----------------------------------------------------

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )


        # ----------------------------------------------------
        # APPLY CAMERA
        # ----------------------------------------------------

        camera.apply()


        # ----------------------------------------------------
        # DRAW GROUND
        # ----------------------------------------------------

        draw_ground()


        # ----------------------------------------------------
        # DRAW ZOMBIES
        # ----------------------------------------------------

        for target in targets:

            target.draw()


        # ----------------------------------------------------
        # 2D HUD PROJECTION
        # ----------------------------------------------------

        glMatrixMode(
            GL_PROJECTION
        )

        glPushMatrix()

        glLoadIdentity()

        glOrtho(
            0,
            WINDOW_WIDTH,
            0,
            WINDOW_HEIGHT,
            -1,
            1
        )


        glMatrixMode(
            GL_MODELVIEW
        )

        glPushMatrix()

        glLoadIdentity()


        glDisable(
            GL_DEPTH_TEST
        )


        # Crosshair
        draw_crosshair()


        # HUD
        draw_hud(
            game_state,
            font,
            screen
        )


        glEnable(
            GL_DEPTH_TEST
        )


        # Restore matrices
        glPopMatrix()


        glMatrixMode(
            GL_PROJECTION
        )

        glPopMatrix()

        glMatrixMode(
            GL_MODELVIEW
        )
        # ----------------------------------------------------
        # DISPLAY FRAME
        # ----------------------------------------------------
        pygame.display.flip()
        # Approximately 60 FPS
        clock.tick(60)


    # ========================================================
    # CLEANUP
    # ========================================================

    pygame.event.set_grab(False)

    pygame.mouse.set_visible(True)

    pygame.quit()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()