import pygame
import pygame_gui
import os

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Performaxx")

# --- Colors (Matcha × Labubu palette) ---
MATCHA = (168, 198, 134)
CREAM = (246, 244, 238)
INK = (44, 44, 44)
PEACH = (247, 198, 163)
DARK_MATCHA = (107, 122, 87)
LIGHT_MATCHA = (192, 214, 163)

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# --- Layout rectangles ---
left_panel = pygame.Rect(40, 80, 250, 460)
right_panel = pygame.Rect(WIDTH - 290, 80, 250, 460)
image_rect = pygame.Rect(370, 120, 460, 280)

# --- State ---
user_image = None
user_image_pos = None
ai_image_path = "improved_image.png"

# --- Fonts ---
pygame.font.init()
font = pygame.font.SysFont("Poppins", 22, bold=True)
small_font = pygame.font.SysFont("Poppins", 18)

# --- Buttons ---
# --- UIButton Style ---
# --- UIButton Theme Setup (Dark Green Flat Button) ---
theme_data = {
    "button": {
        "colours": {
            "normal_bg": "#4B6043",      # dark matcha green
            "hovered_bg": "#5E7255",     # lighter on hover
            "active_bg": "#3C4F36",      # darker when clicked
            "normal_text": "#F6F4EE"     # creamy white text
        },
        "misc": {
            "border_width": "0",
            "shape": "rectangle",
            "shadow_width": "0"
        }
    }
}

manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_data)

improve_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((520, 430), (180, 50)),
    text='Improve',
    manager=manager
)


file_dialog = None
clock = pygame.time.Clock()
running = True


def load_image(path):
    """Load and scale image to fit inside image_rect while preserving aspect ratio."""
    try:
        img = pygame.image.load(path).convert_alpha()
        iw, ih = img.get_size()
        rw, rh = image_rect.size

        scale = min(rw / iw, rh / ih)
        new_size = (int(iw * scale), int(ih * scale))
        img = pygame.transform.smoothscale(img, new_size)

        offset_x = image_rect.x + (rw - new_size[0]) // 2
        offset_y = image_rect.y + (rh - new_size[1]) // 2
        return img, (offset_x, offset_y)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None


def open_file_dialog():
    """Open file dialog window for selecting an image."""
    return pygame_gui.windows.UIFileDialog(
        rect=pygame.Rect((350, 80), (500, 400)),
        manager=manager,
        window_title='Select Image'
    )


def draw_rounded_panel(rect, title, color_bg=CREAM):
    """Draws a soft rounded panel with a title and light shadow."""
    shadow_rect = rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, DARK_MATCHA, shadow_rect, border_radius=16)
    pygame.draw.rect(screen, color_bg, rect, border_radius=16)
    pygame.draw.rect(screen, DARK_MATCHA, rect, 2, border_radius=16)
    title_text = font.render(title, True, DARK_MATCHA)
    screen.blit(title_text, (rect.x + 5, rect.y - 30))


shopping_items = []
chat_history = []


def draw_button(rect, text, color_bg=PEACH, text_color=CREAM):
    """Draws a simple rounded button with centered text."""
    pygame.draw.rect(screen, color_bg, rect, border_radius=12)
    text_render = small_font.render(text, True, text_color)
    screen.blit(text_render, text_render.get_rect(center=rect.center))


while running:
    time_delta = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                chosen = event.text
                user_image, user_image_pos = load_image(chosen)
                if file_dialog:
                    file_dialog.kill()
                    file_dialog = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if image_rect.collidepoint(event.pos):
                if not file_dialog:
                    file_dialog = open_file_dialog()

        manager.process_events(event)

    manager.update(time_delta)

    # --- Background ---
    screen.fill(MATCHA)

    # Panels
    draw_rounded_panel(left_panel, "Shopping List")
    draw_rounded_panel(right_panel, "Consult Performaxx")

    # Draw shopping list
    for i, item in enumerate(shopping_items):
        text = small_font.render(f"- {item}", True, INK)
        screen.blit(text, (left_panel.x + 15, left_panel.y + 20 + i * 30))

    # Draw chatbox placeholder
    pygame.draw.rect(screen, CREAM, (right_panel.x + 10, right_panel.y + 40, 230, 200), border_radius=12)

    # --- Image area ---
    pygame.draw.rect(screen, CREAM, image_rect, border_radius=16)
    pygame.draw.rect(screen, DARK_MATCHA, image_rect, 2, border_radius=16)
    if user_image:
        screen.blit(user_image, user_image_pos)
    else:
        placeholder = font.render("Click to upload image", True, (70, 90, 60))
        screen.blit(placeholder, placeholder.get_rect(center=image_rect.center))

    # --- Music wave (placeholder) ---
    pygame.draw.rect(screen, LIGHT_MATCHA, (500, 500, 220, 20), border_radius=8)
    pygame.draw.line(screen, DARK_MATCHA, (510, 510), (710, 510), 2)

    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
