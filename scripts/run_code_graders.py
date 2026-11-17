#!/usr/bin/env python3
"""Run the code-based graders from a machine-readable Eval PRD against a golden set and system outputs.

Covers the checks that need no LLM judge:
  - forbidden_retrieval_rate    (any forbidden doc retrieved or cited, in any turn of any run)
  - canary_leak_rate            (any canary string in a response, in any turn of any run)
  - forbidden_tool_call_rate    (any forbidden tool called, in any turn of any run)
  - behavior_accuracy           (single-question cases: answer / abstain / clarify / escalate / refuse ...)
  - recall_at_k                 (share of expected docs retrieved, averaged over turns that list any)
  - conversation_success_first_run   (conversation cases that meet every turn's checkpoint on run 1)
  - conversation_success_all_runs    (conversation cases that meet every checkpoint on every run, i.e. pass^k)

A case can be a single question (`input` + `expected_behavior`) or a conversation
(`turns`, each with its own checkpoint). Outputs can hold several runs of the same
case (`run`: 1, 2, 3 ...). A case only counts as passing when every run passes,
because the same conversation can go well once and badly the next time.

Judge-based pass bars (grader: judge) are reported as NOT RUN; wire them to your
judge runner of choice (DeepEval, Ragas, Promptfoo, Inspect, MLflow, ...).

Usage:
  python scripts/run_code_graders.py \
      --prd examples/help-center-assistant/eval-prd.yaml \
      --golden examples/help-center-assistant/golden.jsonl \
      --outputs examples/help-center-assistant/sample_outputs.jsonl \
      --k 5

Exit code is 1 if any blocking pass bar fails, so it can be used as a CI gate.
"""
import argparse
import json
import sys
from collections import defaultdict

import yaml


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def case_turns(case):
    """Return the list of turn checkpoints for a case, single question or conversation."""
    if case.get("turns"):
        return case["turns"]
    return [{
        "user": case.get("input"),
        "expected_behavior": case.get("expected_behavior"),
        "expected_doc_ids": case.get("expected_doc_ids", []),
    }]


def output_turns(out):
    return out["turns"] if "turns" in out else [out]


def grade_run(case, out, k):
    """Grade one run of one case. Returns a dict with issues per turn."""
    checkpoints = case_turns(case)
    turns = output_turns(out)
    forbidden_all = set(case.get("forbidden_doc_ids", []))
    canaries = case.get("canary_strings", [])
    bad_tools = set(case.get("forbidden_tool_calls", []))
    result = {"forbidden_hit": [], "canary_hit": [], "tool_hit": [], "behavior_misses": [],
              "recalls": [], "first_failed_turn": None}

    if len(turns) < len(checkpoints):
        result["first_failed_turn"] = len(turns) + 1
        result["behavior_misses"].append((len(turns) + 1, "no reply", "conversation ended early"))

    for i, (cp, t) in enumerate(zip(checkpoints, turns), start=1):
        failed = False
        retrieved = t.get("retrieved_doc_ids", [])[:k]
        surfaced = set(retrieved) | set(t.get("cited_doc_ids", []))
        forbidden = forbidden_all | set(cp.get("forbidden_doc_ids", []))
        hit = sorted(surfaced & forbidden)
        if hit:
            result["forbidden_hit"].append((i, hit))
            failed = True
        leaked = [c for c in canaries if c in t.get("response", "")]
        if leaked:
            result["canary_hit"].append((i, leaked))
            failed = True
        tools = [c.get("name") if isinstance(c, dict) else c for c in t.get("tool_calls", [])]
        tool_hit = sorted(set(tools) & bad_tools)
        if tool_hit:
            result["tool_hit"].append((i, tool_hit))
            failed = True
        expected = cp.get("expected_behavior")
        if expected and t.get("behavior") != expected:
            result["behavior_misses"].append((i, t.get("behavior"), expected))
            failed = True
        exp_docs = cp.get("expected_doc_ids", [])
        if exp_docs:
            result["recalls"].append(len(set(exp_docs) & set(retrieved)) / len(exp_docs))
        if failed and result["first_failed_turn"] is None:
            result["first_failed_turn"] = i

    result["passed"] = result["first_failed_turn"] is None
    return result


def grade(golden, outputs, k):
    runs_by_id = defaultdict(list)
    for o in outputs:
        runs_by_id[o["id"]].append(o)
    rows = []
    for case in golden:
        runs = sorted(runs_by_id.get(case["id"], []), key=lambda o: o.get("run", 1))
        if not runs:
            rows.append({"id": case["id"], "missing_output": True})
            continue
        graded = [(o.get("run", 1), grade_run(case, o, k)) for o in runs]
        rows.append({
            "id": case["id"],
            "slice": case.get("slice"),
            "conversation": bool(case.get("turns")),
            "runs": graded,
        })
    return rows


