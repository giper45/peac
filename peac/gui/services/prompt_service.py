from __future__ import annotations
import os
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
import traceback

from peac.core.peac import PromptYaml


class PromptService:
    @staticmethod
    def generate_prompt_sentence(yaml_data: Dict[str, Any], working_dir: Optional[str] = None) -> str:
        """Generate prompt via PromptYaml using a temporary yaml file.
        
        Args:
            yaml_data: The YAML data to process
            working_dir: Directory where to create temp file (default: system temp dir)
        """
        print(f"[DEBUG PromptService] Starting with yaml_data: {yaml_data}")
        print(f"[DEBUG PromptService] Working directory: {working_dir}")
        
        # Create temp file in working directory if specified
        if working_dir and os.path.isdir(working_dir):
            tmp_path = os.path.join(working_dir, ".peac_temp.yaml")
            print(f"[DEBUG PromptService] Creating temp file in working dir: {tmp_path}")
            with open(tmp_path, 'w', encoding='utf-8') as tmp:
                yaml.dump(yaml_data, tmp, default_flow_style=False, sort_keys=False)
        else:
            # Fallback to system temp directory
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding='utf-8') as tmp:
                yaml.dump(yaml_data, tmp, default_flow_style=False, sort_keys=False)
                tmp_path = tmp.name
        
        print(f"[DEBUG PromptService] Created temp file: {tmp_path}")
        
        # Read and print the temp file content
        try:
            with open(tmp_path, 'r') as f:
                content = f.read()
                print(f"[DEBUG PromptService] Temp file content:\n{content}")
        except Exception as e:
            print(f"[ERROR PromptService] Cannot read temp file: {e}")

        try:
            # Check if extends file exists
            if 'extends' in yaml_data:
                extends = yaml_data['extends']
                extends_list = [extends] if isinstance(extends, str) else extends
                for ext in extends_list:
                    ext_path = ext if isinstance(ext, str) else ext.get('source', '')
                    if ext_path:
                        exists = os.path.exists(ext_path)
                        print(f"[DEBUG PromptService] Extends file '{ext_path}' exists: {exists}")
                        if exists:
                            try:
                                with open(ext_path, 'r') as f:
                                    ext_content = f.read()
                                    print(f"[DEBUG PromptService] Extends file content (first 200 chars):\n{ext_content[:200]}")
                            except Exception as e:
                                print(f"[ERROR PromptService] Cannot read extends file: {e}")
            
            print(f"[DEBUG PromptService] Creating PromptYaml instance...")
            prompt_yaml = PromptYaml(tmp_path)
            print(f"[DEBUG PromptService] Calling get_prompt_sentence()...")
            result = prompt_yaml.get_prompt_sentence()
            print(f"[DEBUG PromptService] Result length: {len(result) if result else 0}")
            return result
        except Exception as e:
            error_msg = f"Error in PromptService: {str(e)}\n{traceback.format_exc()}"
            print(f"[ERROR PromptService] {error_msg}")
            raise
        finally:
            try:
                os.unlink(tmp_path)
                print(f"[DEBUG PromptService] Cleaned up temp file")
            except Exception:
                pass
