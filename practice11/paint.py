import pygame
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Drawing App")
    clock = pygame.time.Clock()

    radius = 15          
    mode = 'blue'        
    points = []         
    # history stores every finished drawn object in creation order.
    # Each entry is either:
    #   ('stroke', pts, mode, radius)              – freehand or eraser line
    #   ('figure', coords, mode, radius, d_mode)   – any shape
    history = []
    figures = []         
    drawing = True       
    drawing_mode = 1     # 1=line, 2=rect, 3=circle, 4=square,
                         # 5=right-triangle, 6=equilateral-triangle, 7=rhombus
    fig_start = (0, 0)   # mouse position where the current shape drag began

    # Instruction text shown in the top-left panel
    text = (
        "  P = Stop/Draw\n"
        "  Z = Draw rectangle\n"
        "  X = Draw circle\n"
        "  Q = Draw square\n"
        "  W = Draw right triangle\n"
        "  E = Draw equilateral triangle\n"
        "  R = Draw rhombus\n"
        "  L = Draw line\n"
        "  C = Eraser\n"
        "  A = Clear"
    )

    r_btn = pygame.Rect(30, 220, 30, 30)
    g_btn = pygame.Rect(30, 270, 30, 30)
    b_btn = pygame.Rect(30, 320, 30, 30)

    # Modes that produce a "figure" (not a freehand stroke)
    FIGURE_MODES = (2, 3, 4, 5, 6, 7)


    while True:
        pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        alt_held  = pressed[pygame.K_LALT]  or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w and ctrl_held) \
                        or (event.key == pygame.K_F4 and alt_held) \
                        or event.key == pygame.K_ESCAPE:
                    return

                # Toggle drawing on/off
                if event.key == pygame.K_p:
                    drawing = not drawing

                # --- Tool / mode selection keys ---
                elif event.key == pygame.K_l:
                    drawing_mode = 1   # freehand line

                elif event.key == pygame.K_z:
                    drawing_mode = 2   # rectangle

                elif event.key == pygame.K_x:
                    drawing_mode = 3   # circle

                elif event.key == pygame.K_q:
                    drawing_mode = 4   # square

                elif event.key == pygame.K_w:
                    drawing_mode = 5   # right triangle

                elif event.key == pygame.K_e:
                    drawing_mode = 6   # equilateral triangle

                elif event.key == pygame.K_r:
                    drawing_mode = 7   # rhombus

                elif event.key == pygame.K_c:
                    mode = 'erase'
                    if points:
                        history.append(('stroke', points.copy(), mode, radius))
                    points = []

                elif event.key == pygame.K_a:
                    # Clear the entire canvas
                    history = []
                    points  = []
                    figures = []

            # ---- Mouse button DOWN ----
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    # Remember where the drag started for shape modes
                    if drawing_mode in FIGURE_MODES:
                        fig_start = mouse_pos

                    # For freehand: commit any previous unfinished stroke
                    if drawing_mode == 1:
                        if points:
                            history.append(('stroke', points.copy(), mode, radius))
                        points = []

                    radius = min(200, radius + 1)   # grow brush on click

                elif event.button == 3:             # right click shrinks brush
                    radius = max(1, radius - 1)

                # Check color-picker buttons
                if r_btn.collidepoint(mouse_pos):
                    mode = 'red'
                    if points:
                        history.append(('stroke', points.copy(), mode, radius))
                    points = []
                elif g_btn.collidepoint(mouse_pos):
                    mode = 'green'
                    if points:
                        history.append(('stroke', points.copy(), mode, radius))
                    points = []
                elif b_btn.collidepoint(mouse_pos):
                    mode = 'blue'
                    if points:
                        history.append(('stroke', points.copy(), mode, radius))
                    points = []

            # ---- Mouse button UP: commit the finished object ----
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if drawing_mode == 1 and points:
                        # Commit the freehand stroke
                        history.append(('stroke', points.copy(), mode, radius))
                        points = []
                    elif drawing_mode in FIGURE_MODES and figures:
                        # Commit the finished shape
                        history.append(('figure', figures.copy(), mode, radius, drawing_mode))
                        figures = []

            # ---- Mouse motion: update the live preview ----
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:   # left button held
                    if drawing_mode == 1:
                        # Accumulate freehand points (cap at 256 to avoid lag)
                        points = (points + [event.pos])[-256:]
                    elif drawing_mode in FIGURE_MODES:
                        # Store only the start/end pair; redrawn every frame
                        figures = [(fig_start, mouse_pos)]


        screen.fill((0, 0, 0))   # clear to black each frame

        # --- Replay history in creation order ---
        for entry in history:
            if entry[0] == 'stroke':
                _, pts, col_mode, rad = entry
                for i in range(len(pts) - 1):
                    drawLineBetween(screen, i, pts[i], pts[i + 1], rad, col_mode)

            elif entry[0] == 'figure':
                _, coords, col_mode, rad, d_mode = entry
                st, et = coords[0]
                drawfig(screen, 0, st, et, rad, col_mode, d_mode)

        # --- Draw the live/in-progress object (preview while dragging) ---
        if drawing:
            if drawing_mode == 1:
                for i in range(len(points) - 1):
                    drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            elif drawing_mode in FIGURE_MODES and figures:
                s, e = figures[0]
                drawfig(screen, 0, s, e, radius, mode, drawing_mode)

        font = pygame.font.SysFont(None, 24)
        for line_idx, line in enumerate(text.splitlines()):
            rendered = font.render(line, True, (255, 255, 255))
            screen.blit(rendered, (0, line_idx * 20))

        pygame.draw.rect(screen, (0, 0, 255), b_btn)
        pygame.draw.rect(screen, (255, 0, 0), r_btn)
        pygame.draw.rect(screen, (0, 255, 0), g_btn)

        pygame.display.flip()
        clock.tick(60)



