import screen_brightness_control as sbc
import pyautogui
import math

class SystemSkills:
    @staticmethod
    def set_volume(level: int):
        # PyAutoGUI can't set exact percentage easily without external tools, 
        # so we will just support mute/unmute or standard key presses.
        # For this requirement, we will try to approximate or just inform the user.
        # Better approach: Use nircmd (if available) or just stick to key presses.
        # For now, let's use the keyboard keys to change volume relatively.
        
        # To strictly "set" volume, we would need pycaw. Since pycaw failed, 
        # let's fallback to telling the user or using a simple loop of presses.
        # A simple hack: Press volume down 50 times (mute), then up N times.
        try:
            for _ in range(50):
                pyautogui.press("volumedown")
            
            # Approx: 2 steps per press usually, strictly imprecise but working.
            clicks = int(level / 2) 
            for _ in range(clicks):
                pyautogui.press("volumeup")
                
            return f"Volume adjusted to approx {level}%."
        except Exception as e:
            return f"Error setting volume: {str(e)}"

    @staticmethod
    def mute_volume():
        try:
            pyautogui.press("volumemute")
            return "Volume muted/unmuted."
        except Exception as e:
            return f"Error muting volume: {str(e)}"

    @staticmethod
    def set_brightness(level: int):
        try:
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%."
        except Exception as e:
            return f"Error setting brightness: {str(e)}"

    @staticmethod
    def take_screenshot():
        try:
            # Save to user's Pictures folder or current dir
            import os
            from datetime import datetime
            
            # Simple timestamped filename
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}."
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    @staticmethod
    def lock_pc():
        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Locking PC."
        except Exception as e:
            return f"Error locking PC: {str(e)}"

    @staticmethod
    def shutdown_pc():
        # Warning: This shuts down immediately
        # os.system("shutdown /s /t 5")
        return "I can request a shutdown, but for safety, please confirm manually. (Command: shutdown /s /t 5)"

    @staticmethod
    def minimize_all():
        try:
            pyautogui.hotkey('win', 'd')
            return "Minimized all windows."
        except Exception as e:
            return f"Error minimizing windows: {str(e)}"

    @staticmethod
    def type_text(text: str):
        try:
            pyautogui.write(text, interval=0.05)
            return f"Typed: {text}"
        except Exception as e:
            return f"Error typing text: {str(e)}"
