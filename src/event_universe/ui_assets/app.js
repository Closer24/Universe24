"use strict";

const $ = (selector) => document.querySelector(selector);
const token = $('meta[name="workspace-token"]').content;
let templates = [], selected = "", source = "", summary = null;
let runs = [], selectedRun = null, busy = false, loading = false, selectionVersion = 0;
let drafts = {};
try { drafts = JSON.parse(localStorage.getItem("universe24-drafts-v2") || "{}"); } catch { /* Start fresh if local storage is unavailable. */ }
if (!drafts || typeof drafts !== "object" || Array.isArray(drafts)) drafts = {};
drafts = Object.assign(Object.create(null), drafts);

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
  try { localStorage.setItem("universe24-drafts-v2", JSON.stringify(drafts)); }
  catch { message("Browser storage is unavailable. Export JSON to keep your changes.", "warning"); }
}

function refreshSummary() {
  const checked = Boolean(summary);
  $("#draft-state").textContent = checked ? "Checked" : "Draft";
  $("#draft-state").className = "draft-tag" + (checked ? " valid" : "");
  $("#model-heading").textContent = summary?.model || "World file";
  $("#duration-label").textContent = `${summary?.ticks ?? "—"} ticks`;
  const name = templates.find(t => t.id === selected)?.name || "Custom world";
  $("#selected-description").textContent = summary
    ? `${name} · ${summary.shape.join(" × ")} · ${summary.families} families · ${summary.contents} held contents`
    : `${name} · check the world file to run it`;
  $("#template-label").textContent = selected === "custom" ? "CUSTOM WORLD" : `${selected.toUpperCase()} TEMPLATE`;
  $("#run").disabled = !checked || busy || loading || runs.some(run => run.status === "running");
}

async function validate(show = true) {
  const checkedSource = source;
  const result = await api("/api/validate", { source: checkedSource });
  if (source !== checkedSource) throw new Error("The world file changed while checking. Please check it again.");
  summary = result.summary; refreshSummary();
  if (show) message(`Checked. ${summary.model} is ready for ${summary.ticks} ticks.`);
  return result;
}

async function selectTemplate(id, reset = false) {
  const template = templates.find(item => item.id === id);
  const version = ++selectionVersion;
  const candidate = (!reset && typeof drafts[id] === "string" ? drafts[id] : template?.source) || "{}";
  loading = true; refreshSummary();
  let checked = null;
  try { checked = (await api("/api/validate", { source: candidate })).summary; }
  catch { /* Keep an invalid saved draft in the editor for repair. */ }
  if (version !== selectionVersion) return;
  selected = id; source = candidate; summary = checked; loading = false;
  $("#source").value = source;
  remember(); renderTemplates(); refreshSummary(); message("");
}

function renderTemplates() {
  $("#template-count").textContent = String(templates.length);
  const list = [...templates];
  if (drafts.custom && !list.some(t => t.id === "custom")) list.push({ id: "custom", name: "Custom world", summary: null });
  $("#templates").replaceChildren(...list.map(template => {
    const button = node("button", "", "template-button" + (selected === template.id ? " selected" : ""));
    button.type = "button"; button.setAttribute("aria-pressed", String(selected === template.id));
    button.append(node("strong", template.name));
    const s = template.summary;
    button.append(node("small", s ? `${s.shape.join("×")} · ${s.contents} contents · ${s.ticks} ticks` : "Your saved JSON draft"));
    button.addEventListener("click", () => selectTemplate(template.id).catch(error => message(error.message, "error")));
    return button;
  }));
}

