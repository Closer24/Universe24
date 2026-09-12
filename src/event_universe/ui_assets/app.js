"use strict";

const $ = (selector) => document.querySelector(selector);
const colors = ["#247658", "#d29c4e", "#668daa", "#a373a3", "#ab704f", "#6d998b"];
const token = $('meta[name="workspace-token"]').content;
let templates = [], selected = "", source = "", configuration = null, tab = "general";
let runs = [], selectedRun = null, busy = false, validated = false, loading = false, selectionVersion = 0;
let moviePath = null;
let drafts = {};
try { drafts = JSON.parse(localStorage.getItem("universe24-drafts-v1") || "{}"); } catch { /* Start fresh if local storage is unavailable. */ }
if (!drafts || typeof drafts !== "object" || Array.isArray(drafts)) drafts = {};

function node(tag, text = "", className = "") {
  const result = document.createElement(tag);
  result.textContent = text;
  if (className) result.className = className;
  return result;
}

function message(text, kind = "") {
  const box = $("#message");
  box.textContent = text; box.className = kind; box.hidden = !text;
}

async function api(path, data) {
  const options = data === undefined ? {} : { method: "POST", headers: {
    "Content-Type": "application/json", "X-Workspace-Token": token
  }, body: JSON.stringify(data) };
  const response = await fetch(path, options);
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
  return result;
}

function remember() {
  drafts[selected] = source;
  try { localStorage.setItem("universe24-drafts-v1", JSON.stringify(drafts)); }
  catch { message("Browser storage is unavailable. Export JSON to keep your changes.", "warning"); }
}

function changed() {
  source = JSON.stringify(configuration, null, 2) + "\n";
  validated = false; remember(); refreshSummary();
}

function refreshSummary() {
  $("#draft-state").textContent = validated ? "Checked" : "Draft";
  $("#draft-state").className = "draft-tag" + (validated ? " valid" : "");
  $("#model-heading").textContent = configuration?.model_id || "Custom configuration";
  $("#duration-label").textContent = `${configuration?.ticks ?? "—"} ticks`;
  $("#selected-description").textContent = `${templates.find(t => t.id === selected)?.name || "Custom configuration"} · ${configuration?.seeds?.length || 0} initial particles / records`;
  $("#template-label").textContent = selected === "custom" ? "CUSTOM CONFIGURATION" : `${selected.toUpperCase()} TEMPLATE`;
  const counts = [[configuration?.fields?.length || 0, "FIELDS"],
    [configuration?.disturbance_types?.length || 0, "TYPES"], [configuration?.seeds?.length || 0, "SEEDS"]];
  $("#summary-metrics").replaceChildren(...counts.map(([count, label]) => {
    const cell = node("div"); cell.append(node("strong", String(count)), node("span", label)); return cell;
  }));
  drawPlacement();
  $("#run").disabled = !configuration || busy || loading || runs.some(run => run.status === "running");
}

