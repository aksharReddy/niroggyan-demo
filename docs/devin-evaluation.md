# Devin AI — Complete Evaluation Report
**NirogGyan Internal R&D | June 2026**
**Evaluated by:** Akshar | **Repo used:** github.com/aksharReddy/niroggyan-demo

---

## Table of Contents
1. [What is Devin AI](#1-what-is-devin-ai)
2. [Problem It Solves](#2-problem-it-solves)
3. [Where It Fits in Engineering](#3-where-it-fits-in-engineering)
4. [Key Capabilities](#4-key-capabilities)
5. [Limitations](#5-limitations)
6. [Common Misconceptions](#6-common-misconceptions)
7. [Pricing](#7-pricing)
8. [Devin vs Other AI Tools](#8-devin-vs-other-ai-tools)
9. [Hands-On Test Results](#9-hands-on-test-results)
10. [NirogGyan Specific Use Cases](#10-niroggyan-specific-use-cases)
11. [Final Recommendation](#11-final-recommendation)

---

## 1. What is Devin AI

Devin is an autonomous AI software engineer. Unlike AI chat tools (ChatGPT, Claude) that suggest code for you to copy, or review tools (CodeRabbit) that read code and post comments, Devin **executes tasks inside a real computer environment**.

It has access to:
- A full terminal — runs commands, installs packages, executes tests
- A code editor — writes and modifies files
- A browser — reads documentation, checks URLs
- GitHub — clones repos, commits code, opens Pull Requests

You give it a task in plain English. It plans the steps, executes them, reads errors, fixes them, and iterates until done or stuck.

---

## 2. Problem It Solves

| Situation | Without Devin | With Devin |
|---|---|---|
| "Run the test suite and report what's failing" | Developer runs manually, reads output | Devin runs, interprets, reports structured results |
| "Fix this failing test" | Dev investigates root cause, writes fix | Devin traces failure, fixes, re-runs to verify |
| "Write unit tests for this function" | Dev spends 1-2 hours writing edge cases | Devin writes comprehensive tests in minutes |
| "This CI build is broken" | Senior dev investigates logs for 1 hour | Devin reads logs, traces error, opens fix PR |
| "Integrate this new SDK" | Dev reads docs, writes boilerplate, debugs | Devin reads the docs itself, implements |

Core value: **It executes the mechanical, well-defined parts of engineering work autonomously.**

---

## 3. Where It Fits in Engineering

```
Developer writes feature code
        ↓
Devin writes tests for it           ← Devin (test generation)
        ↓
Developer opens Pull Request
        ↓
CodeRabbit reviews the PR           ← CodeRabbit (static review)
        ↓
Devin runs full test suite          ← Devin (CI execution + reporting)
        ↓
Devin fixes any test failures       ← Devin (autonomous bug fixing)
        ↓
CodeRabbit reviews Devin's fix PR   ← CodeRabbit (validates Devin's code)
        ↓
Human approves and merges
```

Devin handles **execution and generation**. CodeRabbit handles **reading and reviewing**. They do not compete.

---

## 4. Key Capabilities

### 4.1 Autonomous task execution
Devin creates a plan, breaks it into subtasks, and executes each one. It shows you its work in real time — you can watch it type commands in the terminal, see what it installs, read what errors it encounters.

### 4.2 Runs real code
This is the fundamental difference from every other AI tool. Devin does not just suggest code — it runs it. If the code throws an error, Devin reads the error and tries to fix it. If tests fail, it sees exactly which assertions failed and why.

### 4.3 Test generation
Devin's strongest consistent use case. Given a function, it can write:
- Happy path tests
- Error handling tests (None input, missing fields)
- Boundary condition tests (values at exact thresholds)
- Clamping tests (max/min value enforcement)
It correctly uses the `{**base, "field": value}` isolation pattern to test one variable at a time.

### 4.4 Bug fixing from test failures
If you point Devin at a failing test suite, it traces the failure to the root cause and fixes the source code. Tested on our demo repo — it correctly fixed a return type bug and a missing null check from test failures alone.

### 4.5 Reads documentation independently
Devin has a browser. You can give it tasks like "integrate the Razorpay payment SDK" and it will read the Razorpay documentation itself rather than relying on training data.

### 4.6 Works in parallel
Multiple Devin sessions can run simultaneously on independent tasks, effectively giving you multiple AI engineers working in parallel.

---

## 5. Limitations

| Limitation | Practical Impact |
|---|---|
| Weaker model than Claude 4 | Will make mistakes Claude Code wouldn't. Always review Devin's output before merging |
| Expensive at scale | ~$500/month or pay-per-ACU. Must assign tasks strategically |
| Struggles with vague tasks | "Improve the codebase" spirals and wastes money. Tasks need clear success criteria |
| No memory between sessions | Each session starts fresh. Must re-explain context every time |
| Can loop on hard bugs | Sometimes iterates without progress. Needs human to rephrase or intervene |
| Cannot catch non-runtime issues | Won't catch business logic violations, PII, or API contract issues unless a test specifically covers them |
| Not production-ready without review | Devin's code must go through CodeRabbit or human review before merging |
| No domain knowledge | Does not know your clinical rules, scoring logic, or compliance requirements unless explicitly told |

---

## 6. Common Misconceptions

**"Devin replaces developers."**
No. Devin handles well-defined mechanical tasks. Architectural decisions, business logic design, and complex debugging still need senior engineers.

**"Devin is just ChatGPT that writes code."**
No. ChatGPT suggests code. Devin runs it, sees if it works, and iterates. That's a fundamentally different capability.

**"It's always accurate."**
No. Devin makes mistakes. It fixed both bugs correctly in our test, but in complex scenarios it can introduce new bugs while fixing old ones. Review is mandatory.

**"More expensive = always use it."**
Wrong. Devin is expensive. Use it for tasks with clear scope and success criteria. Don't use it for exploratory or open-ended work.

**"It can replace CodeRabbit."**
No. Devin cannot catch static issues — PII in source code, business rule violations, API contract changes. It can only catch things that manifest as test failures. CodeRabbit and Devin cover different failure modes.

---

## 7. Pricing

| Plan | Structure | Suitable for |
|---|---|---|
| Pay-per-ACU | Charged by compute time per task | Occasional specific tasks |
| Teams plan | ~$500/month | Regular engineering use |
| Enterprise | Custom | Large orgs |

**ACU cost guidance:**
| Task | Estimated cost |
|---|---|
| Run test suite and report | ~$0.50 |
| Fix one specific known bug | ~$1-2 |
| Write unit tests for one function | ~$1-2 |
| Fix a failing CI build | ~$2-5 |
| Open-ended "improve codebase" | $10-20+ (avoid) |

**For NirogGyan:** Current balance $909. For focused evaluation (3 tasks), spent approximately $2-3. Budget is not a concern for strategic use — waste risk only comes from vague, open-ended tasks.

---

## 8. Devin vs Other AI Tools

| Tool | What it does | Runs code? | Commits to GitHub? | Reviews PRs? |
|---|---|---|---|---|
| **Devin** | Autonomous engineering tasks | Yes | Yes | No |
| **CodeRabbit** | AI code review | No | No | Yes |
| **Claude Code** | AI pair programmer (local) | Yes (local) | With permission | No |
| **ChatGPT / Claude chat** | Code suggestions | No | No | No |
| **GitHub Copilot** | Inline code completion | No | No | Limited |

**The stack:** Devin + CodeRabbit + Claude Code covers the full engineering loop. None of them overlap.

---

## 9. Hands-On Test Results

We tested Devin on the `niroggyan-demo` repo using the same 6 bugs introduced for CodeRabbit testing. Three tasks were run.

---

### Task 1 — Run Test Suite and Report

**Prompt given:**
> Clone the repo, install dependencies, run pytest, report pass/fail counts and per-failure errors. Do not fix anything.

**What Devin did:**
1. Cloned the repo
2. Detected there was no `requirements.txt` — installed `pytest` independently
3. Ran `python3 -m pytest` from project root
4. Reported structured results

**Result:** 14 passed, 0 failed (main branch has clean code — correct baseline)
**Time:** 27 seconds
**Estimated cost:** ~$0.50

**What this proves:** Devin can autonomously set up an unknown codebase and execute its test suite without any handholding. In a real workflow this is the nightly health check.

---

### Task 2 — Identify Failures and Fix Bugs

**Prompt given:**
> On branch `feature/scoring-v4-global-rules-test`, run pytest, show failures, fix two specific bugs in `calculate_cardiovascular_risk()`: wrong return type (float instead of dict) and missing None/empty input check. Run tests again to confirm. Open a PR.

**What Devin did:**
1. Checked out the feature branch
2. Ran pytest — correctly identified 6 failing tests before touching any code
3. Traced failures to `calculate_cardiovascular_risk()` returning a float
4. Fixed return type: now returns `{"score": ..., "risk_level": ..., "patient_id": ...}`
5. Added `if not patient_data: raise ValueError(...)` at function top
6. Re-ran pytest: 14 passed, 0 failed
7. Opened a Pull Request with the fix

**Result:** Both bugs fixed correctly. Tests went from 6 failed → 0 failed.
**Estimated cost:** ~$1-2

**Critical finding:** Devin caught and fixed Bug 1 (missing null check) which CodeRabbit **missed across all 4 test PRs**. Devin caught it because the tests failed at runtime — CodeRabbit missed it because it only reads code statically.

---

### Task 3 — Write Edge Case Tests

**Prompt given:**
> Write 8 edge case tests for `calculate_diabetes_risk()` covering: None input, empty input, missing field, age boundary (44 vs 45), BMI boundary (24.9 vs 25.0), glucose boundary (99 vs 100), max risk clamped at 100, healthy patient = LOW risk. Run pytest after. Open a PR.

**What Devin produced:**
All 8 tests written correctly:

| Test | What it validates |
|---|---|
| `test_none_input_raises_value_error` | None → ValueError |
| `test_empty_input_raises_value_error` | `{}` → ValueError |
| `test_missing_required_field_raises_key_error` | Missing `hba1c` → KeyError |
| `test_age_threshold_44_vs_45_differs` | Age boundary: +8 vs +15 points |
| `test_bmi_threshold_24_9_vs_25_0_differs` | BMI boundary: 0 vs +10 points |
| `test_fasting_glucose_threshold_99_vs_100_differs` | Glucose boundary: 0 vs +15 points |
| `test_all_maximum_risk_factors_clamped_at_100` | Score never exceeds 100 |
| `test_all_minimum_values_is_low_risk` | Healthy patient → LOW level |

**Test quality note:** Devin correctly used `{**base, "field": value}` isolation pattern — varying only one field per boundary test so each test proves exactly one threshold. This is correct engineering practice.

**Result:** 21 passed (8 new + 13 existing), 0 failed.
**Estimated cost:** ~$1-2

---

### Devin vs CodeRabbit — Same Bugs, Different Coverage

| Bug | CodeRabbit caught? | Devin caught? | How |
|---|---|---|---|
| Bug 1 — null check missing | No | **Yes + fixed** | Test failure at runtime |
| Bug 2 — age formula removed | Yes (with config) | Not tested | Would need a test for this |
| Bug 3 — HDL division by zero | Yes (natively) | Would catch | If test with HDL=0 existed |
| Bug 4 — returns float not dict | Yes (natively) | **Yes + fixed** | Test failure + static analysis |
| Bug 5 — PII in source | Yes (natively) | No | Devin cannot detect PII |
| Bug 6 — API contract broken | Yes (with config) | Only if tested | Needs explicit test coverage |

**Conclusion:** CodeRabbit and Devin have almost zero overlap. Each catches what the other misses.

---

## 10. NirogGyan Specific Use Cases

### Primary use case — Test suite health at end of sprint
After each sprint, run a Devin session: *"Run the full test suite, report what's failing, fix any failures that are caused by recent code changes rather than intentionally broken tests."*

This gives your team a clean green build before release without a developer spending 2-3 hours debugging CI.

### Secondary use case — Test coverage for scoring engine
The risk scoring engine is the most critical code in NirogGyan. Currently test coverage is likely incomplete. Devin can write boundary tests for every scoring threshold — age, BMI, HbA1c, cholesterol ratios — systematically.

Task format: *"Write edge case tests for [function name] covering all threshold boundaries defined in the scoring algorithm."*

### Tertiary use case — Fix specific known bugs
When a bug is reported by QA or a client, and the root cause is known, give it to Devin as a bounded fix task rather than a developer. Saves 1-2 hours of developer time per bug.

### What NOT to use Devin for at NirogGyan
- Designing the scoring algorithm (clinical domain expertise required)
- Writing new features from scratch (too open-ended, expensive)
- Anything requiring HIPAA/compliance judgment (no domain awareness)
- Complex architectural decisions

### Teams that benefit
| Team | Use |
|---|---|
| Backend developers | Offload test writing, CI debugging |
| QA engineers | Automated test suite execution + reporting |
| Tech lead | Sprint-end health checks, coverage reports |

---

## 11. Final Recommendation

### Recommended usage
- Run test suite and report at end of each sprint — clear, bounded, low cost
- Write unit tests for functions that lack coverage — especially scoring engine
- Fix specific, well-scoped bugs where root cause is known
- Tasks with a clear "done" condition (tests pass / CI green)

### Not recommended usage
- Open-ended feature development
- Architectural or clinical logic decisions
- Anything requiring NirogGyan business domain knowledge
- Tasks without clear success criteria

### Implementation priority
**Medium.** Valuable but requires strategic use. Not an always-on tool like CodeRabbit. Best used as a sprint-end or on-demand resource for specific engineering tasks.

### Risks
- Devin can introduce subtle bugs while fixing others — mandatory code review on all Devin PRs via CodeRabbit
- Subscription expires — have clear tasks lined up before expiry to maximise value
- Vague tasks waste budget quickly

### Expected ROI for NirogGyan
- 1-2 hours saved per sprint on CI debugging and test writing
- Complete boundary test coverage on scoring engine: ~2 Devin sessions (~$4-6)
- Nightly test suite run: ~$0.50/day if automated via scheduled sessions

### Bottom Line
Devin is a fast, autonomous executor for well-defined engineering tasks. Its real value at NirogGyan is not replacing developers but eliminating the mechanical, time-consuming parts of their work — running tests, writing edge cases, fixing known bugs. Given the limited subscription, prioritise test coverage for the scoring engine and sprint-end CI health checks before the subscription expires.

---

*Document generated from live hands-on evaluation — 3 tasks run, ~$2-3 spent, all tasks completed successfully.*
