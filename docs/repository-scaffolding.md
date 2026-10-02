# Repository scaffolding

The repository factory builds a purpose-specific **local starting directory** from explicit construction inputs. It is a deterministic materialization step over the current canonical control catalog and repository-owned templates. It is not a repository hosting service, a policy adoption workflow, a compliance assessment, or an enforcement rollout.

## Inputs and records

The factory keeps project intent, applicability, artifact selection and generation evidence as separate objects:

| Object | Role | What it does not establish |
|---|---|---|
| Repository spec | Declares the intended repository identity, proposed GitHub metadata, purpose, required profile, review-candidate materialization mode and project-specific template parameters. The example uses schema `ges.repository-spec.v1`. | It does not create the repository, apply metadata, prove the purpose is accurate, or authorize publication. |
| Profile | Supplies the explicit context used to evaluate every canonical control. The supplied profiles are draft target policies and require target-specific review and adoption. | Selecting a profile does not adopt its controls, prove applicability, or certify enforcement. Any `UNKNOWN` applicability stops generation. |
| Artifact catalog | Maps every supported `file_present` control revision to one repository-owned template destination and lists deliberately unsupported capabilities. The default is `factory/artifacts.json`, schema `ges.artifact-catalog.v1`. | It is not a list of every file a project needs, and it does not convert a reviewed-draft control into accepted policy. |
| Standard lock | Records generator version and source-module digests, canonical catalog digest and count, profile identity/status/digest, artifact-catalog identity/revision/digest and repository-spec digest. It uses schema `ges.standard-lock.v1`. | A digest lock proves the identity of the recorded inputs and generator files, not semantic correctness, adoption, compliance or current upstream authority. |
| Generation manifest | Records the proposed repository metadata, every control applicability decision, materialized and omitted artifacts, unsupported capabilities, output digests and explicit status boundaries. It uses schema `ges.generation-manifest.v1`. | It is a construction receipt, not a validation receipt for a hosted repository or evidence that policy is enforced. |

The generated `.ges/standards-checklist.md` is a project-specific planning view of applicable controls. Checking a box is not evidence by itself; actual observations, scoped human attestations and native readback remain distinct.

## Prepare a project spec

Copy `examples/repository-spec.json` to a project-owned location and replace every example value. The strict schema requires:

- repository name, title, owner, visibility and default branch;
- proposed description and topics;
- purpose statement, function, repository type, lifecycle stage, criticality, deliverables, scope, interfaces and toolchain;
- the exact draft profile name and `review_candidate` materialization mode; and
- all template parameters required by the applicable artifacts.

`PROJECT_TITLE` and `PURPOSE` are derived from the repository title and purpose statement; do not add them to `template_parameters`. Names and topics use lowercase hyphenated slugs. Proposed GitHub metadata remains proposed because the command performs no API calls.

Review the chosen profile for the real target rather than treating the example as a default policy. The CLI profile must match the name bound in the spec. Generation rejects mistyped control-relevant context values and fails if the profile leaves any canonical control's applicability unknown. A false or not-applicable dimension must be an intentional project statement, not a way to evade a failing control. Rendered consumer files also may not name an artifact that the selected profile omits.

## Preview without writing

Run from the `github-engineering-standards` source root:

```sh
python -m ges scaffold \
  --spec examples/repository-spec.json \
  --profile profiles/solo-software.json \
  --artifacts factory/artifacts.json \
  --output .cache/repository-factory-demo \
  --dry-run
```

The dry run validates the repository-spec and artifact-catalog contracts, checks the profile status and control-relevant context types, requires referenced policy parameters, rejects unknown applicability, verifies the spec/profile binding and referenced control revisions, and validates the required template parameters, rendered cross-references and structured files. It prints `would_create` and the complete proposed manifest to standard output. It does not create the output directory or any scaffold files. These structural checks do not independently prove that every profile context value is semantically appropriate for the target; that remains a required review.

Before writing, inspect at least:

- the target identity and proposed metadata;
- every `APPLICABLE` and `NOT_APPLICABLE_WITH_REASON` decision;
- the materialized and omitted artifact lists;
- the `unsupported` entries; and
- the status boundary, which must continue to report no recorded adoption, no assessment, no established semantic review, no native changes, no Git initialization and no remote creation.

## Create the local scaffold

Use the same reviewed inputs without `--dry-run`:

```sh
python -m ges scaffold \
  --spec examples/repository-spec.json \
  --profile profiles/solo-software.json \
  --artifacts factory/artifacts.json \
  --output .cache/repository-factory-demo
```

The destination must not exist. The writer builds complete files in a staging directory, atomically reserves the destination name as a new directory, and moves the staged entries into that owned directory. During publication, `.ges-scaffold-incomplete` marks the tree as unusable and the `.ges` receipt directory moves last; the marker is removed only after every staged entry is present. A hard process death can therefore leave an explicitly incomplete tree, not an apparently complete receipt. Ordinary errors and interrupts clean the reserved directory. The writer refuses to overwrite an existing file, directory or symlink.

For the supplied `solo-software` example, the applicable consumer artifacts are `README.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, the pull-request template, bug and feature issue forms, and Dependabot configuration. `CITATION.cff` and funding configuration are recorded as omitted because the profile declares scholarly and funding applicability false. Different reviewed profile context can produce a different set.

Every scaffold also contains:

- `.ges/repository-spec.json`, a normalized copy of the validated project spec;
- `.ges/standard.lock.json`, the generation-input lock;
- `.ges/standards-checklist.md`, the applicable-control planning view; and
- `.ges/generation-manifest.json`, the construction receipt and boundary record.

## Deliberate limits

This release does not generate or select:

- a `LICENSE`, because rights and license choice require project-specific review;
- a `.gitignore`, because ignore rules depend on the actual toolchain;
- CI workflows, because no general language/toolchain workflow has been reviewed for this purpose;
- build, package or runtime files, because those follow the declared implementation; or
- GitHub rulesets or other native settings, because activation requires separate approval and verified readback.

The command also does not run `git init`, create commits or branches, create a GitHub remote, push files, modify credentials, publish content, or assess the generated directory. Those are later, separately authorized lifecycle steps. Before using a scaffold as a real repository, owners must review its rendered content, replace any inaccurate project statements, make the unsupported decisions, implement the actual toolchain, and verify the result at the intended target.
