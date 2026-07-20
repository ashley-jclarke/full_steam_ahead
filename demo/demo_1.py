import pygame
import random


win = pygame.display.set_mode((320, 320))


BLACK = (0,0,0)
DARK = (50, 100, 10)
LIGHT = (50, 180, 10)
BRIGHT = (80, 255, 10)

class Train:
    def __init__(self):
        self.acceleration = 0.002
        self.speed = 0
        self.max_speed = 1.0
        self.max_bonus = 1.5
        self.fuel = 100
        self.position = 0
        self.track = 2
        self.boost = False
        self.end_boost_time = 0
        
    def tick(self, delta, time):
        if time > self.end_boost_time and self.boost:
            self.boost = False
            print("End boost")
        max_speed = self.max_speed if not self.boost else self.max_speed * self.max_bonus
        if self.speed < max_speed:
            self.speed += self.acceleration * (1 if not self.boost else 4)
        if self.speed > max_speed:
            self.speed -= self.acceleration * 4
        self.position += self.speed
        
    def activate_boost(self, time):
        if self.boost: return # Can't double boost
        self.fuel -= 5
        if self.fuel < 0: return
        self.end_boost_time = time + 3000
        self.max_speed += 0.1
        self.boost = True

    def cart_height(self):
        return 2 + int(4.0*(self.fuel/100.0))
    

class TrackChange:
    def __init__(self, from_track: int, to_track: int, start_position: int):
        self.from_track = from_track
        self.to_track = to_track
        self.start_position = start_position
        self.end_position = start_position + 40

class Obstruction:
    def __init__(self, pos, track):
        self.pos = pos
        self.track = track

class Page:
    def __init__(self):
        self.track_count = 8
        self.changes = []
        self.obstructions = []
        
        for i in range(5):
            t = random.randrange(0, 8)
            c = random.choice([-1, 1])
            if t == 0: c = 1
            if t == 7: c = -1
            e = t + c
            p = random.randrange(40, 120)
            self.changes.append(TrackChange(t, e, p))
            
            if random.choice([False, False, False, True]):self.obstructions.append(Obstruction(p+40, t))

    def track_y(self, i):
        if i < self.track_count: return 30+i*14

    def change_y(self, i, pos):
        change = self.changes[i]

        start_y = self.track_y(change.from_track)
        end_y   = self.track_y(change.to_track)

        start_x = change.start_position
        end_x   = change.end_position

        if pos < start_x: return start_y
        if pos > end_x: return end_y
        diff = end_x - start_x
        loc = end_x - pos
        scale = loc / diff
        return end_y + (start_y - end_y) * scale
        
    
    def draw(self, surface):
        for i in range(self.track_count):
            y = self.track_y(i)
            pygame.draw.line(surface, DARK, (0, y), (160, y))
        
        for change in self.changes:
            start = (
                    change.start_position,
                    self.track_y(change.from_track)
                )
            end = (
                    change.end_position,
                    self.track_y(change.to_track)
                )
            pygame.draw.line(surface, DARK, start, end)

    def draw_obstructions(self, surface):
        for obstruction in self.obstructions:
            pygame.draw.ellipse(surface, LIGHT, (obstruction.pos, 2+self.track_y(obstruction.track)-10, 10, 10))

    def crosses_change(self, x, prev_x, track):
        for i, change in enumerate(self.changes):
            if track == change.from_track:
                if change.start_position <= x and change.start_position > prev_x:
                    return i + self.track_count
        return -1

    def returns_change(self, x, prev_x, track):
        change_track = track - self.track_count
        if change_track < 0: return -1
        for i, change in enumerate(self.changes):
            if i == change_track:
                if prev_x > change.end_position:
                    return change.to_track
        return -1

    def hits_obstruction(self, x, prev_x, track):
        for obstruction in self.obstructions:
            if track != obstruction.track: continue
            if obstruction.pos <= x and obstruction.pos > prev_x:
                return True
        return False

    def draw_train(self, canvas, position, track, cart_height):

        if track >= self.track_count:
            track -= self.track_count
            pygame.draw.rect(canvas, BRIGHT, (position- 6, self.change_y(track, position)-6, 10, 6))
            pygame.draw.rect(canvas, BRIGHT, (position-18, self.change_y(track, position-6)-cart_height, 10, cart_height))
        else:
            pygame.draw.rect(canvas, BRIGHT, (position- 6, self.track_y(track)-6, 10, 6))
            pygame.draw.rect(canvas, BRIGHT, (position-18, self.track_y(track)-cart_height, 10, cart_height))

    

def main():
    player = Train()
    clock = pygame.time.Clock()
    canvas = pygame.surface.Surface((160, 160))
    page = Page()
    time = 0
    change = -2000

    pygame.font.init() # you have to call this at the start, 
                       # if you want to use this module.
    my_font = pygame.font.SysFont('Comic Sans MS', 12)
    
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and change + 750 < time:
                    change = time + 500
                if event.key == pygame.K_x:
                    player.activate_boost(time)
                
        
        canvas.fill(BLACK)
        
        dt = clock.tick(60)
        time += dt
        player.tick(dt, time)
        
        prev_pos = player.position - player.speed*4
        now_pos  = player.position

        if change > time:
            new_track = page.crosses_change(now_pos, prev_pos, player.track)
            if new_track != -1:
                player.track = new_track

        r = page.returns_change(now_pos, prev_pos, player.track)
        if r != -1:
            player.track = r

        if page.hits_obstruction(now_pos, prev_pos, player.track):
            player.speed *= 0.2
        
            

        page.draw(canvas)
        page.draw_train(canvas, player.position, player.track, player.cart_height())
        page.draw_obstructions(canvas)

        control_colour = DARK

        if change > time:
            control_colour = LIGHT
        elif change + 1000 > time:
            control_colour = BLACK


        pygame.draw.ellipse(canvas, control_colour, (20, 140, 15, 15))

        control_colour = DARK
        if player.boost: control_colour = LIGHT

        pygame.draw.ellipse(canvas, control_colour, (40, 140, 15, 15))

        z_text = my_font.render('Z', False, BRIGHT)
        x_text = my_font.render('X', False, BRIGHT)

        canvas.blit(z_text, (23, 138))
        canvas.blit(x_text, (43, 138))
        
        speed_text = my_font.render(f"{str(round(player.speed*35, 0))[:-2]} MPH", False, BRIGHT)
        canvas.blit(speed_text, (83, 138))


        # End of fuel carriage goes offscreen
        # Wrap the play position back on screen
        if player.position-18 > 160:
            player.position = -6
            page = Page()


        win.blit(pygame.transform.scale(canvas, win.get_rect().size), (0,0))

        pygame.display.update()

if __name__=="__main__":
    main()
