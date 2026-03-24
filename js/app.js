'use strict';

// ============================================================
// STATE
// ============================================================
const state = {
    variables: [],  // [{ id: Number, name: String }]
    links: [],      // [{ from: Number, to: Number, sign: '+' | '-' }]
    nextId: 1
};

// ============================================================
// CORE LOGIC – loop detection & classification
// ============================================================

/**
 * Find all elementary directed cycles in the current graph.
 *
 * To avoid counting the same cycle multiple times we restrict the DFS so
 * that every intermediate node visited must have an ID strictly greater than
 * the starting node's ID.  This ensures each unique cycle is enumerated
 * exactly once (always starting from its minimum-ID node).
 *
 * @returns {number[][]}  Each element is an array of variable IDs forming
 *                         one directed cycle (last → first to close it).
 */
function findAllCycles() {
    const cycles = [];

    state.variables.forEach(startVar => {
        const startId = startVar.id;

        (function dfs(currentId, path, pathSet) {
            const neighbors = state.links
                .filter(l => l.from === currentId)
                .map(l => l.to);

            for (const nextId of neighbors) {
                if (nextId === startId && path.length >= 2) {
                    // Closed the cycle back to start — record it.
                    cycles.push([...path]);
                } else if (!pathSet.has(nextId) && nextId > startId) {
                    // Only extend through nodes with higher IDs to prevent
                    // duplicate enumeration.
                    pathSet.add(nextId);
                    path.push(nextId);
                    dfs(nextId, path, pathSet);
                    path.pop();
                    pathSet.delete(nextId);
                }
            }
        })(startId, [startId], new Set([startId]));
    });

    return cycles;
}

/**
 * Count the number of negative (−) causal links within a directed cycle.
 *
 * @param {number[]} cycle  Ordered array of variable IDs forming the cycle.
 * @returns {number}
 */
function countNegativeLinks(cycle) {
    let count = 0;
    for (let i = 0; i < cycle.length; i++) {
        const from = cycle[i];
        const to   = cycle[(i + 1) % cycle.length];
        const link = state.links.find(l => l.from === from && l.to === to);
        if (link && link.sign === '-') count++;
    }
    return count;
}

/**
 * Classify a cycle as Reinforcing (R) or Balancing (B).
 *
 * Rule:
 *   • Even number of negative links  →  Reinforcing (R)
 *     A positive change amplifies itself (virtuous / vicious cycle).
 *   • Odd  number of negative links  →  Balancing  (B)
 *     A positive change eventually creates an opposing force.
 *
 * @param {number[]} cycle
 * @returns {'R' | 'B'}
 */
function classifyLoop(cycle) {
    return countNegativeLinks(cycle) % 2 === 0 ? 'R' : 'B';
}

/**
 * Validate the "train rule": within the set of nodes in this cycle, every
 * node must have *exactly one* incoming and *exactly one* outgoing causal
 * link that connects it to other nodes in the same cycle.
 *
 * A violation (e.g. two in-links or two out-links for one node) means the
 * loop is not a clean single-path cycle — additional shortcuts or branches
 * exist among the same variables.
 *
 * @param {number[]} cycle
 * @returns {boolean}
 */
function validateTrainRule(cycle) {
    const cycleSet = new Set(cycle);
    for (const nodeId of cycle) {
        const inCount  = state.links.filter(l => l.to   === nodeId && cycleSet.has(l.from)).length;
        const outCount = state.links.filter(l => l.from === nodeId && cycleSet.has(l.to)).length;
        if (inCount !== 1 || outCount !== 1) return false;
    }
    return true;
}

/**
 * Build a human-readable chain string for a cycle, showing each step's sign.
 * e.g.  "Population →(+)→ Births →(+)→ Population"
 *
 * @param {number[]} cycle
 * @returns {string}
 */
function buildChainString(cycle) {
    const parts = [];
    for (let i = 0; i < cycle.length; i++) {
        const from   = cycle[i];
        const to     = cycle[(i + 1) % cycle.length];
        const link   = state.links.find(l => l.from === from && l.to === to);
        const sign   = link ? link.sign : '?';
        const toName = varName(to);
        parts.push(varName(from) + ` <span class="arrow-sign ${sign === '+' ? 'pos' : 'neg'}">→(${sign})→</span> `);
        if (i === cycle.length - 1) parts.push(toName);
    }
    return parts.join('');
}

// ============================================================
// HELPERS
// ============================================================

function varName(id) {
    const v = state.variables.find(v => v.id === id);
    return v ? escHtml(v.name) : '?';
}

