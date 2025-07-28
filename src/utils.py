import json
import os

def load_settings(config_path='config/settings.json'):
    """Loads settings from a JSON configuration file."""
    script_dir = os.path.dirname(__file__)
    abs_config_path = os.path.join(script_dir, '..', config_path)
    try:
        with open(abs_config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {abs_config_path}. Please ensure it exists.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in config file at {abs_config_path}.")
        exit(1)

SETTINGS = load_settings()

def is_bold(span):
    """Checks if a span's font is likely bold."""
    font_name = span['font'].lower()
    return 'bold' in font_name or 'black' in font_name or 'heavy' in font_name

def is_italic(span):
    """Checks if a span's font is likely italic."""
    font_name = span['font'].lower()
    return 'italic' in font_name or 'oblique' in font_name