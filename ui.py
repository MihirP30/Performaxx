import pygame
import pygame_gui
import os
from scanner import analyze_image, generate_more_performative_image, AI_IMAGE_OUTPUT_PATH
from music import play_song
from gemini_wrapper import GeminiClientWrapper

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Performaxx")

# --- Colors ---
MATCHA = (168, 198, 134)
CREAM = (246, 244, 238)
INK = (44, 44, 44)
PEACH = (247, 198, 163)
DARK_MATCHA = (107, 122, 87)
LIGHT_MATCHA = (192, 214, 163)

# --- UI Theme ---
theme_data = {
    "button": {
        "colours": {
            "normal_bg": "#4B6043",
            "hovered_bg": "#5E7255",
            "active_bg": "#3C4F36",
            "normal_text": "#F6F4EE"
        },
        "misc": {"border_width": "0", "shape": "rectangle", "shadow_width": "0"}
    }
}
manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_data)

# --- Layout ---
left_panel = pygame.Rect(40, 80, 250, 460)
right_panel = pygame.Rect(WIDTH - 290, 80, 250, 460)
image_rect = pygame.Rect(370, 120, 460, 280)

# --- Fonts ---
pygame.font.init()
font = pygame.font.SysFont("Poppins", 22, bold=True)
small_font = pygame.font.SysFont("Poppins", 18)

# --- Buttons ---
improve_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((520, 430), (180, 50)),
    text='Improve',
    manager=manager
)

gemini_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((WIDTH - 280, 490), (180, 35)),
    manager=manager
)

gemini_send_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 90, 490), (50, 35)),
    text='→',
    manager=manager
)

# --- State ---
file_dialog = None
clock = pygame.time.Clock()
running = True
user_image = None
user_image_pos = None
current_image_path = None
shopping_items = []
chat_history = []

# --- Gemini Setup ---
gemini = GeminiClientWrapper()

# --- Sample Performative Items ---
performative_items = {
    "matcha": {"name": "Otsuka Green Tea Co Shizuoka Matcha Powder", "price": 13.00},
    "labubu": {"name": "POP MART Kasing Labubu The Monsters Exciting Macarons Figure", "price": 37.99},
    "feminine_literature": {"name": "Pride and Prejudice", "price": 6.99},
    "flannel": {"name": "Legendary Whitetails Men's Flannel Cedarwood Plaid Shirt", "price": 58.09},
    "baggy_jeans": {"name": "Baggy Skater Vintage Casual Jeans", "price": 25.00},
    "tote_bag": {"name": "Tote Bag", "price": 17.99},
    "wired_headphones": {"name": "Apple Wired Headphones", "price": 19.99},
    "vintage_clothing": {"name": "Thrifted Vintage Clothing", "price": 0.00},
    "rings": {"name": "Rings", "price": 13.99}
}


# -------------------- Utility Functions --------------------

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
    """Draw a soft rounded panel with a title."""
    shadow_rect = rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, DARK_MATCHA, shadow_rect, border_radius=16)
    pygame.draw.rect(screen, color_bg, rect, border_radius=16)
    pygame.draw.rect(screen, DARK_MATCHA, rect, 2, border_radius=16)
    title_text = font.render(title, True, DARK_MATCHA)
    screen.blit(title_text, (rect.x + 5, rect.y - 30))


def handle_improve_action():
    """Called when 'Improve' is pressed."""
    global current_image_path, user_image, user_image_pos, shopping_items

    if not current_image_path:
        print("System: Please upload an image first.")
        return

    print("System: Starting image analysis (Step 1/2)...")
    pil_image, analysis_result_text, shopping_list = analyze_image(current_image_path)

    if shopping_list and isinstance(shopping_list, list):
        shopping_items = shopping_list

    print("System: Starting image generation (Step 2/2)...")
    if generate_more_performative_image(current_image_path):
        img, pos = load_image(AI_IMAGE_OUTPUT_PATH)
        if img is not None:
            user_image = img
            user_image_pos = pos
            current_image_path = AI_IMAGE_OUTPUT_PATH
            play_song()
        else:
            print("System: Failed to load generated image.")


# -------------------- Main Loop --------------------

while running:
    time_delta = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == improve_btn:
                    handle_improve_action()

                elif event.ui_element == gemini_send_btn:
                    prompt = gemini_input.get_text().strip()
                    if prompt:
                        full_prompt = f"{prompt}\n\nKeep your response less than 15 words."
                        try:
                            response = gemini.generate_text(full_prompt)
                            chat_history.append((prompt, response))
                            print(f"You: {prompt}")
                            print(f"Gemini: {response}")
                        except Exception as e:
                            print(f"Gemini Error: {e}")
                        gemini_input.set_text("")

            elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                chosen_path = event.text
                img, pos = load_image(chosen_path)
                if img is not None:
                    user_image = img
                    user_image_pos = pos
                    current_image_path = chosen_path
                    print("System: Image loaded.")
                if file_dialog:
                    file_dialog.kill()
                    file_dialog = None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if image_rect.collidepoint(event.pos):
                if not file_dialog:
                    file_dialog = open_file_dialog()

        manager.process_events(event)

    manager.update(time_delta)

    # --- Drawing ---
    screen.fill(MATCHA)

    draw_rounded_panel(left_panel, "Shopping List")
    draw_rounded_panel(right_panel, "Consult Performaxx")

    # --- Shopping List ---
    for i in range(len(shopping_items)):
        item_name = shopping_items[i]['name']
        item_price = shopping_items[i]['price']
        if len(item_name) > 28:
            item_name = item_name[:25] + "..."
        text = small_font.render(f"• {item_name} - ${item_price}", True, INK)
        screen.blit(text, (left_panel.x + 10, left_panel.y + 20 + i * 30))

    # --- Image Display ---
    pygame.draw.rect(screen, CREAM, image_rect, border_radius=16)
    pygame.draw.rect(screen, DARK_MATCHA, image_rect, 2, border_radius=16)
    if user_image and user_image_pos:
        screen.blit(user_image, user_image_pos)
    else:
        placeholder = font.render("Click to upload image", True, (70, 90, 60))
        screen.blit(placeholder, placeholder.get_rect(center=image_rect.center))

    # --- Gemini Chat Log ---
    y_offset = right_panel.y + 20
    visible_chats = chat_history[-7:]
    for user_msg, ai_msg in visible_chats:
        user_text = small_font.render(f"You: {user_msg}", True, INK)
        ai_text = small_font.render(f"AI: {ai_msg}", True, DARK_MATCHA)
        screen.blit(user_text, (right_panel.x + 10, y_offset))
        y_offset += 25
        screen.blit(ai_text, (right_panel.x + 10, y_offset))
        y_offset += 40

    # --- Music Wave Placeholder ---
    pygame.draw.rect(screen, DARK_MATCHA, (500, 500, 220, 20), border_radius=8)

    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()