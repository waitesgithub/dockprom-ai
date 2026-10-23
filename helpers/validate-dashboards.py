#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "grafana" / "dashboards"
SUPPORTED_PANEL_TYPES = {"timeseries", "stat", "table"}


def main():
    dashboards = sorted(DASHBOARD_DIR.glob("*.json"))
    if not dashboards:
        raise SystemExit("No Grafana dashboards found")

    for path in dashboards:
        dashboard = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(dashboard.get("schemaVersion"), int) or dashboard["schemaVersion"] < 41:
            raise SystemExit(f"{path.name}: schemaVersion must be 41 or newer")
        if not isinstance(dashboard.get("panels"), list) or not dashboard["panels"]:
            raise SystemExit(f"{path.name}: dashboard must contain panels")

        for panel in dashboard["panels"]:
            if panel.get("type") not in SUPPORTED_PANEL_TYPES:
                raise SystemExit(f"{path.name}: unsupported panel type {panel.get('type')!r}")
            field_config = panel.get("fieldConfig")
            if not isinstance(field_config, dict) or not isinstance(field_config.get("defaults"), dict):
                raise SystemExit(f"{path.name}: panel {panel.get('id')} needs fieldConfig.defaults")
            if not isinstance(field_config.get("overrides"), list):
                raise SystemExit(f"{path.name}: panel {panel.get('id')} needs fieldConfig.overrides")
            grid_pos = panel.get("gridPos", {})
            if not all(isinstance(grid_pos.get(key), int) for key in ("h", "w", "x", "y")):
                raise SystemExit(f"{path.name}: panel {panel.get('id')} needs a valid gridPos")

        print(f"Validated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