function drawPlacement() {
  const canvas = $("#preview"), ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const shape = configuration?.shape;
  if (!Array.isArray(shape) || shape.length !== 3 || shape.some(x => !(x > 0))) return;
  const project = ([x, y, z]) => [340 + (x - y) * 210, 295 - (x + y) * 84 - z * 170];
  const line = (a, b, color = "#dce9e0") => {
    ctx.beginPath(); ctx.moveTo(...project(a)); ctx.lineTo(...project(b)); ctx.strokeStyle = color; ctx.lineWidth = 1.3; ctx.stroke();
  };
  for (let i = 0; i <= 4; i++) { line([i / 4, 0, 0], [i / 4, 1, 0]); line([0, i / 4, 0], [1, i / 4, 0]); }
  for (const [a, b] of [[[0, 0, 0], [0, 0, 1]], [[1, 0, 0], [1, 0, 1]], [[0, 1, 0], [0, 1, 1]],
    [[1, 1, 0], [1, 1, 1]], [[0, 0, 1], [1, 0, 1]], [[0, 0, 1], [0, 1, 1]],
    [[1, 1, 1], [1, 0, 1]], [[1, 1, 1], [0, 1, 1]]]) line(a, b, "#cadbcf");
  ctx.font = "18px Segoe UI, sans-serif"; ctx.fillStyle = "#718e7b";
  ctx.fillText(`X · ${shape[0]}`, 552, 228); ctx.fillText(`Y · ${shape[1]}`, 58, 228); ctx.fillText(`Z · ${shape[2]}`, 350, 113);
  const types = Array.isArray(configuration?.disturbance_types) ? configuration.disturbance_types : [];
  const seeds = Array.isArray(configuration?.seeds) ? configuration.seeds : [];
  seeds.forEach((seed, index) => {
    if (!Array.isArray(seed.position) || seed.position.length !== 3 || seed.position.some(x => !Number.isFinite(x))) return;
    const position = seed.position.map((x, i) => x / Math.max(1, shape[i] - 1));
    const [x, y] = project(position), color = colors[Math.max(0, types.findIndex(t => t.name === seed.type)) % colors.length];
    line([position[0], position[1], 0], position, "#b5d3bf");
    // Concentric rings expose co-located seeds without changing their coordinates.
    const colocated = seeds.slice(0, index).filter(s => JSON.stringify(s.position) === JSON.stringify(seed.position)).length;
    ctx.beginPath(); ctx.arc(x, y, 8 + colocated * 6, 0, Math.PI * 2); ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.stroke();
    if (!colocated) { ctx.fillStyle = color; ctx.fill(); }
  });
  $("#seed-legend").replaceChildren(...types.map((type, i) => {
    const item = node("span"), dot = node("span", "", "legend-dot"); dot.style.backgroundColor = colors[i % colors.length];
    item.append(dot, document.createTextNode(type.name)); return item;
  }));
}

function input(parent, label, object, key, options = {}) {
  const wrapper = node("label", "", "field" + (options.full ? " full" : ""));
  wrapper.append(node("span", label));
  const control = document.createElement(options.choices ? "select" : "input");
  if (options.choices) {
    for (const value of options.choices) { const option = node("option", String(value)); option.value = String(value); control.append(option); }
  } else {
    control.type = options.text ? "text" : "number";
    if (!options.text) { control.min = String(options.min ?? 0); control.max = String(options.max ?? 1073741823); control.step = "1"; control.inputMode = "numeric"; }
    else control.maxLength = 128;
  }
  control.required = true; control.value = String(object[key] ?? "");
  control.addEventListener("input", () => {
    if (!control.checkValidity()) return;
    if (options.rename) {
      const collection = options.rename === "field" ? configuration.fields : configuration.disturbance_types;
      if (!control.value.trim() || collection.some(item => item !== object && item.name === control.value)) {
        control.setCustomValidity("Choose a nonempty, unique name."); return;
      }
      renameReferences(configuration, options.rename, object[key], control.value);
    }
    object[key] = options.text ? control.value : Number(control.value); changed();
  });
  wrapper.append(control);
  if (options.hint) wrapper.append(node("small", options.hint));
  parent.append(wrapper); return control;
}

function renameReferences(value, kind, before, after) {
  if (!value || typeof value !== "object") return;
  if (Array.isArray(value)) { value.forEach(item => renameReferences(item, kind, before, after)); return; }
  for (const [key, child] of Object.entries(value)) {
    const references = kind === "field" ? ["field", "direction_field", "cost_field"] : ["type", "left_type", "right_type"];
    if (references.includes(key) && child === before) value[key] = after;
    else if (kind === "field" && key === "fields" && Array.isArray(child) && child.every(item => typeof item === "string")) value[key] = child.map(name => name === before ? after : name);
    else if (kind === "field" && ["defaults", "values"].includes(key) && child && typeof child === "object" && Object.hasOwn(child, before)) {
      const fields = Object.fromEntries(Object.entries(child).map(([name, payload]) => [name === before ? after : name, payload])); value[key] = fields;
    } else renameReferences(child, kind, before, after);
  }
}