def summarize(rows):
    graded = [r for r in rows if not r.get("missing_output")]
    singles = [r for r in graded if not r["conversation"]]
    convos = [r for r in graded if r["conversation"]]

    def any_run(r, key):
        return any(res[key] for _, res in r["runs"])

    def rate(items, pred):
        return (sum(1 for r in items if pred(r)) / len(items)) if items else None

    recalls = [x for r in graded for _, res in r["runs"] for x in res["recalls"]]
    uses_tools = any(res["tool_hit"] for r in graded for _, res in r["runs"])
    return {
        "forbidden_retrieval_rate": rate(graded, lambda r: any_run(r, "forbidden_hit")),
        "canary_leak_rate": rate(graded, lambda r: any_run(r, "canary_hit")),
        "forbidden_tool_call_rate": rate(graded, lambda r: any_run(r, "tool_hit")) if uses_tools else 0.0,
        "behavior_accuracy": rate(singles, lambda r: not any_run(r, "behavior_misses")),
        "recall_at_k": (sum(recalls) / len(recalls)) if recalls else None,
        "conversation_success_first_run": rate(convos, lambda r: r["runs"][0][1]["passed"]),
        "conversation_success_all_runs": rate(convos, lambda r: all(res["passed"] for _, res in r["runs"])),
        "missing_outputs": sum(1 for r in rows if r.get("missing_output")),
    }


OPS = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: abs(a - b) < 1e-9}


def describe(res, conversation):
    issues = []
    where = (lambda i: f"turn {i}: ") if conversation else (lambda i: "")
    for i, hit in res["forbidden_hit"]:
        issues.append(f"{where(i)}forbidden docs surfaced {hit}")
    for i, hit in res["canary_hit"]:
        issues.append(f"{where(i)}canary leaked {hit}")
    for i, hit in res["tool_hit"]:
        issues.append(f"{where(i)}forbidden tool called {hit}")
    for i, actual, expected in res["behavior_misses"]:
        issues.append(f"{where(i)}behavior {actual} != expected {expected}")
    for x in res["recalls"]:
        if x < 1:
            issues.append(f"recall@k {x:.2f}")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prd", "--spec", dest="prd", required=True, help="machine-readable Eval PRD (eval-prd.yaml)")
    ap.add_argument("--golden", required=True)
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()

    with open(args.prd, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    rows = grade(load_jsonl(args.golden), load_jsonl(args.outputs), args.k)
    metrics = summarize(rows)
    grader_types = {c["id"]: c["grader"] for c in spec.get("checks", [])}

    print(f"\n{spec['feature']['name']}  ({spec['stakes']['level']} stakes)\n")
    print("Per-case failures:")
    for r in rows:
        if r.get("missing_output"):
            print(f"  {r['id']}: MISSING OUTPUT")
            continue
        n_runs = len(r["runs"])
        failed_runs = [(run, res) for run, res in r["runs"] if not res["passed"] or describe(res, r["conversation"])]
        if not failed_runs:
            continue
        label = f"  {r['id']} [{r['slice']}]"
        if n_runs == 1 and not r["conversation"]:
            print(label + ": " + "; ".join(describe(failed_runs[0][1], False)))
            continue
        if n_runs > 1:
            label += f" failed {sum(1 for _, res in failed_runs if not res['passed'])} of {n_runs} runs"
        print(label + ":")
        for run, res in failed_runs:
            prefix = f"    run {run}, " if n_runs > 1 else "    "
            if r["conversation"] and res["first_failed_turn"]:
                prefix += f"first failed at turn {res['first_failed_turn']}; "
            print(prefix + "; ".join(describe(res, r["conversation"])))

    print("\nPass bars:")
    blocking_failed = False
    for g in spec.get("pass_bars", []):
        name, op, thr = g["metric"], g["operator"], g["threshold"]
        if grader_types.get(g.get("check")) != "code" or metrics.get(name) is None:
            print(f"  [NOT RUN] {name} {op} {thr}  (judge or missing metric)")
            continue
        val = metrics[name]
        ok = OPS[op](val, thr)
        if not ok and g.get("blocking", True):
            blocking_failed = True
        tag = "PASS" if ok else ("FAIL" if g.get("blocking", True) else "WARN")
        print(f"  [{tag}] {name} = {val:.3f}  (bar {op} {thr})")

    if metrics.get("conversation_success_first_run") is not None:
        print(f"\nConversations: {metrics['conversation_success_first_run']:.0%} pass on the first run, "
              f"{metrics['conversation_success_all_runs']:.0%} pass on every run.")

    print("\nDecision:", "HOLD (a blocking pass bar failed)" if blocking_failed else "Code checks pass; run the judge checks before shipping")
    sys.exit(1 if blocking_failed else 0)


if __name__ == "__main__":
    main()
