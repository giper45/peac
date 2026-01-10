from __future__ import annotations
import flet as ft
from typing import Optional, List, Callable
from peac.gui.models.rule import RuleData, RuleType
from peac.gui.services.path_resolver_service import PathResolverService


class RuleCard(ft.Container):
    def __init__(
        self,
        rule_type: RuleType,
        page: ft.Page,
        rule_name: str = "",
        on_delete=None,
        on_change=None,
        editing_mode: bool = True,
        get_base_dir: Optional[Callable[[], Optional[str]]] = None,
    ):
        super().__init__()
        self.rule_type = rule_type
        self.rule_name = rule_name or f"New {rule_type.title()} Rule"
        self.on_delete = on_delete
        self.on_change = on_change
        self.page = page
        self.editing_mode = editing_mode
        self.get_base_dir = get_base_dir  # Callback to get base directory for path resolution

        # Styling
        self.padding = 20
        self.bgcolor = "#ffffff"
        self.border_radius = 12

        # Fields
        self.name_field: Optional[ft.TextField] = None
        self.preamble_field: Optional[ft.TextField] = None
        self.path_field: Optional[ft.TextField] = None

        self.url_field: Optional[ft.TextField] = None
        self.xpath_field: Optional[ft.TextField] = None

        # Local-specific fields
        self.recursive_checkbox: Optional[ft.Checkbox] = None
        self.extension_field: Optional[ft.TextField] = None
        self.local_filter_field: Optional[ft.TextField] = None

        # RAG-specific fields
        self.query_field: Optional[ft.TextField] = None
        self.source_folder_field: Optional[ft.TextField] = None  # Folder to embed if FAISS doesn't exist
        self.model_dropdown: Optional[ft.Dropdown] = None  # Embedding model selection
        self.force_override_checkbox: Optional[ft.Checkbox] = None  # Force recreate FAISS
        self.topk_field: Optional[ft.TextField] = None
        self.chunk_field: Optional[ft.TextField] = None
        self.overlap_field: Optional[ft.TextField] = None
        self.filter_field: Optional[ft.TextField] = None

        self.edit_save_button: Optional[ft.IconButton] = None

        self.all_fields: List[ft.TextField] = []
        self.browse_buttons: List[ft.IconButton] = []

        self._state_hint: Optional[ft.Container] = None

        self._build()
        self.apply_visual_state()
        if self.editing_mode:
            self.focus_first_field()

    # ---------- UI ----------
    def _build(self):
        self.name_field = ft.TextField(
            value=self.rule_name,
            label="Rule Name",
            expand=True,
            on_change=self._sanitize_name,
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
            on_change=self._on_change,
            border_color="#e5e7eb",
            read_only=not self.editing_mode,
        )
        self.all_fields.append(self.preamble_field)

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

        specific = self._build_specific_fields()

        self.content = ft.Column(
            [
                header,
                state_hint,
                ft.Divider(height=1, color="#e5e7eb"),
                ft.Column(
                    [
                        ft.Text("Preamble:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                        self.preamble_field,
                    ],
                    spacing=8,
                ),
                *specific,
            ],
            spacing=15,
        )

    def _build_specific_fields(self):
        fields: List[ft.Control] = []

        if self.rule_type == "local":
            self.path_field = ft.TextField(
                label="File or folder path",
                expand=True,
                on_change=self._on_change,
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.path_field)

            browse_file_btn = ft.IconButton(
                ft.icons.INSERT_DRIVE_FILE,
                icon_color="#1877f2",
                tooltip="Browse Files",
                on_click=lambda _: self.pick_file_local(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            
            browse_folder_btn = ft.IconButton(
                ft.icons.FOLDER_OPEN,
                icon_color="#2ecc71",
                tooltip="Browse Folders",
                on_click=lambda _: self.pick_folder_local(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            self.browse_buttons.extend([browse_file_btn, browse_folder_btn])

            # Recursive checkbox
            self.recursive_checkbox = ft.Checkbox(
                label="Recursive",
                value=False,
                on_change=self._on_change,
                disabled=not self.editing_mode,
            )

            # Extension filter
            self.extension_field = ft.TextField(
                label="Extension (e.g., py, txt, *)",
                hint_text="* for all files",
                value="*",
                on_change=self._on_change,
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.extension_field)

            # Regex filter
            self.local_filter_field = ft.TextField(
                label="Regex Filter (optional)",
                hint_text="e.g., ^test_.*\.py$",
                on_change=self._on_change,
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.local_filter_field)

            fields.append(
                ft.Column(
                    [
                        ft.Text("Source Path:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                        ft.Row([self.path_field, browse_file_btn, browse_folder_btn], spacing=8),
                        self.recursive_checkbox,
                        ft.Row(
                            [self.extension_field, self.local_filter_field],
                            spacing=8,
                        ),
                    ],
                    spacing=4,
                )
            )

        elif self.rule_type == "web":
            self.url_field = ft.TextField(
                label="https://example.com/page",
                on_change=self._on_change,
                border_color="#e5e7eb",
                read_only=not self.editing_mode,
            )
            self.xpath_field = ft.TextField(
                label="//div[@class='content']",
                on_change=self._on_change,
                border_color="#e5e7eb",
                hint_text="Leave empty to scrape entire page",
                read_only=not self.editing_mode,
            )
            self.all_fields.extend([self.url_field, self.xpath_field])

            fields.extend(
                [
                    ft.Column(
                        [ft.Text("Source URL:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"), self.url_field],
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
            # FAISS Index File
            self.path_field = ft.TextField(
                label="Path to FAISS file (.faiss)",
                on_change=self._on_change,
                expand=True,
                border_color="#e5e7eb",
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.path_field)

            browse_faiss = ft.IconButton(
                ft.icons.FOLDER_OPEN,
                icon_color="#1877f2",
                tooltip="Browse FAISS file",
                on_click=lambda _: self.pick_file(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            self.browse_buttons.append(browse_faiss)
            
            # Source Folder (to embed if FAISS doesn't exist)
            self.source_folder_field = ft.TextField(
                label="Source folder to embed if FAISS doesn't exist",
                on_change=self._on_change,
                expand=True,
                border_color="#e5e7eb",
                hint_text="Leave empty if FAISS already exists",
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.source_folder_field)
            
            browse_folder = ft.IconButton(
                ft.icons.FOLDER,
                icon_color="#1877f2",
                tooltip="Browse source folder",
                on_click=lambda _: self.pick_folder(),
                icon_size=24,
                disabled=not self.editing_mode,
            )
            self.browse_buttons.append(browse_folder)

            # Search Query
            self.query_field = ft.TextField(
                label="What to search for in the index",
                on_change=self._on_change,
                border_color="#e5e7eb",
                hint_text="e.g., 'Python best practices'",
                read_only=not self.editing_mode,
            )
            self.all_fields.append(self.query_field)
            
            # Embedding Model Dropdown
            self.model_dropdown = ft.Dropdown(
                label="Embedding Model",
                options=[
                    ft.dropdown.Option("all-MiniLM-L6-v2"),
                    ft.dropdown.Option("paraphrase-multilingual-MiniLM-L12-v2"),
                    ft.dropdown.Option("all-mpnet-base-v2"),
                    ft.dropdown.Option("multi-qa-MiniLM-L6-cos-v1"),
                    ft.dropdown.Option("paraphrase-MiniLM-L6-v2"),
                ],
                value="all-MiniLM-L6-v2",
                on_change=self._on_change,
                border_color="#e5e7eb",
                disabled=not self.editing_mode,
            )
            
            # Force Override Checkbox
            self.force_override_checkbox = ft.Checkbox(
                label="Force Recreate FAISS Index",
                value=False,
                on_change=self._on_change,
                disabled=not self.editing_mode,
            )
            
            # RAG Parameters
            self.topk_field = ft.TextField(
                value="5", 
                width=100, 
                label="Top K",
                on_change=self._on_change, 
                read_only=not self.editing_mode,
                border_color="#e5e7eb"
            )
            self.chunk_field = ft.TextField(
                value="512", 
                width=100,
                label="Chunk Size", 
                on_change=self._on_change, 
                read_only=not self.editing_mode,
                border_color="#e5e7eb"
            )
            self.overlap_field = ft.TextField(
                value="50", 
                width=100,
                label="Overlap", 
                on_change=self._on_change, 
                read_only=not self.editing_mode,
                border_color="#e5e7eb"
            )
            
            # Filter Regex
            self.filter_field = ft.TextField(
                label="Regex pattern for post-filtering",
                on_change=self._on_change,
                border_color="#e5e7eb",
                hint_text="e.g., .*python.* (optional)",
                read_only=not self.editing_mode,
            )
            self.all_fields.extend([self.topk_field, self.chunk_field, self.overlap_field, self.filter_field])

            fields.extend(
                [
                    ft.Column(
                        [
                            ft.Text("FAISS Index File:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row([self.path_field, browse_faiss], spacing=8),
                        ],
                        spacing=8,
                    ),
                    ft.Column(
                        [
                            ft.Text("Source Folder (for embedding):", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row([self.source_folder_field, browse_folder], spacing=8),
                        ],
                        spacing=8,
                    ),
                    ft.Column(
                        [ft.Text("Search Query:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"), self.query_field],
                        spacing=8,
                    ),
                    ft.Column(
                        [
                            ft.Text("Embedding Configuration:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row([
                                self.model_dropdown,
                                self.force_override_checkbox,
                            ], spacing=15),
                        ],
                        spacing=8,
                    ),
                    ft.Column(
                        [
                            ft.Text("RAG Parameters:", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"),
                            ft.Row(
                                [
                                    self.topk_field,
                                    self.chunk_field,
                                    self.overlap_field,
                                ],
                                spacing=15,
                            ),
                        ],
                        spacing=4,
                    ),
                    ft.Column(
                        [ft.Text("Filter Regex (optional):", weight=ft.FontWeight.BOLD, size=14, color="#1f2937"), self.filter_field],
                        spacing=4,
                    ),
                ]
            )

        return fields

    # ---------- Behavior ----------
    def apply_visual_state(self):
        if self.editing_mode:
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

        if self._state_hint:
            self._state_hint.visible = self.editing_mode

    def focus_first_field(self):
        try:
            if self.rule_type in ("local", "rag") and self.path_field:
                self.path_field.focus()
            elif self.rule_type == "web" and self.url_field:
                self.url_field.focus()
            elif self.name_field:
                self.name_field.focus()
        except Exception:
            pass

    def toggle_editing_mode(self):
        self.editing_mode = not self.editing_mode

        for f in self.all_fields:
            f.read_only = not self.editing_mode
        for b in self.browse_buttons:
            b.disabled = not self.editing_mode

        # Handle checkboxes separately
        if self.recursive_checkbox:
            self.recursive_checkbox.disabled = not self.editing_mode
        if self.force_override_checkbox:
            self.force_override_checkbox.disabled = not self.editing_mode
        
        # Handle dropdown
        if self.model_dropdown:
            self.model_dropdown.disabled = not self.editing_mode

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

    def pick_file(self):
        """Pick file for local/extends rules or directory for local rules"""
        def on_result(e: ft.FilePickerResultEvent):
            if self.path_field:
                # Handle both files (from pick_files) and directory (from get_directory_path)
                selected_path = None
                if e.files and len(e.files) > 0:
                    selected_path = e.files[0].path
                elif e.path:  # Directory picker result
                    selected_path = e.path
                
                if selected_path:
                    # Normalize path (remove platform-specific prefixes)
                    selected_path = PathResolverService.normalize_path(selected_path)
                    # Convert to relative path if we have a base directory
                    if self.get_base_dir:
                        base_dir = self.get_base_dir()
                        if base_dir:
                            selected_path = PathResolverService.get_relative_path(selected_path, base_dir)
                    self.path_field.value = selected_path
                    self.path_field.update()
                    self._on_change()

        fp = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(fp)
        self.page.update()

        if self.rule_type == "rag":
            fp.pick_files(dialog_title="Select FAISS index file", allowed_extensions=["faiss", "index"], allow_multiple=False)
        elif self.rule_type == "local":
            # For local rules, allow picking both files and directories
            # Use wildcard to show all files on Windows
            fp.pick_files(dialog_title="Select file or folder", allowed_extensions=["*"], allow_multiple=False)
        else:
            # For extends rules, pick files
            fp.pick_files(dialog_title="Select configuration file", allow_multiple=False)
    
    def pick_file_local(self):
        """Pick file for local rules"""
        def on_result(e: ft.FilePickerResultEvent):
            if self.path_field and e.files and len(e.files) > 0:
                selected_path = e.files[0].path
                # Normalize path (remove platform-specific prefixes)
                selected_path = PathResolverService.normalize_path(selected_path)
                # Convert to relative path if we have a base directory
                if self.get_base_dir:
                    base_dir = self.get_base_dir()
                    if base_dir:
                        selected_path = PathResolverService.get_relative_path(selected_path, base_dir)
                self.path_field.value = selected_path
                self.path_field.update()
                self._on_change()

        fp = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(fp)
        self.page.update()
        fp.pick_files(dialog_title="Select file", allowed_extensions=["*"], allow_multiple=False)
    
    def pick_folder_local(self):
        """Pick folder for local rules"""
        def on_result(e: ft.FilePickerResultEvent):
            if self.path_field and e.path:
                selected_path = e.path
                # Normalize path (remove platform-specific prefixes)
                selected_path = PathResolverService.normalize_path(selected_path)
                # Convert to relative path if we have a base directory
                if self.get_base_dir:
                    base_dir = self.get_base_dir()
                    if base_dir:
                        selected_path = PathResolverService.get_relative_path(selected_path, base_dir)
                self.path_field.value = selected_path
                self.path_field.update()
                self._on_change()

        fp = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(fp)
        self.page.update()
        fp.get_directory_path(dialog_title="Select folder")
        """Pick folder for RAG source directory"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.path and self.source_folder_field:
                selected_path = e.path
                # Normalize path (remove platform-specific prefixes)
                selected_path = PathResolverService.normalize_path(selected_path)
                # Convert to relative path if we have a base directory
                if self.get_base_dir:
                    base_dir = self.get_base_dir()
                    if base_dir:
                        selected_path = PathResolverService.get_relative_path(selected_path, base_dir)
                self.source_folder_field.value = selected_path
                self.source_folder_field.update()
                self._on_change()

        fp = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(fp)
        self.page.update()
        fp.get_directory_path(dialog_title="Select source folder for embedding")

    def to_rule_data(self) -> RuleData:
        """Map UI -> RuleData"""
        rd = RuleData(type=self.rule_type)
        # Sanitize rule name: no spaces, replace with underscores
        raw_name = (self.name_field.value or "") if self.name_field else ""
        rd.name = raw_name.replace(" ", "_") if raw_name else ""
        rd.preamble = (self.preamble_field.value or "") if self.preamble_field else ""

        if self.rule_type == "local":
            rd.source = (self.path_field.value or "") if self.path_field else None
            rd.recursive = self.recursive_checkbox.value if self.recursive_checkbox else False
            rd.extension = (self.extension_field.value or None) if self.extension_field else None
            rd.filter = (self.local_filter_field.value or None) if self.local_filter_field else None

        elif self.rule_type == "web":
            rd.url = (self.url_field.value or "") if self.url_field else None
            rd.xpath = (self.xpath_field.value or "") if self.xpath_field else None

        elif self.rule_type == "rag":
            rd.faiss_file = (self.path_field.value or "") if self.path_field else None
            rd.source_folder = (self.source_folder_field.value or "") if self.source_folder_field else None
            rd.query = (self.query_field.value or "") if self.query_field else None
            rd.embedding_model = (self.model_dropdown.value or "all-MiniLM-L6-v2") if self.model_dropdown else "all-MiniLM-L6-v2"
            rd.force_override = self.force_override_checkbox.value if self.force_override_checkbox else False
            rd.top_k = _safe_int(self.topk_field.value if self.topk_field else None)
            rd.chunk_size = _safe_int(self.chunk_field.value if self.chunk_field else None)
            rd.overlap = _safe_int(self.overlap_field.value if self.overlap_field else None)
            rd.filter_regex = (self.filter_field.value or "") if self.filter_field else None

        return rd

    def fill_from_rule_data(self, rd: RuleData):
        """Map RuleData -> UI"""
        if self.name_field:
            self.name_field.value = rd.name or self.rule_name
        if self.preamble_field:
            self.preamble_field.value = rd.preamble or ""

        if self.rule_type == "local" and self.path_field:
            self.path_field.value = rd.source or ""
            if self.recursive_checkbox:
                self.recursive_checkbox.value = rd.recursive or False
            if self.extension_field:
                self.extension_field.value = rd.extension or "*"
            if self.local_filter_field:
                self.local_filter_field.value = rd.filter or ""

        if self.rule_type == "web":
            if self.url_field:
                self.url_field.value = rd.url or ""
            if self.xpath_field:
                self.xpath_field.value = rd.xpath or ""

        if self.rule_type == "rag":
            if self.path_field:
                self.path_field.value = rd.faiss_file or ""
            if self.source_folder_field:
                self.source_folder_field.value = rd.source_folder or ""
            if self.query_field:
                self.query_field.value = rd.query or ""
            if self.model_dropdown:
                self.model_dropdown.value = rd.embedding_model or "all-MiniLM-L6-v2"
            if self.force_override_checkbox:
                self.force_override_checkbox.value = rd.force_override or False
            if self.topk_field and rd.top_k is not None:
                self.topk_field.value = str(rd.top_k)
            if self.chunk_field and rd.chunk_size is not None:
                self.chunk_field.value = str(rd.chunk_size)
            if self.overlap_field and rd.overlap is not None:
                self.overlap_field.value = str(rd.overlap)
            if self.filter_field:
                self.filter_field.value = rd.filter_regex or ""

    def _sanitize_name(self, e=None):
        """Sanitize rule name: replace spaces with underscores and trigger change"""
        if self.name_field and self.name_field.value:
            # Replace spaces with underscores
            sanitized = self.name_field.value.replace(" ", "_")
            if sanitized != self.name_field.value:
                self.name_field.value = sanitized
        self._on_change()

    def _on_change(self, e=None):
        if self.on_change:
            self.on_change()


def _safe_int(x):
    try:
        if x is None:
            return None
        s = str(x).strip()
        if not s:
            return None
        return int(s)
    except Exception:
        return None
