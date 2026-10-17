# Main branch admission: GitHub provider activation (issue #60)

**Status (2026-10-17): prepared and testable, not activated.** This document is a repository-specific runbook, **not** an enforced policy merely because it is committed. The enforcement authority is GitHub's active ruleset for `ryjen/agent-delivery-playbook`, not this file, CI logs, or a model review. The connected GitHub integration can read but cannot write repository rulesets. Applying changes requires a separate authorized repository administrator with `Administration: write`.

## Verified original configuration

- Repository: `ryjen/agent-delivery-playbook` (public, personal account).
- Active branch ruleset: [`default`, ID `17832277`](https://github.com/ryjen/agent-delivery-playbook/rules/17832277), matching `~DEFAULT_BRANCH`.
- Enforced rules on 2026-10-17: `deletion` and `non_fast_forward` only.
- Existing bypass: `RepositoryRole` actor 5 in `always` mode (ambient administrator-role bypass).
- Provider ruleset `updated_at`: `2026-06-18T01:09:46.285-07:00`.
- GitHub Actions workflow: [`validate.yml`](../../.github/workflows/validate.yml), triggered by `pull_request` and `push` to `main`, with `contents: read`, SHA-pinned actions, non-persisted checkout credentials and Nix-owned checks.
- Real check contexts: **`Repository integrity`** and **`Task envelopes`**, both emitted by `github-actions` (GitHub App integration ID **15368**). Confirmed on merged PR #79's `main` commit `d05e55b142e7ddcbf610ea3d44f9ef59b854b3c5`.

The above is a timestamped observation, not a future guarantee. Always read live ruleset state before activation.

## Proposed minimum provider configuration

The candidate provider payload is [`examples/provider-admission/main.ruleset.json`](../../examples/provider-admission/main.ruleset.json). It retains deletion and force-push prevention and adds:

1. **Pull request required for all normal changes to `main`**. Conversation resolution is required.
2. **Two required status checks**, explicitly sourced to the `github-actions` integration ID 15368: `Repository integrity` and `Task envelopes`.
3. **Strict branch freshness**: a PR becomes stale when `main` advances; rerun/refresh checks for the current base before admission.
4. **No ambient ruleset bypass actor**. Administration of ruleset settings itself remains a high-trust, out-of-band operation.
5. **Zero required approving reviews**, intentionally. A solo-maintainer personal repository cannot satisfy a separate human approval without another eligible contributor. This does not demonstrate human separation of duties: require accountable risk/evidence review procedurally and do not call Codex approval sufficient. If another trusted maintainer becomes available, separately review a one-review protected policy.

Avoid silently making the project unusable with an unsatisfiable review requirement. Changes to protected files, actions, authentication or admission rules still require risk escalation under [the trust model](../trust-model.md). No GitHub rule here can prove semantic reviewer independence, model integrity, or exact accepted post-squash revision.

**Provider limits:** For `pull_request`, GitHub Actions ordinarily checks the PR's candidate merge ref; strict checks require freshness with the base branch. The final squash/rebase merge commit differs from the tested PR head. A `push` run on `main` is corroborating **post-admission** evidence, not a pre-merge test of the identical final commit. Do not call this full exact-result attestation. For true post-merge effect qualification, add a separately designed release gate, not a weaker interpretation of green PR checks.

## Operator sequence: inspect -> verify -> apply -> observe

This requires GitHub CLI (`gh`), a GitHub identity authorized for repository-ruleset administration, and a trusted operator environment. Execute from the repository's reviewed `main` **after this runbook PR passes and merges**. Do not paste tokens in terminals, reports, or issue comments.

### 1. Verify source and snapshot (read-only)

```bash
gh auth status
gh api repos/ryjen/agent-delivery-playbook/rulesets/17832277 \
  > /tmp/agent-delivery-playbook-ruleset-before.json
python3 scripts/check-admission-ruleset.py --mode proposal
python3 scripts/check-admission-ruleset.py \
  --mode baseline --observed /tmp/agent-delivery-playbook-ruleset-before.json
```

The `baseline` guard checks the **full selected policy fields**, ruleset ID/source, and the observed provider `updated_at` as an offset-aware instant, allowing equivalent UTC representations. A changed result is a **stop and reconcile**, never a reason to overwrite new rules. Inspect the live diff and issue/ruleset history first. The API has no concurrency lease in this runbook; re-read immediately before updating, and limit the time between the final check and write.

### 2. Apply through the authorized provider API (one explicit mutation)

```bash
# Re-read and re-check immediately before the admin operation.
gh api repos/ryjen/agent-delivery-playbook/rulesets/17832277 \
  > /tmp/agent-delivery-playbook-ruleset-before.json
python3 scripts/check-admission-ruleset.py \
  --mode baseline --observed /tmp/agent-delivery-playbook-ruleset-before.json

gh api --method PUT \
  -H 'Accept: application/vnd.github+json' \
  repos/ryjen/agent-delivery-playbook/rulesets/17832277 \
  --input examples/provider-admission/main.ruleset.json \
  > /tmp/agent-delivery-playbook-ruleset-after.json
```

The `PUT` is a **provider administrator action** that may replace the existing rules array and bypass list. Do not use on an unreviewed or changed target. A 401/403/404/422 is not permission to use an agent shell, another credential, or an ungoverned execution path.

### 3. Observe read-back (read-only)

```bash
gh api repos/ryjen/agent-delivery-playbook/rulesets/17832277 \
  > /tmp/agent-delivery-playbook-ruleset-observed.json
python3 scripts/check-admission-ruleset.py \
  --mode active --observed /tmp/agent-delivery-playbook-ruleset-observed.json
```

Require the live ruleset to be **active**, match `~DEFAULT_BRANCH`, have no ambient bypass, keep both original protections, and require both check contexts with integration ID 15368. The checker normalizes only known inert provider-response defaults (for example, `do_not_enforce_on_create: false`); unexpected properties or a changed setting still fail the comparison. It is an **offline structural preflight** and does not prove that GitHub rejects unauthorized writes.

### 4. Provider-backed negative admission test (human-operated)

Use a disposable branch/PR, **never `main`**. A suitable candidate introduces a local Markdown link to a nonexistent relative file, causing `Repository integrity` to fail, while keeping `Task envelopes` untouched. Wait until both checks conclude. Observe that GitHub's merge box is blocked by the required failing context **for the current PR candidate**. Record:

- PR URL, head SHA, current base SHA, workflow run/job URL, check conclusion and expected GitHub admission rejection;
- ruleset ID and live read-back URI; operator identity and time;
- whether a direct push without a PR is rejected (optional: prefer a GitHub branch-rules simulation rather than making a risky direct push);
- any bypass warning, missing check, wrong integration source or stale-branch anomaly.

Then close the disposable PR and remove the disposable branch through the normal process. A missing required check must also block admission; test safely with a no-effect PR/staging scenario if available. **Do not create a fake-success status**, use admin bypass to merge the invalid PR, or stage failure in protected production code. If a required test cannot be demonstrated, record it as **unverified**, not completed.

## Break-glass and recovery

An administrator's ability to **edit the ruleset** is a residual control-plane privilege even when `bypass_actors` is empty. GitHub's public repository rulesets do not make the maintainer independent of their own admin authority.

For an emergency:

1. Record the incident/task, accountable human, exact protected action, minimal requested exception, affected revision and expiry/restore condition.
2. Preserve the existing ruleset JSON and active ruleset history. Prefer a narrow fix through an ordinary passing PR.
3. If an emergency provider override is unavoidable, have the authorized administrator make an explicitly logged temporary ruleset change. Do not create a permanent `always` bypass or hidden alternate write route.
4. Restore and re-read the original protected configuration immediately after the bounded operation; collect effect/recovery evidence. Record any interval of weakened enforcement.
5. If restoration, checks, or attribution cannot be verified, leave #60 **blocked** and raise an operational finding.

Do not place private credentials or audit-sensitive evidence in the public repository. Link provider-generated evidence when safe.

## Completion / claim gate

- [x] Real baseline ruleset inspected.
- [x] Required contexts and GitHub Actions provider identity confirmed.
- [x] Proposed configuration, structural preflight, and bounded activation runbook prepared.
- [ ] Administrator applied the provider rule and independent live read-back passed.
- [ ] Failing or absent required check demonstrably blocked a normal merge.
- [ ] Break-glass/accountability and remaining limitations were recorded.
- [ ] Issue #60 and capability status reconciled against those **external observations**.

A green CI run, approved documentation PR, or structural preflight does **not** close #60 without active provider enforcement and negative admission evidence.
