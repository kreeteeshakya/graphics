from OpenGL.GL import *
# ============================================================
# BASIC CUBE
# ============================================================

def draw_cube(width, height, depth, color):
    """Draw a rectangular cuboid using OpenGL QUADS."""

    w = width / 2
    h = height / 2
    d = depth / 2

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


# ============================================================
# ZOMBIE COLORS
# ============================================================

SKIN = (0.55, 0.60, 0.45)
SKIN_DARK = (0.42, 0.47, 0.35)

SHIRT = (0.35, 0.32, 0.40)
TIE = (0.50, 0.15, 0.15)
PANTS = (0.30, 0.30, 0.32)

EYE_BLACK = (0.05, 0.05, 0.05)
MOUTH_DARK = (0.15, 0.05, 0.05)
TEETH = (0.85, 0.80, 0.65)


# ============================================================
# HEAD
# ============================================================

def draw_head():
    """Draw the zombie's head."""

    glPushMatrix()

    # Main head
    draw_cube(0.75, 0.70, 0.70, SKIN)

    front_z = 0.36

    # Eyes
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(side * 0.18, 0.10, front_z)
        draw_cube(0.14, 0.14, 0.04, EYE_BLACK)
        glPopMatrix()

    # Lower jaw
    glPushMatrix()
    glTranslatef(0, -0.28, front_z + 0.03)
    draw_cube(0.55, 0.22, 0.15, SKIN_DARK)
    glPopMatrix()

    # Mouth
    glPushMatrix()
    glTranslatef(0, -0.15, front_z)
    draw_cube(0.45, 0.16, 0.06, MOUTH_DARK)
    glPopMatrix()

    # Teeth
    tooth_positions = [-0.16, -0.06, 0.04, 0.14]
    tooth_heights = [0.09, 0.05, 0.08, 0.06]

    for x, tooth_height in zip(tooth_positions, tooth_heights):
        glPushMatrix()
        glTranslatef(x, -0.07 - tooth_height / 2, front_z + 0.02)
        draw_cube(0.07, tooth_height, 0.04, TEETH)
        glPopMatrix()

    glPopMatrix()


# ============================================================
# TORN CLOTH
# ============================================================

def draw_torn_flap(x, y, z, width, height, rotation):
    """Draw a torn piece of clothing."""

    glPushMatrix()

    glTranslatef(x, y, z)
    glRotatef(rotation, 0, 0, 1)

    draw_cube(width, height, 0.08, SHIRT)

    glPopMatrix()


# ============================================================
# TORSO
# ============================================================

def draw_torso():
    """Draw the zombie's torso."""

    glPushMatrix()

    # Hunched body
    glRotatef(15, 1, 0, 0)
    draw_cube(1.3, 1.7, 0.65, SHIRT)

    # Tie
    glPushMatrix()
    glTranslatef(0, 0.1, 0.35)
    draw_cube(0.18, 0.9, 0.04, TIE)
    glPopMatrix()

    # Torn clothing
    draw_torn_flap(-0.5, -0.75, 0.3, 0.25, 0.35, -20)
    draw_torn_flap(0.15, -0.85, 0.28, 0.20, 0.30, 12)
    draw_torn_flap(0.5, -0.7, -0.2, 0.22, 0.40, 25)

    glPopMatrix()


# ============================================================
# ARMS
# ============================================================

def draw_arm(x_offset):
    """Draw one zombie arm."""

    glPushMatrix()

    glTranslatef(x_offset, 0.55, 0)

    glRotatef(
        15 * (1 if x_offset > 0 else -1),
        0,
        0,
        1
    )

    glRotatef(-85, 1, 0, 0)

    # Upper arm
    draw_cube(0.28, 0.75, 0.28, SKIN)

    # Forearm
    glTranslatef(0, -0.72, 0)
    glRotatef(10, 1, 0, 0)
    draw_cube(0.24, 0.70, 0.24, SKIN)

    # Hand
    glTranslatef(0, -0.42, 0)
    draw_cube(0.30, 0.22, 0.28, SKIN_DARK)

    glPopMatrix()


# ============================================================
# LEGS
# ============================================================

def draw_leg(x_offset):
    """Draw one zombie leg."""

    glPushMatrix()

    glTranslatef(x_offset, -1.55, 0.1)
    glRotatef(-8, 1, 0, 0)

    draw_cube(0.42, 1.5, 0.42, PANTS)

    glPopMatrix()


# ============================================================
# COMPLETE ZOMBIE
# ============================================================

def draw_zombie():
    """Draw the complete hierarchical zombie model."""

    glPushMatrix()

    # Torso
    glPushMatrix()
    glTranslatef(0, 0.1, -0.1)
    draw_torso()
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 1.55, 0.25)
    glRotatef(10, 1, 0, 0)
    draw_head()
    glPopMatrix()

    # Arms
    draw_arm(-0.85)
    draw_arm(0.85)

    # Legs
    draw_leg(-0.28)
    draw_leg(0.28)

    glPopMatrix()