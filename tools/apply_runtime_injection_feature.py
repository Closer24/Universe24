"""Apply the bounded runtime-disturbance injection and workspace editor change."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"expected one patch anchor in {path}: {old[:80]!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


def append_once(path: str, marker: str, addition: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if marker in text:
        return
    target.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


replace_once(
    "src/event_universe/core/disturbance_state.py",
    "MAX_RULES = 32\nMAX_EXPRESSION_NODES = 64\n",
    "MAX_RULES = 32\nMAX_RUNTIME_INJECTIONS = 256\nMAX_EXPRESSION_NODES = 64\n",
)
replace_once(
    "src/event_universe/core/disturbance_state.py",
    "@dataclass(frozen=True, slots=True)\nclass Seed:\n    position: Address3\n    record: DisturbanceRecord\n\n\n@dataclass(frozen=True, slots=True)\nclass InitialState:\n",
    "@dataclass(frozen=True, slots=True)\nclass Seed:\n    position: Address3\n    record: DisturbanceRecord\n\n\n@dataclass(frozen=True, slots=True)\nclass RuntimeInjection:\n    tick: int\n    position: Address3\n    record: DisturbanceRecord\n\n\n@dataclass(frozen=True, slots=True)\nclass InitialState:\n",
)
replace_once(
    "src/event_universe/core/disturbance_state.py",
    "    event_program: str | None = None\n",
    "    event_program: str | None = None\n    runtime_injections: tuple[RuntimeInjection, ...] = ()\n",
)

replace_once(
    "src/event_universe/initialization.py",
    "    MAX_RULES,\n    MAX_SLOTS,\n",
    "    MAX_RULES,\n    MAX_RUNTIME_INJECTIONS,\n    MAX_SLOTS,\n",
)
replace_once(
    "src/event_universe/initialization.py",
    "    Seed,\n    TransportDefinition,\n",
    "    RuntimeInjection,\n    Seed,\n    TransportDefinition,\n",
)
replace_once(
    "src/event_universe/initialization.py",
    "    return tuple(result)\n\n\ndef _decay(value: object) -> DecayDefinition:\n",
    """    return tuple(result)\n\n\ndef _runtime_injections(\n    value: object,\n    fields: tuple[FieldDefinition, ...],\n    disturbances: tuple[DisturbanceDefinition, ...],\n    shape: Address3,\n    capacity: int,\n) -> tuple[RuntimeInjection, ...]:\n    result: list[RuntimeInjection] = []\n    occupied: dict[tuple[int, Address3], int] = {}\n    names = _names(disturbances)\n    phases = tuple(pack((0,) * field.components) for field in fields)\n    for index, raw in enumerate(\n        _array(value, \"runtime_injections\", MAX_RUNTIME_INJECTIONS)\n    ):\n        obj = _object(\n            raw,\n            f\"runtime_injections[{index}]\",\n            {\"tick\", \"position\", \"type\", \"values\"},\n            {\"tick\", \"position\", \"type\"},\n        )\n        tick = _integer(obj[\"tick\"], f\"runtime_injections[{index}].tick\", 1)\n        position = _address(obj[\"position\"], f\"runtime_injections[{index}].position\", 0)\n        if any(coordinate >= length for coordinate, length in zip(position, shape, strict=True)):\n            raise ValueError(\"runtime injection position must be within shape\")\n        key = (tick, position)\n        occupied[key] = occupied.get(key, 0) + 1\n        if occupied[key] > capacity:\n            raise ValueError(\n                \"runtime injections at the same tick and position exceed slots_per_cell\"\n            )\n        type_index = _index(obj[\"type\"], names, f\"runtime_injections[{index}].type\")\n        definition = disturbances[type_index]\n        values = _values(\n            obj.get(\"values\", {}), fields, definition.fields, definition.defaults\n        )\n        result.append(\n            RuntimeInjection(\n                tick, position, DisturbanceRecord(type_index, values, phases)\n            )\n        )\n    return tuple(result)\n\n\ndef _decay(value: object) -> DecayDefinition:\n""",
)
replace_once(
    "src/event_universe/initialization.py",
    "            \"event_program\",\n            \"observer\",\n",
    "            \"event_program\",\n            \"observer\",\n            \"runtime_injections\",\n",
)
replace_once(
    "src/event_universe/initialization.py",
    "        seeds=_seeds(obj[\"seeds\"], fields, disturbances, shape, capacity),\n        spatial_fields=spatial,\n",
    "        seeds=_seeds(obj[\"seeds\"], fields, disturbances, shape, capacity),\n        runtime_injections=_runtime_injections(\n            obj.get(\"runtime_injections\", []), fields, disturbances, shape, capacity\n        ),\n        spatial_fields=spatial,\n",
)

replace_once(
    "src/event_universe/core/disturbance_engine.py",
    "    PendingCycle,\n    bounded,\n",
    "    PendingCycle,\n    RuntimeInjection,\n    bounded,\n",
)
replace_once(
    "src/event_universe/core/disturbance_engine.py",
    "        self._escaped_totals = [[0] * f.components for f in initial.fields]\n        self._coupled_types = {rule.type_index for rule in initial.spatial_couplings} | {\n",
    """        self._escaped_totals = [[0] * f.components for f in initial.fields]\n        schedule: dict[int, list[RuntimeInjection]] = {}\n        for injection in initial.runtime_injections:\n            schedule.setdefault(injection.tick, []).append(injection)\n        self._runtime_injections = {\n            tick: tuple(injections) for tick, injections in schedule.items()\n        }\n        self._runtime_injections_applied = 0\n        self._coupled_types = {rule.type_index for rule in initial.spatial_couplings} | {\n""",
)
replace_once(
    "src/event_universe/core/disturbance_engine.py",
    "        report: dict[str, object] = {\n            \"model_operations_cost\": self._model_work,\n            \"local_cycles_started\": self._local_cycles,\n        }\n",
    """        report: dict[str, object] = {\n            \"model_operations_cost\": self._model_work,\n            \"local_cycles_started\": self._local_cycles,\n            \"runtime_injections_scheduled\": len(self.initial.runtime_injections),\n            \"runtime_injections_applied\": self._runtime_injections_applied,\n        }\n""",
)
replace_once(
    "src/event_universe/core/disturbance_engine.py",
    "    def step(self) -> None:\n",
    """    def _inject_due(self) -> None:\n        injections = self._runtime_injections.get(self.tick, ())\n        if not injections:\n            return\n        grouped: dict[Address3, list[RuntimeInjection]] = {}\n        for injection in injections:\n            grouped.setdefault(injection.position, []).append(injection)\n        for position, local in grouped.items():\n            cell = self._cells.get(position)\n            if cell is not None and cell.pending is not None:\n                raise ValueError(\n                    \"runtime injection cannot modify a cell with a pending local cycle\"\n                )\n            free = (\n                self.initial.slots_per_cell\n                if cell is None\n                else sum(record is None for record in cell.records)\n            )\n            if len(local) > free:\n                raise ValueError(\"runtime injection capacity exceeded\")\n        if self.event_space is not None:\n            self.event_space.require_room(len(injections))\n\n        committed: list[RuntimeInjection] = []\n        for injection in injections:\n            cell = self._at(injection.position)\n            records = list(cell.records)\n            slot = records.index(None)\n            records[slot] = injection.record\n            cell.records = tuple(records)\n            for field_index, payload in enumerate(injection.record.values):\n                for component, value in enumerate(unpack(payload)):\n                    self._source_totals[field_index][component] += value\n            committed.append(injection)\n        self._runtime_injections_applied += len(committed)\n\n        # Ownership and accounting commit before diagnostics can fail.\n        for injection in committed:\n            self._emit(\n                \"runtime_injected\",\n                injection.position,\n                disturbance=self.initial.disturbances[injection.record.type_index].name,\n                values=self.record_values(injection.record),\n            )\n\n    def step(self) -> None:\n""",
)
replace_once(
    "src/event_universe/core/disturbance_engine.py",
    "            for position in sorted(self._cells):\n                self._commit(position, self._cells[position])\n            if self._resolver is not None:\n",
    """            for position in sorted(self._cells):\n                self._commit(position, self._cells[position])\n            self._inject_due()\n            if self._resolver is not None:\n""",
)

replace_once(
    "src/event_universe/runner.py",
    '        "link_ticks": initial.link_ticks,\n        "computation": world.computation_report(),\n',
    '        "link_ticks": initial.link_ticks,\n        "runtime_injections_scheduled": len(initial.runtime_injections),\n        "computation": world.computation_report(),\n',
)

replace_once(
    "src/event_universe/ui.py",
    '        "seeds": len(initial.seeds),\n',
    '        "seeds": len(initial.seeds),\n        "runtime_injections": len(initial.runtime_injections),\n',
)

replace_once(
    "src/event_universe/ui_assets/index.html",
    '<button role="tab" aria-selected="true" aria-controls="editor-panel" data-tab="names">Names</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="general">General</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="fields">Fields</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="types">Disturbances</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="seeds">Initial state</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="rules">Rules &amp; costs</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="json">JSON</button></div>',
    '<button role="tab" aria-selected="true" aria-controls="editor-panel" data-tab="names">Names</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="general">General</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="fields">Fields</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="types">Disturbances</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="seeds">Initial state</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="timeline">Timed placement</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="rules">Rules &amp; costs</button><button role="tab" aria-selected="false" aria-controls="editor-panel" data-tab="json">JSON</button></div>',
)

replace_once(
    "src/event_universe/ui_assets/app.js",
    "let moviePath = null;\nlet drafts = {};\n",
    'let moviePath = null;\nlet placementType = "", placementPlane = "XY", placementTick = 1, placementLayer = 0;\nlet drafts = {};\n',
)
replace_once(
    "src/event_universe/ui_assets/app.js",
    '  $("#selected-description").textContent = `${templates.find(t => t.id === selected)?.name || "Custom configuration"} · ${configuration?.seeds?.length || 0} initial particles / records`;\n  $("#template-label").textContent = selected === "custom" ? "CUSTOM CONFIGURATION" : `${selected.toUpperCase()} TEMPLATE`;\n  const counts = [[configuration?.fields?.length || 0, "FIELDS"],\n    [configuration?.disturbance_types?.length || 0, "TYPES"], [configuration?.seeds?.length || 0, "SEEDS"]];\n',
    '  const scheduled = configuration?.runtime_injections?.length || 0;\n  $("#selected-description").textContent = `${templates.find(t => t.id === selected)?.name || "Custom configuration"} · ${configuration?.seeds?.length || 0} initial records · ${scheduled} timed injections`;\n  $("#template-label").textContent = selected === "custom" ? "CUSTOM CONFIGURATION" : `${selected.toUpperCase()} TEMPLATE`;\n  const counts = [[configuration?.fields?.length || 0, "FIELDS"],\n    [configuration?.disturbance_types?.length || 0, "TYPES"], [configuration?.seeds?.length || 0, "SEEDS"], [scheduled, "INJECTIONS"]];\n',
)
replace_once(
    "src/event_universe/ui_assets/app.js",
    "  drawPlacement();\n  $(\"#run\").disabled = !configuration || busy || loading || runs.some(run => run.status === \"running\");\n",
    "  drawPlacement();\n  redrawTimedPlacement();\n  $(\"#run\").disabled = !configuration || busy || loading || runs.some(run => run.status === \"running\");\n",
)

TIMED_PLACEMENT = r'''
const placementPlanes = {XY: [0, 1, 2], XZ: [0, 2, 1], YZ: [1, 2, 0]};

function placementAxes() { return placementPlanes[placementPlane] || placementPlanes.XY; }

function placementPosition(event, canvas) {
  const shape = configuration?.shape, [first, second, hidden] = placementAxes();
  if (!Array.isArray(shape) || shape.length !== 3) return null;
  const rect = canvas.getBoundingClientRect(), pad = 44;
  const x = (event.clientX - rect.left) * canvas.width / Math.max(1, rect.width);
  const y = (event.clientY - rect.top) * canvas.height / Math.max(1, rect.height);
  const usableX = Math.max(1, canvas.width - pad * 2), usableY = Math.max(1, canvas.height - pad * 2);
  const maxFirst = Math.max(0, shape[first] - 1), maxSecond = Math.max(0, shape[second] - 1);
  const firstValue = Math.max(0, Math.min(maxFirst, Math.round((x - pad) / usableX * maxFirst)));
  const secondValue = Math.max(0, Math.min(maxSecond, Math.round((canvas.height - pad - y) / usableY * maxSecond)));
  const position = [0, 0, 0];
  position[first] = firstValue; position[second] = secondValue;
  position[hidden] = Math.max(0, Math.min(shape[hidden] - 1, placementLayer));
  return position;
}

function appendRuntimeInjection(typeName, position) {
  if (!configuration || !typeName || !position) return;
  if (!Array.isArray(configuration.runtime_injections)) configuration.runtime_injections = [];
  configuration.runtime_injections.push({tick: placementTick, position, type: typeName});
  changed(); renderEditor();
}

function redrawTimedPlacement() {
  const canvas = document.querySelector("#timed-placement-canvas");
  if (!canvas || !configuration) return;
  const ctx = canvas.getContext("2d"), shape = configuration.shape, [first, second, hidden] = placementAxes();
  const pad = 44, usableX = canvas.width - pad * 2, usableY = canvas.height - pad * 2;
  const maxFirst = Math.max(0, shape[first] - 1), maxSecond = Math.max(0, shape[second] - 1);
  const project = position => [
    pad + (maxFirst ? position[first] / maxFirst : 0.5) * usableX,
    canvas.height - pad - (maxSecond ? position[second] / maxSecond : 0.5) * usableY,
  ];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#f7fbf8"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#d4e4d9"; ctx.lineWidth = 1;
  const grid = (axisMax, horizontal) => {
    const steps = Math.min(axisMax, 20);
    for (let i = 0; i <= steps; i++) {
      const fraction = steps ? i / steps : 0.5;
      ctx.beginPath();
      if (horizontal) { const y = canvas.height - pad - fraction * usableY; ctx.moveTo(pad, y); ctx.lineTo(canvas.width - pad, y); }
      else { const x = pad + fraction * usableX; ctx.moveTo(x, pad); ctx.lineTo(x, canvas.height - pad); }
      ctx.stroke();
    }
  };
  grid(maxFirst, false); grid(maxSecond, true);
  ctx.strokeStyle = "#8fb19a"; ctx.strokeRect(pad, pad, usableX, usableY);
  ctx.fillStyle = "#557363"; ctx.font = "14px Segoe UI, sans-serif";
  ctx.fillText(`${"XYZ"[first]} 0–${maxFirst}`, pad, canvas.height - 14);
  ctx.fillText(`${"XYZ"[second]} 0–${maxSecond}`, pad, 22);
  ctx.fillText(`${"XYZ"[hidden]} = ${placementLayer} · tick ${placementTick}`, canvas.width - 180, 22);

  const types = Array.isArray(configuration.disturbance_types) ? configuration.disturbance_types : [];
  const colorFor = name => colors[Math.max(0, types.findIndex(type => type.name === name)) % colors.length];
  for (const seed of configuration.seeds || []) {
    if (seed.position?.[hidden] !== placementLayer) continue;
    const [x, y] = project(seed.position); ctx.beginPath(); ctx.arc(x, y, 8, 0, Math.PI * 2);
    ctx.strokeStyle = colorFor(seed.type); ctx.lineWidth = 2; ctx.setLineDash([4, 3]); ctx.stroke(); ctx.setLineDash([]);
  }
  for (const item of configuration.runtime_injections || []) {
    if (item.tick !== placementTick || item.position?.[hidden] !== placementLayer) continue;
    const [x, y] = project(item.position), color = colorFor(item.type);
    ctx.beginPath(); ctx.arc(x, y, 9, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = "#294438"; ctx.font = "12px Segoe UI, sans-serif"; ctx.fillText(item.type, x + 12, y - 10);
  }
  const caption = document.querySelector("#placement-caption");
  if (caption) caption.textContent = `Selected ${placementPlane} slice · ${"XYZ"[hidden]}=${placementLayer} · injection tick ${placementTick}. Dashed rings are initial seeds.`;
}

function renderTimedPlacement(doc) {
  const editor = $("#editor-panel"), block = node("section", "", "timed-placement-editor");
  block.append(node("h4", "Timed disturbance placement"));
  block.append(node("p", "Drag a disturbance type onto a lattice node, or select a type and tap the grid. Each placement writes one generic runtime_injections entry.", "editor-description"));
  const types = Array.isArray(doc.disturbance_types) ? doc.disturbance_types : [];
  if (!types.some(type => type.name === placementType)) placementType = types[0]?.name || "";

  const toolbar = node("div", "", "placement-toolbar");
  const planeLabel = node("label", "", "field"), plane = document.createElement("select");
  planeLabel.append(node("span", "Projection"));
  for (const value of Object.keys(placementPlanes)) { const option = node("option", value); option.value = value; plane.append(option); }
  plane.value = placementPlane; plane.addEventListener("change", () => { placementPlane = plane.value; placementLayer = 0; renderEditor(); }); planeLabel.append(plane);
  const tickLabel = node("label", "", "field"), tick = document.createElement("input");
  tickLabel.append(node("span", "Injection tick")); tick.type = "number"; tick.min = "1"; tick.step = "1"; tick.inputMode = "numeric"; tick.value = String(placementTick);
  tick.addEventListener("input", () => { if (tick.validity.valid) { placementTick = Number(tick.value); redrawTimedPlacement(); } }); tickLabel.append(tick);
  const [,, hidden] = placementAxes(), layerLabel = node("label", "", "field"), layer = document.createElement("input");
  layerLabel.append(node("span", `${"XYZ"[hidden]} layer`)); layer.type = "number"; layer.min = "0"; layer.max = String(Math.max(0, doc.shape[hidden] - 1)); layer.step = "1"; layer.inputMode = "numeric";
  placementLayer = Math.max(0, Math.min(doc.shape[hidden] - 1, placementLayer)); layer.value = String(placementLayer);
  layer.addEventListener("input", () => { if (layer.validity.valid) { placementLayer = Number(layer.value); redrawTimedPlacement(); } }); layerLabel.append(layer);
  toolbar.append(planeLabel, tickLabel, layerLabel); block.append(toolbar);

  const palette = node("div", "", "placement-palette");
  for (const [index, type] of types.entries()) {
    const button = node("button", type.name, "placement-token" + (type.name === placementType ? " selected" : ""));
    button.type = "button"; button.draggable = true; button.style.setProperty("--token-color", colors[index % colors.length]);
    button.addEventListener("dragstart", event => { placementType = type.name; event.dataTransfer?.setData("text/plain", type.name); });
    button.addEventListener("click", () => { placementType = type.name; renderEditor(); }); palette.append(button);
  }
  block.append(palette);

  const canvas = document.createElement("canvas"); canvas.id = "timed-placement-canvas"; canvas.className = "placement-canvas"; canvas.width = 760; canvas.height = 460;
  canvas.setAttribute("aria-label", "Timed disturbance placement grid");
  canvas.addEventListener("dragover", event => { event.preventDefault(); });
  canvas.addEventListener("drop", event => { event.preventDefault(); const typeName = event.dataTransfer?.getData("text/plain") || placementType; appendRuntimeInjection(typeName, placementPosition(event, canvas)); });
  canvas.addEventListener("click", event => { if (placementType) appendRuntimeInjection(placementType, placementPosition(event, canvas)); });
  block.append(canvas, node("p", "", "preview-caption")); block.lastChild.id = "placement-caption";
  editor.append(block); redrawTimedPlacement();
}
'''
replace_once(
    "src/event_universe/ui_assets/app.js",
    "function renderEditor() {\n",
    TIMED_PLACEMENT + "\nfunction renderEditor() {\n",
)
replace_once(
    "src/event_universe/ui_assets/app.js",
    """    addButton(\"Add seed\", () => doc.seeds.push({position: [0, 0, 0], type: doc.disturbance_types[0]?.name || \"\"}));\n  } else if (tab === \"rules\") {\n""",
    """    addButton(\"Add seed\", () => doc.seeds.push({position: [0, 0, 0], type: doc.disturbance_types[0]?.name || \"\"}));\n  } else if (tab === \"timeline\") {\n    renderTimedPlacement(doc);\n    const scheduled = Array.isArray(doc.runtime_injections) ? doc.runtime_injections : [];\n    editor.append(node(\"hr\", \"\", \"editor-divider\"));\n    if (!scheduled.length) editor.append(node(\"p\", \"No timed disturbances are scheduled yet. Drag or tap above to add one.\", \"editor-description\"));\n    scheduled.forEach((item, i) => {\n      const panel = card(`Injection ${i + 1} · tick ${item.tick}`, () => doc.runtime_injections.splice(i, 1)), grid = node(\"div\", \"\", \"field-grid\"); panel.append(grid);\n      input(grid, \"Disturbance type\", item, \"type\", {text: true, choices: doc.disturbance_types.map(type => type.name), full: true});\n      input(grid, \"Tick\", item, \"tick\", {min: 1});\n      const position = node(\"div\", \"\", \"field-grid three field full\"); grid.append(position);\n      [\"X position\", \"Y position\", \"Z position\"].forEach((label, j) => input(position, label, item.position, j, {max: Math.max(0, doc.shape[j] - 1)}));\n      jsonField(grid, \"Field values at insertion\", item, \"values\", {}, \"Values override the selected disturbance type defaults at the configured tick.\");\n    });\n    addButton(\"Add timed injection\", () => {\n      if (!Array.isArray(doc.runtime_injections)) doc.runtime_injections = [];\n      doc.runtime_injections.push({tick: placementTick, position: [0, 0, 0], type: doc.disturbance_types[0]?.name || \"\"});\n    });\n  } else if (tab === \"rules\") {\n""",
)

append_once(
    "src/event_universe/ui_assets/style.css",
    ".timed-placement-editor",
    r'''
.timed-placement-editor { margin-bottom: 22px; }
.placement-toolbar { display: grid; grid-template-columns: repeat(3, minmax(130px, 1fr)); gap: 12px; margin: 12px 0; }
.placement-palette { display: flex; flex-wrap: wrap; gap: 9px; margin: 10px 0 14px; }
.placement-token { border: 1px solid color-mix(in srgb, var(--token-color) 65%, #466155); border-left: 8px solid var(--token-color); border-radius: 999px; background: #fff; min-height: 42px; padding: 8px 13px; color: #294438; cursor: grab; font: inherit; }
.placement-token:active { cursor: grabbing; }
.placement-token.selected { box-shadow: 0 0 0 3px color-mix(in srgb, var(--token-color) 24%, transparent); font-weight: 700; }
.placement-canvas { display: block; width: 100%; height: auto; max-height: 58vh; border: 1px solid #bdd2c3; border-radius: 14px; background: #f7fbf8; touch-action: manipulation; cursor: crosshair; }
@media (max-width: 700px) {
  .placement-toolbar { grid-template-columns: 1fr; }
  .placement-token { min-height: 46px; }
  .placement-canvas { max-height: 50vh; }
}
''',
)

replace_once(
    "docs/DISTURBANCES.md",
    "| `seeds` | Positions, disturbance type names and optional value overrides |\n| `spatial_fields` |",
    "| `seeds` | Positions, disturbance type names and optional value overrides |\n| `runtime_injections` | Optional bounded external disturbance placements with a tick, position, type and optional value overrides |\n| `spatial_fields` |",
)
replace_once(
    "docs/DISTURBANCES.md",
    "```json\n{\"position\": [2, 2, 2], \"type\": \"carrier\", \"values\": {\"inventory\": 6}}\n```\n\n### Transport\n",
    """```json\n{\"position\": [2, 2, 2], \"type\": \"carrier\", \"values\": {\"inventory\": 6}}\n```\n\n### Runtime injections\n\n`runtime_injections` is an optional bounded schedule of explicit external interventions.\nIt uses the same disturbance type definitions, defaults and value validation as seeds,\nbut each entry has a positive `tick`. Tick zero remains initial state and must use\n`seeds`. A scheduled entry is data, not a remote-state query or a hidden physical law:\n\n```json\n{\"tick\": 5, \"position\": [7, 4, 2], \"type\": \"carrier\",\n \"values\": {\"inventory\": 3, \"heading\": [1, 0, 0]}}\n```\n\nAt tick `T`, completed link deliveries and already-ready local commits are resolved\nfirst. The complete injection batch for `T` is then validated and inserted at its\ndeclared cells. The tick-`T` snapshot includes the new records; their ordinary local\ncycles can begin on the following transition. A target cell with a frozen pending\ncycle rejects an injection, and insufficient resident capacity rejects the whole due\nbatch before any injection is inserted. The schedule contains at most 256 entries,\nand entries at one tick/address cannot exceed `slots_per_cell`.\n\nEvery injected payload is recorded as explicit source input for accounting. This\nallows conserved quantities to change without pretending the change emerged from\nclosed local dynamics. The engine never selects an injection from a physical name,\nglobal measurement or remote state. A run that ends before a future scheduled tick\nsimply leaves that entry unapplied.\n\n### Transport\n""",
)

replace_once(
    "SIMULATOR_DEFINITIONS.md",
    "[docs/DISTURBANCES.md](docs/DISTURBANCES.md) is the authoritative active schema\nand transition contract: bounded scalar/vector payloads, whole-record or extensive\ntransport, atomic local exchange, explicit sources, fixed link transit, local\ncomputation delay without debt, capacity failures and headless output.\n",
    """[docs/DISTURBANCES.md](docs/DISTURBANCES.md) is the authoritative active schema\nand transition contract: bounded scalar/vector payloads, whole-record or extensive\ntransport, atomic local exchange, explicit sources, fixed link transit, local\ncomputation delay without debt, capacity failures and headless output. The optional\n`runtime_injections` schedule is an explicit external source intervention: it inserts\na prevalidated generic disturbance only at its declared tick and address, contributes\nits payload to source accounting, and then leaves the record to ordinary local laws.\nIt is not emergent dynamics, a remote signal or a display-side state mutation.\n""",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "`initialization.py` reads strict JSON data and resolves names to bounded typed\ndefinitions. `core/disturbance_state.py` owns fixed schemas and payload coding;\n`fields/disturbances.py` owns expression arithmetic, updates, paired coupling\nand transport proposals; `core/disturbance_engine.py` owns addresses, capacity,\nfixed transit and delayed atomic commits. No layer branches on a physical field\nname or imports Python code named by initialization.\n",
    """`initialization.py` reads strict JSON data and resolves names to bounded typed\ndefinitions. `core/disturbance_state.py` owns fixed schemas and payload coding;\n`fields/disturbances.py` owns expression arithmetic, updates, paired coupling\nand transport proposals; `core/disturbance_engine.py` owns addresses, capacity,\nfixed transit and delayed atomic commits. No layer branches on a physical field\nname or imports Python code named by initialization.\n\nThe optional runtime-injection schedule is immutable host control input parsed with\nthe initialization. The engine owns its tick-boundary commit because scheduling and\ncapacity already belong there. The schedule is globally bounded and cannot inspect\nworld state to choose a target. At a due tick, each declared record is validated\nagainst only its configured address capacity and frozen-cycle status; its conserved\npayload is explicit source input. This external intervention is not a local physical\nlaw and cannot be used to repair a failed trajectory or conservation result.\n""",
)

replace_once(
    "docs/WORKSPACE.md",
    "- **Initial state:** seed positions, disturbance types and value overrides.\n- **Rules & costs:**",
    "- **Initial state:** seed positions, disturbance types and value overrides.\n- **Timed placement:** drag or tap a disturbance onto a selected lattice slice and tick, then edit its exact field values.\n- **Rules & costs:**",
)
replace_once(
    "docs/WORKSPACE.md",
    "The initial-placement diagram reads configured seed positions, not computed\nmotion. It is an isometric projection; concentric rings denote co-located seeds.\nThe preview never supplies physical inputs.\n",
    """The initial-placement diagram reads configured seed positions, not computed\nmotion. It is an isometric projection; concentric rings denote co-located seeds.\nThe preview never supplies physical inputs.\n\nThe Timed placement tab edits physical input, not playback. Choose XY, XZ or YZ,\na layer and a positive tick, then drag a disturbance-type token onto the grid. On\ntouch devices, select the token and tap a node. The editor writes the exact integer\naddress and type into `runtime_injections`; the cards below the grid expose tick,\ncoordinates and optional field-value overrides. Initial seeds appear as dashed\nreference rings. Running submits an immutable JSON snapshot, so changing the draft\ndoes not mutate a child simulation already in progress.\n""",
)

replace_once(
    "docs/TEST_EXPECTATIONS.md",
    "| Ordinary headless run | Input, event, metadata and final-state files; no frame capture/render import |\n\n`test_initialization.py` covers",
    """| Ordinary headless run | Input, event, metadata and final-state files; no frame capture/render import |\n| Runtime injection at tick 1 | Absent at tick 0; inserted after tick-1 deliveries/ready commits; full payload counted as source input; `runtime_injected` event at tick 1 |\n| Runtime injection into full or frozen-pending cell | Whole due batch rejects before injected occupancy or source accounting changes |\n| Timed-placement workspace | Same strict JSON validator; drag/drop and touch placement write only generic `runtime_injections`; direct runner remains the sole engine |\n\n`test_runtime_injections.py` covers parsing, tick-boundary ownership, source\naccounting, capacity/frozen-cycle rejection and explicit visual recording.\n`test_runtime_injection_workspace.py` covers workspace validation and the generic\ndrag/touch editor surface.\n\n`test_initialization.py` covers""",
)