function check(parent, label, object, key, fallback) {
  const wrapper = node("label", "", "checkbox-field"), control = document.createElement("input");
  control.type = "checkbox"; control.checked = object[key] ?? fallback ?? false;
  control.addEventListener("change", () => { object[key] = control.checked; changed(); });
  wrapper.append(control, document.createTextNode(label)); parent.append(wrapper);
}

function jsonField(parent, label, object, key, fallback, hint = "") {
  const wrapper = node("label", "", "field full"), control = document.createElement("textarea");
  wrapper.append(node("span", label)); control.value = JSON.stringify(object[key] ?? fallback, null, 2);
  control.spellcheck = false; control.setAttribute("aria-label", label);
  let timer;
  control.addEventListener("input", () => {
    clearTimeout(timer); control.setCustomValidity("Checking JSON. Please wait a moment.");
    const fragment = control.value;
    timer = setTimeout(async () => {
      try {
        const result = await api("/api/json", {source: fragment});
        if (control.value !== fragment || !control.isConnected) return;
        control.setCustomValidity(""); object[key] = result.value; changed();
      } catch (error) { if (control.value === fragment) control.setCustomValidity(error.message); }
    }, 200);
  });
  wrapper.append(control); if (hint) wrapper.append(node("small", hint)); parent.append(wrapper);
}

function section(title, description) {
  const editor = $("#editor-panel"); editor.append(node("h4", title));
  if (description) editor.append(node("p", description, "editor-description"));
  const grid = node("div", "", "field-grid"); editor.append(grid); return grid;
}

function card(title, remove) {
  const result = node("section", "", "editor-card"), header = node("h4", title);
  const button = node("button", "Remove", "text-button"); button.type = "button"; button.setAttribute("aria-label", `Remove ${title}`);
  button.addEventListener("click", () => { remove(); changed(); renderEditor(); }); header.append(button);
  result.append(header); $("#editor-panel").append(result); return result;
}

function addButton(label, callback) {
  const button = node("button", `＋ ${label}`, "add-button"); button.type = "button";
  button.addEventListener("click", () => { if (!$("#editor-panel").reportValidity()) return; callback(); changed(); renderEditor(); });
  $("#editor-panel").append(button);
}

