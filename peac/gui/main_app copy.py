"""
PEaC GUI - Flet Implementation
Modern, fast, cross-platform desktop GUI with complete feature support
Follows Google Material Design principles
"""
import flet as ft
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
import sys
import tempfile
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from peac.core.peac import PromptYaml


class RuleCard(ft.Container):
    """Reusable card component for rules (Local, Web, RAG)"""

    def __init__(
        self,
        rule_type: str,
        page: ft.Page,
        rule_name: str = "",
        on_delete=None,
        on_change=None,
        editing_mode: bool = True,
    ):
        super().__init__()
        self.rule_type = rule_type  # 'local', 'web', 'rag'
        self.rule_name = rule_name or f"New {rule_type.title()} Rule"
        self.on_delete = on_delete
        self.on_change = on_change
        self.page = page
        self.editing_mode = editing_mode  # True = editable, False = readonly

        # Base styling (will be updated by apply_visual_state)
        self.padding = 20
        self.bgcolor = "#ffffff"
        self.border_radius = 12

        # Field refs
        self.path_field: Optional[ft.TextField] = None
        self.name_field: Optional[ft.TextField] = None
        self.preamble_field: Optional[ft.TextField] = None
        self.edit_save_button: Optional[ft.IconButton] = None

        # For enabling/disabling all editable fields
        self.all_fields: List[ft.TextField] = []
        self.browse_buttons: List[ft.IconButton] = []

        # Web fields
        self.url_field: Optional[ft.TextField] = None
        self.xpath_field: Optional[ft.TextField] = None

        # RAG fields
        self.query_field: Optional[ft.TextField] = None
        self.topk_field: Optional[ft.TextField] = None
        self.chunk_field: Optional[ft.TextField] = None
        self.overlap_field: Optional[ft.TextField] = None
        self.filter_field: Optional[ft.TextField] = None

        self.build_card()
        self.apply_visual_state()

        # Optional: focus something useful if created in editing mode
        if self.editing_mode:
            self.focus_first_field()

    def build_card(self):
        self.name_field = ft.TextField(
            value=self.rule_name,
            label="Rule Name",
            expand=True,
            on_change=self.on_change_wrapper,
            border_color="#1877f2",
            text_size=16,
            read_only=not self.editing_mode,
        )
        self.all_fields.append(self.name_field)

        self.edit_save_button = ft.IconButton(
            icon=ft.icons.CHECK_CIRCLE if self.editing_mode else ft.icons.EDIT,
            icon_color="#42b72a" if self.editing_mode else "#1877f2",
            tooltip="Save changes" if self.editing_mode else "Edit rule",
            on_click=lambda _: self.toggle_editing_mode(),
            icon_size=24,
        )

        header = ft.Row(
            [
                self.name_field,
                self.edit_save_button,
                ft.IconButton(
                    ft.icons.DELETE_OUTLINE,
                    icon_color="#dc2626",
                    tooltip="Delete rule",
                    on_click=lambda _: self.on_delete(self) if self.on_delete else None,
                    icon_size=24,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.preamble_field = ft.TextField(
            label="Preamble (optional intro text)",
            multiline=True,
            min_lines=3,
            max_lines=5,
            on_change=self.on_change_wrapper,
            border_color="#e5e7eb",
            read_only=not self.editing_mode,
        )
        self.all_fields.append(self.preamble_field)

        preamble_section = ft.Column(
            [
                ft.Text("Preamble:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                self.preamble_field,
            ],
            spacing=8,
        )

        specific_fields = self.build_rule_specific_fields()

        # Small state hint (optional)
        state_hint = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.EDIT, size=16, color=ft.colors.BLUE_700),
                    ft.Text("Editing", size=12, color=ft.colors.BLUE_700),
                ],
                spacing=6,
            ),
            visible=self.editing_mode,
            padding=ft.padding.only(bottom=6),
        )
        self._state_hint = state_hint

        self.content = ft.Column(
            [
                header,
                state_hint,
                ft.Divider(height=1, color="#e5e7eb"),
                preamble_section,
                *specific_fields,
            ],
            spacing=15,
        )

    def build_rule_specific_fields(self) -> List[ft.Control]:
        fields: List[ft.Control] = []

        if self.rule_type == "local":
            self.path_field = ft.TextField(
                label="File or folder path",
                expand=True,
                on_change=self.on_change_wrapper,
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.path_field)

            browse_button = ft.IconButton(
                ft.icons.FOLDER_OPEN,
                icon_color="#1877f2",
                tooltip="Browse for file or folder",
                on_click=lambda _: self.pick_file(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            self.browse_buttons.append(browse_button)

            fields.append(
                ft.Column(
                    [
                        ft.Text("Source Path:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                        ft.Row([self.path_field, browse_button], spacing=8),
                    ],
                    spacing=4,
                )
            )

        elif self.rule_type == "web":
            self.url_field = ft.TextField(
                label="https://example.com/page",
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                read_only=not self.editing_mode,
            )
            self.xpath_field = ft.TextField(
                label="//div[@class='content']",
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="Leave empty to scrape entire page",
                read_only=not self.editing_mode,
            )
            self.all_fields.extend([self.url_field, self.xpath_field])

            fields.extend(
                [
                    ft.Column(
                        [
                            ft.Text("Source URL:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            self.url_field,
                        ],
                        spacing=4,
                    ),
                    ft.Column(
                        [
                            ft.Text("XPath Selector (optional):", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            self.xpath_field,
                        ],
                        spacing=4,
                    ),
                ]
            )

        elif self.rule_type == "rag":
            self.path_field = ft.TextField(
                label="Path to FAISS file",
                on_change=self.on_change_wrapper,
                expand=True,
                border_color="#e5e7eb",
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.path_field)

            browse_button = ft.IconButton(
                ft.icons.FOLDER_OPEN,
                icon_color="#1877f2",
                tooltip="Browse for FAISS file",
                on_click=lambda _: self.pick_file(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            self.browse_buttons.append(browse_button)

            self.query_field = ft.TextField(
                label="What to search for in the index",
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="e.g., 'Python best practices'",
                read_only=not self.editing_mode,
            )
            self.topk_field = ft.TextField(
                value="5",
                width=100,
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="Results",
                read_only=not self.editing_mode,
            )
            self.chunk_field = ft.TextField(
                value="512",
                width=100,
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="Tokens",
                read_only=not self.editing_mode,
            )
            self.overlap_field = ft.TextField(
                value="50",
                width=100,
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="Tokens",
                read_only=not self.editing_mode,
            )
            self.filter_field = ft.TextField(
                label="Regex pattern for post-filtering",
                on_change=self.on_change_wrapper,
                border_color="#e5e7eb",
                hint_text="e.g., .*python.*",
                read_only=not self.editing_mode,
            )

            self.all_fields.extend(
                [self.query_field, self.topk_field, self.chunk_field, self.overlap_field, self.filter_field]
            )

            fields.extend(
                [
                    ft.Column(
                        [
                            ft.Text("FAISS Index File:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row([self.path_field, browse_button], spacing=8),
                        ],
                        spacing=8,
                    ),
                    ft.Column(
                        [
                            ft.Text("Search Query:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            self.query_field,
                        ],
                        spacing=8,
                    ),
                    ft.Column(
                        [
                            ft.Text("RAG Parameters:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row(
                                [
                                    ft.Column([ft.Text("Top K:", size=12, color="#6b7280"), self.topk_field]),
                                    ft.Column([ft.Text("Chunk Size:", size=12, color="#6b7280"), self.chunk_field]),
                                    ft.Column([ft.Text("Overlap:", size=12, color="#6b7280"), self.overlap_field]),
                                ],
                                spacing=15,
                            ),
                        ],
                        spacing=4,
                    ),
                    ft.Column(
                        [
                            ft.Text("Filter Regex (optional):", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            self.filter_field,
                        ],
                        spacing=4,
                    ),
                ]
            )

        return fields

    def apply_visual_state(self):
        """Apply visual styling based on editing/view mode."""
        if self.editing_mode:
            # More prominent when editing
            self.border = ft.border.all(2, "#1877f2")
            self.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.12, ft.colors.BLACK),
                offset=ft.Offset(0, 3),
            )
        else:
            self.border = ft.border.all(1, "#e0e0e0")
            self.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            )

        if hasattr(self, "_state_hint") and self._state_hint:
            self._state_hint.visible = self.editing_mode

    def focus_first_field(self):
        """Focus the most relevant field for the rule type."""
        try:
            target = None
            if self.rule_type in ("local", "rag") and self.path_field:
                target = self.path_field
            elif self.rule_type == "web" and self.url_field:
                target = self.url_field
            else:
                target = self.name_field
            if target:
                target.focus()
        except Exception:
            pass

    def pick_file(self):
        """Open file picker for local/rag rules"""

        def on_result(e: ft.FilePickerResultEvent):
            if e.files and self.path_field:
                self.path_field.value = e.files[0].path
                self.path_field.update()
                self.on_change_wrapper()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()

        if self.rule_type == "rag":
            file_picker.pick_files(
                dialog_title="Select FAISS index file",
                allowed_extensions=["faiss", "index"],
                allow_multiple=False,
            )
        else:
            file_picker.pick_files(
                dialog_title="Select file or folder",
                allow_multiple=False,
            )

    def toggle_editing_mode(self):
        """Toggle between editing and viewing mode"""
        self.editing_mode = not self.editing_mode

        # Toggle fields
        for field in self.all_fields:
            field.read_only = not self.editing_mode

        for btn in self.browse_buttons:
            btn.disabled = not self.editing_mode

        # Button icon
        if self.edit_save_button:
            self.edit_save_button.icon = ft.icons.CHECK_CIRCLE if self.editing_mode else ft.icons.EDIT
            self.edit_save_button.icon_color = "#42b72a" if self.editing_mode else "#1877f2"
            self.edit_save_button.tooltip = "Save changes" if self.editing_mode else "Edit rule"

        self.apply_visual_state()
        self.update()

        if self.editing_mode:
            self.focus_first_field()

        if self.on_change:
            self.on_change()

    def to_dict(self) -> Dict[str, Any]:
        """Convert rule card to dictionary for YAML serialization"""
        result = {}
        
        if self.rule_type == "local":
            if self.path_field and self.path_field.value:
                result["source"] = self.path_field.value
        
        elif self.rule_type == "web":
            if self.url_field and self.url_field.value:
                result["source"] = self.url_field.value
            if self.xpath_field and self.xpath_field.value:
                result["xpath"] = self.xpath_field.value
        
        elif self.rule_type == "rag":
            if self.path_field and self.path_field.value:
                result["faiss_file"] = self.path_field.value
            if self.query_field and self.query_field.value:
                result["query"] = self.query_field.value
            if self.topk_field and self.topk_field.value:
                try:
                    result["top_k"] = int(self.topk_field.value)
                except (ValueError, TypeError):
                    pass
            if self.chunk_field and self.chunk_field.value:
                try:
                    result["chunk_size"] = int(self.chunk_field.value)
                except (ValueError, TypeError):
                    pass
            if self.overlap_field and self.overlap_field.value:
                try:
                    result["overlap"] = int(self.overlap_field.value)
                except (ValueError, TypeError):
                    pass
            if self.filter_field and self.filter_field.value:
                result["filter"] = self.filter_field.value
        
        return result if result else None

    def on_change_wrapper(self, e=None):
        if self.on_change:
            self.on_change()


class PeacFletApp:
    def __init__(self, page: ft.Page):
        self.page = page
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

        self.current_file_path: Optional[str] = None
        self.yaml_data: Dict[str, Any] = {}

        # UI refs
        self.filename_label: Optional[ft.Text] = None
        self.yaml_editor: Optional[ft.TextField] = None
        self.query_input: Optional[ft.TextField] = None

        self.instruction_base: Optional[ft.TextField] = None
        self.instruction_additional: Optional[ft.TextField] = None

        self.context_base: Optional[ft.TextField] = None
        self.output_base: Optional[ft.TextField] = None

        # Rule containers + lists
        self.context_local_rules: List[RuleCard] = []
        self.context_web_rules: List[RuleCard] = []
        self.context_rag_rules: List[RuleCard] = []
        self.output_local_rules: List[RuleCard] = []
        self.output_web_rules: List[RuleCard] = []
        self.output_rag_rules: List[RuleCard] = []

        self.context_local_container: Optional[ft.Column] = None
        self.context_web_container: Optional[ft.Column] = None
        self.context_rag_container: Optional[ft.Column] = None
        self.output_local_container: Optional[ft.Column] = None
        self.output_web_container: Optional[ft.Column] = None
        self.output_rag_container: Optional[ft.Column] = None

        self.status_text: Optional[ft.Text] = None

        self.build_ui()
        self.new_file()

    # ---------- UI helpers ----------
    def section_header(self, title: str, subtitle: str, on_add):
        """Consistent section header with inline primary action (Add)."""
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitle, size=12, color=ft.colors.GREY_700),
                    ],
                    expand=True,
                    spacing=2,
                ),
                ft.FilledButton("Add", icon=ft.icons.ADD, on_click=lambda _: on_add()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def build_ui(self):
        toolbar = self.create_toolbar()
        main_content = self.create_main_content()
        status_bar = self.create_status_bar()

        self.page.add(ft.Column([toolbar, main_content, status_bar], expand=True, spacing=10))

    def create_toolbar(self):
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
                            ft.ElevatedButton(
                                "Preview", icon=ft.icons.VISIBILITY, on_click=lambda _: self.preview_prompt()
                            ),
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

    def create_main_content(self):
        self.query_input = ft.TextField(
            label="Query",
            hint_text="Enter your query here...",
            multiline=False,
            expand=True,
            on_change=lambda _: self.on_change(),
            border_color="#1877f2",
        )

        query_row = ft.Container(
            content=ft.Row(
                [ft.Icon(ft.icons.CHAT_BUBBLE_OUTLINE, color="#1877f2", size=24), self.query_input],
                spacing=15,
                expand=True,
            ),
            padding=15,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
        )

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            tabs=[
                ft.Tab(text="YAML", icon=ft.icons.CODE, content=self.create_yaml_panel()),
                ft.Tab(text="Instruction", icon=ft.icons.EDIT_NOTE, content=self.create_instruction_panel()),
                ft.Tab(text="Context", icon=ft.icons.BOOK, content=self.create_context_panel()),
                ft.Tab(text="Output", icon=ft.icons.OUTPUT, content=self.create_output_panel()),
                ft.Tab(text="Extends", icon=ft.icons.LINK, content=self.create_extends_panel()),
            ],
            expand=True,
        )

        return ft.Column([query_row, tabs], expand=True, spacing=10)

    def create_yaml_panel(self):
        self.yaml_editor = ft.TextField(
            label="YAML Content",
            multiline=True,
            min_lines=25,
            expand=True,
            text_style=ft.TextStyle(font_family="Courier New"),
            on_change=lambda _: self.on_yaml_change(),
            border_color="#e5e7eb",
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("📄 YAML Editor", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Direct YAML editing", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=1, color="#e5e7eb"),
                    self.yaml_editor,
                ],
                expand=True,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def create_instruction_panel(self):
        self.instruction_base = ft.TextField(
            label="Base Instructions (one per line)",
            hint_text="• You are a helpful AI assistant\n• Provide clear and concise answers",
            multiline=True,
            min_lines=10,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )

        self.instruction_additional = ft.TextField(
            label="Additional Instructions (optional)",
            hint_text="Any extra constraints or guidance...",
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
                    self.instruction_base,
                    ft.Divider(height=20),
                    ft.Text("⚙️ Additional Instructions", size=16, weight=ft.FontWeight.BOLD),
                    self.instruction_additional,
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

    def create_context_panel(self):
        self.context_base = ft.TextField(
            label="Base Context (one per line)",
            hint_text="Enter base context information...",
            multiline=True,
            min_lines=6,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )

        self.context_local_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        self.context_web_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        self.context_rag_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("CONTEXT Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Add context information from various sources", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Text("🧩 Base Context", size=16, weight=ft.FontWeight.BOLD),
                    self.context_base,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("📁 Local Files", "Attach files or folders as context", self.add_context_local_rule),
                    self.context_local_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("🌐 Web Pages", "Scrape a page (optionally with XPath)", self.add_context_web_rule),
                    self.context_web_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("🤖 RAG", "Query your FAISS index for relevant chunks", self.add_context_rag_rule),
                    self.context_rag_container,
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

    def create_output_panel(self):
        self.output_base = ft.TextField(
            label="Base Output Rules (one per line)",
            hint_text="Enter desired output format constraints...",
            multiline=True,
            min_lines=6,
            on_change=lambda _: self.on_change(),
            border_color="#e5e7eb",
        )

        self.output_local_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        self.output_web_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)
        self.output_rag_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=15)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("OUTPUT Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Add output constraints and post-processing sources", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Text("🧾 Base Output", size=16, weight=ft.FontWeight.BOLD),
                    self.output_base,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("📁 Local Files", "Add local output rules/sources", self.add_output_local_rule),
                    self.output_local_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("🌐 Web Pages", "Add web output rules/sources", self.add_output_web_rule),
                    self.output_web_container,
                    ft.Divider(height=30, color="#e5e7eb"),
                    self.section_header("🤖 RAG", "Use retrieval to shape output content", self.add_output_rag_rule),
                    self.output_rag_container,
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

    def create_extends_panel(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("EXTENDS Section", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Inherit from other YAML files", color=ft.colors.GREY_700, size=14),
                    ft.Divider(height=20),
                    ft.Icon(ft.icons.LINK, size=48, color=ft.colors.GREY_400),
                    ft.Text("Feature coming soon...", size=14, italic=True, color=ft.colors.GREY_500),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            expand=True,
        )

    def create_status_bar(self):
        self.status_text = ft.Text("", size=14)
        return ft.Container(
            content=self.status_text,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            visible=False,
        )

    # ---- rule management (NOW: new cards start editable) ----
    def add_context_local_rule(self):
        card = RuleCard("local", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.context_local_rules.append(card)
        self.context_local_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_context_web_rule(self):
        card = RuleCard("web", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.context_web_rules.append(card)
        self.context_web_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_context_rag_rule(self):
        card = RuleCard("rag", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.context_rag_rules.append(card)
        self.context_rag_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_output_local_rule(self):
        card = RuleCard("local", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.output_local_rules.append(card)
        self.output_local_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_output_web_rule(self):
        card = RuleCard("web", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.output_web_rules.append(card)
        self.output_web_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def add_output_rag_rule(self):
        card = RuleCard("rag", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=True)
        self.output_rag_rules.append(card)
        self.output_rag_container.controls.append(card)
        self.page.update()
        card.focus_first_field()

    def delete_rule(self, card: RuleCard):
        for lst in [
            self.context_local_rules,
            self.context_web_rules,
            self.context_rag_rules,
            self.output_local_rules,
            self.output_web_rules,
            self.output_rag_rules,
        ]:
            if card in lst:
                lst.remove(card)

        for container in [
            self.context_local_container,
            self.context_web_container,
            self.context_rag_container,
            self.output_local_container,
            self.output_web_container,
            self.output_rag_container,
        ]:
            if container and card in container.controls:
                container.controls.remove(card)

        self.page.update()
        self.on_change()
        self.page.update()

    # ---- file operations ----
    def new_file(self):
        self.current_file_path = None
        self.yaml_data = {"prompt": {"query": ""}}
        self.clear_all_rules()
        self.update_ui_from_data()
        self.update_filename_display()
        self.show_status("New file created", ft.colors.GREEN)

    def clear_all_rules(self):
        self.context_local_rules = []
        self.context_web_rules = []
        self.context_rag_rules = []
        self.output_local_rules = []
        self.output_web_rules = []
        self.output_rag_rules = []

        for container in [
            self.context_local_container,
            self.context_web_container,
            self.context_rag_container,
            self.output_local_container,
            self.output_web_container,
            self.output_rag_container,
        ]:
            if container:
                container.controls.clear()

    def _generate_prompt_from_data(self) -> str:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            yaml.dump(self.yaml_data, tmp, default_flow_style=False, sort_keys=False)
            tmp_path = tmp.name
        try:
            prompt_yaml = PromptYaml(tmp_path)
            return prompt_yaml.get_prompt_sentence()
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def open_file(self):
        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files:
                self.load_file(e.files[0].path)

        file_picker = ft.FilePicker(on_result=pick_file_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["yaml", "yml"], dialog_title="Open YAML file")

    def load_file(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.yaml_data = yaml.safe_load(f) or {}

            self.current_file_path = filepath
            self.clear_all_rules()
            self.update_ui_from_data()
            self.update_filename_display()
            self.show_status(f"Loaded: {Path(filepath).name}", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"Error: {str(e)}", ft.colors.RED)

    def save_file(self):
        if not self.current_file_path:

            def save_file_result(e: ft.FilePickerResultEvent):
                if e.path:
                    self.current_file_path = e.path
                    self.do_save()

            file_picker = ft.FilePicker(on_result=save_file_result)
            self.page.overlay.append(file_picker)
            self.page.update()
            file_picker.save_file(allowed_extensions=["yaml"], dialog_title="Save YAML file", file_name="untitled.yaml")
        else:
            self.do_save()

    def do_save(self):
        try:
            self.sync_ui_to_yaml()
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                yaml.dump(self.yaml_data, f, default_flow_style=False, sort_keys=False)

            self.show_status(f"Saved: {Path(self.current_file_path).name}", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"Error saving: {str(e)}", ft.colors.RED)

    def preview_prompt(self):
        try:
            self.sync_ui_to_yaml()
            prompt_text = self._generate_prompt_from_data()

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
        try:
            self.sync_ui_to_yaml()
            prompt_text = self._generate_prompt_from_data()
            self.page.set_clipboard(prompt_text)
            self.show_status("✅ Prompt copied to clipboard!", ft.colors.GREEN)
        except Exception as e:
            self.show_status(f"❌ Error: {str(e)}", ft.colors.RED)

    def close_dialog(self, dialog: ft.AlertDialog):
        dialog.open = False
        self.page.update()

    def update_filename_display(self):
        if self.current_file_path:
            self.filename_label.value = Path(self.current_file_path).name
        else:
            self.filename_label.value = "Untitled"
        self.page.update()

    def update_ui_from_data(self):
        prompt_data = self.yaml_data.get("prompt", {})

        if self.query_input:
            self.query_input.value = prompt_data.get("query", "")

        if self.yaml_editor:
            self.yaml_editor.value = yaml.dump(self.yaml_data, default_flow_style=False, sort_keys=False)

        instruction_data = prompt_data.get("instruction", {})
        if self.instruction_base:
            base = instruction_data.get("base", []) if isinstance(instruction_data, dict) else []
            self.instruction_base.value = "\n".join(base) if isinstance(base, list) else (str(base) if base else "")
        if self.instruction_additional:
            additional = instruction_data.get("additional", []) if isinstance(instruction_data, dict) else []
            self.instruction_additional.value = (
                "\n".join(additional) if isinstance(additional, list) else (str(additional) if additional else "")
            )

        context_data = prompt_data.get("context", {})
        if self.context_base and isinstance(context_data, dict):
            base = context_data.get("base", [])
            self.context_base.value = "\n".join(base) if isinstance(base, list) else (str(base) if base else "")
        
        # Load context rules from YAML
        if isinstance(context_data, dict):
            for local_rule_data in context_data.get("local", {}).values():
                card = RuleCard("local", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "source" in local_rule_data:
                    card.path_field.value = local_rule_data["source"]
                self.context_local_rules.append(card)
                self.context_local_container.controls.append(card)
            
            for web_rule_data in context_data.get("web", {}).values():
                card = RuleCard("web", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "source" in web_rule_data:
                    card.url_field.value = web_rule_data["source"]
                if "xpath" in web_rule_data:
                    card.xpath_field.value = web_rule_data["xpath"]
                self.context_web_rules.append(card)
                self.context_web_container.controls.append(card)
            
            for rag_rule_data in context_data.get("rag", {}).values():
                card = RuleCard("rag", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "faiss_file" in rag_rule_data:
                    card.path_field.value = rag_rule_data["faiss_file"]
                if "query" in rag_rule_data:
                    card.query_field.value = rag_rule_data["query"]
                if "top_k" in rag_rule_data:
                    card.topk_field.value = str(rag_rule_data["top_k"])
                if "chunk_size" in rag_rule_data:
                    card.chunk_field.value = str(rag_rule_data["chunk_size"])
                if "overlap" in rag_rule_data:
                    card.overlap_field.value = str(rag_rule_data["overlap"])
                if "filter" in rag_rule_data:
                    card.filter_field.value = rag_rule_data["filter"]
                self.context_rag_rules.append(card)
                self.context_rag_container.controls.append(card)

        output_data = prompt_data.get("output", {})
        if self.output_base and isinstance(output_data, dict):
            base = output_data.get("base", [])
            self.output_base.value = "\n".join(base) if isinstance(base, list) else (str(base) if base else "")
        
        # Load output rules from YAML
        if isinstance(output_data, dict):
            for local_rule_data in output_data.get("local", {}).values():
                card = RuleCard("local", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "source" in local_rule_data:
                    card.path_field.value = local_rule_data["source"]
                self.output_local_rules.append(card)
                self.output_local_container.controls.append(card)
            
            for web_rule_data in output_data.get("web", {}).values():
                card = RuleCard("web", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "source" in web_rule_data:
                    card.url_field.value = web_rule_data["source"]
                if "xpath" in web_rule_data:
                    card.xpath_field.value = web_rule_data["xpath"]
                self.output_web_rules.append(card)
                self.output_web_container.controls.append(card)
            
            for rag_rule_data in output_data.get("rag", {}).values():
                card = RuleCard("rag", self.page, on_delete=self.delete_rule, on_change=self.on_change, editing_mode=False)
                if "faiss_file" in rag_rule_data:
                    card.path_field.value = rag_rule_data["faiss_file"]
                if "query" in rag_rule_data:
                    card.query_field.value = rag_rule_data["query"]
                if "top_k" in rag_rule_data:
                    card.topk_field.value = str(rag_rule_data["top_k"])
                if "chunk_size" in rag_rule_data:
                    card.chunk_field.value = str(rag_rule_data["chunk_size"])
                if "overlap" in rag_rule_data:
                    card.overlap_field.value = str(rag_rule_data["overlap"])
                if "filter" in rag_rule_data:
                    card.filter_field.value = rag_rule_data["filter"]
                self.output_rag_rules.append(card)
                self.output_rag_container.controls.append(card)

        self.page.update()

    def sync_ui_to_yaml(self):
        if "prompt" not in self.yaml_data:
            self.yaml_data["prompt"] = {}

        if self.query_input:
            self.yaml_data["prompt"]["query"] = self.query_input.value or ""

        instruction = {}
        if self.instruction_base and self.instruction_base.value:
            lines = [l.strip() for l in self.instruction_base.value.split("\n") if l.strip()]
            if lines:
                instruction["base"] = lines
        if self.instruction_additional and self.instruction_additional.value:
            lines = [l.strip() for l in self.instruction_additional.value.split("\n") if l.strip()]
            if lines:
                instruction["additional"] = lines
        if instruction:
            self.yaml_data["prompt"]["instruction"] = instruction

        context = {}
        if self.context_base and self.context_base.value:
            lines = [l.strip() for l in self.context_base.value.split("\n") if l.strip()]
            if lines:
                context["base"] = lines
        
        # Add context rules as dictionaries with generated names
        context_rules = {"local": {}, "web": {}, "rag": {}}
        
        for idx, card in enumerate(self.context_local_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                context_rules["local"][f"local_{idx}"] = rule_dict
        
        for idx, card in enumerate(self.context_web_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                context_rules["web"][f"web_{idx}"] = rule_dict
        
        for idx, card in enumerate(self.context_rag_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                context_rules["rag"][f"rag_{idx}"] = rule_dict
        
        # Always update or clear rule types
        for rule_type, rules in context_rules.items():
            if rules:
                context[rule_type] = rules
            elif rule_type in context:
                # Remove empty rule type
                del context[rule_type]
        
        if context:
            self.yaml_data["prompt"]["context"] = context
        elif "context" in self.yaml_data["prompt"]:
            del self.yaml_data["prompt"]["context"]

        output = {}
        if self.output_base and self.output_base.value:
            lines = [l.strip() for l in self.output_base.value.split("\n") if l.strip()]
            if lines:
                output["base"] = lines
        
        # Add output rules as dictionaries with generated names
        output_rules = {"local": {}, "web": {}, "rag": {}}
        
        for idx, card in enumerate(self.output_local_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                output_rules["local"][f"local_{idx}"] = rule_dict
        
        for idx, card in enumerate(self.output_web_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                output_rules["web"][f"web_{idx}"] = rule_dict
        
        for idx, card in enumerate(self.output_rag_rules, 1):
            rule_dict = card.to_dict()
            if rule_dict:
                output_rules["rag"][f"rag_{idx}"] = rule_dict
        
        # Always update or clear rule types
        for rule_type, rules in output_rules.items():
            if rules:
                output[rule_type] = rules
            elif rule_type in output:
                # Remove empty rule type
                del output[rule_type]
        
        if output:
            self.yaml_data["prompt"]["output"] = output
        elif "output" in self.yaml_data["prompt"]:
            del self.yaml_data["prompt"]["output"]

    def on_yaml_change(self):
        try:
            if self.yaml_editor and self.yaml_editor.value:
                self.yaml_data = yaml.safe_load(self.yaml_editor.value) or {}
        except Exception:
            pass

    def on_change(self):
        """Auto-sync changes to YAML when rules are modified"""
        self.sync_ui_to_yaml()
        if self.current_file_path:
            try:
                with open(self.current_file_path, "w", encoding="utf-8") as f:
                    yaml.dump(self.yaml_data, f, default_flow_style=False, sort_keys=False)
            except Exception:
                pass  # Silently ignore save errors to avoid interrupting user workflow

    def show_status(self, message: str, color: str):
        if self.status_text:
            self.status_text.value = message
            self.status_text.color = color
            parent = self.status_text.parent
            if parent:
                parent.visible = True
            self.page.update()

            import time
            import threading

            def hide():
                time.sleep(3)
                if self.status_text and self.status_text.parent:
                    self.status_text.parent.visible = False
                    self.page.update()

            threading.Thread(target=hide, daemon=True).start()


def start_flet_gui():
    def main(page: ft.Page):
        PeacFletApp(page)

    ft.app(target=main)


if __name__ == "__main__":
    start_flet_gui()
