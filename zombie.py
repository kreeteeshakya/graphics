from OpenGL.GL import *


def draw_cube(width, height, depth, color):
    w, h, d = width / 2, height / 2, depth / 2
    glPushMatrix()
    glColor3f(*color)

    glBegin(GL_QUADS)

    # Front face
    glVertex3f(-w, -h, d)
    glVertex3f(w, -h, d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    # Back face
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, -h, -d)

    # Top face
    glVertex3f(-w, h, -d)
    glVertex3f(-w, h, d)
    glVertex3f(w, h, d)
    glVertex3f(w, h, -d)

    # Bottom face
    glVertex3f(-w, -h, -d)
    glVertex3f(w, -h, -d)
    glVertex3f(w, -h, d)
    glVertex3f(-w, -h, d)

    # Right face
    glVertex3f(w, -h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, h, d)
    glVertex3f(w, -h, d)

    # Left face
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, -h, d)
    glVertex3f(-w, h, d)
    glVertex3f(-w, h, -d)

    glEnd()
    glPopMatrix()


def draw_zombie():
    glPushMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 0)
    draw_cube(1.2, 2.0, 0.6, (0.1, 0.5, 0.2))
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 1.6, 0)
    draw_cube(0.8, 0.8, 0.8, (0.3, 0.8, 0.3))
    glPopMatrix()

    # Left Arm
    glPushMatrix()
    glTranslatef(-0.9, 0.4, 0)
    draw_cube(0.3, 1.5, 0.3, (0.3, 0.8, 0.3))
    glPopMatrix()

    # Right Arm
    glPushMatrix()
    glTranslatef(0.9, 0.4, 0)
    draw_cube(0.3, 1.5, 0.3, (0.3, 0.8, 0.3))
    glPopMatrix()

    # Left Leg
    glPushMatrix()
    glTranslatef(-0.3, -1.7, 0)
    draw_cube(0.4, 1.6, 0.4, (0.2, 0.2, 0.7))
    glPopMatrix()

    # Right Leg
    glPushMatrix()
    glTranslatef(0.3, -1.7, 0)
    draw_cube(0.4, 1.6, 0.4, (0.2, 0.2, 0.7))
    glPopMatrix()

    glPopMatrix()