function escHtml(str) {
    return str
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;');
}

// ============================================================
// STATE MUTATIONS
// ============================================================

function addVariable() {
    const input = document.getElementById('varName');
    const name  = input.value.trim();
    if (!name) { showMsg('varError', 'Please enter a variable name.'); return; }
    if (state.variables.find(v => v.name.toLowerCase() === name.toLowerCase())) {
        showMsg('varError', 'A variable with that name already exists.');
        return;
    }
    clearMsg('varError');
    state.variables.push({ id: state.nextId++, name });
    input.value = '';
    input.focus();
    renderAll();
}

function removeVariable(id) {
    state.variables = state.variables.filter(v => v.id !== id);
    state.links      = state.links.filter(l => l.from !== id && l.to !== id);
    renderAll();
}

function addLink() {
    const from = parseInt(document.getElementById('linkFrom').value, 10);
    const to   = parseInt(document.getElementById('linkTo').value,   10);
    const sign = document.querySelector('input[name="sign"]:checked').value;

    if (!from || !to) { showMsg('linkError', 'Select both a "From" and a "To" variable.'); return; }
    if (from === to)  { showMsg('linkError', 'A variable cannot link to itself.'); return; }
    if (state.links.find(l => l.from === from && l.to === to)) {
        showMsg('linkError', 'This causal link already exists.');
        return;
    }
    clearMsg('linkError');
    state.links.push({ from, to, sign });
    renderAll();
}

function removeLink(from, to) {
    state.links = state.links.filter(l => !(l.from === from && l.to === to));
    renderAll();
}

function loadSample() {
    clearAll(false);
    // Sample: two classic feedback loops
    //   Loop R – Population & Births (Reinforcing, 0 negatives)
    //   Loop B – Population & Deaths (Balancing,    1 negative)
    const vars = [
        { id: 1, name: 'Population' },
        { id: 2, name: 'Births' },
        { id: 3, name: 'Deaths' }
    ];
    const links = [
        { from: 1, to: 2, sign: '+' },  // Population → Births  (+)
        { from: 2, to: 1, sign: '+' },  // Births → Population  (+)  ← R loop
        { from: 1, to: 3, sign: '+' },  // Population → Deaths  (+)
        { from: 3, to: 1, sign: '-' }   // Deaths → Population  (−)  ← B loop
    ];
    state.variables = vars;
    state.links     = links;
    state.nextId    = 4;
    renderAll();
    analyzeLoops();
}

function clearAll(resetResults = true) {
    state.variables = [];
    state.links     = [];
    state.nextId    = 1;
    clearMsg('varError');
    clearMsg('linkError');
    renderAll();
    if (resetResults) {
        document.getElementById('results').innerHTML =
            '<p class="placeholder-text">Add variables and causal links, then click <strong>Analyze Loops</strong>.</p>';
    }
}

// ============================================================
// ANALYSIS
// ============================================================

function analyzeLoops() {
    const resultsDiv = document.getElementById('results');

    if (state.variables.length < 2) {
        resultsDiv.innerHTML = '<p class="msg msg-warning">Add at least 2 variables to analyze loops.</p>';
        return;
    }
    if (state.links.length === 0) {
        resultsDiv.innerHTML = '<p class="msg msg-warning">Add causal links to form loops.</p>';
        return;
    }

    const cycles = findAllCycles();

    if (cycles.length === 0) {
        resultsDiv.innerHTML =
            '<p class="msg msg-warning">No feedback loops detected. ' +
            'Make sure the diagram contains at least one directed cycle.</p>';
        return;
    }

    let html = `<p class="result-summary">${cycles.length} feedback loop${cycles.length > 1 ? 's' : ''} found:</p>`;

    cycles.forEach((cycle, i) => {
        const type       = classifyLoop(cycle);
        const negCount   = countNegativeLinks(cycle);
        const trainOk    = validateTrainRule(cycle);
        const typeClass  = type === 'R' ? 'reinforcing' : 'balancing';
        const typeLabel  = type === 'R' ? 'Reinforcing (R)' : 'Balancing (B)';
        const evenOdd    = negCount % 2 === 0 ? 'even' : 'odd';
        const negClass   = negCount % 2 === 0 ? 'tag-even' : 'tag-odd';

        html += `
        <div class="loop-card ${typeClass}">
            <div class="loop-card-header">
                <span class="loop-type-badge">${typeLabel}</span>
                <span class="loop-number">Loop ${i + 1}</span>
            </div>
            <div class="loop-path">${buildChainString(cycle)}</div>
            <div class="loop-meta">
                <span>Negative links: <strong class="${negClass}">${negCount} (${evenOdd})</strong>
                    &mdash; ${type === 'R' ? 'even → Reinforcing' : 'odd → Balancing'}</span>
                <span class="${trainOk ? 'tag-valid' : 'tag-invalid'}">
                    Train rule: ${trainOk
                        ? '✓ Valid — each variable has exactly one in-connection and one out-connection within this loop'
                        : '✗ Invalid — one or more variables have multiple in- or out-connections within this loop'}
                </span>
            </div>
            <div class="loop-explanation">
                ${type === 'R'
                    ? '⚡ <strong>Reinforcing:</strong> A positive change amplifies itself — leads to exponential growth (virtuous cycle) or collapse (vicious cycle). "The more A, the more B, which leads to even more A."'
                    : '⚖ <strong>Balancing:</strong> A positive change triggers an opposing force — goal-seeking or stabilising behaviour. "The more A, the more B, which pushes A back down."'}
            </div>
        </div>`;
    });

    resultsDiv.innerHTML = html;
}

