import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    points = []
    strokes = [] 
    drawing = True
    drawing_mode = 1
    text = """
            P = Stop/Draw
            Z = Draw rectangle
            X = Draw circle
            L = Draw line
            C = Eraser
            A = Clear
            """
    r = pygame.Rect(30, 150, 30, 30)
    g = pygame.Rect(30, 200, 30, 30)
    b = pygame.Rect(30, 250, 30, 30)
    while True:
        pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        for event in pygame.event.get():
            
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_p:
                    drawing = not drawing
            
                # determine if a letter key was pressed
                
                elif event.key == pygame.K_c:
                    mode = 'erase'
                    if points:   
                        strokes.append((points.copy(), mode, radius))
                    points = []   # start a new continuous line
                elif event.key == pygame.K_l:
                    drawing_mode = 1
                elif event.key == pygame.K_z:
                    drawing_mode = 2
                elif event.key == pygame.K_x:
                    drawing_mode = 3 
                elif event.key == pygame.K_a:
                    strokes = []
                    points = []                      
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click grows radius
                    radius = min(200, radius + 1)
                    
                    if points:   
                        strokes.append((points.copy(), mode, radius))
                    points = []   # start a new continuous line
                    
                elif event.button == 3: # right click shrinks radius
                    radius = max(1, radius - 1)
                if g.collidepoint(mouse_pos) or r.collidepoint(mouse_pos) or b.collidepoint(mouse_pos):
                    print("Button Clicked!")
                if r.collidepoint(mouse_pos):
                    mode = 'red'
                    if points:   
                        strokes.append((points.copy(), mode, radius))
                    points = []   # start a new continuous line
                elif g.collidepoint(mouse_pos):
                    mode = 'green'
                    if points:   
                        strokes.append((points.copy(), mode, radius))
                    points = []   # start a new continuous line
                elif b.collidepoint(mouse_pos):
                    mode = 'blue'
                    if points:   
                        strokes.append((points.copy(), mode, radius))
                    points = []   # start a new continuous line
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and points:
                    strokes.append((points.copy(), mode, radius))
                    points = []
                    
            
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:   # Left mouse button is held
                    position = event.pos
                    points = points + [position]
                    points = points[-256:]
                
                
        screen.fill((0, 0, 0))

        

        # --- Draw all saved strokes ---
        for pts, col_mode, rad, d_mode in strokes:
            for i in range(len(pts) - 1):
                drawLineBetween(screen, i, pts[i], pts[i+1], rad, col_mode)

        # --- Draw the current stroke (if drawing is enabled) ---
        if drawing:
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i+1], radius, mode)
            
        font = pygame.font.SysFont(None, 26)
        p_text = font.render(text, True, (255, 255, 255))
        screen.blit(p_text, (-35, 0))

        pygame.draw.rect(screen, (0, 0, 255), b)
        pygame.draw.rect(screen, (255, 0, 0), r)
        pygame.draw.rect(screen, (0, 255, 0), g)
        pygame.display.flip()
        
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'erase':
        color = (0,0,0)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)
    
        
        
main()