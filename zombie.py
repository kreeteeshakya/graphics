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


# --- PvZ-style palette ---
SKIN = (0.55, 0.6, 0.45)        # sickly olive-gray
SKIN_DARK = (0.42, 0.47, 0.35)  # shading
SHIRT = (0.35, 0.32, 0.4)       # tattered purple-gray shirt
TIE = (0.5, 0.15, 0.15)         # dark red tie
PANTS = (0.3, 0.3, 0.32)        # gray trousers
EYE_BLACK = (0.05, 0.05, 0.05)
MOUTH_DARK = (0.15, 0.05, 0.05)
TEETH = (0.85, 0.8, 0.65)       # yellowed teeth


def draw_head():
    """Boxy bald head with simple button eyes and a gaping jaw"""
    glPushMatrix()

    draw_cube(0.75, 0.7, 0.7, SKIN)

    front_z = 0.36

    # --- Simple round-ish eyes (small black cubes, PvZ style) ---
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(side * 0.18, 0.1, front_z)
        draw_cube(0.14, 0.14, 0.04, EYE_BLACK)
        glPopMatrix()

    # --- Lower jaw, offset downward and slightly forward (open-mouth look) ---
    glPushMatrix()
    glTranslatef(0, -0.28, front_z + 0.03)
    draw_cube(0.55, 0.22, 0.15, SKIN_DARK)
    glPopMatrix()

    # --- Mouth cavity ---
    glPushMatrix()
    glTranslatef(0, -0.15, front_z)
    draw_cube(0.45, 0.16, 0.06, MOUTH_DARK)
    glPopMatrix()

    # --- Ragged teeth, uneven sizes for a broken look ---
    tooth_positions = [-0.16, -0.06, 0.04, 0.14]
    tooth_heights = [0.09, 0.05, 0.08, 0.06]
    for x, th in zip(tooth_positions, tooth_heights):
        glPushMatrix()
        glTranslatef(x, -0.07 - th / 2, front_z + 0.02)
        draw_cube(0.07, th, 0.04, TEETH)
        glPopMatrix()

    glPopMatrix()


def draw_torn_flap(x, y, z, w, h, rot):
    """A small tilted cube to fake a torn strip of cloth hanging off the shirt"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    draw_cube(w, h, 0.08, SHIRT)
    glPopMatrix()


def draw_torso():
    """Hunched, tattered-shirt torso with a loose tie"""
    glPushMatrix()

    # Main torso, tilted forward for the hunch
    glRotatef(15, 1, 0, 0)
    draw_cube(1.3, 1.7, 0.65, SHIRT)

    # Tie hanging down the front
    glPushMatrix()
    glTranslatef(0, 0.1, 0.35)
    draw_cube(0.18, 0.9, 0.04, TIE)
    glPopMatrix()

    # Torn cloth flaps at odd angles - the classic PvZ ragged hem
    draw_torn_flap(-0.5, -0.75, 0.3, 0.25, 0.35, -20)
    draw_torn_flap(0.15, -0.85, 0.28, 0.2, 0.3, 12)
    draw_torn_flap(0.5, -0.7, -0.2, 0.22, 0.4, 25)

    glPopMatrix()


def draw_arm(x_offset):
    """Arm locked straight out forward - the iconic PvZ reaching pose"""
    glPushMatrix()
    glTranslatef(x_offset, 0.55, 0)
    glRotatef(15 * (1 if x_offset > 0 else -1), 0, 0, 1)  # slight outward splay
    glRotatef(-85, 1, 0, 0)  # straight out forward, barely bent

    # Upper arm
    draw_cube(0.28, 0.75, 0.28, SKIN)

    # Forearm - only a slight elbow bend, not a full right angle
    glTranslatef(0, -0.72, 0)
    glRotatef(10, 1, 0, 0)
    draw_cube(0.24, 0.7, 0.24, SKIN)

    # Hand - slightly wider cube for that grasping look
    glTranslatef(0, -0.42, 0)
    draw_cube(0.3, 0.22, 0.28, SKIN_DARK)

    glPopMatrix()


def draw_leg(x_offset):
    """Slightly bent, shuffling legs"""
    glPushMatrix()
    glTranslatef(x_offset, -1.55, 0.1)
    glRotatef(-8, 1, 0, 0)
    draw_cube(0.42, 1.5, 0.42, PANTS)
    glPopMatrix()


def draw_zombie():
    glPushMatrix()

    # Torso (hunched)
    glPushMatrix()
    glTranslatef(0, 0.1, -0.1)
    draw_torso()
    glPopMatrix()

    # Head - lowered and pushed forward slightly to match the hunch
    glPushMatrix()
    glTranslatef(0, 1.55, 0.25)
    glRotatef(10, 1, 0, 0)
    draw_head()
    glPopMatrix()

    # Arms - straight out forward
    draw_arm(-0.85)
    draw_arm(0.85)

    # Legs
    draw_leg(-0.28)
    draw_leg(0.28)

    glPopMatrix()