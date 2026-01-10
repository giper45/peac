from __future__ import annotations
import flet as ft
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import traceback
import os

from peac.gui.ui.components import section_header
from peac.gui.ui.rule_card import RuleCard
from peac.gui.services.yaml_service import YamlService
from peac.gui.services.prompt_service import PromptService
from peac.gui.services.config_service import GuiConfig
from peac.gui.services.path_resolver_service import PathResolverService
from peac.gui.services.rule_parsing_service import RuleParsingService
from peac.gui.services.file_service import FileService
from peac.gui.models.rule import RuleData


class ExtendsCard:
    """Represents a single extends card with its data - simplified per EBNF spec"""
    def __init__(self, source: str = "", on_change=None):
        self.on_change = on_change
        
        self.source_field = ft.TextField(
            label="Source",
            value=source,
            hint_text="Relative path to YAML file (e.g., ../base.yaml)",
            expand=True,
            on_change=lambda _: self.on_change() if self.on_change else None,
            border_color="#1877f2",
        )
        
        self.container = None
    
    def get_data(self) -> Optional[str]:
        """Get extends data from the card - returns just the source path string per EBNF"""
        source = self.source_field.value.strip() if self.source_field.value else ""
        if not source:
            return None
        return source
    
    def load_data(self, extends_data):
        """Load data into the extends card"""
        if isinstance(extends_data, str):
            # Simple string format (standard EBNF)
            self.source_field.value = extends_data
        elif isinstance(extends_data, dict):
            # Legacy object format - extract source only
            self.source_field.value = extends_data.get('source', '')
        else:
            self.source_field.value = ""


class FileTab:
    """Represents a single file tab with its own state"""
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.yaml_data: Dict[str, Any] = {"prompt": {"query": ""}}
        self.unsaved_changes = False
        
        # UI elements for this file
        self.query_input: Optional[ft.TextField] = None
        self.instruction_base: Optional[ft.TextField] = None
        self.instruction_additional: Optional[ft.TextField] = None
        self.context_base: Optional[ft.TextField] = None
        self.output_base: Optional[ft.TextField] = None
        self.yaml_editor: Optional[ft.TextField] = None
        
        # rule lists
        self.context_local_rules: List[RuleCard] = []
        self.context_web_rules: List[RuleCard] = []
        self.context_rag_rules: List[RuleCard] = []
        self.output_local_rules: List[RuleCard] = []
        self.output_web_rules: List[RuleCard] = []
        self.output_rag_rules: List[RuleCard] = []
        
        # containers
        self.context_local_container: Optional[ft.Column] = None
        self.context_web_container: Optional[ft.Column] = None
        self.context_rag_container: Optional[ft.Column] = None
        self.output_local_container: Optional[ft.Column] = None
        self.output_web_container: Optional[ft.Column] = None
        self.output_rag_container: Optional[ft.Column] = None
        
        # extends
        self.extends_container: Optional[ft.Column] = None
        self.extends_cards: List = []
        
        self.content: Optional[ft.Tab] = None
    
    def get_display_name(self) -> str:
        """Get the display name for the tab"""
        if not self.file_path:
            return "Untitled*" if self.unsaved_changes else "Untitled"
        name = Path(self.file_path).name
        return f"{name}*" if self.unsaved_changes else name


class PeacFletApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()

        # Configuration service
        self.config = GuiConfig()

        # Multi-file management
        self.open_files: Dict[str, FileTab] = {}  # path -> FileTab
        self.current_tab: Optional[FileTab] = None
        self.file_tabs: Optional[ft.Tabs] = None

        # UI refs
        self.filename_label: Optional[ft.Text] = None
        self.status_text: Optional[ft.Text] = None
        self.toolbar: Optional[ft.Container] = None

        self._build_ui()
        
        # Restore open files from previous session, or create a new file if none
        if not self._restore_open_files():
            self.new_file()

    # ---------- setup ----------
    def _setup_page(self):
        self.page.title = "PEaC - Prompt Engineering as Code"
        self.page.window_width = 1600
        self.page.window_height = 1000
        self.page.window_min_width = 1200
        self.page.window_min_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20

        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#1877f2",
                secondary="#f0f2f5",
                surface="#ffffff",
                background="#f0f2f5",
            )
        )

    # ---------- UI build ----------
    def _build_ui(self):
        self.toolbar = self._create_toolbar()
        file_tabs_container = self._create_file_tabs_container()
        status = self._create_status_bar()

        self.page.add(ft.Column([self.toolbar, file_tabs_container, status], expand=True, spacing=10))

    def _create_file_tabs_container(self):
        """Create container with file tabs"""
        self.file_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            on_change=lambda _: self._on_file_tab_changed(),
            tabs=[],  # Will be populated dynamically
            expand=True,
        )
        
        return ft.Container(
            content=self.file_tabs,
            expand=True,
        )
    
    def _add_file_tab(self, file_tab: FileTab):
        """Add a new file tab to the interface"""
        # If a tab for this file already exists, focus it instead of adding
        if file_tab.file_path and file_tab.file_path in self.open_files:
            existing = self.open_files[file_tab.file_path]
            if self.file_tabs and existing.content in self.file_tabs.tabs:
                self.file_tabs.selected_index = self.file_tabs.tabs.index(existing.content)
                self.current_tab = existing
                self.update_filename_display()
                self.page.update()
            return
        tab_content = self._create_file_content(file_tab)
        
        # Create tab with close button
        close_button = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_size=16,
            tooltip="Close tab",
            on_click=lambda _: self._close_file_tab(file_tab),
            icon_color=ft.colors.GREY_700,
        )
        
        tab_text = ft.Row(
            [
                ft.Icon(ft.icons.DESCRIPTION, size=16),
                ft.Text(file_tab.get_display_name(), size=14),
                close_button,
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        file_tab.content = ft.Tab(
            tab_content=tab_text,
            content=tab_content,
        )
        
        # Add to open files and tabs
        key = file_tab.file_path or f"untitled_{len(self.open_files)}"
        self.open_files[key] = file_tab
        self.file_tabs.tabs.append(file_tab.content)
        self.file_tabs.selected_index = len(self.file_tabs.tabs) - 1
        self.current_tab = file_tab
        
        # Load extends data from yaml (important for new files and existing files)
        self._load_extends_from_data(file_tab)
        
        # Save the updated list of open files
        self._save_open_files()
        
        self.page.update()
    
    def _on_file_tab_changed(self):
        """Handle tab change event"""
        if not self.file_tabs or self.file_tabs.selected_index < 0:
            return
        
        # Get the selected tab
        selected_tab = self.file_tabs.tabs[self.file_tabs.selected_index]
        
        # Find the corresponding FileTab from open_files
        for file_tab in self.open_files.values():
            if file_tab.content == selected_tab:
                self.current_tab = file_tab
                self.update_filename_display()
                break
        
        # Update the list of open files in config
        self._save_open_files()
    
    def _restore_open_files(self) -> bool:
        """Restore files from previous session. Returns True if files were restored."""
        files_to_open = self.config.get_open_files()
        if not files_to_open:
            return False
        
        opened_count = 0
        for filepath in files_to_open:
            try:
                self.load_file(filepath)
                opened_count += 1
            except Exception as e:
                print(f"[DEBUG] Failed to restore file {filepath}: {e}")
                continue
        
        if opened_count > 0:
            self.show_status(f"Restored {opened_count} file(s) from previous session", ft.colors.GREEN)
            return True
        return False
    
    def _save_open_files(self):
        """Save current open files to config"""
        open_files_list = list(self.open_files.keys())
        self.config.set_open_files(open_files_list)
    
    def _close_file_tab(self, file_tab: FileTab):
        """Close a specific file tab"""
        # Do not allow closing the last remaining tab
        if not self.file_tabs or len(self.file_tabs.tabs) <= 1:
            self.show_status("Cannot close the last tab", ft.colors.BLUE)
            return
        
        # Check for unsaved changes
        if file_tab.unsaved_changes:
            filename = Path(file_tab.file_path).name if file_tab.file_path else "Untitled"
            
            def handle_save_response(action: str):
                if action == "save":
                    # Set as current and save
                    self.current_tab = file_tab
                    self.save_file()
                    # After saving, close the tab
                    self._do_close_file_tab(file_tab)
                elif action == "discard":
                    # Close without saving
                    self._do_close_file_tab(file_tab)
                # If cancel, do nothing
            
            # Show dialog
            dlg = ft.AlertDialog(
                title=ft.Text(f"Unsaved Changes", size=18, weight=ft.FontWeight.BOLD),
                content=ft.Text(f"'{filename}' has unsaved changes. Do you want to save before closing?"),
                actions=[
                    ft.TextButton("Save", on_click=lambda _: (handle_save_response("save"), dlg.open and setattr(dlg, 'open', False), self.page.update())),
                    ft.TextButton("Discard", on_click=lambda _: (handle_save_response("discard"), dlg.open and setattr(dlg, 'open', False), self.page.update())),
                    ft.TextButton("Cancel", on_click=lambda _: (setattr(dlg, 'open', False), self.page.update())),
                ],
            )
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            return
        
        # No unsaved changes, close directly
        self._do_close_file_tab(file_tab)
    
    def _do_close_file_tab(self, file_tab: FileTab):
        """Actually close a file tab (after checking for unsaved changes)"""
        # Find the tab in the tabs list
        if file_tab.content in self.file_tabs.tabs:
            tab_index = self.file_tabs.tabs.index(file_tab.content)
            
            # Remove from tabs
            self.file_tabs.tabs.remove(file_tab.content)
            
            # Remove from open_files
            key_to_remove = None
            for k, v in self.open_files.items():
                if v is file_tab:
                    key_to_remove = k
                    break
            if key_to_remove is not None:
                del self.open_files[key_to_remove]
            
            # If we closed the current tab, select another one
            if file_tab == self.current_tab:
                if len(self.file_tabs.tabs) > 0:
                    # Select previous tab if available, otherwise next
                    new_index = max(0, min(tab_index - 1, len(self.file_tabs.tabs) - 1))
                    self.file_tabs.selected_index = new_index
                    self._on_file_tab_changed()
            
            # Save the updated list of open files
            self._save_open_files()
            self.page.update()
    
    def _create_file_content(self, file_tab: FileTab) -> ft.Container:
        """Create the content container for a file tab"""
        file_tab.query_input = ft.TextField(
            label="Query",
            hint_text="Enter your query here...",
            multiline=False,
            expand=True,
            on_change=lambda _: self.on_change(),
            border_color="#1877f2",
        )

        query_row = ft.Container(
            content=ft.Row(
                [ft.Icon(ft.icons.CHAT_BUBBLE_OUTLINE, color="#1877f2", size=24), file_tab.query_input],
                spacing=15,
                expand=True,
            ),
            padding=15,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
        )

        # Build tabs list
        tabs_list = [
            ft.Tab(text="Instruction", icon=ft.icons.EDIT_NOTE, content=self._create_instruction_panel(file_tab)),
            ft.Tab(text="Context", icon=ft.icons.BOOK, content=self._create_context_panel(file_tab)),
            ft.Tab(text="Output", icon=ft.icons.OUTPUT, content=self._create_output_panel(file_tab)),
            ft.Tab(text="Extends", icon=ft.icons.LINK, content=self._create_extends_panel(file_tab)),
        ]
        
        # Add YAML tab if DEBUG mode is enabled
        if os.environ.get('DEBUG', '').lower() in ('true', '1', 'yes'):
            tabs_list.append(
                ft.Tab(text="YAML", icon=ft.icons.CODE, content=self._create_yaml_panel(file_tab))
            )
        
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            tabs=tabs_list,
            expand=True,
        )

        return ft.Column([query_row, tabs], expand=True, spacing=10)

    def _create_toolbar(self):
        self.filename_label = ft.Text("Untitled", size=18, weight=ft.FontWeight.BOLD)

        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton("New", icon=ft.icons.ADD, on_click=lambda _: self.new_file()),
                            ft.ElevatedButton("Open", icon=ft.icons.FOLDER_OPEN, on_click=lambda _: self.open_file()),
                            ft.ElevatedButton("Save", icon=ft.icons.SAVE, on_click=lambda _: self.save_file()),
                        ],
                        spacing=10,
                    ),
                    ft.Container(expand=True, content=self.filename_label, alignment=ft.alignment.center),
                    ft.Row(
                        [
                            ft.ElevatedButton("Preview", icon=ft.icons.VISIBILITY, on_click=lambda _: self.preview_prompt()),
                            ft.ElevatedButton("Copy", icon=ft.icons.COPY, on_click=lambda _: self.copy_prompt()),
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.colors.with_opacity(0.1, ft.colors.BLACK)),
        )

    def _create_instruction_panel(self, file_tab: FileTab):
        file_tab.instruction_base = ft.TextField(
            label="Base Instructions (one per line)",
            multiline=True,
            min_lines=10,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )
        file_tab.instruction_additional = ft.TextField(
            label="Additional Instructions (optional)",
            multiline=True,
            min_lines=10,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("INSTRUCTION Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Define base and additional instructions", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Text("📝 Base Instructions", size=16, weight=ft.FontWeight.BOLD),
                    file_tab.instruction_base,
                    ft.Divider(height=20),
                    ft.Text("⚙️ Additional Instructions", size=16, weight=ft.FontWeight.BOLD),
                    file_tab.instruction_additional,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def _create_context_panel(self, file_tab: FileTab):
        file_tab.context_base = ft.TextField(
            label="Base Context (one per line)",
            multiline=True,
            min_lines=6,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )
        file_tab.context_local_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        file_tab.context_web_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        file_tab.context_rag_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("CONTEXT Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Add context information from various sources", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Text("🧩 Base Context", size=16, weight=ft.FontWeight.BOLD),
                    file_tab.context_base,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("📁 Local Files", "Attach files or folders as context", self.add_context_local_rule),
                    file_tab.context_local_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("🌐 Web Pages", "Scrape a page (optionally with XPath)", self.add_context_web_rule),
                    file_tab.context_web_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("🤖 RAG", "Query your FAISS index for relevant chunks", self.add_context_rag_rule),
                    file_tab.context_rag_container,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def _create_output_panel(self, file_tab: FileTab):
        file_tab.output_base = ft.TextField(
            label="Base Output Rules (one per line)",
            multiline=True,
            min_lines=6,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )
        file_tab.output_local_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        file_tab.output_web_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        file_tab.output_rag_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("OUTPUT Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Add output constraints and post-processing sources", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Text("🧾 Base Output", size=16, weight=ft.FontWeight.BOLD),
                    file_tab.output_base,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("📁 Local Files", "Add local output rules/sources", self.add_output_local_rule),
                    file_tab.output_local_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("🌐 Web Pages", "Add web output rules/sources", self.add_output_web_rule),
                    file_tab.output_web_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    section_header("🤖 RAG", "Use retrieval to shape output content", self.add_output_rag_rule),
                    file_tab.output_rag_container,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def _create_yaml_panel(self, file_tab: FileTab):
        """Create YAML debug panel - only shown when DEBUG=True"""
        import yaml
        
        # Initialize yaml_editor if not exists
        if not file_tab.yaml_editor:
            file_tab.yaml_editor = ft.TextField(
                label="YAML Source",
                multiline=True,
                min_lines=20,
                max_lines=50,
                expand=True,
                on_change=lambda _: self.on_yaml_change(),
                border_color="#1877f2",
                text_style=ft.TextStyle(font_family="Courier New", size=12),
            )
        
        # Sync current yaml_data to editor
        if file_tab.yaml_data:
            file_tab.yaml_editor.value = yaml.dump(file_tab.yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        def refresh_yaml():
            """Sync UI to yaml_data and update editor"""
            self.sync_ui_to_yaml()
            file_tab.yaml_editor.value = yaml.dump(file_tab.yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
            file_tab.yaml_editor.update()
            self.show_status("YAML refreshed from UI", ft.colors.BLUE)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text("YAML Debug View", size=20, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("🔄 Refresh from UI", on_click=lambda _: refresh_yaml(), icon=ft.icons.REFRESH),
                    ], spacing=15),
                    ft.Text("Live YAML representation - edit directly or refresh from UI", color=ft.colors.GREY_700, size=12),
                    ft.Divider(height=10),
                    file_tab.yaml_editor,
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def _create_extends_panel(self, file_tab: FileTab):
        """Create extends/inheritance panel"""
        file_tab.extends_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        
        def add_extends():
            if not file_tab:
                return
            card = self._create_extends_card(file_tab)
            file_tab.extends_cards.append(card)
            file_tab.extends_container.controls.append(card.container)
            self.page.update()
            self.on_change()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("EXTENDS Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Inherit from other YAML files", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Row([
                        ft.Text("Inheritance Configuration:", size=16, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("➕ Add Extends", on_click=lambda _: add_extends(), icon=ft.icons.ADD),
                    ], spacing=15),
                    file_tab.extends_container,
                    ft.Text("Tips:", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_600),
                    ft.Text(
                        "• Paths can be relative (../other.yaml) or absolute\n"
                        "• Relative paths are calculated from the current file's directory\n"
                        "• Priority: high > normal > low",
                        size=11, color=ft.colors.GREY_600
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )
    
    def _create_extends_card(self, file_tab: FileTab):
        """Create a single extends card"""
        extends_card = ExtendsCard(on_change=self.on_change)
        
        def on_delete():
            file_tab.extends_cards.remove(extends_card)
            file_tab.extends_container.controls.remove(extends_card.container)
            self.page.update()
            self.on_change()
        
        def browse_file():
            def on_file_selected(selected_path: Optional[str]):
                try:
                    if selected_path:
                        extends_card.source_field.value = selected_path
                        self.page.update()
                        self.on_change()
                except Exception as ex:
                    error_msg = f"Error in file picker: {str(ex)}\n{traceback.format_exc()}"
                    print(f"[ERROR] {error_msg}")
                    logging.error(error_msg)
                    self.show_status(f"Error selecting file: {str(ex)}", ft.colors.RED)
            
            FileService.pick_yaml_file_for_extends(
                self.page,
                on_file_selected,
                initial_directory=self.config.get_last_directory()
            )
        
        extends_card.container = ft.Container(
            content=ft.Column([
                ft.Row([
                    extends_card.source_field,
                    ft.IconButton(ft.icons.FOLDER_OPEN, on_click=lambda _: browse_file(), tooltip="Browse for YAML file"),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda _: on_delete(), icon_color=ft.colors.RED, tooltip="Remove"),
                ], spacing=5, expand=True),
            ], spacing=10),
            padding=15,
            bgcolor=ft.colors.GREY_100,
            border_radius=8,
        )
        
        return extends_card

    def _create_status_bar(self):
        self.status_text = ft.Text("", size=14)
        return ft.Container(content=self.status_text, padding=10, bgcolor=ft.colors.WHITE, border_radius=12, visible=False)

    # ---------- rules ----------
    def _add_rule(self, kind: str, bucket: str):
        """
        kind: 'local'|'web'|'rag'
        bucket: 'context'|'output'
        """
        if not self.current_tab:
            self.show_status("No file open", ft.colors.RED)
            return
        
        # Determine target list to count existing rules
        if bucket == "context":
            target_list = {
                "local": self.current_tab.context_local_rules,
                "web": self.current_tab.context_web_rules,
                "rag": self.current_tab.context_rag_rules,
            }[kind]
        else:
            target_list = {
                "local": self.current_tab.output_local_rules,
                "web": self.current_tab.output_web_rules,
                "rag": self.current_tab.output_rag_rules,
            }[kind]
        
        # Auto-generate rule name: local_1, local_2, web_1, etc.
        rule_number = len(target_list) + 1
        default_rule_name = f"{kind}_{rule_number}"
            
        card = RuleCard(
            kind, 
            self.page, 
            rule_name=default_rule_name,
            on_delete=self.delete_rule, 
            on_change=self.on_change, 
            editing_mode=True,
            get_base_dir=self._get_base_dir_for_resolution
        )

        if bucket == "context":
            target_list, target_container = {
                "local": (self.current_tab.context_local_rules, self.current_tab.context_local_container),
                "web": (self.current_tab.context_web_rules, self.current_tab.context_web_container),
                "rag": (self.current_tab.context_rag_rules, self.current_tab.context_rag_container),
            }[kind]
        else:
            target_list, target_container = {
                "local": (self.current_tab.output_local_rules, self.current_tab.output_local_container),
                "web": (self.current_tab.output_web_rules, self.current_tab.output_web_container),
                "rag": (self.current_tab.output_rag_rules, self.current_tab.output_rag_container),
            }[kind]

        target_list.append(card)
        target_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_context_local_rule(self): self._add_rule("local", "context")
    def add_context_web_rule(self): self._add_rule("web", "context")
    def add_context_rag_rule(self): self._add_rule("rag", "context")

    def add_output_local_rule(self): self._add_rule("local", "output")
    def add_output_web_rule(self): self._add_rule("web", "output")
    def add_output_rag_rule(self): self._add_rule("rag", "output")

    def delete_rule(self, card: RuleCard):
        if not self.current_tab:
            return
            
        # remove from lists
        for lst in [self.current_tab.context_local_rules, self.current_tab.context_web_rules, self.current_tab.context_rag_rules,
                    self.current_tab.output_local_rules, self.current_tab.output_web_rules, self.current_tab.output_rag_rules]:
            if card in lst:
                lst.remove(card)

        # remove from containers
        for container in [self.current_tab.context_local_container, self.current_tab.context_web_container, self.current_tab.context_rag_container,
                          self.current_tab.output_local_container, self.current_tab.output_web_container, self.current_tab.output_rag_container]:
            if container and card in container.controls:
                container.controls.remove(card)

        self.page.update()
        self.on_change()

    def _clear_rule_ui(self):
        if not self.current_tab:
            return
            
        self.current_tab.context_local_rules.clear()
        self.current_tab.context_web_rules.clear()
        self.current_tab.context_rag_rules.clear()
        self.current_tab.output_local_rules.clear()
        self.current_tab.output_web_rules.clear()
        self.current_tab.output_rag_rules.clear()

        for container in [self.current_tab.context_local_container, self.current_tab.context_web_container, self.current_tab.context_rag_container,
                          self.current_tab.output_local_container, self.current_tab.output_web_container, self.current_tab.output_rag_container]:
            if container:
                container.controls.clear()

    # ---------- file ops ----------
    def _get_next_untitled_path(self, directory: str = None) -> str:
        """Find next available untitled_X.yaml filename in directory"""
        if directory is None:
            # Use last directory from config if available, otherwise current working directory
            directory = self.config.get_last_directory() or os.getcwd()
        
        # Find existing untitled files
        existing_untitled = []
        try:
            for filename in os.listdir(directory):
                if filename.startswith("untitled_") and filename.endswith(".yaml"):
                    # Extract number from untitled_X.yaml
                    try:
                        num_str = filename[9:-5]  # Remove "untitled_" and ".yaml"
                        num = int(num_str)
                        existing_untitled.append(num)
                    except ValueError:
                        continue
        except OSError:
            pass
        
        # Find next available number
        next_num = 1
        while next_num in existing_untitled:
            next_num += 1
        
        return os.path.join(directory, f"untitled_{next_num}.yaml")
    
    def new_file(self):
        # Create file with auto-generated name in last used directory
        new_filepath = self._get_next_untitled_path()
        
        file_tab = FileTab(new_filepath)
        self._add_file_tab(file_tab)
        
        # Save empty file immediately
        try:
            FileService.save_yaml_file(new_filepath, file_tab.yaml_data)
            # Update last directory in config
            self.config.set_last_directory(os.path.dirname(new_filepath))
            self.show_status(f"Created: {os.path.basename(new_filepath)}", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"Error creating file: {str(e)}", ft.colors.RED)

    def open_file(self):
        def on_file_selected(filepath: Optional[str]):
            if filepath:
                self.load_file(filepath)

        FileService.open_yaml_file_picker(
            self.page,
            on_file_selected,
            initial_directory=self.config.get_last_directory(),
            dialog_title="Open YAML file"
        )

    def load_file(self, filepath: str):
        try:
            # If file is already open, focus the existing tab instead of opening another
            if filepath in self.open_files:
                existing_tab = self.open_files[filepath]
                if self.file_tabs and existing_tab.content in self.file_tabs.tabs:
                    self.file_tabs.selected_index = self.file_tabs.tabs.index(existing_tab.content)
                    self.current_tab = existing_tab
                    self.update_filename_display()
                    self.page.update()
                self.show_status(f"Already open: {Path(filepath).name}", ft.colors.BLUE)
                return

            file_tab = FileTab(filepath)
            file_tab.yaml_data = FileService.load_yaml_file(filepath)
            self._add_file_tab(file_tab)
            self.update_ui_from_data()
            # Update last directory in config
            self.config.set_last_directory(os.path.dirname(filepath))
            self.show_status(f"Loaded: {Path(filepath).name}", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"Error: {str(e)}", ft.colors.RED)

    def save_file(self):
        if not self.current_tab:
            self.show_status("No file open", ft.colors.RED)
            return
        
        # Prompt for filename when path is missing or auto-generated (untitled)
        need_save_as = False
        if not self.current_tab.file_path:
            need_save_as = True
        else:
            basename = os.path.basename(self.current_tab.file_path).lower()
            if basename.startswith("untitled_") or basename.startswith("untitle_"):
                need_save_as = True
        
        if need_save_as:
            def on_file_selected(filepath: Optional[str]):
                if filepath:
                    self.current_tab.file_path = filepath
                    self.do_save()

            FileService.save_yaml_file_picker(
                self.page,
                on_file_selected,
                initial_directory=self.config.get_last_directory(),
                file_name="untitled.yaml",
                dialog_title="Save YAML file"
            )
        else:
            self.do_save()

    def do_save(self):
        if not self.current_tab:
            return
            
        try:
            self.sync_ui_to_yaml()
            FileService.save_yaml_file(self.current_tab.file_path, self.current_tab.yaml_data)
            self.current_tab.unsaved_changes = False
            
            # Update last directory in config
            self.config.set_last_directory(os.path.dirname(self.current_tab.file_path))
            
            # Update tab display name and remove unsaved indicator
            self.update_filename_display()
            self._update_tab_label()
            
            # If this was an untitled file, update the key in open_files
            untitled_keys = [k for k in self.open_files.keys() if k.startswith("untitled_")]
            if untitled_keys:
                old_key = untitled_keys[0]
                if self.open_files.get(old_key) == self.current_tab:
                    del self.open_files[old_key]
                    self.open_files[self.current_tab.file_path] = self.current_tab
            
            # Save the updated list of open files (important when renaming untitled files)
            self._save_open_files()
            
            self.page.update()
            self.show_status(f"Saved: {Path(self.current_tab.file_path).name}", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"Error saving: {str(e)}", ft.colors.RED)

    # ---------- prompt ops ----------
    def preview_prompt(self):
        if not self.current_tab:
            self.show_status("No file open", ft.colors.RED)
            return
            
        try:
            print("[DEBUG] preview_prompt: Starting...")
            self.sync_ui_to_yaml()
            print(f"[DEBUG] yaml_data after sync: {self.current_tab.yaml_data}")
            
            # Resolve relative extends paths to absolute before generating prompt
            resolved_data = self._resolve_extends_to_absolute(self.current_tab.yaml_data)
            print(f"[DEBUG] resolved_data with absolute paths: {resolved_data}")
            
            # Get working directory from current file path
            working_dir = os.path.dirname(self.current_tab.file_path) if self.current_tab.file_path else None
            
            prompt_text = PromptService.generate_prompt_sentence(resolved_data, working_dir)
            print(f"[DEBUG] Generated prompt (first 100 chars): {prompt_text[:100] if prompt_text else 'EMPTY'}")

            preview_text = ft.TextField(
                value=prompt_text,
                multiline=True,
                min_lines=25,
                read_only=True,
                text_style=ft.TextStyle(font_family="Courier New"),
                border_color="#e5e7eb",
            )

            dlg = ft.AlertDialog(
                title=ft.Text("Prompt Preview", size=20, weight=ft.FontWeight.BOLD),
                content=ft.Container(content=preview_text, width=900, height=700),
                actions=[ft.TextButton("Close", on_click=lambda _: self.close_dialog(dlg))],
            )
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
        except Exception as e:
            self.show_status(f"Error: {str(e)}", ft.colors.RED)

    def copy_prompt(self):
        if not self.current_tab:
            self.show_status("No file open", ft.colors.RED)
            return
            
        try:
            self.sync_ui_to_yaml()
            # Resolve relative extends paths to absolute before generating prompt
            resolved_data = self._resolve_extends_to_absolute(self.current_tab.yaml_data)
            
            # Get working directory from current file path
            working_dir = os.path.dirname(self.current_tab.file_path) if self.current_tab.file_path else None
            
            prompt_text = PromptService.generate_prompt_sentence(resolved_data, working_dir)
            self.page.set_clipboard(prompt_text)
            self.show_status("✅ Prompt copied to clipboard!", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"❌ Error: {str(e)}", ft.colors.RED)

    def close_dialog(self, dialog: ft.AlertDialog):
        dialog.open = False
        self.page.update()

    # ---------- sync UI <-> YAML ----------
    def update_ui_from_data(self):
        if not self.current_tab:
            return
        
        # Clear existing rules before loading new ones
        containers = RuleParsingService.prepare_rule_containers(self.current_tab)
        RuleParsingService.clear_rules_from_containers(containers)
            
        prompt = self.current_tab.yaml_data.get("prompt", {}) if isinstance(self.current_tab.yaml_data.get("prompt"), dict) else {}
        if self.current_tab.query_input:
            self.current_tab.query_input.value = prompt.get("query", "")

        if self.current_tab.yaml_editor:
            import yaml
            self.current_tab.yaml_editor.value = yaml.dump(self.current_tab.yaml_data, default_flow_style=False, sort_keys=False)

        instruction = prompt.get("instruction", {}) if isinstance(prompt.get("instruction"), dict) else {}
        if self.current_tab.instruction_base:
            self.current_tab.instruction_base.value = "\n".join(YamlService.read_base_lines(instruction, "base"))
        if self.current_tab.instruction_additional:
            self.current_tab.instruction_additional.value = "\n".join(YamlService.read_base_lines(instruction, "additional"))

        context = prompt.get("context", {}) if isinstance(prompt.get("context"), dict) else {}
        if self.current_tab.context_base:
            self.current_tab.context_base.value = "\n".join(YamlService.read_base_lines(context, "base"))

        output = prompt.get("output", {}) if isinstance(prompt.get("output"), dict) else {}
        if self.current_tab.output_base:
            self.current_tab.output_base.value = "\n".join(YamlService.read_base_lines(output, "base"))

        # Load rules into UI using the parsing service
        ctx_local, ctx_web, ctx_rag, out_local, out_web, out_rag = RuleParsingService.extract_all_rules(prompt)

        self._load_rules_into_ui(ctx_local, "context", "local")
        self._load_rules_into_ui(ctx_web, "context", "web")
        self._load_rules_into_ui(ctx_rag, "context", "rag")
        self._load_rules_into_ui(out_local, "output", "local")
        self._load_rules_into_ui(out_web, "output", "web")
        self._load_rules_into_ui(out_rag, "output", "rag")

        self.page.update()

    def _load_rules_into_ui(self, rules: List[RuleData], bucket: str, kind: str):
        if not self.current_tab:
            return
            
        for rd in rules:
            card = RuleCard(
                kind, 
                self.page, 
                on_delete=self.delete_rule, 
                on_change=self.on_change, 
                editing_mode=False,
                get_base_dir=self._get_base_dir_for_resolution
            )
            card.fill_from_rule_data(rd)

            if bucket == "context":
                target_list, target_container = {
                    "local": (self.current_tab.context_local_rules, self.current_tab.context_local_container),
                    "web": (self.current_tab.context_web_rules, self.current_tab.context_web_container),
                    "rag": (self.current_tab.context_rag_rules, self.current_tab.context_rag_container),
                }[kind]
            else:
                target_list, target_container = {
                    "local": (self.current_tab.output_local_rules, self.current_tab.output_local_container),
                    "web": (self.current_tab.output_web_rules, self.current_tab.output_web_container),
                    "rag": (self.current_tab.output_rag_rules, self.current_tab.output_rag_container),
                }[kind]

            target_list.append(card)
            target_container.controls.append(card)

    def sync_ui_to_yaml(self):
        if not self.current_tab:
            return
            
        YamlService.ensure_prompt_root(self.current_tab.yaml_data)
        prompt = self.current_tab.yaml_data["prompt"]

        prompt["query"] = (self.current_tab.query_input.value or "") if self.current_tab.query_input else ""

        # instruction
        instruction: Dict[str, Any] = prompt.get("instruction", {}) if isinstance(prompt.get("instruction"), dict) else {}
        if self.current_tab.instruction_base:
            YamlService.write_base_lines(instruction, "base", self.current_tab.instruction_base.value or "")
        if self.current_tab.instruction_additional:
            YamlService.write_base_lines(instruction, "additional", self.current_tab.instruction_additional.value or "")
        if instruction:
            prompt["instruction"] = instruction
        else:
            prompt.pop("instruction", None)

        # context
        context: Dict[str, Any] = prompt.get("context", {}) if isinstance(prompt.get("context"), dict) else {}
        if self.current_tab.context_base:
            YamlService.write_base_lines(context, "base", self.current_tab.context_base.value or "")
        YamlService.rules_to_yaml_section(context, "local", [c.to_rule_data() for c in self.current_tab.context_local_rules])
        YamlService.rules_to_yaml_section(context, "web", [c.to_rule_data() for c in self.current_tab.context_web_rules])
        YamlService.rules_to_yaml_section(context, "rag", [c.to_rule_data() for c in self.current_tab.context_rag_rules])
        if context:
            prompt["context"] = context
        else:
            prompt.pop("context", None)

        # output
        output: Dict[str, Any] = prompt.get("output", {}) if isinstance(prompt.get("output"), dict) else {}
        if self.current_tab.output_base:
            YamlService.write_base_lines(output, "base", self.current_tab.output_base.value or "")
        YamlService.rules_to_yaml_section(output, "local", [c.to_rule_data() for c in self.current_tab.output_local_rules])
        YamlService.rules_to_yaml_section(output, "web", [c.to_rule_data() for c in self.current_tab.output_web_rules])
        YamlService.rules_to_yaml_section(output, "rag", [c.to_rule_data() for c in self.current_tab.output_rag_rules])
        if output:
            prompt["output"] = output
        else:
            prompt.pop("output", None)

        # Save extends data
        self._save_extends_to_yaml()

        # Keep YAML editor in sync (optional)
        if self.current_tab.yaml_editor:
            import yaml
            self.current_tab.yaml_editor.value = yaml.dump(self.current_tab.yaml_data, default_flow_style=False, sort_keys=False)

    def _load_extends_from_data(self, file_tab: FileTab):
        """Load extends from YAML data into the UI - loads from prompt.extends per PEaC core spec"""
        if not file_tab.extends_container:
            return
        
        # Clear existing extends cards
        file_tab.extends_cards.clear()
        file_tab.extends_container.controls.clear()
        
        # Get extends from prompt section (per PEaC core spec)
        prompt = file_tab.yaml_data.get('prompt', {})
        extends_data = prompt.get('extends', None)
        if not extends_data:
            return
        
        # Handle both list and single extends
        extends_list = []
        if isinstance(extends_data, list):
            extends_list = extends_data
        elif isinstance(extends_data, (str, dict)):
            extends_list = [extends_data]
        
        # Load each extends into a card
        for extends_item in extends_list:
            extends_card = self._create_extends_card(file_tab)
            extends_card.load_data(extends_item)
            file_tab.extends_cards.append(extends_card)
            file_tab.extends_container.controls.append(extends_card.container)
    
    def _save_extends_to_yaml(self):
        """Save extends from UI back to YAML data - saves to prompt.extends as per PEaC core spec.
        Always saves paths as RELATIVE paths"""
        print(f"[DEBUG] _save_extends_to_yaml: Starting...")
        
        # Ensure prompt section exists
        YamlService.ensure_prompt_root(self.current_tab.yaml_data)
        prompt = self.current_tab.yaml_data["prompt"]
        
        if not self.current_tab or not self.current_tab.extends_cards:
            # Clear extends if no cards
            print(f"[DEBUG] No current_tab or no extends_cards, clearing extends")
            prompt.pop('extends', None)
            return
        
        print(f"[DEBUG] Found {len(self.current_tab.extends_cards)} extends cards")
        # Collect extends data from all cards (now always strings per EBNF)
        extends_list = []
        
        for i, card in enumerate(self.current_tab.extends_cards):
            data = card.get_data()  # Returns string or None
            print(f"[DEBUG] Card {i}: get_data() = {data}")
            if data:
                # Normalize and ensure relative path
                data = PathResolverService.normalize_path(data)
                last_dir = PathResolverService.normalize_path(self.config.get_last_directory())
                # Convert to relative if it's absolute
                if os.path.isabs(data):
                    data = PathResolverService.get_relative_path(data, last_dir)
                print(f"[DEBUG] Card {i}: normalized+relative = {data}")
                extends_list.append(data)
        
        print(f"[DEBUG] extends_list after collecting: {extends_list}")
        # Save to prompt.extends (per PEaC EBNF spec) - always as list of relative paths
        if extends_list:
            prompt['extends'] = extends_list
            print(f"[DEBUG] Saved extends list (relative): {extends_list}")
        else:
            prompt.pop('extends', None)
    
    def _resolve_extends_to_absolute(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a copy of yaml_data with extends paths converted to absolute for prompt generation.
        Works with prompt.extends as per PEaC core spec"""
        import copy
        resolved_data = copy.deepcopy(yaml_data)
        
        # Get base directory for resolution
        base_dir = self.config.get_last_directory() or (os.path.dirname(self.current_tab.file_path) if self.current_tab and self.current_tab.file_path else None)
        
        # Get extends from prompt section (per PEaC core spec)
        if 'prompt' not in resolved_data or 'extends' not in resolved_data['prompt']:
            return resolved_data
        
        extends = resolved_data['prompt']['extends']
        if isinstance(extends, str):
            # Single string extends - normalize and resolve to absolute
            extends = PathResolverService.normalize_path(extends)
            resolved_data['prompt']['extends'] = [PathResolverService.get_absolute_path(extends, base_dir)]
        elif isinstance(extends, list):
            # List of extends
            resolved_list = []
            for item in extends:
                if isinstance(item, str):
                    item = PathResolverService.normalize_path(item)
                    resolved_list.append(PathResolverService.get_absolute_path(item, base_dir))
                elif isinstance(item, dict):
                    resolved_item = item.copy()
                    if 'source' in resolved_item:
                        resolved_item['source'] = PathResolverService.normalize_path(resolved_item['source'])
                        resolved_item['source'] = PathResolverService.get_absolute_path(resolved_item['source'], base_dir)
                    resolved_list.append(resolved_item)
                else:
                    resolved_list.append(item)
            resolved_data['prompt']['extends'] = resolved_list
        
        return resolved_data

    def _get_base_dir_for_resolution(self) -> Optional[str]:
        """Get the base directory for path resolution (directory where YAML file is located)."""
        if self.current_tab and self.current_tab.file_path:
            return os.path.dirname(self.current_tab.file_path)
        return self.config.get_last_directory()

    # ---------- events ----------
    def on_yaml_change(self):
        if not self.current_tab or not self.current_tab.yaml_editor:
            return
            
        try:
            import yaml
            if self.current_tab.yaml_editor.value:
                self.current_tab.yaml_data = yaml.safe_load(self.current_tab.yaml_editor.value) or {}
        except Exception:
            pass

    def on_change(self):
        # keep yaml_data coherent in memory
        self.sync_ui_to_yaml()
        # Mark as modified
        if self.current_tab:
            self.current_tab.unsaved_changes = True
            self._update_tab_label()

    # ---------- misc ----------
    def _update_tab_label(self):
        """Update tab label to show unsaved changes indicator (asterisk from get_display_name)"""
        if not self.current_tab or not self.current_tab.content:
            return
        
        if hasattr(self.current_tab.content, 'tab_content') and isinstance(self.current_tab.content.tab_content, ft.Row):
            # Find and update the Text widget in the tab row
            for control in self.current_tab.content.tab_content.controls:
                if isinstance(control, ft.Text):
                    # Use display name which includes asterisk for unsaved changes
                    control.value = self.current_tab.get_display_name()
                    break
            self.page.update()
    
    def update_filename_display(self):
        if not self.current_tab:
            self.filename_label.value = "Untitled"
        else:
            self.filename_label.value = Path(self.current_tab.file_path).name if self.current_tab.file_path else "Untitled"
            # Update tab label to reflect unsaved indicator
            self._update_tab_label()
        self.page.update()

    def show_status(self, message: str, color: str):
        if not self.status_text:
            return
        self.status_text.value = message
        self.status_text.color = color
        parent = self.status_text.parent
        if parent:
            parent.visible = True
        self.page.update()

        import time, threading

        def hide():
            time.sleep(3)
            if self.status_text and self.status_text.parent:
                self.status_text.parent.visible = False
                self.page.update()

        threading.Thread(target=hide, daemon=True).start()
