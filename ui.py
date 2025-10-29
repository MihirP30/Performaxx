import pygame
import pygame_gui
import os
import threading
import queue
# Import the custom wrapper function
from performative_chat_wrapper import get_performative_response
# Import API Key used in the wrapper (or set it here if you prefer)
# NOTE: The provided key is used directly in the wrapper function call in this file.
GEMINI_API_KEY = "AIzaSyAaXqJNqCAI1Bee3vJgqUt0ah4FktPEwG8" 

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

# Initialize UIManager with a custom theme
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
    },
    # Style the chat input box
    "text_entry_line": {
        "colours": {
            "normal_bg": "#FFFFFF",
            "normal_border": "#A8C686",
            "text": "#2C2C2C"
        },
        "misc": {
            "border_width": "1"
        }
    },
    # Style the chat log text box
    "text_box": {
        "colours": {
            "normal_bg": "#FFFFFF",
            "normal_border": "#A8C686",
            "text": "#2C2C2C"
        },
        "misc": {
            "border_width": "1"
        }
    }
}

manager = pygame_gui.UIManager((WIDTH, HEIGHT), os.path.join(os.getcwd(), 'theme.json') if os.path.exists('theme.json') else theme_data)


# --- Layout rectangles ---
left_panel = pygame.Rect(40, 80, 250, 460)
right_panel = pygame.Rect(WIDTH - 290, 80, 250, 460)
image_rect = pygame.Rect(370, 120, 460, 280)

# --- Chat Rectangles (Inside right_panel) ---
chat_log_rect = pygame.Rect(right_panel.x + 10, right_panel.y + 40, 230, 300)
chat_input_rect = pygame.Rect(right_panel.x + 10, chat_log_rect.bottom + 10, 230, 30)
chat_send_rect = pygame.Rect(right_panel.x + 10, chat_input_rect.bottom + 5, 230, 40)

# --- Chat GUI Elements ---
chat_log = pygame_gui.elements.UITextBox(
    html_text="<b>Vibe Guide:</b> Hello! Ask me about male aesthetic trends.",
    relative_rect=chat_log_rect,
    manager=manager,
    wrap_to_height=True
)

chat_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=chat_input_rect,
    manager=manager,
    placeholder_text="Enter performative query..."
)

chat_send_button = pygame_gui.elements.UIButton(
    relative_rect=chat_send_rect,
    text='VibeCheck!',
    manager=manager,
    object_id='#chat_send_button'
)

# --- State ---
user_image = None
user_image_pos = None
ai_image_path = "improved_image.png"
chat_history = []
ai_response_queue = queue.Queue() # Queue for thread-safe communication
is_ai_thinking = False

# --- Pygame Setup ---
pygame.font.init()
font = pygame.font.SysFont("Poppins", 22, bold=True)
small_font = pygame.font.SysFont("Poppins", 18)

# --- Buttons ---
improve_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((520, 430), (180, 50)),
    text='Improve Image',
    manager=manager
)


file_dialog = None
clock = pygame.time.Clock()
running = True

# --- Async Functionality ---
def run_ai_in_thread(prompt):
    """Worker function to call the Gemini API in a separate thread."""
    global is_ai_thinking
    is_ai_thinking = True
    try:
        response = get_performative_response(prompt, GEMINI_API_KEY)
        ai_response_queue.put(response)
    except Exception as e:
        ai_response_queue.put(f"⚠️ Thread Error: {e}")
    finally:
        is_ai_thinking = False

def send_chat_message(user_prompt):
    """Starts a new thread for the AI response."""
    global is_ai_thinking
    if not is_ai_thinking:
        # Append user message to log
        new_log = f"<br><b>You:</b> {user_prompt}"
        chat_log.append_html_text(new_log)

        # Clear input field
        chat_input.set_text("")

        # Disable input/send button while waiting
        chat_input.disable()
        chat_send_button.disable()

        # Start the background thread
        threading.Thread(target=run_ai_in_thread, args=(user_prompt,), daemon=True).start()
    else:
        chat_log.append_html_text("<br><i>Please wait for the Vibe Guide to finish its current thought.</i>")

# --- Drawing Functions ---
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


while running:
    time_delta = clock.tick(60) / 1000

    # --- Check for AI Response ---
    try:
        # Check the queue without blocking
        ai_response = ai_response_queue.get_nowait()
        
        # Append AI response to log
        new_log = f"<br><br><b>Vibe Guide:</b> {ai_response}"
        chat_log.append_html_text(new_log)
        chat_log.rebuild() # Force text box update

        # Re-enable input/send button
        chat_input.enable()
        chat_send_button.enable()
        
    except queue.Empty:
        pass # No response yet

    # --- Event Handling ---
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
            
            # Handle Chat Send Button Press
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == chat_send_button:
                    user_prompt = chat_input.get_text()
                    if user_prompt:
                        send_chat_message(user_prompt)

            # Handle Enter key press in the chat input field
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == chat_input:
                    user_prompt = chat_input.get_text()
                    if user_prompt:
                        send_chat_message(user_prompt)

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

    # --- Image area ---
    pygame.draw.rect(screen, CREAM, image_rect, border_radius=16)
    pygame.draw.rect(screen, DARK_MATCHA, image_rect, 2, border_radius=16)
    if user_image:
        screen.blit(user_image, user_image_pos)
    else:
        placeholder = font.render("Click to upload image", True, (70, 90, 60))
        screen.blit(placeholder, placeholder.get_rect(center=image_rect.center))
        
    # --- Score/Improvement Placeholder ---
    score_placeholder = font.render("Aesthetic Score: N/A", True, DARK_MATCHA)
    screen.blit(score_placeholder, (image_rect.x, image_rect.bottom + 10))

    # --- Music wave (placeholder) ---
    pygame.draw.rect(screen, LIGHT_MATCHA, (500, 500, 220, 20), border_radius=8)
    pygame.draw.line(screen, DARK_MATCHA, (510, 510), (710, 510), 2)
    music_text = small_font.render("🎧 Vibe Match Track", True, INK)
    screen.blit(music_text, (530, 525))
    
    # AI Thinking Indicator
    if is_ai_thinking:
        thinking_text = small_font.render("Vibe Guide is thinking...", True, (255, 0, 0))
        screen.blit(thinking_text, (chat_log_rect.x, chat_log_rect.bottom + 5))
    
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
