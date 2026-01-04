try:
    import screen_brightness_control as sbc
    import pyautogui
    SKILLS_AVAILABLE = True
except (ImportError, KeyError, OSError):
    # KeyError: 'DISPLAY' handled here for headless environments
    SKILLS_AVAILABLE = False
    print("Warning: System control skills unavailable (Headless/No Display detected).")

import math

class SystemSkills:
    @staticmethod
    def _check_availability():
        if not SKILLS_AVAILABLE:
            return False, "I cannot control this system (Headless environment detected)."
        return True, ""

    @staticmethod
    def set_volume(level: int):
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            for _ in range(50):
                pyautogui.press("volumedown")
            
            clicks = int(level / 2) 
            for _ in range(clicks):
                pyautogui.press("volumeup")
                
            return f"Volume adjusted to approx {level}%."
        except Exception as e:
            return f"Error setting volume: {str(e)}"

    @staticmethod
    def mute_volume():
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            pyautogui.press("volumemute")
            return "Volume muted/unmuted."
        except Exception as e:
            return f"Error muting volume: {str(e)}"

    @staticmethod
    def set_brightness(level: int):
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%."
        except Exception as e:
            return f"Error setting brightness: {str(e)}"

    @staticmethod
    def take_screenshot():
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            import os
            from datetime import datetime
            
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}."
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    @staticmethod
    def lock_pc():
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Locking PC."
        except Exception as e:
            return f"Error locking PC: {str(e)}"

    @staticmethod
    def shutdown_pc():
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        return "I can request a shutdown, but for safety, please confirm manually. (Command: shutdown /s /t 5)"

    @staticmethod
    def minimize_all():
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            pyautogui.hotkey('win', 'd')
            return "Minimized all windows."
        except Exception as e:
            return f"Error minimizing windows: {str(e)}"

    @staticmethod
    def type_text(text: str):
        available, msg = SystemSkills._check_availability()
        if not available: return msg

        try:
            pyautogui.write(text, interval=0.05)
            return f"Typed: {text}"
        except Exception as e:
            return f"Error typing text: {str(e)}"
