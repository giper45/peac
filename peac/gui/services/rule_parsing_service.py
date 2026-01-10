"""
Rule Parsing Service

Handles parsing and loading of rules from YAML data into the UI.
Extracts rule sections and manages rule card creation and population.
"""
from __future__ import annotations
from typing import Dict, Any, List
from peac.gui.models.rule import RuleData


class RuleParsingService:
    """Service for parsing rules from YAML data"""
    
    @staticmethod
    def extract_all_rules(prompt: Dict[str, Any]) -> tuple:
        """
        Extract all rules from prompt data (context and output sections).
        
        Returns tuple of:
        (ctx_local, ctx_web, ctx_rag, out_local, out_web, out_rag)
        """
        from peac.gui.services.yaml_service import YamlService
        
        context = prompt.get("context", {}) if isinstance(prompt.get("context"), dict) else {}
        output = prompt.get("output", {}) if isinstance(prompt.get("output"), dict) else {}

        ctx_local = YamlService.rules_from_yaml_section(context, "local")
        ctx_web = YamlService.rules_from_yaml_section(context, "web")
        ctx_rag = YamlService.rules_from_yaml_section(context, "rag")

        out_local = YamlService.rules_from_yaml_section(output, "local")
        out_web = YamlService.rules_from_yaml_section(output, "web")
        out_rag = YamlService.rules_from_yaml_section(output, "rag")

        return ctx_local, ctx_web, ctx_rag, out_local, out_web, out_rag
    
    @staticmethod
    def clear_rules_from_containers(containers: Dict[str, Any]) -> None:
        """
        Clear all rules from UI containers before loading new ones.
        
        Args:
            containers: Dict with keys like "context_local", "context_web", etc.
                       Values are tuples of (rule_list, container_control)
        """
        for container_key, (rule_list, container) in containers.items():
            if container and hasattr(container, 'controls'):
                container.controls.clear()
            rule_list.clear()
    
    @staticmethod
    def prepare_rule_containers(file_tab) -> Dict[str, tuple]:
        """
        Prepare a dict mapping container names to (rule_list, container_control) tuples.
        
        Args:
            file_tab: The FileTab instance
            
        Returns:
            Dict with keys: context_local, context_web, context_rag, output_local, output_web, output_rag
        """
        return {
            "context_local": (file_tab.context_local_rules, file_tab.context_local_container),
            "context_web": (file_tab.context_web_rules, file_tab.context_web_container),
            "context_rag": (file_tab.context_rag_rules, file_tab.context_rag_container),
            "output_local": (file_tab.output_local_rules, file_tab.output_local_container),
            "output_web": (file_tab.output_web_rules, file_tab.output_web_container),
            "output_rag": (file_tab.output_rag_rules, file_tab.output_rag_container),
        }
