from __future__ import annotations
from typing import Dict, Any, List, Tuple
import yaml
from peac.gui.models.rule import RuleData


class YamlService:
    @staticmethod
    def load_file(filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def save_file(filepath: str, data: Dict[str, Any]) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def ensure_prompt_root(data: Dict[str, Any]) -> Dict[str, Any]:
        if "prompt" not in data or not isinstance(data["prompt"], dict):
            data["prompt"] = {}
        return data

    @staticmethod
    def read_base_lines(section: Dict[str, Any], key: str) -> List[str]:
        val = section.get(key, [])
        if isinstance(val, list):
            return [str(x) for x in val]
        if val:
            return [str(val)]
        return []

    @staticmethod
    def write_base_lines(section: Dict[str, Any], key: str, text: str) -> None:
        lines = [l.strip() for l in (text or "").split("\n") if l.strip()]
        if lines:
            section[key] = lines
        elif key in section:
            del section[key]

    @staticmethod
    def rules_from_yaml_section(section: Dict[str, Any], rule_type: str) -> List[RuleData]:
        """Convert section['local'|'web'|'rag'] dict -> list of RuleData."""
        out: List[RuleData] = []
        blob = section.get(rule_type, {})
        if not isinstance(blob, dict):
            return out

        for _name, payload in blob.items():
            if not isinstance(payload, dict):
                continue

            if rule_type == "local":
                out.append(RuleData(
                    type="local",
                    name=_name,
                    source=payload.get("source"),
                    recursive=payload.get("recursive", False),
                    extension=payload.get("extension"),
                    filter=payload.get("filter"),
                ))

            elif rule_type == "web":
                out.append(RuleData(type="web", name=_name, url=payload.get("source"), xpath=payload.get("xpath")))

            elif rule_type == "rag":
                out.append(
                    RuleData(
                        type="rag",
                        name=_name,
                        faiss_file=payload.get("faiss_file"),
                        query=payload.get("query"),
                        top_k=_safe_int(payload.get("top_k")),
                        chunk_size=_safe_int(payload.get("chunk_size")),
                        overlap=_safe_int(payload.get("overlap")),
                        filter_regex=payload.get("filter"),
                    )
                )

        return out

    @staticmethod
    def rules_to_yaml_section(section: Dict[str, Any], rule_type: str, rules: List[RuleData]) -> None:
        """Write rules into section under local/web/rag using their names."""
        out: Dict[str, Any] = {}
        for r in rules:
            d = r.to_yaml_dict()
            if d:
                # Use rule name if available, otherwise generate one
                rule_key = r.name if r.name else f"{rule_type}_{len(out) + 1}"
                out[rule_key] = d

        if out:
            section[rule_type] = out
        else:
            section.pop(rule_type, None)

    @staticmethod
    def extract_all_rules(prompt: Dict[str, Any]) -> Tuple[List[RuleData], List[RuleData], List[RuleData],
                                                          List[RuleData], List[RuleData], List[RuleData]]:
        context = prompt.get("context", {}) if isinstance(prompt.get("context"), dict) else {}
        output = prompt.get("output", {}) if isinstance(prompt.get("output"), dict) else {}

        ctx_local = YamlService.rules_from_yaml_section(context, "local")
        ctx_web = YamlService.rules_from_yaml_section(context, "web")
        ctx_rag = YamlService.rules_from_yaml_section(context, "rag")

        out_local = YamlService.rules_from_yaml_section(output, "local")
        out_web = YamlService.rules_from_yaml_section(output, "web")
        out_rag = YamlService.rules_from_yaml_section(output, "rag")

        return ctx_local, ctx_web, ctx_rag, out_local, out_web, out_rag


def _safe_int(x):
    try:
        if x is None:
            return None
        return int(x)
    except Exception:
        return None