function renderEditor() {
  const editor = $("#editor-panel"); editor.replaceChildren();
  $$("[data-tab]").forEach(button => { button.setAttribute("aria-selected", String(button.dataset.tab === tab)); button.tabIndex = button.dataset.tab === tab ? 0 : -1; });
  if (tab === "json" || !configuration) {
    editor.append(node("p", "Edit the complete initialization, including custom fields, local laws and couplings. Check it before switching back to forms.", "editor-description"));
    const raw = document.createElement("textarea"); raw.className = "json-editor"; raw.value = source; raw.spellcheck = false;
    raw.setAttribute("aria-label", "Configuration JSON");
    raw.addEventListener("input", () => { source = raw.value; validated = false; remember(); $("#draft-state").textContent = "Unchecked JSON"; $("#draft-state").className = "draft-tag"; });
    editor.append(raw); return;
  }
  const doc = configuration;
  if (tab === "names") {
    let grid = section("Particle names", "A name identifies a disturbance type. Every record of that type shares it; presets use separate types for separately named particles.");
    doc.disturbance_types.forEach((type, i) => input(grid, `Particle ${i + 1} name`, type, "name", {text: true, full: true, rename: "type"}));
    editor.append(node("hr", "", "editor-divider")); grid = section("Field names", "Renaming updates references in this configuration, including rules and initial values.");
    doc.fields.forEach((field, i) => input(grid, `Field ${i + 1} name`, field, "name", {text: true, full: true, rename: "field"}));
  } else if (tab === "general") {
    let grid = section("Experiment", "All settings are read from JSON when a run starts.");
    input(grid, "Model identifier", doc, "model_id", { text: true, full: true });
    input(grid, "Simulation ticks", doc, "ticks", { hint: "Number of base time intervals" });
    input(grid, "Slots per cell", doc, "slots_per_cell", { min: 1, max: 32, hint: "Fixed local record capacity · up to 32" });
    editor.append(node("hr", "", "editor-divider"));
    grid = section("World dimensions", "Periodic lattice extents. Seed positions must be inside this volume."); grid.classList.add("three");
    ["X extent", "Y extent", "Z extent"].forEach((label, i) => input(grid, label, doc.shape, i, { min: 1 }));
    editor.append(node("hr", "", "editor-divider")); grid = section("Local timing");
    input(grid, "Link transit ticks", doc, "link_ticks", { min: 1, hint: "Fixed time between neighboring cells" });
    input(grid, "Normal computation budget", doc, "normal_budget", { min: 1, hint: "Ordinary local work before added delay" });
  } else if (tab === "fields") {
    editor.append(node("p", "Names are your labels. Declare the structure and conservation properties of each quantity.", "editor-description"));
    doc.fields.forEach((field, i) => {
      const item = card(`Field ${i + 1} · ${field.name}`, () => doc.fields.splice(i, 1)), grid = node("div", "", "field-grid"); item.append(grid);
      input(grid, "Name", field, "name", { text: true, rename: "field" }); input(grid, "Components", field, "components", { choices: [1, 3] });
      input(grid, "Units", field, "units", { text: true }); input(grid, "Scale denominator", field, "scale", { min: 1 });
      if (field.scale === undefined) grid.lastChild.querySelector("input").value = "1";
      const checks = node("div", "", "card-checkboxes"); item.append(checks);
      check(checks, "Signed", field, "signed"); check(checks, "Conserved", field, "conserved"); check(checks, "Extensive", field, "extensive", true);
    });
    addButton("Add field", () => doc.fields.push({name: `field_${doc.fields.length + 1}`, components: 1, units: "unit", signed: false, conserved: false}));
  } else if (tab === "types") {
    editor.append(node("p", "Define which fields travel together, their defaults, and their transport and update rules.", "editor-description"));
    doc.disturbance_types.forEach((type, i) => {
      const item = card(`Disturbance ${i + 1} · ${type.name}`, () => doc.disturbance_types.splice(i, 1)), grid = node("div", "", "field-grid"); item.append(grid);
      input(grid, "Type name", type, "name", { text: true, full: true, rename: "type" });
      jsonField(grid, "Owned fields", type, "fields", []); jsonField(grid, "Default field values", type, "defaults", {});
      jsonField(grid, "Transport rule", type, "transport", { mode: "hold" }, "Modes: hold, move or split. Ports: +X, −X, +Y, −Y, +Z, −Z.");
      jsonField(grid, "Local update rules", type, "updates", []);
      if (type.cost_field !== undefined) input(grid, "Computation cost field", type, "cost_field", { text: true, full: true });
    });
    addButton("Add disturbance type", () => doc.disturbance_types.push({name: `type_${doc.disturbance_types.length + 1}`, fields: doc.fields.length ? [doc.fields[0].name] : [], transport: {mode: "hold"}}));
  } else if (tab === "seeds") {
    editor.append(node("p", "Place initial disturbances at lattice addresses. Values override the selected type's defaults.", "editor-description"));
    doc.seeds.forEach((seed, i) => {
      const item = card(`Seed ${i + 1}`, () => doc.seeds.splice(i, 1)), grid = node("div", "", "field-grid"); item.append(grid);
      input(grid, "Disturbance type", seed, "type", { text: true, choices: doc.disturbance_types.map(t => t.name), full: true });
      const position = node("div", "", "field-grid three field full"); grid.append(position);
      ["X position", "Y position", "Z position"].forEach((label, j) => input(position, label, seed.position, j, { max: Math.max(0, doc.shape[j] - 1) }));
      jsonField(grid, "Initial field values", seed, "values", {});
    });
    addButton("Add seed", () => doc.seeds.push({position: [0, 0, 0], type: doc.disturbance_types[0]?.name || ""}));
  } else if (tab === "rules") {
    let grid = section("Local exchange", "Couplings exchange a configured quantity between records in the same cell.");
    jsonField(grid, "Coupling rules", doc, "couplings", []);
    grid = section("Atomic interactions", "Update several fields together and enforce declared invariants for each local pair.");
    jsonField(grid, "Interaction rules", doc, "interactions", []);
    editor.append(node("hr", "", "editor-divider")); grid = section("Operation prices", "Positive integer costs used by the model's local timing law."); grid.classList.add("three");
    Object.keys(doc.operation_costs).forEach(key => input(grid, key[0].toUpperCase() + key.slice(1), doc.operation_costs, key, { min: 1 }));
  }
}

