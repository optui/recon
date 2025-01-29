# views/factory.py
from views import MenuView, CreatorView, EditorView

def create_views(controller):
    """Create and return a dictionary of views by name."""
    views = {
        "menu": MenuView(controller),
        "simulation": CreatorView(controller, show=True),
        "editor": EditorView(controller, show=False)
    }
    return views
