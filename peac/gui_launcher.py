#!/usr/bin/env python3
"""
PEaC GUI Launcher
Launches the GUI directly without CLI interface
"""

if __name__ == "__main__":
    from peac.gui_ctk.main_app import PeacApp
    app = PeacApp()
    app.mainloop()