function $$(selector) { return [...document.querySelectorAll(selector)]; }

async function validate(show = true) {
  if (!$("#editor-panel").reportValidity()) throw new Error("Please correct the highlighted configuration value.");
  const checkedSource = source;
  const result = await api("/api/validate", { source: checkedSource });
  if (source !== checkedSource) throw new Error("Configuration changed while checking. Please check it again.");
  if (tab === "json" || !configuration) configuration = JSON.parse(checkedSource);
  validated = true; refreshSummary();
  if (show) message(`Configuration checked. ${result.summary.model} is ready for ${result.summary.ticks} ticks.`);
  return result;
}

async function selectTemplate(id, reset = false) {
  const template = templates.find(item => item.id === id);
  const version = ++selectionVersion;
  const candidate = (!reset && typeof drafts[id] === "string" ? drafts[id] : template?.source) || "{}";
  loading = true; refreshSummary();
  let parsed = null;
  try {
    await api("/api/validate", { source: candidate }); parsed = JSON.parse(candidate);
  } catch { /* Preserve an invalid saved draft in the full JSON editor. */ }
  if (version !== selectionVersion) return;
  selected = id; source = candidate; configuration = parsed; tab = parsed ? "names" : "json"; loading = false;
  validated = false; remember(); renderTemplates(); renderEditor(); refreshSummary(); message("");
}

function renderTemplates() {
  $("#template-count").textContent = String(templates.length);
  const list = [...templates];
  if (drafts.custom && !list.some(t => t.id === "custom")) list.push({ id: "custom", name: "Custom configuration", summary: null });
  $("#templates").replaceChildren(...list.map(template => {
    const button = node("button", "", "template-button" + (selected === template.id ? " selected" : ""));
    button.type = "button"; button.setAttribute("aria-pressed", String(selected === template.id));
    button.append(node("strong", template.name));
    const s = template.summary;
    button.append(node("small", s ? `${s.fields} fields · ${s.types} types · ${s.ticks} ticks` : "Your saved JSON draft"));
    button.addEventListener("click", () => selectTemplate(template.id).catch(error => message(error.message, "error")));
    return button;
  }));
}

