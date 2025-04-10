class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pygame.Surface((32, 32)),
            pygame.Surface((32, 32)),
            pygame.Surface((32, 32))
        ]
        # Заполняем кадры анимации
        self.frames[0].fill((255, 0, 0))
        self.frames[1].fill((200, 0, 0))
        self.frames[2].fill((150, 0, 0))
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_speed = 0.1
        self.frame_counter = 0
        
    def update(self):
        # Анимация
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed * 60:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        
        # Движение
        self.rect.x -= 2