// ============================================================
// RENDER HELPERS
// ============================================================

function renderAll() {
    renderVarList();
    renderLinkList();
    updateSelects();
    renderDiagram();
}

function renderVarList() {
    const ul = document.getElementById('varList');
    if (state.variables.length === 0) {
        ul.innerHTML = '<li class="list-empty">No variables yet.</li>';
        return;
    }
    ul.innerHTML = state.variables.map(v => `
        <li>
            <span class="item-label">${escHtml(v.name)}</span>
            <button class="btn-remove" onclick="removeVariable(${v.id})" title="Remove variable">✕</button>
        </li>`).join('');
}

function renderLinkList() {
    const ul = document.getElementById('linkList');
    if (state.links.length === 0) {
        ul.innerHTML = '<li class="list-empty">No links yet.</li>';
        return;
    }
    ul.innerHTML = state.links.map(l => {
        const fName = varName(l.from);
        const tName = varName(l.to);
        const cls   = l.sign === '+' ? 'pos' : 'neg';
        return `
        <li>
            <span class="item-label">${fName}
                <span class="link-sign ${cls}">→(${l.sign})→</span>
                ${tName}
            </span>
            <button class="btn-remove" onclick="removeLink(${l.from},${l.to})" title="Remove link">✕</button>
        </li>`;
    }).join('');
}

function updateSelects() {
    const opts      = state.variables.map(v => `<option value="${v.id}">${escHtml(v.name)}</option>`).join('');
    const fromSel   = document.getElementById('linkFrom');
    const toSel     = document.getElementById('linkTo');
    const prevFrom  = fromSel.value;
    const prevTo    = toSel.value;
    fromSel.innerHTML = '<option value="">From…</option>' + opts;
    toSel.innerHTML   = '<option value="">To…</option>'   + opts;
    if (state.variables.find(v => v.id == prevFrom)) fromSel.value = prevFrom;
    if (state.variables.find(v => v.id == prevTo))   toSel.value   = prevTo;
}

// ============================================================
// SVG DIAGRAM
// ============================================================

const NODE_R   = 32;   // node circle radius (px)
const SIGN_R   = 10;   // sign badge radius
const CURVE_D  = 30;   // curvature offset for bidirectional links

function renderDiagram() {
    const svg  = document.getElementById('diagram');
    const W    = svg.clientWidth  || 600;
    const H    = svg.clientHeight || 380;

    if (state.variables.length === 0) {
        svg.innerHTML = `<text x="50%" y="50%" text-anchor="middle"
            class="svg-placeholder">Add variables to see the diagram</text>`;
        return;
    }

    // Position nodes in a circle
    const cx = W / 2;
    const cy = H / 2;
    const r  = Math.min(cx, cy) * 0.68;
    const step = (2 * Math.PI) / state.variables.length;

    const pos = {};
    state.variables.forEach((v, i) => {
        const angle = i * step - Math.PI / 2;
        pos[v.id]   = { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) };
    });

    let svgInner = buildDefs();

    // Draw edges first (below nodes)
    state.links.forEach(link => {
        const P = pos[link.from];
        const Q = pos[link.to];
        if (!P || !Q) return;

        // Check if a reverse link also exists (needs curvature to stay visible)
        const hasReverse = state.links.some(l => l.from === link.to && l.to === link.from);
        svgInner += buildEdge(P, Q, link.sign, hasReverse);
    });

    // Draw nodes on top
    state.variables.forEach(v => {
        const p = pos[v.id];
        const words = wrapLabel(v.name, 10); // max 10 chars per line
        svgInner += buildNode(p.x, p.y, words);
    });

    svg.innerHTML = svgInner;
}

