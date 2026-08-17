import os

def detect_environment():
    if os.path.exists("/data/data/com.termux"):
        return "development"
    elif os.path.exists("/system/app"):
        return "production"
    else:
        return "unknown"

def setup_display():
    env = detect_environment()
    if env == "development":
        os.environ["SDL_VIDEODRIVER"] = "x11"
        os.environ["SDL_RENDER_DRIVER"] = "software"
        if not os.environ.get("DISPLAY"):
            os.environ["DISPLAY"] = ":1"
    return env
