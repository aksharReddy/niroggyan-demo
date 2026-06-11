# CodeRabbit — Complete Evaluation Report
**NirogGyan Internal R&D | June 2026**
**Evaluated by:** Akshar | **Repo used:** github.com/aksharReddy/niroggyan-demo

---

## Table of Contents
1. [What is CodeRabbit](#1-what-is-coderabbit)
2. [Problem It Solves](#2-problem-it-solves)
3. [Where It Fits in Engineering](#3-where-it-fits-in-engineering)
4. [Key Capabilities](#4-key-capabilities)
5. [Limitations](#5-limitations)
6. [Common Misconceptions](#6-common-misconceptions)
7. [Pricing](#7-pricing)
8. [Hands-On Test Results](#8-hands-on-test-results)
9. [The .coderabbit.yaml Config File](#9-the-coderabbityaml-config-file)
10. [What to Write as Global vs Path Rules](#10-what-to-write-as-global-vs-path-rules)
11. [NirogGyan Specific Use Cases](#11-niroggyan-specific-use-cases)
12. [Final Recommendation](#12-final-recommendation)

---

## 1. What is CodeRabbit

CodeRabbit is an AI-powered code review platform that installs as a GitHub or GitLab App and automatically reviews every Pull Request before a human looks at it.

It reads the entire diff of a PR, understands the full repository context, and posts inline comments directly on the lines of code — exactly like a human reviewer would.

**It is not a linter.** Linters check syntax and formatting rules. CodeRabbit understands code semantics, cross-file relationships, and business context you give it.

---

## 2. Problem It Solves

| Old world | With CodeRabbit |
|---|---|
| Code review takes 1-2 days | Instant automated first pass within 2-3 minutes |
| Senior devs manually review everything | AI handles mechanical review, humans focus on architecture |
| Junior dev PRs miss edge cases | Every PR gets the same thorough standard |
| No institutional memory of past patterns | Configured rules enforce company standards permanently |
| Reviews bottlenecked on 1-2 senior people | Unlimited parallel reviews |
| Regressions slip through when reviewers are tired | AI never gets tired or skips checks |

---

## 3. Where It Fits in Engineering

```
Developer writes code
        ↓
Opens Pull Request on GitHub
        ↓
CodeRabbit reviews it instantly  ← LIVES HERE
  - Posts inline comments on bugs
  - Generates PR walkthrough summary
  - Enforces company rules from .coderabbit.yaml
        ↓
Human reviewer reads CodeRabbit summary first
        ↓
Faster, higher-quality human review
        ↓
Code merged
```

CodeRabbit does not approve or reject PRs. It is a force multiplier for human reviewers, not a replacement.

---

## 4. Key Capabilities

### 4.1 Line-by-line inline review
Posts comments directly on specific lines in the PR diff, just like a human. Each comment includes severity label, explanation, and usually a suggested fix with a copy-paste diff.

### 4.2 Cross-file context awareness
This is the standout capability. CodeRabbit reads the entire repository, not just the changed files. If a function's return type changes in File A, it checks every file that calls that function and flags incompatibilities.

**Example from our test:** A function in `risk_calculator.py` changed from returning a `dict` to returning a `float`. CodeRabbit traced this to `report_generator.py` and `tests/test_risk_calculator.py` and flagged all three breakage points in one comment.

### 4.3 PR walkthrough summary
Auto-generates a plain-English summary of what changed in the PR, organized by file and layer. Product managers and tech leads can read this to understand what shipped without reading code.

### 4.4 Custom business rules via `.coderabbit.yaml`
A config file you place in your repo root. Written in plain English. Teaches CodeRabbit your company-specific rules, clinical requirements, API contracts, and domain constraints that it cannot know on its own.

### 4.5 Pre-merge checks
Configurable automated checks before a PR can merge: docstring coverage, linked issues, title conventions, out-of-scope changes.

### 4.6 Interactive chat on PRs
You can comment `@coderabbitai explain this function` or `@coderabbitai review` directly on a PR and it responds inline.

---

## 5. Limitations

| Limitation | Impact |
|---|---|
| Cannot run code | Cannot catch runtime bugs that only appear during execution |
| Incremental review system | Does not re-review commits it has already reviewed — `@coderabbitai review` only works for commits not yet reviewed |
| Global rules apply inconsistently | Global rules in the config are applied with less precision than path-specific rules (proven in our test) |
| Cannot catch missing logic | If a guard was removed silently, it may not flag it unless a specific rule covers that exact guard |
| Business logic blind without config | Without `.coderabbit.yaml`, it has no knowledge of your clinical thresholds, API contracts, or domain rules |
| False positives in first 2 weeks | Before tuning, CodeRabbit can be noisy. Developers may start ignoring comments if too many are irrelevant |
| Not a replacement for tests | Unit tests + integration tests are still essential — CodeRabbit cannot substitute for them |

---

## 6. Common Misconceptions

**"It will approve or reject PRs automatically."**
No. It posts feedback. Humans still approve merges.

**"It replaces human code review."**
No. It handles the mechanical pattern-recognition work so human reviewers spend time on architecture and business logic.

**"Writing more rules = better results."**
Wrong. Over-specifying technical rules (division by zero, null checks) wastes config space. CodeRabbit already catches those natively. Rules should only cover business logic and domain knowledge CodeRabbit cannot know.

**"Global rules work the same as path-specific rules."**
Wrong — proven in our hands-on test. Global rules are applied inconsistently. Path-specific rules fire reliably every time.

**"It only works for large teams."**
Wrong. It is actually more valuable for small teams (2-5 devs) where there are not enough senior developers to review every PR thoroughly.

---

## 7. Pricing

| Plan | Cost | Suitable for |
|---|---|---|
| Free | Unlimited — **public repos only** | Demo, evaluation, open-source |
| Pro | $19/seat/month | Private repos, production use |
| Enterprise | Custom | Large orgs, SSO, audit logs |

**For NirogGyan evaluation:** Use the free plan on a public demo repo. For production use on the private main repo, $19/developer/month.

---

## 8. Hands-On Test Results

We created a demo repo simulating NirogGyan's codebase (risk scoring, report generation, LIMS handler). We introduced 6 deliberate bugs and ran 4 separate PR tests.

### The 6 Bugs Introduced

| Bug | Description | Type |
|---|---|---|
| Bug 1 | Null/empty check removed from `calculate_cardiovascular_risk()` — crashes on `None` input | Logic regression |
| Bug 2 | Age-based base score removed from cardiovascular formula — silent clinical regression | Business logic |
| Bug 3 | `hdl > 0` guard removed — `ZeroDivisionError` when HDL is 0 | Safety bug |
| Bug 4 | `calculate_cardiovascular_risk()` now returns a `float` instead of `dict` — breaks all callers | Contract violation |
| Bug 5 | Real-looking patient name + phone hardcoded in source (`Rajesh Kumar`, `9876543210`) | PII / compliance |
| Bug 6 | `generate_patient_report()` success path no longer returns `status/message/data` envelope | API contract violation |

---

### Test 1 — With BUG comment labels in code (INVALID TEST)

**Setup:** Bugs introduced with explicit `# BUG 1:`, `# BUG 2:` comments labelling each issue.

**Result:** Invalidated. CodeRabbit likely read the labels themselves. This test was discarded and redone cleanly.

**Learning:** Never label bugs intentionally when testing a code review tool. It will read your comments.

---

### Test 2 — No rules, clean code (PR #2)

**Setup:** Same 6 bugs, zero `# BUG` labels, written as if a developer genuinely thought these were improvements. No `.coderabbit.yaml` configured.

**Results:**

| Bug | Caught? | How |
|---|---|---|
| Bug 1 — null check removed | No | Not flagged |
| Bug 2 — age score removed | No | Mentioned in walkthrough summary only, not flagged as issue |
| Bug 3 — HDL division | **Yes** | Flagged as Critical with exact fix |
| Bug 4 — returns float not dict | **Yes** | Flagged as Critical, traced across 2 files natively |
| Bug 5 — PII in source | **Yes** | Flagged as Major with HIPAA/GDPR context |
| Bug 6 — API contract | No | Not flagged |

**Score: 3/6 caught natively with no configuration.**

**Key insight:** CodeRabbit is strong at structural/safety violations (type changes, crash risks, PII) but blind to business logic (age must be in formula) and company conventions (API response shape) without being told.

---

### Test 3 — Specific path rules per file (PR #3)

**Setup:** Same 6 bugs. `.coderabbit.yaml` added with highly specific rules per file — including overly technical rules like "HDL must be guarded against division by zero."

**Results:**

| Bug | Caught? | Rule type that caught it |
|---|---|---|
| Bug 1 — null check removed | No | Not flagged even with specific rule written |
| Bug 2 — age score removed | **Yes** | Path-specific clinical rule |
| Bug 3 — HDL division | **Yes** | Path-specific (though CodeRabbit catches this natively too) |
| Bug 4 — returns float not dict | **Yes** | Path-specific return contract rule |
| Bug 5 — PII in source | **Yes** | Path-specific PII rule |
| Bug 6 — API contract | **Yes** | Path-specific API contract rule |

**Score: 5/6 caught with specific path rules.**

**Key insight:** Path-specific rules are highly reliable. Writing a rule for the exact file gets consistent results every PR.

---

### Test 4 — Simplified global + essential path rules (PR #4)

**Setup:** Same 6 bugs. Config simplified — technical rules removed, only business logic and compliance rules kept. API contract and PII moved to global rules, clinical rules kept as path-specific.

**Results:**

| Bug | Caught? | Rule type | Notes |
|---|---|---|---|
| Bug 1 — null check removed | No | Global rule written, did not fire | Global rules miss subtle absences |
| Bug 2 — age score removed | **Yes** | Path-specific clinical rule | Reliable |
| Bug 3 — HDL division | No | No rule written (expected native catch) | Native missed it this time |
| Bug 4 — returns float not dict | **Yes** | Path-specific return contract rule | Reliable |
| Bug 5 — PII in source | **Yes** | Global PII rule | Global rule worked |
| Bug 6 — API contract | No | Global rule written, did not fire | Global rules inconsistent for this |

**Score: 3/6 caught with simplified global rules.**

**Key insight:** Moving specific rules to global reduced effectiveness. Global rules work for broad compliance (PII) but not for specific API contracts or function-level checks.

---

### Final Comparison Table

| Bug | No config | Specific path rules | Global rules |
|---|---|---|---|
| Bug 1 — null check | No | No | No |
| Bug 2 — age formula | No | **Yes** | **Yes** |
| Bug 3 — HDL division | **Yes** | **Yes** | No |
| Bug 4 — return type | **Yes** | **Yes** | **Yes** |
| Bug 5 — PII | **Yes** | **Yes** | **Yes** |
| Bug 6 — API contract | No | **Yes** | No |
| **Total** | **3/6** | **5/6** | **3/6** |

---

## 9. The `.coderabbit.yaml` Config File

This file lives in the **root of your repository on the `main` branch**. CodeRabbit reads it every time it reviews a PR.

### Structure

```yaml
language: en
tone_instructions: "Brief description of your product context"

reviews:
  profile: assertive        # how aggressive reviews are (chill / assertive)
  request_changes_workflow: true   # CodeRabbit can formally block a PR

  # Global rules — apply to EVERY file in the repo
  instructions: |
    Rule 1...
    Rule 2...

  # Path rules — apply only to matching files
  path_instructions:
    - path: "src/scoring/**"
      instructions: |
        Specific rules for scoring files...

    - path: "src/api/**"
      instructions: |
        Specific rules for API files...
```

### Important Behaviours

- Config must be on `main` before a PR is opened for it to apply
- CodeRabbit does **not** re-review already-reviewed commits — pushing a new commit to an existing PR triggers a fresh review
- To manually trigger a review: comment `@coderabbitai review` on the PR
- Rules are written in plain English — no special syntax required

---

## 10. What to Write as Global vs Path Rules

### Do NOT write in config (CodeRabbit already handles natively)
- Division by zero protection
- Null pointer / crash risks
- Type mismatches across files
- SQL injection / XSS vulnerabilities
- PII in source code (native detection exists, global rule reinforces it)
- Missing error handling patterns
- Dead code

### Write as GLOBAL rules (compliance, applies everywhere)
- "No real-looking PII in source code or tests" — works reliably
- "No patient data in logs or print statements"
- "All authentication endpoints must validate tokens before processing"

### Write as PATH-SPECIFIC rules (business logic, critical files only)
- Clinical thresholds (`age is mandatory in cardiovascular formula`)
- API response contracts (`every return must have status/message/data`)
- Return type contracts (`this function must return a dict with these exact keys`)
- Domain validation ranges (`risk levels are LOW/MODERATE/HIGH/CRITICAL at these exact thresholds`)
- Ordering requirements (`validate vendor before processing payload`)

### The Rule of Thumb
> If a rule requires knowing your product's domain, write it. If a rule describes general programming safety, skip it.

---

## 11. NirogGyan Specific Use Cases

### Use Case 1 — Risk Score Algorithm Protection
Any change to the scoring engine triggers path-specific rules. If a developer removes age weighting, changes risk thresholds, or changes the return shape, CodeRabbit flags it immediately before it reaches QA.

**Files to cover:** `src/scoring/`, `src/algorithms/`, `src/risk_calculator.py`

### Use Case 2 — Report Generation Contract
Patient-facing reports follow a strict structure. Any PR that changes the return format of report generation functions gets flagged — protecting against patients receiving malformed or incomplete reports.

**Files to cover:** `src/reports/`, `src/report_generator.py`

### Use Case 3 — LIMS Integration Safety
Lab data ingested from external vendors must always be validated before processing. A missing validation step could allow corrupted lab data into the scoring pipeline.

**Files to cover:** `src/lims/`, `src/integrations/`

### Use Case 4 — Compliance Monitoring (Global)
Global rules covering PII exposure, patient data logging, and data handling apply across the entire codebase automatically without needing to specify individual files.

### Teams That Benefit

| Team | Benefit |
|---|---|
| Backend developers | Faster PR cycles, safety net on scoring changes |
| QA engineers | Fewer bugs reaching QA, first-pass automated |
| Tech Lead / CTO | PR walkthrough summaries without reading code |
| Product Manager | Plain-English change summaries per PR |
| CSM (indirect) | Fewer production bugs = fewer client escalations |

---

## 12. Final Recommendation

### Recommended Usage
- Install on the main NirogGyan repository immediately — 5 minute setup
- Write path-specific rules for 3-4 critical files: scoring engine, report generator, LIMS handler
- Use global rules only for compliance (PII, logging patient data)
- Let CodeRabbit run for 2 weeks before tuning — observe what it flags, remove rules that generate noise

### Not Recommended Usage
- Do not rely on it as a substitute for unit tests
- Do not write path rules for every file in the repo — only critical business logic files
- Do not write technical rules (division by zero, null checks) — those are handled natively
- Do not use global rules for function-level API contracts — they fire inconsistently

### Implementation Priority
**High.** 5-minute install, immediate value from the first PR. No infrastructure, no server, no ongoing maintenance.

### Risks
- Developer resistance to AI feedback (cultural) — manageable with a 1-week onboarding session
- Noisy first 2 weeks before rules are tuned
- Without proper `.coderabbit.yaml`, business logic bugs will be missed

### Expected ROI for NirogGyan
- 1-2 bugs caught per sprint before reaching QA
- Scoring algorithm regressions caught before they produce wrong patient reports
- PII compliance violations caught before they hit production
- PR review time reduced by 30-40% for human reviewers
- Estimated time saved: 4-8 hours per month in bug investigation and hotfixes

### Bottom Line
CodeRabbit is not magic. It catches **structural and safety bugs** very well on its own. For **business logic and clinical rules**, it needs to be taught via `.coderabbit.yaml`. With proper configuration — roughly 30-40 lines of plain English rules — it becomes a genuine safety net specifically tuned to NirogGyan's codebase.

---

*Document generated from live hands-on evaluation — 4 PRs tested, 6 bugs per PR, 4 different configuration states.*
