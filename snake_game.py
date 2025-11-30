"""
Nokia Snake Game Implementation
Classic snake game with Nokia-style graphics
"""
import pygame
import random
from collections import deque

class SnakeGame:
    def __init__(self, width=400, height=400):
        pygame.init()
        
        # Game settings
        self.width = width
        self.height = height
        self.grid_size = 20
        self.grid_width = width // self.grid_size
        self.grid_height = height // self.grid_size
        
        # Colors (Nokia style)
        self.NOKIA_GREEN = (155, 188, 15)
        self.LIGHT_GREEN = (204, 255, 51)
        self.DARK_GREEN = (48, 98, 48)
        self.BLACK = (0, 0, 0)
        
        # Display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Nokia Snake - Gesture Control')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.reset_game()
        
        # Speed settings
        self.base_speed = 8
        self.boost_speed = 15
        self.current_speed = self.base_speed
        
    def reset_game(self):
        """Reset game to initial state"""
        # Snake
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = deque([(start_x, start_y)])
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        
        # Fruit
        self.fruit = self.spawn_fruit()
        
        # Score
        self.score = 0
        self.game_over = False
        
        # Particles for effects
        self.particles = []
    
    def spawn_fruit(self):
        """Spawn fruit at random position not occupied by snake"""
        while True:
            fruit = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if fruit not in self.snake:
                return fruit
    
    def create_particles(self, x, y):
        """Create particle effect when eating fruit"""
        for _ in range(10):
            self.particles.append({
                'x': x * self.grid_size + self.grid_size // 2,
                'y': y * self.grid_size + self.grid_size // 2,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 20
            })
    
    def update_particles(self):
        """Update particle positions and lifetimes"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def handle_input(self, gesture=None, boost=False):
        """Handle keyboard and gesture input"""
        # Keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        
        # Gesture input
        if gesture:
            if gesture == 'UP' and self.direction != 'DOWN':
                self.next_direction = 'UP'
            elif gesture == 'DOWN' and self.direction != 'UP':
                self.next_direction = 'DOWN'
            elif gesture == 'LEFT' and self.direction != 'RIGHT':
                self.next_direction = 'LEFT'
            elif gesture == 'RIGHT' and self.direction != 'LEFT':
                self.next_direction = 'RIGHT'
        
        # Speed boost
        self.current_speed = self.boost_speed if boost else self.base_speed
        
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1
        
        new_head = (head_x, head_y)
        
        # Check wall collision
        if (head_x < 0 or head_x >= self.grid_width or 
            head_y < 0 or head_y >= self.grid_height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check fruit collision
        if new_head == self.fruit:
            self.score += 10
            self.create_particles(self.fruit[0], self.fruit[1])
            self.fruit = self.spawn_fruit()
        else:
            # Remove tail if not eating
            self.snake.pop()
        
        # Update particles
        self.update_particles()
    
    def draw(self):
        """Draw game elements"""
        # Background
        self.screen.fill(self.DARK_GREEN)
        
        # Draw grid
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, self.BLACK, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, self.BLACK, (0, y), (self.width, y), 1)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = self.LIGHT_GREEN if i == 0 else self.NOKIA_GREEN
            rect = pygame.Rect(
                x * self.grid_size + 1,
                y * self.grid_size + 1,
                self.grid_size - 2,
                self.grid_size - 2
            )
            pygame.draw.rect(self.screen, color, rect)
            
            # Draw eyes on head
            if i == 0:
                eye_size = 3
                if self.direction == 'RIGHT':
                    eye1 = (x * self.grid_size + 12, y * self.grid_size + 6)
                    eye2 = (x * self.grid_size + 12, y * self.grid_size + 14)
                elif self.direction == 'LEFT':
                    eye1 = (x * self.grid_size + 8, y * self.grid_size + 6)
                    eye2 = (x * self.grid_size + 8, y * self.grid_size + 14)
                elif self.direction == 'UP':
                    eye1 = (x * self.grid_size + 6, y * self.grid_size + 8)
                    eye2 = (x * self.grid_size + 14, y * self.grid_size + 8)
                else:  # DOWN
                    eye1 = (x * self.grid_size + 6, y * self.grid_size + 12)
                    eye2 = (x * self.grid_size + 14, y * self.grid_size + 12)
                
                pygame.draw.circle(self.screen, self.BLACK, eye1, eye_size)
                pygame.draw.circle(self.screen, self.BLACK, eye2, eye_size)
        
        # Draw fruit
        fruit_rect = pygame.Rect(
            self.fruit[0] * self.grid_size + 2,
            self.fruit[1] * self.grid_size + 2,
            self.grid_size - 4,
            self.grid_size - 4
        )
        pygame.draw.ellipse(self.screen, (255, 0, 0), fruit_rect)
        
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 20))
            color = (255, 255, 0, alpha)
            pygame.draw.circle(self.screen, color[:3], 
                             (int(particle['x']), int(particle['y'])), 3)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, self.LIGHT_GREEN)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, (255, 0, 0))
            restart_text = self.small_font.render('Show UP gesture to restart', True, self.LIGHT_GREEN)
            
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run_frame(self, gesture=None, boost=False):
        """Run one game frame"""
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        # Handle input
        if not self.handle_input(gesture, boost):
            return False
        
        # Restart on UP gesture when game over
        if self.game_over and gesture == 'UP':
            self.reset_game()
        
        # Update game
        if not self.game_over:
            self.update()
        
        # Draw
        self.draw()
        
        # Control frame rate
        self.clock.tick(self.current_speed)
        
        return True
    
    def quit(self):
        """Clean up pygame"""
        pygame.quit()