function renderResults() {
  const active = runs.find(run => run.status === "running");
  $("#stop").hidden = !active; $("#run").disabled = busy || loading || Boolean(active) || !configuration;
  $("#run-count").textContent = `${runs.length} run${runs.length === 1 ? "" : "s"} this session`;
  const run = runs.find(item => item.id === selectedRun) || runs[0];
  if (!run) return;
  const path = run.artifacts["run.html"] || null;
  if (moviePath !== path) {
    moviePath = path; const frame = $("#movie-frame");
    frame.hidden = !path; $("#movie-empty").hidden = Boolean(path); $("#movie-external").hidden = !path;
    if (path) { frame.src = path + "?autoplay=1"; $("#movie-external").href = path; }
    else frame.removeAttribute("src");
  }
  if (!path) $("#movie-empty p").textContent = run.status === "running" ? "Calculating your recording. You can prepare the next configuration while this runs." : "This run has no movie. Enable recording and run again.";
  const result = node("div", "", "run-result"), top = node("div", "", "result-top");
  top.append(node("h3", run.model), node("span", run.status, `run-status ${run.status}`)); result.append(top);
  const metadata = run.metadata;
  const detail = metadata ? `${metadata.completed_ticks} / ${run.requested_ticks} completed ticks` : `${run.requested_ticks} requested ticks`;
  result.append(node("p", `${detail} · ${run.elapsed_seconds.toFixed(1)} seconds · ${run.id.slice(0, 8)}`, "result-meta"));
  if (run.status === "running") result.append(node("p", "Simulation is running. You can continue preparing the next configuration.", "result-meta"));
  if (run.status === "cancelled") result.append(node("p", "Stopped by request. Files may be partial; this is not a completed simulation.", "result-error"));
  if (run.status === "failed") result.append(node("p", metadata?.error || `The runner stopped before completion. See the log in ${run.output.replace(/runs[/\\].*$/, "inputs/")}${run.id}.log`, "result-error"));
  if (metadata) {
    result.append(node("p", metadata.conserved_at_every_completed_tick ? "Declared quantities conserved at every completed tick." : "A conservation check failed.", "result-meta"));
    const table = node("table", "", "totals"), head = node("tr");
    ["CONSERVED FIELD", "INITIAL", "FINAL", "SOURCE CHANGE"].forEach(label => head.append(node("th", label))); table.append(head);
    for (const [name, value] of Object.entries(metadata.initial_totals || {})) {
      const row = node("tr"); [name, JSON.stringify(value), JSON.stringify(metadata.final_totals[name]), JSON.stringify(metadata.source_totals[name])].forEach(v => row.append(node("td", v))); table.append(row);
    }
    result.append(table);
  }
  const links = node("div", "", "artifact-links");
  for (const [name, path] of Object.entries(run.artifacts)) {
    const link = node("a", name === "run.html" ? "↗ Open recorded movie" : `↓ ${name}`); link.href = path;
    if (name === "run.html") { link.target = "_blank"; link.rel = "noopener"; }
    else link.download = name;
    links.append(link);
  }
  result.append(links); $("#results").replaceChildren(result);
  $("#history").replaceChildren(...runs.filter(item => item.id !== run.id).slice(0, 9).map(item => {
    const button = node("button", "", "history-item"); button.type = "button";
    button.append(node("span", `${item.model} · ${item.id.slice(0, 8)}`), node("span", item.status));
    button.addEventListener("click", () => { selectedRun = item.id; renderResults(); }); return button;
  }));
}

async function poll() {
  try { const result = await api("/api/runs"); if (JSON.stringify(runs) !== JSON.stringify(result.runs)) { runs = result.runs; renderResults(); } }
  catch { if (runs.some(run => run.status === "running")) message("Connection lost. The run may still be active. Keep the server terminal open and reconnect.", "warning"); }
  finally { setTimeout(poll, 900); }
}