def drawfig(screen, index, start, end, width, color_mode, draw_mode):
    """
    Draw a shape from *start* to *end* with the given *width* (outline thickness)
    and *color_mode*.  *draw_mode* selects which shape to render:
        2 – rectangle
        3 – circle (bounding-box ellipse-fitting)
        4 – square  (equal sides, derived from the shorter dimension)
        5 – right triangle  (right angle at the start corner)
        6 – equilateral triangle (base along the bottom of the bounding box)
        7 – rhombus (diamond fitted inside the bounding box)
    """
    x1, y1 = start
    x2, y2 = end

    # ---- derive a brightness value from the diagonal length ----
    diag = math.hypot(x2 - x1, y2 - y1)
    r_val = int(diag / 2)
    c1 = max(0, min(255, r_val - 256))
    c2 = max(0, min(255, r_val))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    else:  # 'erase'
        color = (0, 0, 0)

    # ---- Rectangle ----
    if draw_mode == 2:
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, rect, width)

    # ---- Circle (fits inside the bounding box diagonal) ----
    elif draw_mode == 3:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        radius = max(1, int(math.hypot(x2 - x1, y2 - y1) / 2))
        pygame.draw.circle(screen, color, (cx, cy), radius, width)

    # ---- Square (side = min of width/height of drag area) ----
    elif draw_mode == 4:
        # Use the shorter dimension so all sides are equal.
        # The square extends from the start corner in the drag direction.
        side = min(abs(x2 - x1), abs(y2 - y1))
        # Preserve the sign of the drag so the square follows the mouse
        sx = x1 + (side if x2 >= x1 else -side)
        sy = y1 + (side if y2 >= y1 else -side)
        rect = pygame.Rect(min(x1, sx), min(y1, sy), side, side)
        pygame.draw.rect(screen, color, rect, width)

    # ---- Right triangle (right angle at the drag-start corner) ----
    elif draw_mode == 5:
        # Vertices:  bottom-left (right-angle), top-left, bottom-right
        #   A = (x1, y2)  – right-angle vertex
        #   B = (x1, y1)  – top of the vertical leg
        #   C = (x2, y2)  – end of the horizontal leg
        pts = [(x1, y2), (x1, y1), (x2, y2)]
        pygame.draw.polygon(screen, color, pts, width)

    # ---- Equilateral triangle (base spans the bounding box width) ----
    elif draw_mode == 6:
        # Base: left=(x1, y2)  right=(x2, y2)
        # Apex: horizontally centred, height = (sqrt(3)/2) * base_length
        base_len = abs(x2 - x1)
        apex_x   = (x1 + x2) / 2
        # Height of an equilateral triangle
        height   = (math.sqrt(3) / 2) * base_len
        # Place the apex above the base (in the upward direction relative to drag)
        apex_y   = y2 - height if y1 <= y2 else y2 + height
        pts = [(x1, y2), (x2, y2), (apex_x, apex_y)]
        pygame.draw.polygon(screen, color, pts, width)

    # ---- Rhombus (diamond fitted inside the bounding box) ----
    elif draw_mode == 7:
        # Four vertices at the midpoints of the bounding box edges:
        #   top-mid, right-mid, bottom-mid, left-mid
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        pts = [
            (mid_x, y1),   # top
            (x2,   mid_y), # right
            (mid_x, y2),   # bottom
            (x1,   mid_y), # left
        ]
        pygame.draw.polygon(screen, color, pts, width)



def drawLineBetween(screen, index, start, end, width, color_mode):
    """
    Draw a thick line segment between *start* and *end* by placing filled
    circles along the path.  The color shifts subtly with *index* to give
    the stroke a gradient feel.
    """
    # Gradient offset: early points in the stroke are darker
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    else:  # 'erase'
        color = (0, 0, 0)

    # Step from start to end and stamp a circle at each pixel position
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress  = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()