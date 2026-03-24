# Causal Loop Diagram (CLD) Tool

A browser-based tool for building and classifying **Causal Loop Diagrams (CLD)**.
Add variables, connect them with positive (+) or negative (−) causal links, and
instantly detect whether each feedback loop is **Reinforcing (R)** or **Balancing (B)**.

---

## How to Run

Open `index.html` in any modern browser — no server or build step required.

---

## Features

| Feature | Description |
|---|---|
| Add / remove variables | Named nodes in the diagram |
| Add / remove causal links | Directed arrows with **+** (positive) or **−** (negative) sign |
| SVG diagram | Variables shown as circles, arrows colour-coded blue (+) / red (−) |
| Loop detection | Finds all elementary directed cycles automatically |
| Loop classification | **R (Reinforcing)** or **B (Balancing)** per cycle |
| Train-rule validation | Flags cycles where a variable has more than one in- or out-connection within the loop |
| Sample data | One-click example with both an R loop and a B loop |

---

## Loop Classification Rules

### Reinforcing Loop (R) — Amplifying feedback
* Contains an **even** number of negative (−) causal links (0, 2, 4 …).
* A positive initial change circulates and comes back as a positive change,
  amplifying the original direction.
* Creates *virtuous cycles* (growth) or *vicious cycles* (collapse).
* Common language: *"The more A, the more B, which leads to even more A."*

### Balancing Loop (B) — Stabilising feedback
* Contains an **odd** number of negative (−) causal links (1, 3, 5 …).
* A positive initial change circulates and comes back as a negative change,
  opposing the original direction.
* Creates goal-seeking or oscillating behaviour.
* Common language: *"The more A, the more B, which pushes A back down."*

### Train Rule
Every variable in a valid feedback loop must have **exactly one incoming** and
**exactly one outgoing** causal link to/from other variables in the same loop.
If a variable has two in-connections or two out-connections among the loop's
nodes, the loop structure is ambiguous and flagged as invalid.

---

## Quick Example

**Reinforcing loop (0 negative links):**

```
Population →(+)→ Births →(+)→ Population
```
Both links positive → 0 negative links (even) → **Reinforcing (R)** ✓

**Balancing loop (1 negative link):**

```
Population →(+)→ Deaths →(−)→ Population
```
One negative link (odd) → **Balancing (B)** ✓

---

## Project Structure

```
index.html        Main application page
css/style.css     Stylesheet
js/app.js         Core logic: cycle detection, loop classification, diagram rendering
README.md         This file
```

---

## Technology

Pure HTML5 / CSS3 / JavaScript (ES6+) — no frameworks or build tools needed.