function buildDefs() {
    return `
    <defs>
        <marker id="arr-pos" markerWidth="9" markerHeight="6"
                refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#2563eb"/>
        </marker>
        <marker id="arr-neg" markerWidth="9" markerHeight="6"
                refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#dc2626"/>
        </marker>
    </defs>`;
}

function buildEdge(P, Q, sign, curved) {
    const color    = sign === '+' ? '#2563eb' : '#dc2626';
    const markerId = sign === '+' ? 'arr-pos'  : 'arr-neg';

    // Direction unit vector
    const dx   = Q.x - P.x;
    const dy   = Q.y - P.y;
    const dist = Math.hypot(dx, dy);
    const ux   = dx / dist;
    const uy   = dy / dist;

    // Start/end points offset so arrow touches node edge, not center
    const sx = P.x + ux * NODE_R;
    const sy = P.y + uy * NODE_R;
    const ex = Q.x - ux * NODE_R;
    const ey = Q.y - uy * NODE_R;

    let pathD;
    let mx, my; // midpoint for sign badge

    if (curved) {
        // Perpendicular offset
        const px = -uy * CURVE_D;
        const py =  ux * CURVE_D;
        const cpx = (sx + ex) / 2 + px;
        const cpy = (sy + ey) / 2 + py;
        pathD = `M${sx},${sy} Q${cpx},${cpy} ${ex},${ey}`;
        mx = (sx + ex) / 2 + px * 0.5;
        my = (sy + ey) / 2 + py * 0.5;
    } else {
        pathD = `M${sx},${sy} L${ex},${ey}`;
        mx = (sx + ex) / 2;
        my = (sy + ey) / 2;
    }

    return `
    <path d="${pathD}" stroke="${color}" stroke-width="2" fill="none"
          marker-end="url(#${markerId})"/>
    <circle cx="${mx}" cy="${my}" r="${SIGN_R}" fill="${color}"/>
    <text x="${mx}" y="${my}" text-anchor="middle" dominant-baseline="central"
          fill="white" font-size="11" font-weight="bold"
          font-family="monospace">${sign}</text>`;
}

function buildNode(x, y, lines) {
    const lineH = 14;
    const totalH = lines.length * lineH;
    const startY = y - totalH / 2 + lineH / 2;
    const textRows = lines.map((t, i) =>
        `<tspan x="${x}" dy="${i === 0 ? startY - y : lineH}">${escHtml(t)}</tspan>`
    ).join('');

    return `
    <circle cx="${x}" cy="${y}" r="${NODE_R}"
            fill="white" stroke="#374151" stroke-width="2"/>
    <text x="${x}" y="${y}" text-anchor="middle"
          font-size="11" fill="#1f2937" font-family="inherit">
        ${textRows}
    </text>`;
}

/**
 * Wrap a label into lines of at most maxChars characters.
 * Splits on spaces; never splits within a word.
 */
function wrapLabel(text, maxChars) {
    const words = text.split(' ');
    const lines = [];
    let current = '';
    words.forEach(w => {
        if (current.length === 0) {
            current = w;
        } else if (current.length + 1 + w.length <= maxChars) {
            current += ' ' + w;
        } else {
            lines.push(current);
            current = w;
        }
    });
    if (current) lines.push(current);
    return lines;
}

// ============================================================
// UI MESSAGES
// ============================================================

function showMsg(id, text) {
    let el = document.getElementById(id);
    if (!el) {
        el = document.createElement('p');
        el.id = id;
        el.className = 'field-error';
    }
    el.textContent = text;
    // Insert after the relevant button
    const form = id === 'varError'
        ? document.querySelector('.var-form')
        : document.querySelector('.link-form');
    if (form && !document.getElementById(id)) form.appendChild(el);
}

function clearMsg(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ============================================================
// EVENT WIRING
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btnAddVar')
        .addEventListener('click', addVariable);

    document.getElementById('varName')
        .addEventListener('keydown', e => { if (e.key === 'Enter') addVariable(); });

    document.getElementById('btnAddLink')
        .addEventListener('click', addLink);

    document.getElementById('btnAnalyze')
        .addEventListener('click', analyzeLoops);

    document.getElementById('btnSample')
        .addEventListener('click', loadSample);

    document.getElementById('btnClear')
        .addEventListener('click', () => clearAll(true));

    window.addEventListener('resize', () => renderDiagram());

    renderAll();
});