function renderResults() {
  const active = runs.find(run => run.status === "running");
  $("#stop").hidden = !active; refreshSummary();
  $("#run-count").textContent = `${runs.length} run${runs.length === 1 ? "" : "s"} this session`;
  const run = runs.find(item => item.id === selectedRun) || runs[0];
  if (!run) return;
  const result = node("div", "", "run-result"), top = node("div", "", "result-top");
  top.append(node("h3", run.model), node("span", run.status, `run-status ${run.status}`)); result.append(top);
  const metadata = run.metadata;
  const detail = metadata ? `${metadata.completed_ticks} / ${run.requested_ticks} completed ticks` : `${run.requested_ticks} requested ticks`;
  result.append(node("p", `${detail} · ${run.elapsed_seconds.toFixed(1)} seconds · ${run.id.slice(0, 8)}`, "result-meta"));
  if (run.status === "running") result.append(node("p", "The run is in progress. You can prepare the next world meanwhile.", "result-meta"));
  if (run.status === "cancelled") result.append(node("p", "Stopped by request. Files may be partial; this is not a completed run.", "result-error"));
  if (run.status === "failed") result.append(node("p", metadata?.error || `The runner stopped before completion. See the log in ${run.output.replace(/runs[/\\].*$/, "inputs/")}${run.id}.log`, "result-error"));
  if (metadata) {
    const conserved = metadata.conserved_at_every_completed_tick;
    result.append(node("p", `${metadata.law} · ${conserved ? "the books balanced at every completed tick" : "the books did not balance"}`, conserved ? "result-meta" : "result-error"));
    const last = Array.isArray(metadata.audit) && metadata.audit.length ? metadata.audit[metadata.audit.length - 1] : null;
    if (last?.families) {
      const table = node("table", "", "totals"), head = node("tr");
      ["FAMILY", "HELD", "IN FLIGHT", "RELEASED", "ABSORBED", "ESCAPED"].forEach(label => head.append(node("th", label))); table.append(head);
      for (const [name, books] of Object.entries(last.families)) {
        const row = node("tr");
        [name, books.held?.current, books.shadows?.current, books.shadows?.released, books.shadows?.absorbed, books.shadows?.escaped]
          .forEach(v => row.append(node("td", String(v ?? "")))); table.append(row);
      }
      result.append(table);
    }
    if (Array.isArray(metadata.contents)) result.append(node("p", `${metadata.contents.length} held contents at the end of the run.`, "result-meta"));
  }
  const links = node("div", "", "artifact-links");
  for (const [name, path] of Object.entries(run.artifacts)) {
    const link = node("a", `↓ ${name}`); link.href = path; link.download = name; links.append(link);
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
$("#source").addEventListener("input", () => { source = $("#source").value; summary = null; remember(); refreshSummary(); });
$("#validate").addEventListener("click", () => validate().catch(error => message(error.message, "error")));
$("#reset").addEventListener("click", () => {
  if (selected === "custom") { message("A custom draft has no template to reset to. Import a file or select a world.", "warning"); return; }
  selectTemplate(selected, true).catch(error => message(error.message, "error"));
});
$("#export").addEventListener("click", async () => {
  try {
    await validate(false);
    const exported = await api("/api/export", {source});
    message("World file saved. ");
    const link = node("a", "Download JSON"); link.href = exported.url; link.download = exported.name;
    $("#message").append(link); link.click();
  } catch (error) { message(error.message, "error"); }
});
$("#import").addEventListener("click", () => $("#import-file").click());
$("#import-file").addEventListener("change", async event => {
  const file = event.target.files[0]; if (!file) return;
  try {
    if (file.size > 1048576) throw new Error("Choose a world file smaller than 1 MiB.");
    const text = await file.text(); await api("/api/validate", {source: text});
    drafts.custom = text; await selectTemplate("custom"); message(`Loaded ${file.name}. Changes are saved as a separate browser draft.`);
  } catch (error) { message(error.message, "error"); }
  finally { event.target.value = ""; }
});
$("#run").addEventListener("click", async () => {
  if (busy || loading) return;
  busy = true; refreshSummary();
  const submittedSource = source;
  try {
    const run = await api("/api/runs", {source: submittedSource});
    selectedRun = run.id; runs.unshift(run); renderResults(); message("Run started on a saved snapshot of the world file.");
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
    else { selected = "custom"; source = drafts.custom || "{}"; $("#source").value = source; renderTemplates(); refreshSummary(); message("Import a valid world file to get started. No templates were found in the configured folder.", "warning"); }
    poll();
  } catch (error) { message(`Cannot load the workspace: ${error.message}. Check that the local server is running.`, "error"); }
})();