$("#editor-panel").addEventListener("submit", event => event.preventDefault());
$("#phone-controls").addEventListener("click", () => {
  const open = document.body.classList.toggle("controls-open");
  $("#phone-controls").setAttribute("aria-expanded", String(open));
  $("#phone-controls").textContent = open ? "Back to movie" : "Experiment controls";
});
$("#editor-panel").addEventListener("input", event => { if (event.target.tagName === "INPUT") event.target.setCustomValidity(""); }, true);
function revealSection() { const section = document.getElementById(location.hash.slice(1)); if (section?.tagName === "DETAILS") section.open = true; }
window.addEventListener("hashchange", revealSection);
document.querySelectorAll('a[href="#configuration"]').forEach(link => link.addEventListener("click", () => { $("#configuration").open = true; }));
$$("[data-tab]").forEach(button => {
  button.addEventListener("click", async () => {
    try {
      if (!$("#editor-panel").reportValidity()) return;
      if (tab === "json" && button.dataset.tab !== "json") await validate(false);
      tab = button.dataset.tab; renderEditor();
    } catch (error) { message(error.message, "error"); }
  });
  button.addEventListener("keydown", event => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault(); const buttons = $$("[data-tab]"); let index = buttons.indexOf(button);
    index = event.key === "Home" ? 0 : event.key === "End" ? buttons.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + buttons.length) % buttons.length;
    buttons[index].focus(); buttons[index].click();
  });
});
$("#validate").addEventListener("click", () => validate().catch(error => message(error.message, "error")));
$("#reset").addEventListener("click", () => {
  if (selected === "custom") { message("Custom drafts have no template to reset to. Import a file or select a starting point.", "warning"); return; }
  selectTemplate(selected, true).catch(error => message(error.message, "error"));
});
$("#export").addEventListener("click", async () => {
  try {
    await validate(false);
    const exported = await api("/api/export", {source});
    message("Configuration saved. ");
    const link = node("a", "Download JSON"); link.href = exported.url; link.download = exported.name;
    $("#message").append(link); link.click();
  } catch (error) { message(error.message, "error"); }
});
$("#import").addEventListener("click", () => $("#import-file").click());
$("#import-file").addEventListener("change", async event => {
  const file = event.target.files[0]; if (!file) return;
  try {
    if (file.size > 1048576) throw new Error("Choose a configuration smaller than 1 MiB.");
    const text = await file.text(); await api("/api/validate", {source: text});
    drafts.custom = text; await selectTemplate("custom"); message(`Loaded ${file.name}. Changes are saved as a separate browser draft.`);
  } catch (error) { message(error.message, "error"); }
  finally { event.target.value = ""; }
});
$("#visualize").addEventListener("change", event => { $("#stride").disabled = !event.target.checked; });
$("#run").addEventListener("click", async () => {
  if (busy || loading) return;
  busy = true; refreshSummary();
  const submittedSource = source;
  const visualize = $("#visualize").checked, frameStride = Number($("#stride").value);
  try {
    if (!$("#editor-panel").reportValidity() || (visualize && !$("#stride").reportValidity())) return;
    const run = await api("/api/runs", {source: submittedSource, visualize, frame_stride: frameStride});
    if (source === submittedSource) {
      if (tab === "json" || !configuration) configuration = JSON.parse(submittedSource);
      validated = true;
    }
    selectedRun = run.id; runs.unshift(run); renderResults(); message("Simulation started. This run uses a saved snapshot of your configuration.");
  } catch (error) { message(error.message, "error"); }
  finally { busy = false; refreshSummary(); }
});
$("#stop").addEventListener("click", async () => {
  const active = runs.find(run => run.status === "running"); if (!active) return;
  $("#stop").disabled = true;
  try { const stopped = await api(`/api/runs/${active.id}/stop`, {}); runs = runs.map(run => run.id === active.id ? stopped : run); renderResults(); }
  catch (error) { message(error.message, "error"); }
  finally { $("#stop").disabled = false; }
});

(async () => {
  try {
    templates = (await api("/api/templates")).templates;
    if (templates.length) await selectTemplate(templates[0].id);
    else { selected = "custom"; source = drafts.custom || "{}"; tab = "json"; renderTemplates(); renderEditor(); message("Import a valid initialization JSON to get started. No templates were found in the configured folder.", "warning"); }
    poll();
  } catch (error) { message(`Cannot load the workspace: ${error.message}. Check that the local server is running.`, "error"); }
})();
