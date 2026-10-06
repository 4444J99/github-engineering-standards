# C0 source-only reconciliation review

HOLD — all decisions PROPOSED; zero approvals or policy adoption.

SPECIALIZED denotes related source-specific variants, not directional subsumption.
REFERENCE in A5 retains a proposition as source evidence; it does not exclude actionable guidance.
No duplicates or supersessions are asserted across differing scope/applicability.

## semantic-proposition:0068bc452cf1e28c4359c1c178aa42b215be4734235fa643184fd104376030f2

SPECIALIZED: SHOULD repository owner — adapt CONTRIBUTING.md to explain participation and submission

Contribution-guideline adaptation is expressed both as a must-category requirement and a concrete should instruction; retain both strengths and the project placeholders.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 48, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "89784c67479af951c3f4c905529d6b0fc38d41de0eb3589b95f7695143044aff", "start_line": 44}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "CONTRIBUTING.md to explain participation and submission", "parameters": ["YOUR-ORGANIZATION", "YOUR-PROJECT"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source misspells CONTIBUTING.md in prose; target is CONTRIBUTING.md"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:bae7d78cba4471ef4d1e8e17dc8c2f95957fb2ac551394a7ddae8fe7c7aeaf02"], "rationale": "Contribution-guideline adaptation is expressed both as a must-category requirement and a concrete should instruction; retain both strengths and the project placeholders."}]`

## semantic-proposition:0091ef4376e186320ca579d166f239e2422f8dcc90d5bd8d7e456bc1beaef54d

DISTINCT: SHOULD project participants — prefer plain text or Markdown for most developer documentation

Retain an independent source-local proposition: project participants — SHOULD prefer plain text or Markdown for most developer documentation. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 116, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "d030961b738bcd8746c12eeac74349ef2328311aefe2b38c41f1d2a920db2b30", "start_line": 116}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "prefer", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "plain text or Markdown for most developer documentation", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:01e668f06c84b8d3d3f7eb8bf65830ad6f36e003158e165a4b2100dcd7c962f4

SPECIALIZED: MAY other project leaders — allow temporary or permanent repercussions for bad-faith enforcement failures

Bad-faith enforcement consequences are discretionary and source-local, including temporary/permanent leadership consequences.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 73, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "48c162f1c30b5a819c80264adc3a4e1a05a981234501cdb119ea4a7f0f9bd602", "start_line": 71}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "allow", "consequences": [], "exceptions": [], "modality": "MAY", "object": "temporary or permanent repercussions for bad-faith enforcement failures", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "other project leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:8ebf41fe05d620f5ebb2e390b7097a3a3ed39f3bf12fa61b69f8f1aa3e9a1d94"], "rationale": "Bad-faith enforcement consequences are discretionary and source-local, including temporary/permanent leadership consequences."}]`

## semantic-proposition:01f29e4d6e5415c42b7ac03e405f550cbd039af3648c0529024084a7ebe1e0f4

SPECIALIZED: SHOULD pull-request author — summarize change, linked/fixed issue, motivation, context and required dependencies

PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 5, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "fa5ee4efb32c17d11ea051e3a652fa3f08a79ef13384b024b37a4ac64b55e20d", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "summarize", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "change, linked/fixed issue, motivation, context and required dependencies", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:16699d8d8f97318331befa0dd39a6a0df2394edc20bc2576af2ff34587ab80d5", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:985ff89acd5fd5bc91a0d8f8cd273fbf321dce8495b0b92812636175bbdaf1f9", "semantic-proposition:c3cffdd46526529b4fe52da84168114332ba537c5a195801ed78e8b4bb8ae357"], "rationale": "PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt."}]`

## semantic-proposition:025423f92fa92972acfcbb6ddf5b54070c15eca327f92162d4cf6133fa9e2d8f

DISTINCT: SHOULD reporter — describe the bug clearly and concisely

Retain an independent source-local proposition: reporter — SHOULD describe the bug clearly and concisely. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 11, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "cbcf7f0c9b46babd8b1af3e20dda9de2411b05d9b285036bff511a4c08638159", "start_line": 10}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the bug clearly and concisely", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:02fe131e0ddf9cd3d42c1f087c282e7139ab05b22d47911a326e426f3fc729ef

SPECIALIZED: MUST maintainers — use permanent community public-interaction ban for patterns of violation, harassment or class-based aggression

Permanent-ban guidance shares the misconduct pattern but assigns different source-local leadership roles; neither conduct version supersedes the other.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 96, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "1dad45834632ab66ee3f3d2eeadfaae436046ca5fef8113b40c34c31c83272da", "start_line": 94}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "MUST", "object": "permanent community public-interaction ban for patterns of violation, harassment or class-based aggression", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:03964f849751dfa69d47f5cb2ef4308ffe9f06cbd1549c53b4329eb235a21601"], "rationale": "Permanent-ban guidance shares the misconduct pattern but assigns different source-local leadership roles; neither conduct version supersedes the other."}]`

## semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22

SPECIALIZED: SHOULD project participants — record changes in an issue before creating a pull request

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 45, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "fd787b7e5f1451ed728a23c837642fe654efeb77ef016b2d50504de437905a2b", "start_line": 45}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "record", "consequences": [], "exceptions": ["The tiniest changes"], "modality": "SHOULD", "object": "changes in an issue before creating a pull request", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d", "semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001", "semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf", "semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba", "semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:03964f849751dfa69d47f5cb2ef4308ffe9f06cbd1549c53b4329eb235a21601

SPECIALIZED: MUST leaders — use permanent community public-interaction ban for patterns of violation, harassment or class-based aggression

Permanent-ban guidance shares the misconduct pattern but assigns different source-local leadership roles; neither conduct version supersedes the other.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 113, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "68daedc0e691eda26a7bb6627daba6eef02f79803e26726538afa481b836fbb5", "start_line": 108}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "MUST", "object": "permanent community public-interaction ban for patterns of violation, harassment or class-based aggression", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:02fe131e0ddf9cd3d42c1f087c282e7139ab05b22d47911a326e426f3fc729ef"], "rationale": "Permanent-ban guidance shares the misconduct pattern but assigns different source-local leadership roles; neither conduct version supersedes the other."}]`

## semantic-proposition:066f4f7336fa149491fdbe8d036fe73c830a0c5ecc167f2f692508f3e1362cb9

DISTINCT: MUST pull-request author — avoid new warnings

Retain an independent source-local proposition: pull-request author — MUST avoid new warnings. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 35, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "9b68a8e667b961a34ad631e6b4bc806c58167b8afa5c2700ed0165be11b1be35", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "MUST", "object": "new warnings", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:07690f70055947fc5b8caa1b397fd1f9b71558951a54a20c49de23e546e643a2

DISTINCT: MAY project participants — leave discretionary branch naming

Retain an independent source-local proposition: project participants — MAY leave discretionary branch naming. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 19, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "d0a379ca645e8699b78bf05a8c6356686a9a9755335209ff1bc422e2b608a76e", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "leave discretionary", "consequences": [], "exceptions": [], "modality": "MAY", "object": "branch naming", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Username, humor, descriptive names and issue numbers are alternatives; short branch lifetime is assumed"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:0809500a491391df7e3d569177a86b8f5f5642aaa37a2e7b78bbf912d1913512

SPECIALIZED: SHOULD pull-request author — describe considered alternatives

Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "2ac638530c56711a57688b78aed79e808bd206335877e94c139aace84c8e9970", "end_line": 11, "path": ".github/pull_request_template.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9aa4ce6a1ed8c7edf8173552a7f575f66850b0693414124972d8e0d458d26dea", "start_line": 9}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "considered alternatives", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Alternatives exist"], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:d0ad8ce7c2bb71c33fd3619189222f11f52957614f5fc10f51fa5ef8b7bd8727", "semantic-proposition:e0a92102e1b4669d3d664ac37b86901a6e46b18f874fcc41c2f1a140035e3bea"], "rationale": "Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing."}]`

## semantic-proposition:081409215805f4e5f5a7804dc7a3b11e2c0b27209121daf481b4c0afef9ad229

DISTINCT: MAY reporter — attach optionally screenshots explaining the problem

Retain an independent source-local proposition: reporter — MAY attach optionally screenshots explaining the problem. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 24, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "02062ce30c8eca79d0f06ab005378f7e837f9c6d1ed2d842804acd3a7aae2740", "start_line": 23}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "attach optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "screenshots explaining the problem", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Applicable"], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:081f31a8ff74dff830d11cca35a51038b92f2fd93832577a55eb755f0a666f01

SPECIALIZED: SHOULD participants — show empathy and kindness

Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "show", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "empathy and kindness", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:cc357b938c1a1da5f121260ffced3a6d5f50a118c4c8ed8935510dc496be1767", "semantic-proposition:d265eab3ef6db45e91ef99e5d39138befed6500612f194066ede97023fa3e776", "semantic-proposition:eecd5c8892f0e437dc966170b5bd5618d79ab99c1b90b4f7ae87a5340c5685b9"], "rationale": "Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate."}]`

## semantic-proposition:0868d60e6055ff94cc113c18b0ed3699745f559aaec090fea3feef1331f73e7a

DISTINCT: MUST pull-request author — add tests demonstrating the fix or feature

Retain an independent source-local proposition: pull-request author — MUST add tests demonstrating the fix or feature. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 36, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "e19ed37fa6303a8ebcec833910f67dbb662f10a42743502ab3650f2f37a7058c", "start_line": 36}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "add", "consequences": [], "exceptions": [], "modality": "MUST", "object": "tests demonstrating the fix or feature", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:097f8e363fe0ec382aec886e2f3f67021c4ecd8bb909cc684a081f979b1fccd6

SPECIALIZED: MUST maintainers — use temporary ban for serious violations including sustained misconduct

Temporary-ban guidance retains no-contact scope, unspecified duration and escalation consequences in each project.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 91, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "f54ffc301e7630668e1294891f2ae706dd71ee1dfd9f7cbe3b543d8787f9924c", "start_line": 89}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": ["Violating restrictions may cause permanent ban"], "exceptions": [], "modality": "MUST", "object": "temporary ban for serious violations including sustained misconduct", "parameters": ["specified period; no fixed duration"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No community interaction or public/private contact with involved people including enforcers"], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:be2176bda7d72a972b14963521e1932b0231aa49b55c6395b9efb444bef3dcb4"], "rationale": "Temporary-ban guidance retains no-contact scope, unspecified duration and escalation consequences in each project."}]`

## semantic-proposition:0a5e5b5dfa90f7e5fb7b4f64228b20b4816e46f2d8aa51ec6e37fa0f52084e5a

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate empty later owner entry exempting apps/github from root apps ownership

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate empty later owner entry exempting apps/github from root apps ownership. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 62, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "2cca5b78ee040a75fc56cd38314ecd2f7756a831b14bfcf5169eb56157ade960", "start_line": 58}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "empty later owner entry exempting apps/github from root apps ownership", "parameters": ["/apps/ @octocat", "/apps/github"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:0c11dd0c560d06a61a766831816e8d704ff983ce6c6748eb8d31f8b2f6b43013

REFERENTIAL: DESCRIPTIVE CODEOWNERS comments — assert approval requirements for scripts and nested logs ownership examples

Retain source-local example/reference: CODEOWNERS comments — DESCRIPTIVE assert approval requirements for scripts and nested logs ownership examples. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 56, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d616f99f9a9c66746317983f44f5f8085db469026d3f2c7894fca37e0f0ae9c6", "start_line": 49}]`

Preserved AST/applicability: `{"ambiguities": ["Comments conflate code-owner assignment and required approval; no native enforcement is proven"], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "assert", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "approval requirements for scripts and nested logs ownership examples", "parameters": ["/scripts/ @doctocat @octocat", "**/logs @octocat"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS comments"}}`

Relationships: `[]`

## semantic-proposition:0e0a8ebf96d742bcf8f22c13768e1dcabef8d8c1868cf43c385300d52756080b

DISTINCT: SHOULD reporter — provide ordered reproduction steps

Retain an independent source-local proposition: reporter — SHOULD provide ordered reproduction steps. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 18, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "f4b996618cc71ad581b4c901fc1be5961ef9e9945593ed309560dc4ba1287b62", "start_line": 13}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "provide", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "ordered reproduction steps", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:0e8541d6dcccc73b218d9fa055348d33755adc6b153390116a26f2732f394bf5

SPECIALIZED: SHOULD project participants — write meaningful commit messages

Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 104, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "9bd2acf4b26ac2553de7a27562576f9bb106faec2812a6f1b5dfb6f397ff9c93", "start_line": 104}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "write", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "meaningful commit messages", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Rigid grammar is not required"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:4be68e7e45e38d45af75c12b417ae771c8560f44988e9b235ceb99b9a056d8f3", "semantic-proposition:f3ff9668a240b8a5a2c507ae7331dddcf00460aac4a0a5f1caeee2b1868e7dfa"], "rationale": "Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate."}]`

## semantic-proposition:0f286f7b74b41bc5cc73092a3b91816011ec12ddb5c85a16c315fdc22475d11c

SPECIALIZED: SHOULD participants — use welcoming inclusive language

Inclusive-language guidance remains source-local across the contribution and conduct documents.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 39, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "9465024e8cb4b47befe0d034c8ece409641cf6fce1fa6e21527a12522c2258d1", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "welcoming inclusive language", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:9266fa993dba3186ee5377665df0b4b68c5a1942a81953f41a1708993a16ce4e"], "rationale": "Inclusive-language guidance remains source-local across the contribution and conduct documents."}]`

## semantic-proposition:11d28751b0e31db605d83ca57dd2fd9617a40282e7ce1e639aca5a3d777b3fc7

DISTINCT: SHOULD participant — contact a maintainer for discomfort or perceived breach of conduct intent

Retain an independent source-local proposition: participant — SHOULD contact a maintainer for discomfort or perceived breach of conduct intent. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 13, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "1449304681b7e2a79b40e6d3d543f590939e8a7212f3517a55e095b75cc32a06", "start_line": 9}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "contact", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "a maintainer for discomfort or perceived breach of conduct intent", "parameters": ["USER1", "USER2", "USER3"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participant"}}`

Relationships: `[]`

## semantic-proposition:12eb0d8d0e51bf1f3d23a35ebe00c27ebba8c75b17d218e8d9b6d6c674b3efa3

SPECIALIZED: SHOULD repository owner — adapt then activate funding file and sponsorship button

Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 110, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "645719460a922b1e09c959da32176def6a0f9474da1fb24c70839d3d4b1507c5", "start_line": 104}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt then activate", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "funding file and sponsorship button", "parameters": ["FUNDING.yml", "Settings / General / Sponsorship"], "polarity": "POSITIVE", "preconditions": ["Funding feature is selected"], "qualifiers": ["Root file location is a source assertion; no setting changed"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:48952d712c806f1bf1f9698989e9275fd364cf759dc2402875c25d03cd60878f", "semantic-proposition:4d99d3b09db42bf15e22d97dba0def1704ab59dc96a3f82128c9de8b8963cd3f", "semantic-proposition:8f25cb12afa89114e99ec231d48d0b77da696af99018f085ce985698966a8a22", "semantic-proposition:a2eba302ef01f3a3e0f7e0cb818f262829dff6a359bf912d938be0da39a50d7f"], "rationale": "Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding."}]`

## semantic-proposition:1339572c50667d53c69043aec12314c083d4830300573d4254caf26fef94a577

DISTINCT: SHOULD pull-request author — select relevant change types and remove irrelevant options

Retain an independent source-local proposition: pull-request author — SHOULD select relevant change types and remove irrelevant options. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 14, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "9864ded890adfc1b5a39240b51adbe625af6fcc97f3fe3a56073d13c4aca54da", "start_line": 9}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "select", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "relevant change types and remove irrelevant options", "parameters": ["bug fix", "feature", "breaking change", "documentation update"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:16699d8d8f97318331befa0dd39a6a0df2394edc20bc2576af2ff34587ab80d5

SPECIALIZED: SHOULD pull-request author — describe implemented solution

PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "2ac638530c56711a57688b78aed79e808bd206335877e94c139aace84c8e9970", "end_line": 7, "path": ".github/pull_request_template.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "6bbadef4ea87a2fda00e6f42ee7165b595c558813bedcfd47e25955fa9dd9ba3", "start_line": 5}]`

Preserved AST/applicability: `{"ambiguities": ["Prompt says implemented solution but answer hint says proposed solution; retain both readings for C0"], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "implemented solution", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:01f29e4d6e5415c42b7ac03e405f550cbd039af3648c0529024084a7ebe1e0f4", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:985ff89acd5fd5bc91a0d8f8cd273fbf321dce8495b0b92812636175bbdaf1f9", "semantic-proposition:c3cffdd46526529b4fe52da84168114332ba537c5a195801ed78e8b4bb8ae357"], "rationale": "PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt."}]`

## semantic-proposition:18018c3d2f51c64f579146b297e730c20a8870c50771665b970e073334adbf77

SPECIALIZED: SHOULD repository owner — consider issue/pull-request templates

Considering templates is should-category guidance; adapting optional templates is may guidance. Consideration and activation are different actions, so no contradiction is asserted.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 21, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "6e21d0426c4749dc043e0eab7513435274c83f0ae98eccd3191bf83973e65280", "start_line": 21}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "consider", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "issue/pull-request templates", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source shoulds category"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:b62a8c771e89b598eece178077f095d788a571316d69fd4cce0cfaa1abd32221"], "rationale": "Considering templates is should-category guidance; adapting optional templates is may guidance. Consideration and activation are different actions, so no contradiction is asserted."}]`

## semantic-proposition:183bf337651ff9b6b2cfa68689e8683d48baa172e055aa3c62a6c6edbb9576f2

SPECIALIZED: PROHIBITED participants — avoid public or private harassment

Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 50, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "45749c5f93e83d820404b02ccb9d3e0b4be93d88fd8e73316c88b4a8cadd2c3e", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "public or private harassment", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:6901a5ceda16838921e6391cfdd5f0ff3a47aa501dc8f3308a4a9789eb6f0ef2", "semantic-proposition:7dd372944da500c199a2249e65761fe00af6caccfe3a578425f0eda8abbbcedd"], "rationale": "Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition."}]`

## semantic-proposition:1a7f490828ca2776364f819aee55f6362a3de19f34fc01ec859f1a6836bfcb21

SPECIALIZED: MUST project participants — veto pull requests with failing tests

Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 33, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "dab57f16986c8e079f41887abe2cbe5c32994af11ec4408b22d2cac71a41ea3f", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "veto", "consequences": [], "exceptions": ["Tests may fail in development branches"], "modality": "MUST", "object": "pull requests with failing tests", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Repository has tests"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3c45c72ad7a3bef1764116b9e0875c02f26063599c11462edf7d0cbd933e879c", "semantic-proposition:8aac08345d3d3a6f49610507942453c3edafabcb652f1e466d3610614bea9f1f", "semantic-proposition:b04690db7fd8a0e144ed53ef536afd3912c82bb3caf25f0d67a40accc0e003f2"], "rationale": "Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred."}]`

## semantic-proposition:1b98edd4dbf95e557c9fdffbeeb8751189d29120d763c9c59aabaf1b558bd620

SPECIALIZED: SHOULD participants — prioritize community interests

Community-interest guidance differs in explicit comparison with individual interests; retain that difference.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 39, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "9465024e8cb4b47befe0d034c8ece409641cf6fce1fa6e21527a12522c2258d1", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "prioritize", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "community interests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:986b7c607dfc2d963628001dacbdc340f21ae09301712d9daf29bdec69e64ca8", "semantic-proposition:d6461f6d28d14fab9e3cf56326ea0a252689e6f157f2212dc841ef541cea6b24"], "rationale": "Community-interest guidance differs in explicit comparison with individual interests; retain that difference."}]`

## semantic-proposition:1c1982ad1fae3a4e6cf7a666ab340d9dbd8daad9bcdafc54e19d6a8a6b91e26d

SPECIALIZED: MAY question author — ask a question through the supplied issue prompt

Optional question submission is complemented by clarity/information guidance; optional participation is not turned into a required issue.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "a6dba91fa5b37b2fb9a8e04801285423766e9fcad526eb6a8f427ed4a63c4396", "end_line": 9, "path": ".github/ISSUE_TEMPLATE/question.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "1c883c412ecb99fc9a7c88f1082194292ac9e26c3cf75bc79e02459320569877", "start_line": 7}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "ask", "consequences": [], "exceptions": [], "modality": "MAY", "object": "a question through the supplied issue prompt", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/ISSUE_TEMPLATE/question.md"], "subject": "question author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:61af504542ab7adae3459d4aec4f3c7e2b9253dfd14d088ff759ec4e77708b1c"], "rationale": "Optional question submission is complemented by clarity/information guidance; optional participation is not turned into a required issue."}]`

## semantic-proposition:1ccb50d1b1f156565fa37a51d7c01c9e911344c848e5b0c6f41f4fd4b90a90a1

SPECIALIZED: MUST maintainers — assign issue labels and maintainer/contributor assignees

Label/assignee duties specialize issue and PR administration separately.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 25, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "0c4c337863ad3ff804e849a1412e99a3d496a2ce8b02c51a22f91a582a51ec47", "start_line": 25}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "assign", "consequences": [], "exceptions": [], "modality": "MUST", "object": "issue labels and maintainer/contributor assignees", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:5d47a0d9e956790934c9ad113328b06aa2fc6c577dc386fb9f85128edc54d10a"], "rationale": "Label/assignee duties specialize issue and PR administration separately."}]`

## semantic-proposition:1cecb5afb21e996f63a4dc3aec5df84d23eb66cd4d8a8cd5abb31551ceb5169d

SPECIALIZED: MAY project participants — use optionally release attachments or external storage such as S3

Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 126, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "a5ace811df5ec324efbc8f4514aee73f5f4f004388d93076c9646957eb379491", "start_line": 126}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "use optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "release attachments or external storage such as S3", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Files need not be versioned or stored in Git"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:53e67e234764545f48b50cfd82f628e1efb0bf3c87aedefabd40add401c0a851", "semantic-proposition:afd78843383f4c838e0d09f3587aeed5a1e33118f7c23c5c5c498f6726b74e75"], "rationale": "Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning."}]`

## semantic-proposition:1d289445aee7d57aa7c8c419c9ed9c24b98aadc091b46a254347e85784fbdba1

SPECIALIZED: MUST contributors and maintainers — pledge harassment-free participation regardless of the enumerated personal characteristics

Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 28, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "f9c0e38a9c8c8c4510db64ca3327a332f054e2cde3f2b084ca5797b784818d39", "start_line": 23}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "pledge", "consequences": [], "exceptions": [], "modality": "MUST", "object": "harassment-free participation regardless of the enumerated personal characteristics", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Covenant 1.4-derived pledge; scope and enumeration preserved in source span"], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributors and maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:31ea8e22be5a509bb9ab0ccb80613326b87afd6b2c0ba942072d193d737355d8", "semantic-proposition:87c48b409721f459cde668183ad7c0f0cc5c101075f81fafd6925630393170a0", "semantic-proposition:93b3aff9bb79ce6b681d373dc95a752406c32ea85706d201667d376fcc00224d"], "rationale": "Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor."}]`

## semantic-proposition:217074c1d5a6d4b05ea470e61865f6f3fb53efcbfde25478b4249edd8a184069

CONFLICTING: SHOULD repository owner — adapt or remove SECURITY.md describing vulnerability reporting

Security is placed in the optional coulds category but its file-adaptation instruction is a should with a removal exception. The same-file policy-strength tension remains open; no mandatory security policy is inferred.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 100, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "2dd8f768983ca9e4f0dca1a1069e934d6f53197be5bf1f51d09f0e026f71fe2d", "start_line": 96}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt or remove", "consequences": [], "exceptions": ["Remove if the project does not cover this topic"], "modality": "SHOULD", "object": "SECURITY.md describing vulnerability reporting", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:27553762bc8e81ea584a1bf8ec4aca89e02f9d5ed0c9c74c59cdeca8ebfe11fa"], "rationale": "Security is placed in the optional coulds category but its file-adaptation instruction is a should with a removal exception. The same-file policy-strength tension remains open; no mandatory security policy is inferred."}]`

## semantic-proposition:237dee03fb3e218d1826213bad600cd8ae3b454eecaeee858312ac1ddeaeaa29

REFERENTIAL: SHOULD developer — run example development server and open port 3000

Retain source-local example/reference: developer — SHOULD run example development server and open port 3000. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 92, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "e407a4cb770f055ed383f97d77565eb5ddbf44e3d873232e2c60698902d4e96e", "start_line": 86}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "run", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "example development server and open port 3000", "parameters": ["npm run dev or yarn dev", "localhost:3000"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No execution or functioning application asserted"], "scope": ["atapas/model-repo", "README.md"], "subject": "developer"}}`

Relationships: `[]`

## semantic-proposition:25f0422f4fc05c8cacdee2adc8f9a20a6c7ddaf3f3a1531fcb025917803c31af

SPECIALIZED: MUST leaders — use private written correction for inappropriate/unprofessional/unwelcome behavior

Private correction is parallel conduct guidance; leadership identity and applicability differ, so these are not exact duplicates.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 81, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "892043dd6e1920b0d474c4762b3a64bb4c1b3f377c7cc8adf7c25267a52ba01a", "start_line": 71}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "MUST", "object": "private written correction for inappropriate/unprofessional/unwelcome behavior", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Explain violation; public apology may be requested"], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:8dde6e4fc5c1174464c4f6fe00787f69a7b514531dac1275d3995c8671870572"], "rationale": "Private correction is parallel conduct guidance; leadership identity and applicability differ, so these are not exact duplicates."}]`

## semantic-proposition:2683ea08aa8b36fe7f5cf5eb1d229a1438a32dca6b55acf134a22fa21d447b6c

SPECIALIZED: MAY maintainers — moderate or ban nonconforming contributions and inappropriate, threatening, offensive or harmful participants

Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 62, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "a750d578a48e98269b2cbe7f9057b10d4b762a2ca6e0e26544170a8c079f0c46", "start_line": 58}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "moderate or ban", "consequences": [], "exceptions": [], "modality": "MAY", "object": "nonconforming contributions and inappropriate, threatening, offensive or harmful participants", "parameters": ["temporary or permanent ban"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:345e84c893c49793a31d2f591bb6b2a20804f3972a74cf19f58970c99206c79c", "semantic-proposition:781151aeb26f6aaa2e781d43b6b606ac81986061b1fce5dfbdb9fa6daf4f50d4", "semantic-proposition:a0e5d8e64b6a20002bca5ee9740019c707b8e840198914313ba4999108981d83", "semantic-proposition:ed744ad262eddb97378e9165e803af16d1a4fc504506a403386e4a79bf6ba234"], "rationale": "Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained."}]`

## semantic-proposition:26a25d9b384f2a76243e85456c38a031610ccb8f778100fa192a49bfca9c44c9

SPECIALIZED: MUST participants and project team — report and investigate unacceptable behavior with appropriate response and reporter confidentiality

Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 80, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "1c937a5b82ca4410ab6e542da49675a34ba4c6b78e71fc664f54ef43c18ddff9", "start_line": 75}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "report and investigate", "consequences": [], "exceptions": [], "modality": "MUST", "object": "unacceptable behavior with appropriate response and reporter confidentiality", "parameters": ["Source contact is bound in the span, not a GES destination"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Further enforcement policies may be posted separately"], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants and project team"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:bc7e605d5ac9316dfe746741fd851aff7d8f45e7e8ee5774b1f26252ba970e07", "semantic-proposition:c54d4ba1716a8f3e44183d0f3f963feea46e470d0441904d0a9bb5026eec040e"], "rationale": "Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed."}]`

## semantic-proposition:27553762bc8e81ea584a1bf8ec4aca89e02f9d5ed0c9c74c59cdeca8ebfe11fa

CONFLICTING: MAY repository owner — consider security policy

Security is placed in the optional coulds category but its file-adaptation instruction is a should with a removal exception. The same-file policy-strength tension remains open; no mandatory security policy is inferred.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 25, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "6e219d73067d5b5eeefef49e4f07e2d8c43042ad609cce73af5c1c1f1711c309", "start_line": 25}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "consider", "consequences": [], "exceptions": [], "modality": "MAY", "object": "security policy", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source coulds category"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:217074c1d5a6d4b05ea470e61865f6f3fb53efcbfde25478b4249edd8a184069"], "rationale": "Security is placed in the optional coulds category but its file-adaptation instruction is a should with a removal exception. The same-file policy-strength tension remains open; no mandatory security policy is inferred."}]`

## semantic-proposition:2b7def0f614525b679e2b307e1f1aa2b9c0328bdadbcc5cbd00bcb95a8cfad15

DISTINCT: MAY project — welcome contributions beyond code

Retain an independent source-local proposition: project — MAY welcome contributions beyond code. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 5, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "79e45295c908abac4f5acd496c8b27371c7c8a7704ec5c45dfe6e6418cb24094", "start_line": 5}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "welcome", "consequences": [], "exceptions": [], "modality": "MAY", "object": "contributions beyond code", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "project"}}`

Relationships: `[]`

## semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e

SPECIALIZED: SHOULD project participants — use the well-written pull-request description as primary explanation of changes

PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt. Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 108, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "28ad77a4ff54035426091b8ade9c402aff49f98d0bb5ae292cee637231193b25", "start_line": 108}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the well-written pull-request description as primary explanation of changes", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Commit messages need not be fine art"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:01f29e4d6e5415c42b7ac03e405f550cbd039af3648c0529024084a7ebe1e0f4", "semantic-proposition:16699d8d8f97318331befa0dd39a6a0df2394edc20bc2576af2ff34587ab80d5", "semantic-proposition:985ff89acd5fd5bc91a0d8f8cd273fbf321dce8495b0b92812636175bbdaf1f9", "semantic-proposition:c3cffdd46526529b4fe52da84168114332ba537c5a195801ed78e8b4bb8ae357"], "rationale": "PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt."}, {"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0e8541d6dcccc73b218d9fa055348d33755adc6b153390116a26f2732f394bf5", "semantic-proposition:4be68e7e45e38d45af75c12b417ae771c8560f44988e9b235ceb99b9a056d8f3", "semantic-proposition:f3ff9668a240b8a5a2c507ae7331dddcf00460aac4a0a5f1caeee2b1868e7dfa"], "rationale": "Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate."}]`

## semantic-proposition:2d0f2401df3e1978063ea6ce8f5043cf3fb5500fbf55451394509be5d3460f01

DISTINCT: MUST pull-request author — comment code, especially difficult areas

Retain an independent source-local proposition: pull-request author — MUST comment code, especially difficult areas. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 33, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "df2131ddc014438a4e3d5690df9475f46d8459072ec50583a33e10016313be68", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "comment", "consequences": [], "exceptions": [], "modality": "MUST", "object": "code, especially difficult areas", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:2dafbdaad5c7217c70e7107a6cee140f4f080f15570feec01f8c3b023d3ec431

SPECIALIZED: SHOULD project participants — separate cosmetic work, unrelated fixes and features into separate issues or pull requests

Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 90, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "b92139ea6d30046e8a8dc464186655ba56da878b83889149044e49fca43b09c7", "start_line": 88}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "separate", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "cosmetic work, unrelated fixes and features into separate issues or pull requests", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Discovery does not belong to the current idea"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:393eec09bfe975ee68f3c73e9762ecae6621d27c9159c6f525e3c52d97f8fb33", "semantic-proposition:cb6154618defbce295e39c7f0e69a8b8dcd9c2ca76f4a606fed7a7b19fa1044b", "semantic-proposition:ead9cd2f5bcab669c1da8572ba6e368c1cd9e9a5ac5595e7211d6a59893553c2"], "rationale": "Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible."}]`

## semantic-proposition:2f3680e51c628e278812960d1e27bb6c6f03c90977370b5be7335db7d5b281e2

SPECIALIZED: SHOULD repository owner — adapt CODE_OF_CONDUCT.md including behavior and reporting contacts

Conduct-file adaptation combines a must-category entry with concrete should guidance and reporting-contact customization.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 56, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "3a2f6cac6eab23028ae7940169884a81bfeb8a9909a4d145c498293e6a631440", "start_line": 52}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "CODE_OF_CONDUCT.md including behavior and reporting contacts", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:d9cbbf723ffaf200818c8fb8c7a1b1a647b63bdba9b3c931c657b45b72d79ecb"], "rationale": "Conduct-file adaptation combines a must-category entry with concrete should guidance and reporting-contact customization."}]`

## semantic-proposition:30400257c2df3ce2f826b540fe33f349cfad2376aa5b58bb24467ab6b510867b

CONFLICTING: MAY README — offer and invite demo viewing and optional starring

Earlier optional starring contrasts with later promotional must wording. Preserve the modal tension without interpreting promotional language as an enforceable platform or GES obligation.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 40, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "dc7e8060d6662374202dfd1553b6e29402d17c133908ec5ad261107f7e1732a0", "start_line": 36}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "offer and invite", "consequences": [], "exceptions": [], "modality": "MAY", "object": "demo viewing and optional starring", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Demo link is a personal site, not proof of an operating app"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:7e1f2649dbc489d8e161f908b657639bb039a4bb7bf4df1a2a8f23bb7889763d"], "rationale": "Earlier optional starring contrasts with later promotional must wording. Preserve the modal tension without interpreting promotional language as an enforceable platform or GES obligation."}]`

## semantic-proposition:3083e421dbf320a411b5f14de2b54f10d74c2ea5348218fc7f13e44d958f7073

SPECIALIZED: MUST maintainers — apply conduct rules in project spaces and public representation

Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 71, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "db8250bc810819a6b91a7caf89b36fc35e218a66bd89420752d892b94ec2c869", "start_line": 66}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "apply", "consequences": [], "exceptions": [], "modality": "MUST", "object": "conduct rules in project spaces and public representation", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Examples: project email, official social accounts or appointed representatives; maintainers may clarify representation"], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:93e50bd54ea4deab1e887ca031aeb14c374e48bb3d69c4776518019cce2c062e", "semantic-proposition:dc9bfc2336a131cde0e7e983980976538713a7f0b78370c4ed1786ca69b7ec16"], "rationale": "Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples."}]`

## semantic-proposition:31ea8e22be5a509bb9ab0ccb80613326b87afd6b2c0ba942072d193d737355d8

SPECIALIZED: MUST members, contributors and leaders — pledge harassment-free inclusive healthy participation regardless of enumerated characteristics

Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 6, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "01d45d4dd637c3083246e86bcefbd9808d5cfa789d26f3ef84b32daeca0ed8c8", "start_line": 4}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "pledge", "consequences": [], "exceptions": [], "modality": "MUST", "object": "harassment-free inclusive healthy participation regardless of enumerated characteristics", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Short version includes caste and visible/invisible disability"], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "members, contributors and leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1d289445aee7d57aa7c8c419c9ed9c24b98aadc091b46a254347e85784fbdba1", "semantic-proposition:87c48b409721f459cde668183ad7c0f0cc5c101075f81fafd6925630393170a0", "semantic-proposition:93b3aff9bb79ce6b681d373dc95a752406c32ea85706d201667d376fcc00224d"], "rationale": "Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor."}]`

## semantic-proposition:345e84c893c49793a31d2f591bb6b2a20804f3972a74cf19f58970c99206c79c

SPECIALIZED: MUST community leaders — clarify and enforce acceptable behavior through fair corrective action

Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "98ec25c43139061cb3e923cd5ece83d8dc4aaddc19d42daa5e51cc2f6841215f", "start_line": 41}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "clarify and enforce", "consequences": [], "exceptions": [], "modality": "MUST", "object": "acceptable behavior through fair corrective action", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "community leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2683ea08aa8b36fe7f5cf5eb1d229a1438a32dca6b55acf134a22fa21d447b6c", "semantic-proposition:781151aeb26f6aaa2e781d43b6b606ac81986061b1fce5dfbdb9fa6daf4f50d4", "semantic-proposition:a0e5d8e64b6a20002bca5ee9740019c707b8e840198914313ba4999108981d83", "semantic-proposition:ed744ad262eddb97378e9165e803af16d1a4fc504506a403386e4a79bf6ba234"], "rationale": "Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained."}]`

## semantic-proposition:345f7cd268645eb1992c15501dc81850450d896d607c5ca8ef5c58ca46d6626f

SPECIALIZED: SHOULD project participants — default new primary branch name to main

Defaulting a new branch to main differs from optionally renaming an existing master branch; no forced migration follows.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 21, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "07edccda9b68dc27a55839f1887d8828547bef0026423fe5262b726c3bc31dcc", "start_line": 21}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "default", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "new primary branch name to main", "parameters": ["main"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:6b8daeae2909449abc663607531b9ae5552a202ed8cc99bdefe8e1af90c9699c"], "rationale": "Defaulting a new branch to main differs from optionally renaming an existing master branch; no forced migration follows."}]`

## semantic-proposition:35afe8c2c3330c1f8d93dd9cc48818e278efc29e5e9ef4a0522e7322cd230800

DISTINCT: SHOULD reporter — provide desktop or smartphone environment details

Retain an independent source-local proposition: reporter — SHOULD provide desktop or smartphone environment details. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 35, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "106f1b094b2eb8b8ac21aad854cde6cb69e5c16bfb5966f48639da3f9079fca5", "start_line": 26}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "provide", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "desktop or smartphone environment details", "parameters": ["OS", "browser", "version", "smartphone device"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Example values are placeholders, not supported platform declarations"], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:37539ce9733cdfbf043a6e4a75e2a66c73be3a11d4853dfb15122dc59006a170

SPECIALIZED: SHOULD issue author — provide proposed solution

Proposed and desired solutions are parallel prompts for different issue types and source-local templates.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "a1f028fd0f7eee898fbbd8d070315a6a272d9aea10f65b92dac8d533c5638c17", "end_line": 13, "path": ".github/ISSUE_TEMPLATE/proposal.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "b2e2f3d391a696bd917d10e6a7e464518500eb19da026095c344de5b6ba726fa", "start_line": 11}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "provide", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "proposed solution", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/ISSUE_TEMPLATE/proposal.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:60f99d1ce7f47462bea9c4bfdd7f2f906e56c4d51a51294d9fe99ee4ff87278a"], "rationale": "Proposed and desired solutions are parallel prompts for different issue types and source-local templates."}]`

## semantic-proposition:38d9e9255e66084a702b77a061db0f2cf1600474af1d21229ab4629f81ed262d

SPECIALIZED: SHOULD project participants — use labels for categories and milestones for dated bounded work

Bounded dated milestones complement prohibition of categorical unbounded milestones; labels provide the alternative category mechanism.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 64, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "faaa689adce4ea0a346d9b6dd7e3489d8bc98755aa34b380ca994a94f70885d5", "start_line": 63}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "labels for categories and milestones for dated bounded work", "parameters": ["Example labels: bug, feature", "Example milestone: New feature sprint"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:d80b422b070fae3a3d33db1a231d601a72127da81ddfe4039d48d88d1344c466"], "rationale": "Bounded dated milestones complement prohibition of categorical unbounded milestones; labels provide the alternative category mechanism."}]`

## semantic-proposition:393eec09bfe975ee68f3c73e9762ecae6621d27c9159c6f525e3c52d97f8fb33

SPECIALIZED: SHOULD project participants — keep pull requests short, within a few days and focused on one idea

Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 90, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "b92139ea6d30046e8a8dc464186655ba56da878b83889149044e49fca43b09c7", "start_line": 88}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "keep", "consequences": ["Large diffs impede review, conflict handling and regression diagnosis"], "exceptions": ["Large ideas may need longer diffs"], "modality": "SHOULD", "object": "pull requests short, within a few days and focused on one idea", "parameters": ["A few days; no exact numeric threshold"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2dafbdaad5c7217c70e7107a6cee140f4f080f15570feec01f8c3b023d3ec431", "semantic-proposition:cb6154618defbce295e39c7f0e69a8b8dcd9c2ca76f4a606fed7a7b19fa1044b", "semantic-proposition:ead9cd2f5bcab669c1da8572ba6e368c1cd9e9a5ac5595e7211d6a59893553c2"], "rationale": "Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible."}]`

## semantic-proposition:3af19ca07d23bc0b3c9f4a5b98c62277d71ffdd411d528056cc42db3b4e91070

SPECIALIZED: PROHIBITED participants — avoid private information disclosure without explicit permission

Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 37, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "4b5b6be953bb068f9f45137712fb3ef859e622f1fc8bfd823c00dd7cb4ecfd4c", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "private information disclosure without explicit permission", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:ac4979a6484cf0715ae55c68fe36781f21c8e0af03a0654dc65bd8e2526b6f38", "semantic-proposition:ca4e91daef67b731bbba0d19637d478fc878a2cd2ab748850ae148b8bd805b22"], "rationale": "Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes."}]`

## semantic-proposition:3c26851e223216d5c140388a4eab9873d5a9fc96813ba1fd7d468befdf93ab40

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate ownership for root build/logs and descendants

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate ownership for root build/logs and descendants. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 33, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "958646b3799509b3cbd06289f6efd32aa7d45213e77ca5eb3b4e1f0f41bfa376", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "ownership for root build/logs and descendants", "parameters": ["/build/logs/", "@doctocat"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:3c45c72ad7a3bef1764116b9e0875c02f26063599c11462edf7d0cbd933e879c

SPECIALIZED: MUST project participants — maintain a passing main-branch test suite

Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 33, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "dab57f16986c8e079f41887abe2cbe5c32994af11ec4408b22d2cac71a41ea3f", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "maintain", "consequences": [], "exceptions": [], "modality": "MUST", "object": "a passing main-branch test suite", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Repository has tests"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1a7f490828ca2776364f819aee55f6362a3de19f34fc01ec859f1a6836bfcb21", "semantic-proposition:8aac08345d3d3a6f49610507942453c3edafabcb652f1e466d3610614bea9f1f", "semantic-proposition:b04690db7fd8a0e144ed53ef536afd3912c82bb3caf25f0d67a40accc0e003f2"], "rationale": "Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred."}]`

## semantic-proposition:3de46cee0429fa173e1c9629f138c205382647470bb332cdf6af1f2304081c81

SPECIALIZED: MUST repository owner — edit or adapt project description

Project description adaptation is complemented by About tags and conditional website configuration; retain the source-specific at-least-three-tags threshold.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 11, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "0c8b69b34980fc4e63f80541843f77545b17319411040b3f5dac2f00cf3d3ac0", "start_line": 11}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "project description", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:982e7c9341cb21477124cab32d5356718f1ea587abc43210ce272e2a75c3df85"], "rationale": "Project description adaptation is complemented by About tags and conditional website configuration; retain the source-specific at-least-three-tags threshold."}]`

## semantic-proposition:3eeafa86518088a83e9331db7c4bbba745e4b0993a44c06e1eea9a1c01f821a3

REFERENTIAL: DESCRIPTIVE governance template — define collaborator as willing participant and contributor as collaborator proposing a pull request

Retain source-local example/reference: governance template — DESCRIPTIVE define collaborator as willing participant and contributor as collaborator proposing a pull request. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 19, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "e74c975128e64bc83bb972c83933a4dc8a5e84a59e5ab85a9811570eccf22e39", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "define", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "collaborator as willing participant and contributor as collaborator proposing a pull request", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "governance template"}}`

Relationships: `[]`

## semantic-proposition:416582a26d6ffdd2fb365b7545785296a2776bb84cb62ef7e4263dd06f243ef1

DISTINCT: SHOULD repository owner — choose visibility of Releases, Packages and Environments tabs

Retain an independent source-local proposition: repository owner — SHOULD choose visibility of Releases, Packages and Environments tabs. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 40, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9c5f238756316947c23b650fe6dee2c379d3dd1a694e4ce283b8c228c4dfc117", "start_line": 40}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "choose", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "visibility of Releases, Packages and Environments tabs", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Remove these tabs when uncertain; source recommendation only"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[]`

## semantic-proposition:436ea8d9de93085d32e8ee4ed3ba6d35f20b3402fc83e2c5bf434d030c6a7e6a

SPECIALIZED: MUST participants — follow the code of conduct when participating

Participation requires the locally linked conduct policy; source-specific policies are not a universal adopted rule.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 24, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "11b2d3174fa0877639d89b28dae096ccf21bb01c7be91132db8341ee693f91a0", "start_line": 22}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "follow", "consequences": [], "exceptions": [], "modality": "MUST", "object": "the code of conduct when participating", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:475a38c4d57ce34ce748fa5da082a9375234cbb80972ff213f2b58ac820cd37b"], "rationale": "Participation requires the locally linked conduct policy; source-specific policies are not a universal adopted rule."}]`

## semantic-proposition:44431fcdd4e33b3ed3478a64653fc2642036df49c0f015bdc9b8b15265043377

SPECIALIZED: PROHIBITED participants — avoid other professionally inappropriate conduct

Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "other professionally inappropriate conduct", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:9a745252ccc68d81c02ebb8c6053a2df2c57f2b9187e560eaa462dbde6aa05c8", "semantic-proposition:fdfbd6a953c7f288eaf60f400d3baeb2d3c2759b0f3542e3f3a85520306d49f3"], "rationale": "Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes."}]`

## semantic-proposition:4463ee475b590661ef0fb61909e337267a874b10a9c3fc6c12e71e19438eb497

DISTINCT: MAY contributors and maintainers — submit and assess pull requests under the linked project governance rules

Retain an independent source-local proposition: contributors and maintainers — MAY submit and assess pull requests under the linked project governance rules. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 37, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "3809ba96e345942b1d460625e0b0e3fe59d113bc5c033f6869c60b2f11c14e40", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "submit and assess", "consequences": [], "exceptions": [], "modality": "MAY", "object": "pull requests under the linked project governance rules", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Governance references are internal dependencies, not approval evidence"], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "contributors and maintainers"}}`

Relationships: `[]`

## semantic-proposition:475a38c4d57ce34ce748fa5da082a9375234cbb80972ff213f2b58ac820cd37b

SPECIALIZED: MUST contributor — follow the code of conduct in all project interactions

Participation requires the locally linked conduct policy; source-specific policies are not a universal adopted rule.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 6, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "ab2a8aed2c564bd685c6cd485b4d9f0a2d847b2a7d3dcf1e57eaa59b615c8937", "start_line": 6}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "follow", "consequences": [], "exceptions": [], "modality": "MUST", "object": "the code of conduct in all project interactions", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:436ea8d9de93085d32e8ee4ed3ba6d35f20b3402fc83e2c5bf434d030c6a7e6a"], "rationale": "Participation requires the locally linked conduct policy; source-specific policies are not a universal adopted rule."}]`

## semantic-proposition:48952d712c806f1bf1f9698989e9275fd364cf759dc2402875c25d03cd60878f

SPECIALIZED: MAY repository owner — consider funding configuration

Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 26, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "8dcef1de05d4210a31fd25c79456a3df72db1253ba05dacfc77bfbc5dd1a02e9", "start_line": 26}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "consider", "consequences": [], "exceptions": [], "modality": "MAY", "object": "funding configuration", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source coulds category"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:12eb0d8d0e51bf1f3d23a35ebe00c27ebba8c75b17d218e8d9b6d6c674b3efa3", "semantic-proposition:4d99d3b09db42bf15e22d97dba0def1704ab59dc96a3f82128c9de8b8963cd3f", "semantic-proposition:8f25cb12afa89114e99ec231d48d0b77da696af99018f085ce985698966a8a22", "semantic-proposition:a2eba302ef01f3a3e0f7e0cb818f262829dff6a359bf912d938be0da39a50d7f"], "rationale": "Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding."}]`

## semantic-proposition:48de8e4361223d91529803334613923c8e56c96a20fb831a77cc24377da84260

DISTINCT: SHOULD participants — take responsibility for mistakes, apologize and learn

Retain an independent source-local proposition: participants — SHOULD take responsibility for mistakes, apologize and learn. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 26, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7b3f3a657791bfa3fe208f1d3d64d0065362a575f293cb136b106260921909bf", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "take responsibility", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "for mistakes, apologize and learn", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[]`

## semantic-proposition:4ad7e98a4b3813854ae4c0835a4e3e6494df94de608a843b105ff11a8c353be0

REFERENTIAL: SHOULD developer — create root environment file with local variables

Retain source-local example/reference: developer — SHOULD create root environment file with local variables. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 84, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "ac22d047cb793530e8609dd0818b49985f09692d4b9e18d41593572927e48ac1", "start_line": 80}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "create", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "root environment file with local variables", "parameters": [".env", "KEY=VALUE"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No secrets accessed or file created"], "scope": ["atapas/model-repo", "README.md"], "subject": "developer"}}`

Relationships: `[]`

## semantic-proposition:4be68e7e45e38d45af75c12b417ae771c8560f44988e9b235ceb99b9a056d8f3

SPECIALIZED: MAY project participants — leave discretionary squash, merge or rebase

Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 76, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "1c14146d0d5d1bc6e7269f48411db1d0f4c0c62b189e6fe8b3a80447adb0fa89", "start_line": 74}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "leave discretionary", "consequences": [], "exceptions": [], "modality": "MAY", "object": "squash, merge or rebase", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Different history tradeoffs; fancy history manipulation may waste effort"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0e8541d6dcccc73b218d9fa055348d33755adc6b153390116a26f2732f394bf5", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:f3ff9668a240b8a5a2c507ae7331dddcf00460aac4a0a5f1caeee2b1868e7dfa"], "rationale": "Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate."}]`

## semantic-proposition:4d3f3fc7016b5ad2414e501217a264d7a2470c5c872fb8e0aedfd4ef8656cfa1

DISTINCT: SHOULD maintainer — describe vulnerability reporting channel, update frequency and accepted/declined outcomes

Retain an independent source-local proposition: maintainer — SHOULD describe vulnerability reporting channel, update frequency and accepted/declined outcomes. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "ba9643955bfcb04524a6fe5a8c2929b54abc2e67bb3480ce806e742d506e4dc9", "end_line": 21, "path": "SECURITY.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "0d5c74d9049dfe87c3dc3000b4af9e61893482895350cd7551ec0e7b2ea2e1df", "start_line": 17}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "vulnerability reporting channel, update frequency and accepted/declined outcomes", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "SECURITY.md"], "subject": "maintainer"}}`

Relationships: `[]`

## semantic-proposition:4d99d3b09db42bf15e22d97dba0def1704ab59dc96a3f82128c9de8b8963cd3f

SPECIALIZED: DESCRIPTIVE funding template — illustrate supported funding keys and substitution instructions

Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "74eedd61a6e8bfdb213829cedbcaf93579bf6aef703981b14e692fb40486e8e7", "end_line": 13, "path": "FUNDING.yml", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "89b8bbb10f36e35faeaab4719f23f0e4e83dcaac2b03e4d4be90a58f85aeee9a", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "supported funding keys and substitution instructions", "parameters": ["github: up to 4 sponsor-enabled usernames", "custom: up to 4 URLs", "patreon, open_collective, ko_fi, liberapay, issuehunt, otechie: single username", "tidelift: platform/package", "community_bridge and lfx_crowdfunding: project name"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Keys are source-era examples; B0 does not refresh platform support"], "scope": ["jlcanovas/gh-best-practices-template", "FUNDING.yml"], "subject": "funding template"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:12eb0d8d0e51bf1f3d23a35ebe00c27ebba8c75b17d218e8d9b6d6c674b3efa3", "semantic-proposition:48952d712c806f1bf1f9698989e9275fd364cf759dc2402875c25d03cd60878f", "semantic-proposition:8f25cb12afa89114e99ec231d48d0b77da696af99018f085ce985698966a8a22", "semantic-proposition:a2eba302ef01f3a3e0f7e0cb818f262829dff6a359bf912d938be0da39a50d7f"], "rationale": "Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding."}]`

## semantic-proposition:4f3d21e5bd8dec78d18ffd14bda6b75b89ca0efed760dd2cbfe146e46892f1da

REFERENTIAL: DESCRIPTIVE README — describe model-repo as public repository best-practice examples for engagement

Retain source-local example/reference: README — DESCRIPTIVE describe model-repo as public repository best-practice examples for engagement. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 33, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "81a3be1750a3e5c22a8de3c8f2b1bf7bba6dc86947e57b2f0fca52aababbaba5", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "model-repo as public repository best-practice examples for engagement", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:521bb30cd73e08d37c75d5b97c77726cc3456453f42a899d83d59926fb0d187c

REFERENTIAL: DESCRIPTIVE guidelines — assume admin or owner permissions for the instructions

Retain source-local example/reference: guidelines — DESCRIPTIVE assume admin or owner permissions for the instructions. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 3, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "1e766cec70a1c5d8d123c9f02c151ceb3cd1de33c134026b4431f852682bf3d8", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "assume", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "admin or owner permissions for the instructions", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "guidelines"}}`

Relationships: `[]`

## semantic-proposition:53188c3cc33172714533a89914548b6ada4cd58f56dba5d16d0487aaf4a61971

SPECIALIZED: MAY project participants — offer optionally a Kanban Projects view

Optional Projects presentation is complemented by issue-derived progress when used; optional view availability is retained.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 55, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "ce26f1131100ee83e17182d3c360cf3340c5cd607a5aa1bb3363b84352042bf6", "start_line": 55}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "offer optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "a Kanban Projects view", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Author sees potential manager value without developer/design impact"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:bddc1a14de696ce681b05e1ad843e6e04becec64ff7f6524d121196fa8d7584a"], "rationale": "Optional Projects presentation is complemented by issue-derived progress when used; optional view availability is retained."}]`

## semantic-proposition:53888d0999bc168e78b94ad9f1b47fe98003e10db70a3b13723ed373f4071e50

SPECIALIZED: SHOULD repository owner — define and check CODEOWNERS and necessary write permissions against linked platform documentation

Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 72, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "6b5137ac0685d04957aa9e4ab39ee20ac3ef5751280abae774e217d382cc202c", "start_line": 68}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "define and check", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "CODEOWNERS and necessary write permissions against linked platform documentation", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source claims review requests occur for owned code; enforcement prerequisites not established by template"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:8e17ff56a50fb9d4449e7fa47ac598e02458af76c13f30aef51d1168d68519ed", "semantic-proposition:f2f5fe250f654079981c8a39ead77d76a1e2f1461b86ec4c79a76c2e03c5314a"], "rationale": "Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed."}]`

## semantic-proposition:53e67e234764545f48b50cfd82f628e1efb0bf3c87aedefabd40add401c0a851

SPECIALIZED: SHOULD project participants — avoid large binary history in ordinary Git

Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 122, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "966135d7e383172d8a8712153d4914c755fb2d18cf8b88baedea8268dc4b8417", "start_line": 122}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "avoid", "consequences": ["Every version increases repository size and cloning/storage cost"], "exceptions": [], "modality": "SHOULD", "object": "large binary history in ordinary Git", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1cecb5afb21e996f63a4dc3aec5df84d23eb66cd4d8a8cd5abb31551ceb5169d", "semantic-proposition:afd78843383f4c838e0d09f3587aeed5a1e33118f7c23c5c5c498f6726b74e75"], "rationale": "Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning."}]`

## semantic-proposition:55738ad32c5d3fae226f67367b387fe7214f853b30f61256a92999125295b5cd

SPECIALIZED: SHOULD repository owner — adapt or remove CITATION.cff for paper citation

Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 116, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "cc03ea594e8fe6caf28064a9f07fccff92a96f881f33a0517019a4fe09922c32", "start_line": 114}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt or remove", "consequences": [], "exceptions": ["Otherwise remove the file"], "modality": "SHOULD", "object": "CITATION.cff for paper citation", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Related paper and intent to facilitate citation"], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:89247a9d44e58f1a777d247459ea38211fceb282a42a25a31b64fd0b56e0c164", "semantic-proposition:dd05a0a6aead7e7884ee411c22f0efc6e607521342f04d82b6d63366519020be"], "rationale": "Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts."}]`

## semantic-proposition:568ac038cf9a6fae9062eebd3e64a96dee4ed560f7f0398b77a9c0d64a4f4b76

SPECIALIZED: MAY contributor — merge or delegate a pull request after two other developers sign off

Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 17, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "7c8b1bb0c6228431ae32b7ead2947ef0b2244b9c8a2d16f9a31192c1329c36b0", "start_line": 16}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "merge or delegate", "consequences": [], "exceptions": ["Without permission request the second reviewer to merge"], "modality": "MAY", "object": "a pull request after two other developers sign off", "parameters": ["2 other developers"], "polarity": "POSITIVE", "preconditions": ["Two other developer sign-offs"], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:a99b77a40359d468b19859c0df0259a4f5b3c9bfc1cab066d3305ea33b05c089", "semantic-proposition:b42003b15c2e3ff4d051bf901e5253dd039f6747c1ed219843519c67705be961", "semantic-proposition:df1d8a163fd5dbbc8effc2e935db58de96ff8ff60dab765456105fcd8548fd7d"], "rationale": "Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold."}]`

## semantic-proposition:56e99a199e597592847baddf683cbea61d20c510c05cb17fa68b68f8e99cc7b5

REFERENTIAL: DESCRIPTIVE README presentation — link bug and feature requests to a different project

Retain source-local example/reference: README presentation — DESCRIPTIVE link bug and feature requests to a different project. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 30, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "f21b73e70137d3a79f4df118489e4a146a214defd08b51a3c6a2baa0e96aa29d", "start_line": 27}]`

Preserved AST/applicability: `{"ambiguities": ["Links target TryShape rather than model-repo; unresolved source-specific mismatch"], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "link", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "bug and feature requests to a different project", "parameters": ["TryShape/tryshape"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "README presentation"}}`

Relationships: `[]`

## semantic-proposition:57cc59eb03e8e29d93aa0ab7f1b7d00a789bffa5bf2cba5bed89b9902d0834c8

DISTINCT: SHOULD template user — read and adapt the linked guidelines for local needs

Retain an independent source-local proposition: template user — SHOULD read and adapt the linked guidelines for local needs. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 20, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "7c5a2f96394b0569bb3978a84388f83d6592f3edffae6ae6ab3397609313adbf", "start_line": 18}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "read and adapt", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the linked guidelines for local needs", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "template user"}}`

Relationships: `[]`

## semantic-proposition:59d3b61086aabce28d2b5a6c930881eaa6a3db39a471593f48de3d54eb7018f0

DISTINCT: MAY project participants — leave discretionary post-merge branch deletion

Retain an independent source-local proposition: project participants — MAY leave discretionary post-merge branch deletion. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 27, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "2ce28f6670f08746e24a1d458defeec05216f2269ae0bd8e80519b8420d359dd", "start_line": 25}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "leave discretionary", "consequences": [], "exceptions": [], "modality": "MAY", "object": "post-merge branch deletion", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Deletion can resolve rare name collisions; recovery is a source assertion, not verified platform behavior"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:5bdfde5cc6201ba9b437ce5b1c9283f492bf54522e0b4066badc96ca4a8001eb

DISTINCT: SHOULD project participants — keep core documentation versioned with code in repository Markdown

Retain an independent source-local proposition: project participants — SHOULD keep core documentation versioned with code in repository Markdown. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 114, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "cf375ceddc36bd399ffa38548ff19496bb674fa01aa39cbb3450e6c8baa36324", "start_line": 114}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "keep", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "core documentation versioned with code in repository Markdown", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Wikis and external workspaces can drift and are absent from clones"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:5d47a0d9e956790934c9ad113328b06aa2fc6c577dc386fb9f85128edc54d10a

SPECIALIZED: MUST maintainers — assign pull-request labels and assignees

Label/assignee duties specialize issue and PR administration separately.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 33, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d020b5e0b0d190b84334b0f124ae7125e43cb0f6d1ba42c02ee9f872c57ad1cf", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "assign", "consequences": [], "exceptions": [], "modality": "MUST", "object": "pull-request labels and assignees", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1ccb50d1b1f156565fa37a51d7c01c9e911344c848e5b0c6f41f4fd4b90a90a1"], "rationale": "Label/assignee duties specialize issue and PR administration separately."}]`

## semantic-proposition:5e184bcc226a1545901af898d5975bab446c04427792cf493fb44349f71df5ba

DISTINCT: MUST project participants — follow the linked governance for development/community management

Retain an independent source-local proposition: project participants — MUST follow the linked governance for development/community management. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 26, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "132d3e401582f3b1420821de50e1aa9bd253eaa7aefd70d1996f3a77af087383", "start_line": 26}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "follow", "consequences": [], "exceptions": [], "modality": "MUST", "object": "the linked governance for development/community management", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:60f99d1ce7f47462bea9c4bfdd7f2f906e56c4d51a51294d9fe99ee4ff87278a

SPECIALIZED: SHOULD requester — describe desired solution

Proposed and desired solutions are parallel prompts for different issue types and source-local templates.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "1f48c52f209a971b8e7eae4120144d28fcf8ee38a7778a7b4d8cf1ab356617d2", "end_line": 14, "path": ".github/ISSUE_TEMPLATE/feature_request.md", "repository": "atapas/model-repo", "span_sha256": "1b39f64cb54a0cbc406008891b13d2a5c66cef4612a99ca3c73a1fc547b1c920", "start_line": 13}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "desired solution", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/feature_request.md"], "subject": "requester"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:37539ce9733cdfbf043a6e4a75e2a66c73be3a11d4853dfb15122dc59006a170"], "rationale": "Proposed and desired solutions are parallel prompts for different issue types and source-local templates."}]`

## semantic-proposition:61af504542ab7adae3459d4aec4f3c7e2b9253dfd14d088ff759ec4e77708b1c

SPECIALIZED: SHOULD question author — ask clear concise questions with useful information through the question issue template

Optional question submission is complemented by clarity/information guidance; optional participation is not turned into a required issue.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 11, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "562dd430fd311d964aa5c051d7cb54184bcf6f7e6dad82ac4e51468dbbc64be8", "start_line": 9}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "ask", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "clear concise questions with useful information through the question issue template", "parameters": ["YOUR-ORGANIZATION", "YOUR-PROJECT"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "question author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1c1982ad1fae3a4e6cf7a666ab340d9dbd8daad9bcdafc54e19d6a8a6b91e26d"], "rationale": "Optional question submission is complemented by clarity/information guidance; optional participation is not turned into a required issue."}]`

## semantic-proposition:67354deb32f502da3064e46377507434aade6e18e9a14836c47222f22cfb235c

REFERENTIAL: DESCRIPTIVE README — illustrate feature-description sections with placeholder descriptions

Retain source-local example/reference: README — DESCRIPTIVE illustrate feature-description sections with placeholder descriptions. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 58, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "12485dd33d6cd25807ece54c70089836a1a0ea9bc0059bf6a94baa748583120c", "start_line": 52}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "feature-description sections with placeholder descriptions", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:6753fb346daf0e594532c7da908c9fb04a9310ef5a2493e2188f42c83a0713ac

SPECIALIZED: MUST repository owner — edit or adapt README

README adaptation is specialized by required presentation topics and installation only when needed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 16, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "f0c9af38db4bbca74f05e2b9b3fb8661e8807e92d59c43a570d7cd27df6163ee", "start_line": 16}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "README", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:cecd429bed4c70abd2c4f8e3235dcc14e046475998cdaefa3c67e444d5a0fffc"], "rationale": "README adaptation is specialized by required presentation topics and installation only when needed."}]`

## semantic-proposition:6901a5ceda16838921e6391cfdd5f0ff3a47aa501dc8f3308a4a9789eb6f0ef2

SPECIALIZED: PROHIBITED participants — avoid public or private harassment

Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 37, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "4b5b6be953bb068f9f45137712fb3ef859e622f1fc8bfd823c00dd7cb4ecfd4c", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "public or private harassment", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:183bf337651ff9b6b2cfa68689e8683d48baa172e055aa3c62a6c6edbb9576f2", "semantic-proposition:7dd372944da500c199a2249e65761fe00af6caccfe3a578425f0eda8abbbcedd"], "rationale": "Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition."}]`

## semantic-proposition:6b8daeae2909449abc663607531b9ae5552a202ed8cc99bdefe8e1af90c9699c

SPECIALIZED: MAY project participants — rename optionally an existing master primary branch

Defaulting a new branch to main differs from optionally renaming an existing master branch; no forced migration follows.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 21, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "07edccda9b68dc27a55839f1887d8828547bef0026423fe5262b726c3bc31dcc", "start_line": 21}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "rename optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "an existing master primary branch", "parameters": ["master", "main"], "polarity": "POSITIVE", "preconditions": ["Maintainer considers renaming important"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:345f7cd268645eb1992c15501dc81850450d896d607c5ca8ef5c58ca46d6626f"], "rationale": "Defaulting a new branch to main differs from optionally renaming an existing master branch; no forced migration follows."}]`

## semantic-proposition:6c3ef4d4f2a71d47ede077ddf887c4424efe90135956cda2983328be7a4c6502

SPECIALIZED: SHOULD project participants — choose same-branch development or merge prerequisite then branch from main

Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 15, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "8cd486e6fb13ea12166169996fd1454efa42417b0846bba3f8b2ab4cf84e99f9", "start_line": 15}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "choose", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "same-branch development or merge prerequisite then branch from main", "parameters": [], "polarity": "POSITIVE", "preconditions": ["One feature depends on another"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:7c3403c3ff73b05121b6b222393c2aad0ac19a89943e21ee95c29dcd1f423dce", "semantic-proposition:da0476f1e8c3aa0f2c2ccd2d8ef02f138b13736ac7ded86b662a5224343e95c4"], "rationale": "Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives."}]`

## semantic-proposition:6d46b6276bd7ed16c1b622e3eb202a296171356dea9fce375b941ac1c9287562

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate patterns followed by owners, with wildcard default owners unless a later match overrides

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate patterns followed by owners, with wildcard default owners unless a later match overrides. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 11, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "e3fd6a1a1ec76cc6d8a1c39213f83feec7a963d8b88b643f43864620850a1236", "start_line": 5}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "patterns followed by owners, with wildcard default owners unless a later match overrides", "parameters": ["*", "@global-owner1", "@global-owner2"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:6e628982dc46dd79f431d60dfb96eab73ba79d345fc865c8d184ff8336214ceb

DISTINCT: SHOULD pull-request author — report executed tests, reproduction instructions and test configuration

Retain an independent source-local proposition: pull-request author — SHOULD report executed tests, reproduction instructions and test configuration. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 27, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "a16b696889a49ed794e612dc842ad6a3d47601ae12dc1f9b177211f7eedf0f7b", "start_line": 18}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "report", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "executed tests, reproduction instructions and test configuration", "parameters": ["firmware", "hardware", "toolchain", "SDK"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Test A/B are placeholders, not executed test receipts"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:708d9df155285fca1cdbd5f4b96ec32205f73f54bb3c7ac3b727183c6272fa4b

DISTINCT: SHOULD repository owner — remove the template folder

Retain an independent source-local proposition: repository owner — SHOULD remove the template folder. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 84, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "062ce435b571b17ecf787f3bc3528ca5d2c5f9fdb65599348bd2b0cd239fc128", "start_line": 84}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "remove", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the template folder", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Templates will not be used"], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[]`

## semantic-proposition:719b64fb50665fb2ac9a31c32a8a99def7fadd770c3f418b12429af5c0fc0930

SPECIALIZED: SHOULD participants — respect different viewpoints and experiences

Respect for differing views and experiences overlaps without identical source scope or wording.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 39, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "9465024e8cb4b47befe0d034c8ece409641cf6fce1fa6e21527a12522c2258d1", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "respect", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "different viewpoints and experiences", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:bcae8bfe4b2dfaf08cb9b284c7e526530b19aa247f98380ecb17a352b4e47af5", "semantic-proposition:df3f5d7e8f7bc1cba290bb8cda18896d39a797c42d3be8fe1477f37c6b4cc07f"], "rationale": "Respect for differing views and experiences overlaps without identical source scope or wording."}]`

## semantic-proposition:72d3c816b62fc4a7a905e746ce8c3b8d54b8635f7546359240bea789cda0371d

DISTINCT: MUST contributor — remove install/build dependencies before the build layer ends

Retain an independent source-local proposition: contributor — MUST remove install/build dependencies before the build layer ends. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 11, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "831a56db7ae1968a5a0e6b8613c5b5715476b2a7c53316d6d3d0c9ddf60de4ba", "start_line": 10}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "remove", "consequences": [], "exceptions": [], "modality": "MUST", "object": "install/build dependencies before the build layer ends", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Performing a layered build"], "qualifiers": ["Source wording presumes build layers; no universal container requirement"], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[]`

## semantic-proposition:733988b28e4200894f8b12f1e51f035610bbd766d23ee5eb1ede3a423cd8db8d

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate owner lookup by email as an alternative to username

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate owner lookup by email as an alternative to username. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 22, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d58022df2c7b9feb8b04f14fe15a5b6cd38b8d54c4f0e3f3e80edb534029b45b", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "owner lookup by email as an alternative to username", "parameters": ["*.go", "docs@example.com"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d

SPECIALIZED: SHOULD issue author — use the proposal issue template when no existing issue describes the problem

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 23, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "90db427ef6e4153683b5a958a7b6528fd34bb1320c5a1cab25e0fff265e76cc0", "start_line": 23}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the proposal issue template when no existing issue describes the problem", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22", "semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001", "semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf", "semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba", "semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:781151aeb26f6aaa2e781d43b6b606ac81986061b1fce5dfbdb9fa6daf4f50d4

SPECIALIZED: MUST maintainers — clarify and moderate unacceptable behavior fairly, including contribution removal or participant bans

Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 50, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "224ba9c47fb3e8ae7dc7427f7dbc94f9f1d99981015ddd6f976969e878d2f509", "start_line": 48}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "clarify and moderate", "consequences": [], "exceptions": [], "modality": "MUST", "object": "unacceptable behavior fairly, including contribution removal or participant bans", "parameters": ["temporary or permanent bans"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2683ea08aa8b36fe7f5cf5eb1d229a1438a32dca6b55acf134a22fa21d447b6c", "semantic-proposition:345e84c893c49793a31d2f591bb6b2a20804f3972a74cf19f58970c99206c79c", "semantic-proposition:a0e5d8e64b6a20002bca5ee9740019c707b8e840198914313ba4999108981d83", "semantic-proposition:ed744ad262eddb97378e9165e803af16d1a4fc504506a403386e4a79bf6ba234"], "rationale": "Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained."}]`

## semantic-proposition:7c1b58c56afdbad1aadb30c7cf293a4eeaa1d112f1c95cafb486f328015b0421

CONFLICTING: DESCRIPTIVE README — declare CC BY 4.0 licensing and reuse description

README declares CC BY 4.0 while guidelines describe CC-BY-SA as the starting license. Retain the documented source identity inconsistency; LICENSE.md remains B0 reference-only evidence, and no publication permission is decided.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 43, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "7cc83431282fd106c51961b77f3a194e71af4324eca44bfaa613cc8b536679b3", "start_line": 41}]`

Preserved AST/applicability: `{"ambiguities": ["guidelines.md says CC-BY-SA while README and LICENSE.md say Attribution 4.0"], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "declare", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "CC BY 4.0 licensing and reuse description", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Reference-only assertion; no D3 rights clearance"], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "README"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:e365a85130cfb6e48b9ac62e1a6f3c703b26dc1fd2a62e5cf41084093d8c0e97"], "rationale": "README declares CC BY 4.0 while guidelines describe CC-BY-SA as the starting license. Retain the documented source identity inconsistency; LICENSE.md remains B0 reference-only evidence, and no publication permission is decided."}]`

## semantic-proposition:7c3403c3ff73b05121b6b222393c2aad0ac19a89943e21ee95c29dcd1f423dce

SPECIALIZED: PROHIBITED project participants — avoid branch ancestry beyond the described occasional child of a feature branch

Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 15, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "8cd486e6fb13ea12166169996fd1454efa42417b0846bba3f8b2ab4cf84e99f9", "start_line": 15}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "avoid", "consequences": ["Deeper ancestry impairs review, maintenance and merging"], "exceptions": [], "modality": "PROHIBITED", "object": "branch ancestry beyond the described occasional child of a feature branch", "parameters": [], "polarity": "NEGATIVE", "preconditions": ["Source product-development context"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:6c3ef4d4f2a71d47ede077ddf887c4424efe90135956cda2983328be7a4c6502", "semantic-proposition:da0476f1e8c3aa0f2c2ccd2d8ef02f138b13736ac7ded86b662a5224343e95c4"], "rationale": "Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives."}]`

## semantic-proposition:7cc1bcc7b0c08af8acd5f7540ee7d54b4cec7dde06c65603e119ce8743ad0b7a

REFERENTIAL: MAY README — offer Vercel and Netlify deployment links for the source repository

Retain source-local example/reference: README — MAY offer Vercel and Netlify deployment links for the source repository. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 130, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "6a7156c93b0cbe7258b6938d78bbaf8b0961dca66c62ac317a598daf23d13bb9", "start_line": 125}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "offer", "consequences": [], "exceptions": [], "modality": "MAY", "object": "Vercel and Netlify deployment links for the source repository", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Buttons do not establish deployability, deployment or required provider"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:7d8ac43ec96dd3fbb7769e23fc13972f2e3f1982832bb6b8ac1a4e853ce34acc

REFERENTIAL: MAY reader — access the source repository URL

Retain source-local example/reference: reader — MAY access the source repository URL. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 49, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "6c573b38ab1e0b3858dc9d572e07bba529f452a9c3e77b02fe651a3513cedac7", "start_line": 47}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "access", "consequences": [], "exceptions": [], "modality": "MAY", "object": "the source repository URL", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "reader"}}`

Relationships: `[]`

## semantic-proposition:7dc61b450d8ff640d51bd614674b82d87ff326e8e89e3762895f07f48b56639f

DISTINCT: SHOULD pull-request authors — follow the pull-request template

Retain an independent source-local proposition: pull-request authors — SHOULD follow the pull-request template. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 33, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d020b5e0b0d190b84334b0f124ae7125e43cb0f6d1ba42c02ee9f872c57ad1cf", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "follow", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the pull-request template", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "pull-request authors"}}`

Relationships: `[]`

## semantic-proposition:7dd372944da500c199a2249e65761fe00af6caccfe3a578425f0eda8abbbcedd

SPECIALIZED: PROHIBITED participants — avoid public or private harassment

Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "public or private harassment", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:183bf337651ff9b6b2cfa68689e8683d48baa172e055aa3c62a6c6edbb9576f2", "semantic-proposition:6901a5ceda16838921e6391cfdd5f0ff3a47aa501dc8f3308a4a9789eb6f0ef2"], "rationale": "Harassment prohibition overlaps across conduct versions and projects; scope/applicability prevent an exact duplicate disposition."}]`

## semantic-proposition:7e1f2649dbc489d8e161f908b657639bb039a4bb7bf4df1a2a8f23bb7889763d

CONFLICTING: MUST README — urge starring as motivation in promotional must wording

Earlier optional starring contrasts with later promotional must wording. Preserve the modal tension without interpreting promotional language as an enforceable platform or GES obligation.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 152, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "2c95f0497d1ea2e8e54e6b71395d0684f9a11852f4905fdd59939455768b42ab", "start_line": 150}]`

Preserved AST/applicability: `{"ambiguities": ["Optional earlier star invitation versus promotional must wording retained for C0"], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "urge", "consequences": [], "exceptions": [], "modality": "MUST", "object": "starring as motivation in promotional must wording", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Promotional source expression, not enforceable GitHub platform obligation or GES adoption"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:30400257c2df3ce2f826b540fe33f349cfad2376aa5b58bb24467ab6b510867b"], "rationale": "Earlier optional starring contrasts with later promotional must wording. Preserve the modal tension without interpreting promotional language as an enforceable platform or GES obligation."}]`

## semantic-proposition:7ef30ba51663f16f1847025de9cea9bc99d0f2d0bbb058d72b9d6118f7fd8186

REFERENTIAL: SHOULD developer — enter model-repo working directory

Retain source-local example/reference: developer — SHOULD enter model-repo working directory. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 72, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "c66adc60d4dfba2395333e78f5ddb08c44f30ae9864e50da1b47051fa7f3fd1f", "start_line": 68}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "enter", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "model-repo working directory", "parameters": ["cd model-repo"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "developer"}}`

Relationships: `[]`

## semantic-proposition:7fd5b777fe54d09974108575a3f5300c608adfe87632b10111c7a90e11722cfb

SPECIALIZED: PROHIBITED participants — avoid trolling, insulting comments and personal or political attacks

Trolling and personal/political attacks overlap; insulting versus derogatory language is retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 50, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "45749c5f93e83d820404b02ccb9d3e0b4be93d88fd8e73316c88b4a8cadd2c3e", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "trolling, insulting comments and personal or political attacks", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:b3ee3b0c477a0685b9b9483f2d091818e0f67a1ce829b7ab85563e113123ec73", "semantic-proposition:f4dd7a4697ec6b6981ccdc0d2dcae6422b071c2ebae5fa45f11066cbb9363f18"], "rationale": "Trolling and personal/political attacks overlap; insulting versus derogatory language is retained."}]`

## semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001

SPECIALIZED: SHOULD project participants — link pull requests to the preceding issue

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 45, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "fd787b7e5f1451ed728a23c837642fe654efeb77ef016b2d50504de437905a2b", "start_line": 45}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "link", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "pull requests to the preceding issue", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Ideally use a closing Fixes reference"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22", "semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d", "semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf", "semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba", "semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:87c48b409721f459cde668183ad7c0f0cc5c101075f81fafd6925630393170a0

SPECIALIZED: MUST members, contributors and leaders — pledge harassment-free inclusive healthy participation regardless of enumerated characteristics

Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 13, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7769c3089e7916c5ffb2ae27fe240c614db302b1c066459c00b04c7b978bd3d7", "start_line": 5}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "pledge", "consequences": [], "exceptions": [], "modality": "MUST", "object": "harassment-free inclusive healthy participation regardless of enumerated characteristics", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Covenant 2.0-derived pledge; enumeration bound to source span"], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "members, contributors and leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1d289445aee7d57aa7c8c419c9ed9c24b98aadc091b46a254347e85784fbdba1", "semantic-proposition:31ea8e22be5a509bb9ab0ccb80613326b87afd6b2c0ba942072d193d737355d8", "semantic-proposition:93b3aff9bb79ce6b681d373dc95a752406c32ea85706d201667d376fcc00224d"], "rationale": "Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor."}]`

## semantic-proposition:886502be25fba36356e8b0f1b1d83bb4140778b1f3fc9b8ee0234f9c7aca40cd

SPECIALIZED: SHOULD participants — give and accept constructive feedback

Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 26, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7b3f3a657791bfa3fe208f1d3d64d0065362a575f293cb136b106260921909bf", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "give and accept", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "constructive feedback", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:a4b3551dfd79150eb9d0189f069800629e6983ee36ffe1c5f9e46937e5075773", "semantic-proposition:f0d4e7e90285f95e52ceb9cde4023aef53b1481101730bef23e788f2eac971f1"], "rationale": "Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them."}]`

## semantic-proposition:89247a9d44e58f1a777d247459ea38211fceb282a42a25a31b64fd0b56e0c164

SPECIALIZED: MAY repository owner — consider citation file for related paper

Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 27, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "dbac77e3acd83326d11033417f43cd3ed9216ab8068428c20810a43de76814fd", "start_line": 27}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "consider", "consequences": [], "exceptions": [], "modality": "MAY", "object": "citation file for related paper", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source coulds category"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:55738ad32c5d3fae226f67367b387fe7214f853b30f61256a92999125295b5cd", "semantic-proposition:dd05a0a6aead7e7884ee411c22f0efc6e607521342f04d82b6d63366519020be"], "rationale": "Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts."}]`

## semantic-proposition:8aac08345d3d3a6f49610507942453c3edafabcb652f1e466d3610614bea9f1f

SPECIALIZED: SHOULD project participants — resolve causes of nondeterministic test failure

Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 33, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "dab57f16986c8e079f41887abe2cbe5c32994af11ec4408b22d2cac71a41ea3f", "start_line": 33}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "resolve", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "causes of nondeterministic test failure", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Flaky tests cause failures"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1a7f490828ca2776364f819aee55f6362a3de19f34fc01ec859f1a6836bfcb21", "semantic-proposition:3c45c72ad7a3bef1764116b9e0875c02f26063599c11462edf7d0cbd933e879c", "semantic-proposition:b04690db7fd8a0e144ed53ef536afd3912c82bb3caf25f0d67a40accc0e003f2"], "rationale": "Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred."}]`

## semantic-proposition:8b6cd2331fc1f45d4fbb2fdd33e0d43dfc5de84860bf96b3055ff88142bb2d20

SPECIALIZED: MUST maintainers — use warning with consequences and timed no-contact restrictions for incidents or series of actions

Warning guidance preserves no-contact channels, unspecified duration and possible later bans in each source.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 86, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "73406e11b26a51756ece0868b7fc59712ff1c635449761dca8096177344b7e28", "start_line": 85}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": ["Violation may cause temporary or permanent ban"], "exceptions": [], "modality": "MUST", "object": "warning with consequences and timed no-contact restrictions for incidents or series of actions", "parameters": ["specified period; no fixed duration"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No unsolicited contact including enforcers and external channels"], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:a35df41727b4bb2b50af96fdf3ed9cfd5d99dcea8779e308856c2b7650ee6a97"], "rationale": "Warning guidance preserves no-contact channels, unspecified duration and possible later bans in each source."}]`

## semantic-proposition:8d0ddbbbcfa76b92d5829125da6fa9eeb2767cc78ab27b7fb219f05c5487b676

DISTINCT: SHOULD requester — describe the motivating problem when related to the request

Retain an independent source-local proposition: requester — SHOULD describe the motivating problem when related to the request. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "1f48c52f209a971b8e7eae4120144d28fcf8ee38a7778a7b4d8cf1ab356617d2", "end_line": 11, "path": ".github/ISSUE_TEMPLATE/feature_request.md", "repository": "atapas/model-repo", "span_sha256": "a7324ad74994e91ef60977ea0cdc16458e8da718f78b36330e7fb70af8f1800d", "start_line": 10}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the motivating problem when related to the request", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Feature request concerns a problem"], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/feature_request.md"], "subject": "requester"}}`

Relationships: `[]`

## semantic-proposition:8dde6e4fc5c1174464c4f6fe00787f69a7b514531dac1275d3995c8671870572

SPECIALIZED: MUST maintainers — use private written correction for inappropriate/unprofessional/unwelcome behavior

Private correction is parallel conduct guidance; leadership identity and applicability differ, so these are not exact duplicates.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 81, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "309890f056a93d497e43d9519b5dc65332666da714d8a539a684abcc171ca279", "start_line": 76}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "MUST", "object": "private written correction for inappropriate/unprofessional/unwelcome behavior", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Explain violation; public apology may be requested"], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:25f0422f4fc05c8cacdee2adc8f9a20a6c7ddaf3f3a1531fcb025917803c31af"], "rationale": "Private correction is parallel conduct guidance; leadership identity and applicability differ, so these are not exact duplicates."}]`

## semantic-proposition:8e17ff56a50fb9d4449e7fa47ac598e02458af76c13f30aef51d1168d68519ed

SPECIALIZED: MUST template-defined team owners — require explicit repository write access for team ownership

Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 28, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "f9db9a6e6ed9832a8e4b8c0399c0a43bc2767ae2a40b0eb765d3dfb73808e1b1", "start_line": 24}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "require", "consequences": [], "exceptions": [], "modality": "MUST", "object": "explicit repository write access for team ownership", "parameters": ["@org/team-name", "*.txt @octo-org/octocats"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Borrowed platform statement remains community evidence; verify against Docs in C4"], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "template-defined team owners"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:53888d0999bc168e78b94ad9f1b47fe98003e10db70a3b13723ed373f4071e50", "semantic-proposition:f2f5fe250f654079981c8a39ead77d76a1e2f1461b86ec4c79a76c2e03c5314a"], "rationale": "Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed."}]`

## semantic-proposition:8ebf41fe05d620f5ebb2e390b7097a3a3ed39f3bf12fa61b69f8f1aa3e9a1d94

SPECIALIZED: MAY other project leaders — allow temporary or permanent leadership consequences for bad-faith enforcement failures

Bad-faith enforcement consequences are discretionary and source-local, including temporary/permanent leadership consequences.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 84, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "48c162f1c30b5a819c80264adc3a4e1a05a981234501cdb119ea4a7f0f9bd602", "start_line": 82}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "allow", "consequences": [], "exceptions": [], "modality": "MAY", "object": "temporary or permanent leadership consequences for bad-faith enforcement failures", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "other project leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:01e668f06c84b8d3d3f7eb8bf65830ad6f36e003158e165a4b2100dcd7c962f4"], "rationale": "Bad-faith enforcement consequences are discretionary and source-local, including temporary/permanent leadership consequences."}]`

## semantic-proposition:8edfc2bd46ccd2725261a051a488e496b3cd2475569838880b17b331284cb2ab

REFERENTIAL: DESCRIPTIVE author — frame opinionated system-level recommendations for long-lived continuously deployed products

Retain source-local example/reference: author — DESCRIPTIVE frame opinionated system-level recommendations for long-lived continuously deployed products. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 5, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "95461d2cf177847516363dfe99901fa7d310d78fc2139580ac52da46f480f037", "start_line": 1}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "frame", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "opinionated system-level recommendations for long-lived continuously deployed products", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "author"}}`

Relationships: `[]`

## semantic-proposition:8f25cb12afa89114e99ec231d48d0b77da696af99018f085ce985698966a8a22

SPECIALIZED: MAY README — invite optionally coffee support through the source-specific support link

Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 146, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "6d9142e6a6d52e994dd94b9b56cb243d917bd9a8e41d069ee0044f48651d3e1b", "start_line": 142}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "invite optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "coffee support through the source-specific support link", "parameters": ["greenroots"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No universal donation obligation"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:12eb0d8d0e51bf1f3d23a35ebe00c27ebba8c75b17d218e8d9b6d6c674b3efa3", "semantic-proposition:48952d712c806f1bf1f9698989e9275fd364cf759dc2402875c25d03cd60878f", "semantic-proposition:4d99d3b09db42bf15e22d97dba0def1704ab59dc96a3f82128c9de8b8963cd3f", "semantic-proposition:a2eba302ef01f3a3e0f7e0cb818f262829dff6a359bf912d938be0da39a50d7f"], "rationale": "Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding."}]`

## semantic-proposition:922b4deae39129c716df06c7e85e5d83bdd5af610cc8253b9497df3ebd85cd96

DISTINCT: MAY collaborators and maintainers — propose pull requests

Retain an independent source-local proposition: collaborators and maintainers — MAY propose pull requests. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 31, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "ca0d54de5e9b5ab59a2c4f9fecbdfde7481227726bcb7d1ff4a3c07ebdaffc57", "start_line": 31}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "propose", "consequences": [], "exceptions": [], "modality": "MAY", "object": "pull requests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "collaborators and maintainers"}}`

Relationships: `[]`

## semantic-proposition:9266fa993dba3186ee5377665df0b4b68c5a1942a81953f41a1708993a16ce4e

SPECIALIZED: SHOULD participants — use welcoming inclusive language

Inclusive-language guidance remains source-local across the contribution and conduct documents.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "use", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "welcoming inclusive language", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0f286f7b74b41bc5cc73092a3b91816011ec12ddb5c85a16c315fdc22475d11c"], "rationale": "Inclusive-language guidance remains source-local across the contribution and conduct documents."}]`

## semantic-proposition:93b3aff9bb79ce6b681d373dc95a752406c32ea85706d201667d376fcc00224d

SPECIALIZED: MUST contributors and maintainers — pledge respectful harassment-free contribution through issues, features, documentation, pull requests and other activities

Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 21, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "f72a0c4eca08263b5134fc4f9181af74ca94b8ffe9c5a0c2b0c369b0896b84c3", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "pledge", "consequences": [], "exceptions": [], "modality": "MUST", "object": "respectful harassment-free contribution through issues, features, documentation, pull requests and other activities", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Long pledge has a different enumerated characteristic list from short version"], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "contributors and maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1d289445aee7d57aa7c8c419c9ed9c24b98aadc091b46a254347e85784fbdba1", "semantic-proposition:31ea8e22be5a509bb9ab0ccb80613326b87afd6b2c0ba942072d193d737355d8", "semantic-proposition:87c48b409721f459cde668183ad7c0f0cc5c101075f81fafd6925630393170a0"], "rationale": "Harassment-free pledges span Covenant 1.4/2.0-derived and short/long forms. Enumerated characteristics and participating roles differ; no version is designated a successor."}]`

## semantic-proposition:93e50bd54ea4deab1e887ca031aeb14c374e48bb3d69c4776518019cce2c062e

SPECIALIZED: MUST maintainers and participants — apply and enforce conduct rules in all project spaces for every participant at all times

Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 56, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "f290e56e9516b723086b8a592b3b9e3a6c0d3f1bcb41108bd80ef2e8ff96dd26", "start_line": 54}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "apply and enforce", "consequences": [], "exceptions": [], "modality": "MUST", "object": "conduct rules in all project spaces for every participant at all times", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "maintainers and participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3083e421dbf320a411b5f14de2b54f10d74c2ea5348218fc7f13e44d958f7073", "semantic-proposition:dc9bfc2336a131cde0e7e983980976538713a7f0b78370c4ed1786ca69b7ec16"], "rationale": "Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples."}]`

## semantic-proposition:944813e96e72951c97755c4b54dc4a4db816d10626dec15c6ac321bc3d15db0a

REFERENTIAL: DESCRIPTIVE governance template — describe project development/community governance and administrator maintainers

Retain source-local example/reference: governance template — DESCRIPTIVE describe project development/community governance and administrator maintainers. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 11, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "ae6b3cf20f3ab36fda894237c4e8bfe329fb5b56af76024afeddfe99db6cdd17", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "project development/community governance and administrator maintainers", "parameters": ["USER1", "USER2", "USER3"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Placeholder list does not establish effective access"], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "governance template"}}`

Relationships: `[]`

## semantic-proposition:96eb9373dac6a3ba81eb3e0208755d7a9fdf3e061e71d374e9dc7e1ef92d8b05

DISTINCT: MUST contributor — update README interface changes including variables, ports, useful paths and container parameters

Retain an independent source-local proposition: contributor — MUST update README interface changes including variables, ports, useful paths and container parameters. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 13, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "fb240f7a0917e223fdc193e964b4198a5c03d31058e7b3e3b95ea326ac20ea34", "start_line": 12}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "update", "consequences": [], "exceptions": [], "modality": "MUST", "object": "README interface changes including variables, ports, useful paths and container parameters", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[]`

## semantic-proposition:98215faef7db118ddf84fb9a089b38e323102e68efc657c17c17a9d9668a2f95

REFERENTIAL: DESCRIPTIVE README — declare MIT license with link to local LICENSE

Retain source-local example/reference: README — DESCRIPTIVE declare MIT license with link to local LICENSE. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 104, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "10b695f57dd29ad2430a4b20f4e362784980ce8b1f41efc12d81f26814ab5495", "start_line": 104}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "declare", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "MIT license with link to local LICENSE", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Reference-only; no D3 clearance"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:982e7c9341cb21477124cab32d5356718f1ea587abc43210ce272e2a75c3df85

SPECIALIZED: SHOULD repository owner — edit About description and at least three tags, plus website URL when present

Project description adaptation is complemented by About tags and conditional website configuration; retain the source-specific at-least-three-tags threshold.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 38, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "96c2eb679b754dac225a571f63dee52b59c3909c93d813a4c8a24ddf112b6483", "start_line": 36}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "About description and at least three tags, plus website URL when present", "parameters": ["at least 3 tags"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3de46cee0429fa173e1c9629f138c205382647470bb332cdf6af1f2304081c81"], "rationale": "Project description adaptation is complemented by About tags and conditional website configuration; retain the source-specific at-least-three-tags threshold."}]`

## semantic-proposition:985ff89acd5fd5bc91a0d8f8cd273fbf321dce8495b0b92812636175bbdaf1f9

SPECIALIZED: SHOULD pull-request author — describe the issue addressed by the pull request

PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "2ac638530c56711a57688b78aed79e808bd206335877e94c139aace84c8e9970", "end_line": 3, "path": ".github/pull_request_template.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d6a1c963df68c9d7f9db638de816daac7dbc0b0b9bc95a82cfaa1e635910ebe1", "start_line": 1}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the issue addressed by the pull request", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:01f29e4d6e5415c42b7ac03e405f550cbd039af3648c0529024084a7ebe1e0f4", "semantic-proposition:16699d8d8f97318331befa0dd39a6a0df2394edc20bc2576af2ff34587ab80d5", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:c3cffdd46526529b4fe52da84168114332ba537c5a195801ed78e8b4bb8ae357"], "rationale": "PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt."}]`

## semantic-proposition:986b7c607dfc2d963628001dacbdc340f21ae09301712d9daf29bdec69e64ca8

SPECIALIZED: SHOULD participants — prioritize the overall community rather than individual interests

Community-interest guidance differs in explicit comparison with individual interests; retain that difference.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 26, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7b3f3a657791bfa3fe208f1d3d64d0065362a575f293cb136b106260921909bf", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "prioritize", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the overall community rather than individual interests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1b98edd4dbf95e557c9fdffbeeb8751189d29120d763c9c59aabaf1b558bd620", "semantic-proposition:d6461f6d28d14fab9e3cf56326ea0a252689e6f157f2212dc841ef541cea6b24"], "rationale": "Community-interest guidance differs in explicit comparison with individual interests; retain that difference."}]`

## semantic-proposition:9914a5d030c3fbc60abe9387d5623a1599eef41c2bfd881bb373ecd976ad194b

REFERENTIAL: SHOULD developer — clone the source model repository

Retain source-local example/reference: developer — SHOULD clone the source model repository. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 66, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "fe2b7734d7848983f8e36180867a5b23932c7051d77fccf2a1693afaf746a37e", "start_line": 62}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "clone", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "the source model repository", "parameters": ["git clone https://github.com/atapas/model-repo.git"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Command is unexecuted example data"], "scope": ["atapas/model-repo", "README.md"], "subject": "developer"}}`

Relationships: `[]`

## semantic-proposition:9a745252ccc68d81c02ebb8c6053a2df2c57f2b9187e560eaa462dbde6aa05c8

SPECIALIZED: PROHIBITED participants — avoid other professionally inappropriate conduct

Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 37, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "4b5b6be953bb068f9f45137712fb3ef859e622f1fc8bfd823c00dd7cb4ecfd4c", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "other professionally inappropriate conduct", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:44431fcdd4e33b3ed3478a64653fc2642036df49c0f015bdc9b8b15265043377", "semantic-proposition:fdfbd6a953c7f288eaf60f400d3baeb2d3c2759b0f3542e3f3a85520306d49f3"], "rationale": "Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes."}]`

## semantic-proposition:9b3581dee852be85c346a49007154da28070996215bda16e5dacec61d168473c

SPECIALIZED: PROHIBITED participants — avoid sexualized language or imagery and sexual attention or advances of any kind

Sexual conduct prohibitions differ: attention/advances of any kind versus unwelcome attention/advances. Preserve both predicates; do not claim equivalence.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 37, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "4b5b6be953bb068f9f45137712fb3ef859e622f1fc8bfd823c00dd7cb4ecfd4c", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "sexualized language or imagery and sexual attention or advances of any kind", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:a64896c0bcc4d77fc3b31ea7e8e82fc19688fc8d367abe43ec402150a7172043"], "rationale": "Sexual conduct prohibitions differ: attention/advances of any kind versus unwelcome attention/advances. Preserve both predicates; do not claim equivalence."}]`

## semantic-proposition:9fad09f5b507d22cb9a739a7d4fb56d3b7d3c671f9b8e1e56950ae8b9f3af845

REFERENTIAL: DESCRIPTIVE model author — aim to increase engagements, contributions, stars and sponsorship

Retain source-local example/reference: model author — DESCRIPTIVE aim to increase engagements, contributions, stars and sponsorship. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 6, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "d1a521de25d7adbc9184bd2df7878fd2e5a3184b1f130c3ddc764d7860b34b1e", "start_line": 6}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "aim", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "to increase engagements, contributions, stars and sponsorship", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "model author"}}`

Relationships: `[]`

## semantic-proposition:a0e5d8e64b6a20002bca5ee9740019c707b8e840198914313ba4999108981d83

SPECIALIZED: MUST maintainers — clarify and correct unacceptable behavior appropriately and fairly

Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 56, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "1dc9893bc49e520784a6dcd6800e9dee763cabf9bb7e0184d3fa2cc4a5e06e1e", "start_line": 54}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "clarify and correct", "consequences": [], "exceptions": [], "modality": "MUST", "object": "unacceptable behavior appropriately and fairly", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2683ea08aa8b36fe7f5cf5eb1d229a1438a32dca6b55acf134a22fa21d447b6c", "semantic-proposition:345e84c893c49793a31d2f591bb6b2a20804f3972a74cf19f58970c99206c79c", "semantic-proposition:781151aeb26f6aaa2e781d43b6b606ac81986061b1fce5dfbdb9fa6daf4f50d4", "semantic-proposition:ed744ad262eddb97378e9165e803af16d1a4fc504506a403386e4a79bf6ba234"], "rationale": "Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained."}]`

## semantic-proposition:a0ecb40145c983a611359fcd3806314b8109e21a76a4924dd049e83263061df3

DISTINCT: MAY README — invite positive contributions, existing or new features, and pull requests following linked contribution/conduct process

Retain an independent source-local proposition: README — MAY invite positive contributions, existing or new features, and pull requests following linked contribution/conduct process. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 138, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "eec20a827f2b9cef771cefe88d85ed039115b3fce3374a0bac0288c136b02631", "start_line": 134}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "invite", "consequences": [], "exceptions": [], "modality": "MAY", "object": "positive contributions, existing or new features, and pull requests following linked contribution/conduct process", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:a10b0aafaea9dee32ea090ecdf71b539958ab2738cb6da2c88e3e8f2d6690aa7

DISTINCT: MUST project leaders — limit conduct response to present behavior rather than past behavior or fears based on it

Retain an independent source-local proposition: project leaders — MUST limit conduct response to present behavior rather than past behavior or fears based on it. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 58, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "ee0d9f58f8ca222a71b9817baf0464e8047520de9c8352c1c85e8ce5a54bafb1", "start_line": 58}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "limit", "consequences": [], "exceptions": [], "modality": "MUST", "object": "conduct response to present behavior rather than past behavior or fears based on it", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "project leaders"}}`

Relationships: `[]`

## semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf

SPECIALIZED: SHOULD issue author — search open issues before filing a problem or feature

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 19, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "35fc9514e94a528fe322ec8d1a3d36e2f0621b502cb414031c4687263f4e16a8", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "search", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "open issues before filing a problem or feature", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22", "semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d", "semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001", "semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba", "semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:a2937f92429e841029c0afff2e10315edc378b9b842959b26221ad7b1f6ef54d

REFERENTIAL: SHOULD developer — install example JavaScript dependencies

Retain source-local example/reference: developer — SHOULD install example JavaScript dependencies. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 78, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "943cfe532e87c9782db0d810fb75d8abf370d1944edda8373c6aeddb656fa9d7", "start_line": 74}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "install", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "example JavaScript dependencies", "parameters": ["npm install or yarn install"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Example commands do not prove package manifest/dependencies exist"], "scope": ["atapas/model-repo", "README.md"], "subject": "developer"}}`

Relationships: `[]`

## semantic-proposition:a2eba302ef01f3a3e0f7e0cb818f262829dff6a359bf912d938be0da39a50d7f

SPECIALIZED: DESCRIPTIVE funding example — configure one GitHub sponsor account

Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "8ca043d78f4a8dccc9e346bee4ad9d2250a6ec0287aa6e5fe8eabfd6ad81c09f", "end_line": 3, "path": ".github/FUNDING.yml", "repository": "atapas/model-repo", "span_sha256": "e106d2e431eb0477a39d140d8085047bccf816d11736592a0d24399545dda147", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "configure", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "one GitHub sponsor account", "parameters": ["atapas"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Literal source identity, not a consumer recipient"], "scope": ["atapas/model-repo", ".github/FUNDING.yml"], "subject": "funding example"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:12eb0d8d0e51bf1f3d23a35ebe00c27ebba8c75b17d218e8d9b6d6c674b3efa3", "semantic-proposition:48952d712c806f1bf1f9698989e9275fd364cf759dc2402875c25d03cd60878f", "semantic-proposition:4d99d3b09db42bf15e22d97dba0def1704ab59dc96a3f82128c9de8b8963cd3f", "semantic-proposition:8f25cb12afa89114e99ec231d48d0b77da696af99018f085ce985698966a8a22"], "rationale": "Optional funding selection, conditional activation, funding-key examples, literal sponsor identity and coffee-support invitation differ. Preserve recipients as examples and do not configure consumer funding."}]`

## semantic-proposition:a35df41727b4bb2b50af96fdf3ed9cfd5d99dcea8779e308856c2b7650ee6a97

SPECIALIZED: MUST leaders — use warning with consequences and timed no-contact restrictions for incidents or series of actions

Warning guidance preserves no-contact channels, unspecified duration and possible later bans in each source.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 93, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "0884610b39c6137c8a73fe7b95fedf4c1869ca3f0f8c66878bea0525daf938d3", "start_line": 85}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "use", "consequences": ["Violation may cause temporary or permanent ban"], "exceptions": [], "modality": "MUST", "object": "warning with consequences and timed no-contact restrictions for incidents or series of actions", "parameters": ["specified period; no fixed duration"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No unsolicited contact including enforcers and external channels"], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:8b6cd2331fc1f45d4fbb2fdd33e0d43dfc5de84860bf96b3055ff88142bb2d20"], "rationale": "Warning guidance preserves no-contact channels, unspecified duration and possible later bans in each source."}]`

## semantic-proposition:a4b3551dfd79150eb9d0189f069800629e6983ee36ffe1c5f9e46937e5075773

SPECIALIZED: SHOULD participants — accept constructive criticism gracefully

Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 39, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "9465024e8cb4b47befe0d034c8ece409641cf6fce1fa6e21527a12522c2258d1", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "accept", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "constructive criticism gracefully", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:886502be25fba36356e8b0f1b1d83bb4140778b1f3fc9b8ee0234f9c7aca40cd", "semantic-proposition:f0d4e7e90285f95e52ceb9cde4023aef53b1481101730bef23e788f2eac971f1"], "rationale": "Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them."}]`

## semantic-proposition:a64896c0bcc4d77fc3b31ea7e8e82fc19688fc8d367abe43ec402150a7172043

SPECIALIZED: PROHIBITED participants — avoid sexualized language or imagery and unwelcome attention or advances

Sexual conduct prohibitions differ: attention/advances of any kind versus unwelcome attention/advances. Preserve both predicates; do not claim equivalence.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 50, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "45749c5f93e83d820404b02ccb9d3e0b4be93d88fd8e73316c88b4a8cadd2c3e", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "sexualized language or imagery and unwelcome attention or advances", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:9b3581dee852be85c346a49007154da28070996215bda16e5dacec61d168473c"], "rationale": "Sexual conduct prohibitions differ: attention/advances of any kind versus unwelcome attention/advances. Preserve both predicates; do not claim equivalence."}]`

## semantic-proposition:a99b77a40359d468b19859c0df0259a4f5b3c9bfc1cab066d3305ea33b05c089

SPECIALIZED: SHOULD project participants — prefer pull-request author performing integration

Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 84, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "1b864a89dd0002b0876f56854d8f85f15acdb7c75f61944a732829ca7f267580", "start_line": 80}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "prefer", "consequences": ["Author knows deployed changes and owns immediate post-merge failure repair"], "exceptions": ["Restricted commit access requires authorized integrator", "Absence or urgent integration"], "modality": "SHOULD", "object": "pull-request author performing integration", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Author has permission"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:568ac038cf9a6fae9062eebd3e64a96dee4ed560f7f0398b77a9c0d64a4f4b76", "semantic-proposition:b42003b15c2e3ff4d051bf901e5253dd039f6747c1ed219843519c67705be961", "semantic-proposition:df1d8a163fd5dbbc8effc2e935db58de96ff8ff60dab765456105fcd8548fd7d"], "rationale": "Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold."}]`

## semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba

SPECIALIZED: SHOULD contributor — discuss planned changes with owners before modifying the repository through issue, email or another method

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 4, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "1332072cf75b06c24aae4b38998b64f7abe7c0b324093603029a679fd101d8c3", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "discuss", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "planned changes with owners before modifying the repository through issue, email or another method", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22", "semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d", "semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001", "semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf", "semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:ac4979a6484cf0715ae55c68fe36781f21c8e0af03a0654dc65bd8e2526b6f38

SPECIALIZED: PROHIBITED participants — avoid private information disclosure without explicit permission

Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "private information disclosure without explicit permission", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3af19ca07d23bc0b3c9f4a5b98c62277d71ffdd411d528056cc42db3b4e91070", "semantic-proposition:ca4e91daef67b731bbba0d19637d478fc878a2cd2ab748850ae148b8bd805b22"], "rationale": "Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes."}]`

## semantic-proposition:accb9d966d6975b92ddbe9e8b9decf86957f0fb5b88a5c346f8ef3c0726b6543

SPECIALIZED: MUST maintainers — answer issues within 48 hours

Issue and PR response duties each retain the template-specific 48-hour target; neither becomes a GES service promise.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 27, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9a667a50334e3159d348eba9e3a5809892719e34ba201a930e0e8989890bcc78", "start_line": 27}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "answer", "consequences": [], "exceptions": [], "modality": "MUST", "object": "issues within 48 hours", "parameters": ["48 hours"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template promise, not a GES service level"], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:ba7d93faddc0e18efbd4df5f4dd69b4b1cccaeeac0bdc0196e1a38acc459b1a9"], "rationale": "Issue and PR response duties each retain the template-specific 48-hour target; neither becomes a GES service promise."}]`

## semantic-proposition:aee77883998e6dbbf9033e92355d43a984892f0a4cfb975d23f85aae3d4ed4da

DISTINCT: SHOULD reporter — describe expected behavior

Retain an independent source-local proposition: reporter — SHOULD describe expected behavior. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 21, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "206be874c20b48c395242cae625e10c28550a5870a8522d705de06b190e9c386", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "expected behavior", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:afd78843383f4c838e0d09f3587aeed5a1e33118f7c23c5c5c498f6726b74e75

SPECIALIZED: SHOULD project participants — configure Git LFS for the kinds of large files that require versioning

Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 124, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "22aee417af9e739249d5ab1c3e7b75bb8b7df157716bd46ac11e2a6f3d2cd563", "start_line": 124}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "configure", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "Git LFS for the kinds of large files that require versioning", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Large files must be versioned and kept in the repository"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1cecb5afb21e996f63a4dc3aec5df84d23eb66cd4d8a8cd5abb31551ceb5169d", "semantic-proposition:53e67e234764545f48b50cfd82f628e1efb0bf3c87aedefabd40add401c0a851"], "rationale": "Large-file advice distinguishes ordinary Git history, LFS for versioned files and optional release/external storage for files not needing Git versioning."}]`

## semantic-proposition:b036001bfa4ebb5f7fb298d98481018f13c2bb96e6b1b9a0f4fd50be5b507bfc

DISTINCT: MUST repository owner — edit or adapt license choice

Retain an independent source-local proposition: repository owner — MUST edit or adapt license choice. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 15, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9e9fbfc6b70e1021908347eed541e38c3ec89e4be10abb8bcccade0d06601c24", "start_line": 15}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "license choice", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[]`

## semantic-proposition:b04690db7fd8a0e144ed53ef536afd3912c82bb3caf25f0d67a40accc0e003f2

SPECIALIZED: MUST pull-request author — pass new and existing unit tests locally

Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 37, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "bd27b3a9913c52888e6066bf36c34c905bd0e680902f9c5fe63f1d152c78a157", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "pass", "consequences": [], "exceptions": [], "modality": "MUST", "object": "new and existing unit tests locally", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1a7f490828ca2776364f819aee55f6362a3de19f34fc01ec859f1a6836bfcb21", "semantic-proposition:3c45c72ad7a3bef1764116b9e0875c02f26063599c11462edf7d0cbd933e879c", "semantic-proposition:8aac08345d3d3a6f49610507942453c3edafabcb652f1e466d3610614bea9f1f"], "rationale": "Test health covers merge veto, main-branch passing suite, nondeterminism repair and local attestations. Preserve repository-has-tests conditions and development-branch exception; no execution is inferred."}]`

## semantic-proposition:b0eeb5ae53df2f40e10ddfe586efd5fe2f2f8ce0140152ec2d8713d285686293

DISTINCT: MUST pull-request author — follow project code style

Retain an independent source-local proposition: pull-request author — MUST follow project code style. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 31, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "414558974452653ba4e6bcabb6792237bdb69032e431871267897d9d3f43dfc8", "start_line": 31}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "follow", "consequences": [], "exceptions": [], "modality": "MUST", "object": "project code style", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:b2dad4a1a384a97359075a2be0cafd103d465bb2f6c0d481a11e4435f427ebad

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate unanchored apps directories versus root-anchored docs and descendants

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate unanchored apps directories versus root-anchored docs and descendants. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 47, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9f7afe8ea0a1f4a3b44c0acac1ea5f767b5a40c81bc1b9f672282a5dd35ea473", "start_line": 40}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "unanchored apps directories versus root-anchored docs and descendants", "parameters": ["apps/ @octocat", "/docs/ @doctocat"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:b2fd03a64ff9d30432efa9457db2579ac6c8c69c9fdd32969d1868a33aa8ac0c

DISTINCT: MUST contributor — increment example and README versions using SemVer

Retain an independent source-local proposition: contributor — MUST increment example and README versions using SemVer. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 15, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "0960b2a9d4a1f42350bc0a2423ebffbac55302e1c760023375d38ee2b1b17da4", "start_line": 14}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "increment", "consequences": [], "exceptions": [], "modality": "MUST", "object": "example and README versions using SemVer", "parameters": ["SemVer"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "contributor"}}`

Relationships: `[]`

## semantic-proposition:b3ee3b0c477a0685b9b9483f2d091818e0f67a1ce829b7ab85563e113123ec73

SPECIALIZED: PROHIBITED participants — avoid trolling, derogatory comments and personal or political attacks

Trolling and personal/political attacks overlap; insulting versus derogatory language is retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 37, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "4b5b6be953bb068f9f45137712fb3ef859e622f1fc8bfd823c00dd7cb4ecfd4c", "start_line": 30}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "trolling, derogatory comments and personal or political attacks", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:7fd5b777fe54d09974108575a3f5300c608adfe87632b10111c7a90e11722cfb", "semantic-proposition:f4dd7a4697ec6b6981ccdc0d2dcae6422b071c2ebae5fa45f11066cbb9363f18"], "rationale": "Trolling and personal/political attacks overlap; insulting versus derogatory language is retained."}]`

## semantic-proposition:b42003b15c2e3ff4d051bf901e5253dd039f6747c1ed219843519c67705be961

SPECIALIZED: MUST maintainers — require two maintainer approvals before merge

Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 40, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "ff65d0cae45b1723e71873b88f0d2d15b2730b636cf4cc5a8c03e7c99e5d79d9", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "require", "consequences": [], "exceptions": ["One maintainer approval suffices after more than 14 days open"], "modality": "MUST", "object": "two maintainer approvals before merge", "parameters": ["2 maintainers", "1 maintainer", "more than 14 days"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:568ac038cf9a6fae9062eebd3e64a96dee4ed560f7f0398b77a9c0d64a4f4b76", "semantic-proposition:a99b77a40359d468b19859c0df0259a4f5b3c9bfc1cab066d3305ea33b05c089", "semantic-proposition:df1d8a163fd5dbbc8effc2e935db58de96ff8ff60dab765456105fcd8548fd7d"], "rationale": "Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold."}]`

## semantic-proposition:b62a8c771e89b598eece178077f095d788a571316d69fd4cce0cfaa1abd32221

SPECIALIZED: MAY repository owner — adapt optionally issue and pull-request templates under .github

Considering templates is should-category guidance; adapting optional templates is may guidance. Consideration and activation are different actions, so no contradiction is asserted.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 82, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "5d959899f5268471f80f53c19c2f43149fe961abf7b0bdad1917dcdc0f8acd18", "start_line": 76}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt optionally", "consequences": [], "exceptions": [], "modality": "MAY", "object": "issue and pull-request templates under .github", "parameters": [".github/ISSUE_TEMPLATE", ".github"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:18018c3d2f51c64f579146b297e730c20a8870c50771665b970e073334adbf77"], "rationale": "Considering templates is should-category guidance; adapting optional templates is may guidance. Consideration and activation are different actions, so no contradiction is asserted."}]`

## semantic-proposition:b6b1c1c7ffd037aa6e4f6ee469a91f45e2c3bf5e4a054b86cec7cabc61da46fb

REFERENTIAL: DESCRIPTIVE template project — provide adaptable project bootstrap files and linked guidelines

Retain source-local example/reference: template project — DESCRIPTIVE provide adaptable project bootstrap files and linked guidelines. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 7, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "11edb2dc7f7c3234b95e185e5facb9f2ac6d4d5b0259e8614fbdea67480a58be", "start_line": 3}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "provide", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "adaptable project bootstrap files and linked guidelines", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "template project"}}`

Relationships: `[]`

## semantic-proposition:b7f600ea8726903fd3347fe81506cf175f06e3884fd59b15d1695574cb72b8a6

SPECIALIZED: SHOULD issue author — describe detected issue or problem

Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "a1f028fd0f7eee898fbbd8d070315a6a272d9aea10f65b92dac8d533c5638c17", "end_line": 9, "path": ".github/ISSUE_TEMPLATE/proposal.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "2037ed5fc2494011a268d659d624f2c560a1774d23dffd93406e68451f9912a1", "start_line": 7}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "detected issue or problem", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/ISSUE_TEMPLATE/proposal.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:031cc9fd8d53d51678e9773ac78a7718e4a754c26e4b101469fa536bd73d1e22", "semantic-proposition:765865566b2fd3f0e289453b175d044828aef1945816649cfe8379a21bf6114d", "semantic-proposition:85b4a380beb7691ff384c58e954d1f38d294280f52f1d7d78a0371d7ea2d3001", "semantic-proposition:a1d2b8a2cb1f1d2695caf96ac2bad1a7778d62cc175ce03c31f7632e4c7790bf", "semantic-proposition:aad87746726494dd28b204c8ad11720b30321704fff023577eae2d6aa86b52ba"], "rationale": "Issue-first planning, searching existing issues, proposal problem description and linking PRs are complementary. Preserve tiniest-change exception and atapas issue/email/other discussion alternatives."}]`

## semantic-proposition:b824cdb6320b941ee778b27224bbc81cd7f662a008c1e265be49a887264ac09a

DISTINCT: MUST maintainers — organize and maintain project development and updates; review and merge pull requests

Retain an independent source-local proposition: maintainers — MUST organize and maintain project development and updates; review and merge pull requests. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 17, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "32f8a36b0f6968af401842f04582d156620a682c4bc2707698024c4482c43936", "start_line": 17}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "organize and maintain", "consequences": [], "exceptions": [], "modality": "MUST", "object": "project development and updates; review and merge pull requests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[]`

## semantic-proposition:ba7d93faddc0e18efbd4df5f4dd69b4b1cccaeeac0bdc0196e1a38acc459b1a9

SPECIALIZED: MUST maintainers — answer pull requests within 48 hours

Issue and PR response duties each retain the template-specific 48-hour target; neither becomes a GES service promise.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 35, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "b3815e1ddb85d930bb16fb27b3dc3830e5985129cba1653ad86df1cee3b58650", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "answer", "consequences": [], "exceptions": [], "modality": "MUST", "object": "pull requests within 48 hours", "parameters": ["48 hours"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:accb9d966d6975b92ddbe9e8b9decf86957f0fb5b88a5c346f8ef3c0726b6543"], "rationale": "Issue and PR response duties each retain the template-specific 48-hour target; neither becomes a GES service promise."}]`

## semantic-proposition:bae7d78cba4471ef4d1e8e17dc8c2f95957fb2ac551394a7ddae8fe7c7aeaf02

SPECIALIZED: MUST repository owner — edit or adapt contribution guidelines

Contribution-guideline adaptation is expressed both as a must-category requirement and a concrete should instruction; retain both strengths and the project placeholders.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 12, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "51f27d536210725e2c956d3fd3f0e07dd5ff0d4e030072b805c9f2e53381fc6d", "start_line": 12}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "contribution guidelines", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0068bc452cf1e28c4359c1c178aa42b215be4734235fa643184fd104376030f2"], "rationale": "Contribution-guideline adaptation is expressed both as a must-category requirement and a concrete should instruction; retain both strengths and the project placeholders."}]`

## semantic-proposition:bc7e605d5ac9316dfe746741fd851aff7d8f45e7e8ee5774b1f26252ba970e07

SPECIALIZED: MUST participants and leaders — report and investigate unacceptable behavior promptly and fairly while protecting reporter privacy/security

Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 67, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "e5a167b46e04beb2fce1b1a5e2e7d8d7cd2059479415550e7c8ec7e7f0b4de21", "start_line": 61}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "report and investigate", "consequences": [], "exceptions": [], "modality": "MUST", "object": "unacceptable behavior promptly and fairly while protecting reporter privacy/security", "parameters": ["Source email is bound in span; no GES reporting recipient"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants and leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:26a25d9b384f2a76243e85456c38a031610ccb8f778100fa192a49bfca9c44c9", "semantic-proposition:c54d4ba1716a8f3e44183d0f3f963feea46e470d0441904d0a9bb5026eec040e"], "rationale": "Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed."}]`

## semantic-proposition:bcae8bfe4b2dfaf08cb9b284c7e526530b19aa247f98380ecb17a352b4e47af5

SPECIALIZED: SHOULD participants — respect different opinions, viewpoints and experiences

Respect for differing views and experiences overlaps without identical source scope or wording.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 26, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7b3f3a657791bfa3fe208f1d3d64d0065362a575f293cb136b106260921909bf", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "respect", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "different opinions, viewpoints and experiences", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:719b64fb50665fb2ac9a31c32a8a99def7fadd770c3f418b12429af5c0fc0930", "semantic-proposition:df3f5d7e8f7bc1cba290bb8cda18896d39a797c42d3be8fe1477f37c6b4cc07f"], "rationale": "Respect for differing views and experiences overlaps without identical source scope or wording."}]`

## semantic-proposition:bce1a8bda9e4ea8d01cc99f6298307ce8f9d49f762066d7f08c1fe41c0e6cfba

DISTINCT: MUST pull-request author — confirm dependent changes merged and published downstream

Retain an independent source-local proposition: pull-request author — MUST confirm dependent changes merged and published downstream. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 38, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "ad92ddeb62965f2f38effa0eac4ef4a35dd5fd72421236b4cff3263138135a8b", "start_line": 38}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "confirm", "consequences": [], "exceptions": [], "modality": "MUST", "object": "dependent changes merged and published downstream", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:bd5bc0b89624b928f0922711341bf756fbb0570eb18d871670a70585a0af2eeb

REFERENTIAL: DESCRIPTIVE governance template — attribute acceptance of change responsibility to contributor through approval wording

Retain source-local example/reference: governance template — DESCRIPTIVE attribute acceptance of change responsibility to contributor through approval wording. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 42, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "18a8c8f90e3ade080fb085b1b2efaa64795b7eb2dd6beaad31b049c76f567cc9", "start_line": 41}]`

Preserved AST/applicability: `{"ambiguities": ["Approver role versus contributor responsibility is not fully clear in the source wording"], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "attribute", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "acceptance of change responsibility to contributor through approval wording", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "governance template"}}`

Relationships: `[]`

## semantic-proposition:bddc1a14de696ce681b05e1ad843e6e04becec64ff7f6524d121196fa8d7584a

SPECIALIZED: SHOULD project participants — derive Projects progress from issues rather than parallel notes

Optional Projects presentation is complemented by issue-derived progress when used; optional view availability is retained.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 59, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "d6bc0d0b1ed0eb779d6b4d8e13a164b27db610a34f099b8c0f1b83ffce6b684b", "start_line": 57}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "derive", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "Projects progress from issues rather than parallel notes", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Best case includes automated movement as pull requests resolve issues"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:53188c3cc33172714533a89914548b6ada4cd58f56dba5d16d0487aaf4a61971"], "rationale": "Optional Projects presentation is complemented by issue-derived progress when used; optional view availability is retained."}]`

## semantic-proposition:be2176bda7d72a972b14963521e1932b0231aa49b55c6395b9efb444bef3dcb4

SPECIALIZED: MUST leaders — use temporary ban for serious violations including sustained misconduct

Temporary-ban guidance retains no-contact scope, unspecified duration and escalation consequences in each project.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 104, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "060bc7db3647510585350cc693e23b77c5442c98b3f52ce048ed3579c9e5d018", "start_line": 97}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "use", "consequences": ["Violating restrictions may cause permanent ban"], "exceptions": [], "modality": "MUST", "object": "temporary ban for serious violations including sustained misconduct", "parameters": ["specified period; no fixed duration"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No community interaction or public/private contact with involved people including enforcers"], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:097f8e363fe0ec382aec886e2f3f67021c4ecd8bb909cc684a081f979b1fccd6"], "rationale": "Temporary-ban guidance retains no-contact scope, unspecified duration and escalation consequences in each project."}]`

## semantic-proposition:c3cffdd46526529b4fe52da84168114332ba537c5a195801ed78e8b4bb8ae357

SPECIALIZED: SHOULD project participants — describe issues and pull requests for other readers, including solo projects

PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 41, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "feea21dd2985b4a94bd369d0fd902ab677ca080de4876304c228826836458794", "start_line": 39}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "issues and pull requests for other readers, including solo projects", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Avoid author knowledge assumptions; an external concept link is reference-only"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:01f29e4d6e5415c42b7ac03e405f550cbd039af3648c0529024084a7ebe1e0f4", "semantic-proposition:16699d8d8f97318331befa0dd39a6a0df2394edc20bc2576af2ff34587ab80d5", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:985ff89acd5fd5bc91a0d8f8cd273fbf321dce8495b0b92812636175bbdaf1f9"], "rationale": "PR communication combines issue/motivation/dependencies, implemented solution and reader context. Tmcw prefers the PR description over polished commit art; this does not replace any prompt."}]`

## semantic-proposition:c54d4ba1716a8f3e44183d0f3f963feea46e470d0441904d0a9bb5026eec040e

SPECIALIZED: MUST participants and project team — report and investigate unacceptable behavior through maintainer contacts, appropriate response and reporter confidentiality

Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 69, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "345db621913cd9260e972cc435de38fe6e9a6e070435cd0fbeb160e597640836", "start_line": 61}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "report and investigate", "consequences": [], "exceptions": [], "modality": "MUST", "object": "unacceptable behavior through maintainer contacts, appropriate response and reporter confidentiality", "parameters": ["USER1", "USER2", "USER3"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants and project team"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:26a25d9b384f2a76243e85456c38a031610ccb8f778100fa192a49bfca9c44c9", "semantic-proposition:bc7e605d5ac9316dfe746741fd851aff7d8f45e7e8ee5774b1f26252ba970e07"], "rationale": "Reporting/investigation overlaps, but promptness, privacy/security and literal versus placeholder reporting contacts differ. No real GES recipient is installed."}]`

## semantic-proposition:c989526098ddd79efccb930eb72c52f54e32e14e03baff8a249d22a7409bbacb

DISTINCT: MAY collaborators and maintainers — propose and discuss issues subject to the code of conduct

Retain an independent source-local proposition: collaborators and maintainers — MAY propose and discuss issues subject to the code of conduct. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 23, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "78b0d22a51872d9ffb790d8c23e9cb193dc5f551d4d49fc7c479e97b45ed050e", "start_line": 23}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "propose and discuss", "consequences": [], "exceptions": [], "modality": "MAY", "object": "issues subject to the code of conduct", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "collaborators and maintainers"}}`

Relationships: `[]`

## semantic-proposition:ca4e91daef67b731bbba0d19637d478fc878a2cd2ab748850ae148b8bd805b22

SPECIALIZED: PROHIBITED participants — avoid publishing private information without explicit permission

Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 50, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "45749c5f93e83d820404b02ccb9d3e0b4be93d88fd8e73316c88b4a8cadd2c3e", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "publishing private information without explicit permission", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3af19ca07d23bc0b3c9f4a5b98c62277d71ffdd411d528056cc42db3b4e91070", "semantic-proposition:ac4979a6484cf0715ae55c68fe36781f21c8e0af03a0654dc65bd8e2526b6f38"], "rationale": "Privacy prohibitions preserve explicit-permission requirements and their respective participant scopes."}]`

## semantic-proposition:cb6154618defbce295e39c7f0e69a8b8dcd9c2ca76f4a606fed7a7b19fa1044b

SPECIALIZED: SHOULD issue author — file one problem or feature per issue with reproduction information where possible

Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 29, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "dcfcd04dd4e505d3152dc56e6ca970bbc9928898d087252974e343d7f9ed15cc", "start_line": 27}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "file", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "one problem or feature per issue with reproduction information where possible", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2dafbdaad5c7217c70e7107a6cee140f4f080f15570feec01f8c3b023d3ec431", "semantic-proposition:393eec09bfe975ee68f3c73e9762ecae6621d27c9159c6f525e3c52d97f8fb33", "semantic-proposition:ead9cd2f5bcab669c1da8572ba6e368c1cd9e9a5ac5595e7211d6a59893553c2"], "rationale": "Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible."}]`

## semantic-proposition:cc357b938c1a1da5f121260ffced3a6d5f50a118c4c8ed8935510dc496be1767

SPECIALIZED: SHOULD participants — show empathy towards community members

Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "show", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "empathy towards community members", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:081f31a8ff74dff830d11cca35a51038b92f2fd93832577a55eb755f0a666f01", "semantic-proposition:d265eab3ef6db45e91ef99e5d39138befed6500612f194066ede97023fa3e776", "semantic-proposition:eecd5c8892f0e437dc966170b5bd5618d79ab99c1b90b4f7ae87a5340c5685b9"], "rationale": "Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate."}]`

## semantic-proposition:ce11547b84128cda63b864547e9023f5cb126728c015db99aaa6cfa08ff7ece5

SPECIALIZED: MUST repository owner — edit or adapt governance rules

Governance adaptation preserves must-category wording and should-level details for authority, timing and admission.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 14, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "d757fa556a8358051495c0b83d9b14f528889582fa4728cdae666fd5caa3deb3", "start_line": 14}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "governance rules", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:d0269d064c4b97dac959524e29c63481024cf5c38751376fca42c899e37419e0"], "rationale": "Governance adaptation preserves must-category wording and should-level details for authority, timing and admission."}]`

## semantic-proposition:ce57e57c9db42c28687ca212a418f2d5b29ac35f8c970e2276980a5502c58322

DISTINCT: SHOULD issue author — comment or react on an existing issue with relevant information, using reactions rather than +1 comments

Retain an independent source-local proposition: issue author — SHOULD comment or react on an existing issue with relevant information, using reactions rather than +1 comments. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "810b425907a9cfd4c098e0cd25d772d3f0d7c9e318e8bf4207ac0acbd1138907", "end_line": 21, "path": "CONTRIBUTING.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "536b92b4eb70e684f258a14d9c33108bce8a2c8ad18ac0eab0868372ac758198", "start_line": 21}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "comment or react", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "on an existing issue with relevant information, using reactions rather than +1 comments", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Issue already exists"], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CONTRIBUTING.md"], "subject": "issue author"}}`

Relationships: `[]`

## semantic-proposition:cecd429bed4c70abd2c4f8e3235dcc14e046475998cdaefa3c67e444d5a0fffc

SPECIALIZED: SHOULD repository owner — summarize description, conditional installation, repository structure, usage, contribution/governance, conduct and license in README

README adaptation is specialized by required presentation topics and installation only when needed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 128, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "c2340f9f63c70674753bca3e40c930881ed56dd2c8aacc881dab813332a67e96", "start_line": 120}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "summarize", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "description, conditional installation, repository structure, usage, contribution/governance, conduct and license in README", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Installation only if required"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:6753fb346daf0e594532c7da908c9fb04a9310ef5a2493e2188f42c83a0713ac"], "rationale": "README adaptation is specialized by required presentation topics and installation only when needed."}]`

## semantic-proposition:d0269d064c4b97dac959524e29c63481024cf5c38751376fca42c899e37419e0

SPECIALIZED: SHOULD repository owner — adapt GOVERNANCE.md covering decision authority, timing and leadership admission

Governance adaptation preserves must-category wording and should-level details for authority, timing and admission.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 64, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "a3997653763864fd8c4445f3266dce9942c6d75a6a79d47c0c35a41d0e42b870", "start_line": 60}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "adapt", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "GOVERNANCE.md covering decision authority, timing and leadership admission", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:ce11547b84128cda63b864547e9023f5cb126728c015db99aaa6cfa08ff7ece5"], "rationale": "Governance adaptation preserves must-category wording and should-level details for authority, timing and admission."}]`

## semantic-proposition:d0ad8ce7c2bb71c33fd3619189222f11f52957614f5fc10f51fa5ef8b7bd8727

SPECIALIZED: SHOULD issue author — describe considered alternatives

Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "a1f028fd0f7eee898fbbd8d070315a6a272d9aea10f65b92dac8d533c5638c17", "end_line": 17, "path": ".github/ISSUE_TEMPLATE/proposal.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "cd8ebab5177fda913ef175fc84d90c9db4d686fc4253cb39490642395a3347ec", "start_line": 15}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "considered alternatives", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Alternatives exist"], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", ".github/ISSUE_TEMPLATE/proposal.md"], "subject": "issue author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0809500a491391df7e3d569177a86b8f5f5642aaa37a2e7b78bbf912d1913512", "semantic-proposition:e0a92102e1b4669d3d664ac37b86901a6e46b18f874fcc41c2f1a140035e3bea"], "rationale": "Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing."}]`

## semantic-proposition:d0e450d8fbabc1b7a133cdfd63b1d16a7f8c068398b855632f2e2ae3abd7aef3

DISTINCT: MUST pull-request author — perform self-review

Retain an independent source-local proposition: pull-request author — MUST perform self-review. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 32, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "efa4f277f602bf8cae50289be4394edfaac5a651cdf523c312a896d73eed15c2", "start_line": 32}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "perform", "consequences": [], "exceptions": [], "modality": "MUST", "object": "self-review", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:d265eab3ef6db45e91ef99e5d39138befed6500612f194066ede97023fa3e776

SPECIALIZED: SHOULD participants — show empathy and kindness

Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 26, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "7b3f3a657791bfa3fe208f1d3d64d0065362a575f293cb136b106260921909bf", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "show", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "empathy and kindness", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:081f31a8ff74dff830d11cca35a51038b92f2fd93832577a55eb755f0a666f01", "semantic-proposition:cc357b938c1a1da5f121260ffced3a6d5f50a118c4c8ed8935510dc496be1767", "semantic-proposition:eecd5c8892f0e437dc966170b5bd5618d79ab99c1b90b4f7ae87a5340c5685b9"], "rationale": "Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate."}]`

## semantic-proposition:d28b5849c24430e7d48f0c2ebc38fee2ba6ae3ce44bc86d3d659baa31c3417b7

DISTINCT: MUST pull-request author — update corresponding documentation

Retain an independent source-local proposition: pull-request author — MUST update corresponding documentation. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "215fecebc0056f8126c91a008934166f518bbe1526e3d5203531b6274299d675", "end_line": 34, "path": ".github/pull_request_template.md", "repository": "atapas/model-repo", "span_sha256": "08a0b37c33c7242de4ac6b8ffbd76b4fdaadba83ea9a09d20632757017e13053", "start_line": 34}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "update", "consequences": [], "exceptions": [], "modality": "MUST", "object": "corresponding documentation", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source template attestation; not an observed result"], "scope": ["atapas/model-repo", ".github/pull_request_template.md"], "subject": "pull-request author"}}`

Relationships: `[]`

## semantic-proposition:d2cfe22abc1107856833c93230be148450c20fd91e0fe43d3f60999bf3030d1b

DISTINCT: SHOULD reporter — add other relevant context

Retain an independent source-local proposition: reporter — SHOULD add other relevant context. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "0c8d64f29fb4536513653bf8c97da30f3340e2041b91c8952db1515d6b23a7b3", "end_line": 38, "path": ".github/ISSUE_TEMPLATE/bug_report.md", "repository": "atapas/model-repo", "span_sha256": "7b9206ea73cdf921b47bd7d3abc0071d36b08a9e06787d3dabaa3e89028efb6b", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "add", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "other relevant context", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/bug_report.md"], "subject": "reporter"}}`

Relationships: `[]`

## semantic-proposition:d3da8be789b90874747957fb43bf9ebb672e921e9117edd8554c2e40f67d3140

REFERENTIAL: MAY template user — create then adapt a repository using the template button and copied files

Retain source-local example/reference: template user — MAY create then adapt a repository using the template button and copied files. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "e275e420804025a8fda3625a7a296a3baa5a0f179ab8239c7978798b0052b48f", "end_line": 14, "path": "README.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "ee0e345066f4da48fabb33facd2eb4e8773f2b90c918538980878676d108c5f8", "start_line": 11}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "create then adapt", "consequences": [], "exceptions": [], "modality": "MAY", "object": "a repository using the template button and copied files", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "README.md"], "subject": "template user"}}`

Relationships: `[]`

## semantic-proposition:d6461f6d28d14fab9e3cf56326ea0a252689e6f157f2212dc841ef541cea6b24

SPECIALIZED: SHOULD participants — prioritize community interests

Community-interest guidance differs in explicit comparison with individual interests; retain that difference.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "prioritize", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "community interests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:1b98edd4dbf95e557c9fdffbeeb8751189d29120d763c9c59aabaf1b558bd620", "semantic-proposition:986b7c607dfc2d963628001dacbdc340f21ae09301712d9daf29bdec69e64ca8"], "rationale": "Community-interest guidance differs in explicit comparison with individual interests; retain that difference."}]`

## semantic-proposition:d79887bdcba6f9d19709b6679ff89ab38202f2f283ea6bb24baab538668b9c4a

DISTINCT: PROHIBITED participants — avoid violent threats or language directed at another person

Retain an independent source-local proposition: participants — PROHIBITED avoid violent threats or language directed at another person. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "violent threats or language directed at another person", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[]`

## semantic-proposition:d80b422b070fae3a3d33db1a231d601a72127da81ddfe4039d48d88d1344c466

SPECIALIZED: PROHIBITED project participants — avoid categorical unbounded milestones

Bounded dated milestones complement prohibition of categorical unbounded milestones; labels provide the alternative category mechanism.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 68, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "18ed90a4677c5cd1aeaabe7332d5602cef6c70f43db14a9c0991a6abd39b65f1", "start_line": 66}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "avoid", "consequences": ["Progress cannot complete and deadline semantics are unsuitable"], "exceptions": [], "modality": "PROHIBITED", "object": "categorical unbounded milestones", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:38d9e9255e66084a702b77a061db0f2cf1600474af1d21229ab4629f81ed262d"], "rationale": "Bounded dated milestones complement prohibition of categorical unbounded milestones; labels provide the alternative category mechanism."}]`

## semantic-proposition:d9cbbf723ffaf200818c8fb8c7a1b1a647b63bdba9b3c931c657b45b72d79ecb

SPECIALIZED: MUST repository owner — edit or adapt code of conduct

Conduct-file adaptation combines a must-category entry with concrete should guidance and reporting-contact customization.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 13, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "170aa5f3a2acc82d1adaff04cb288acf2994cc495cb79dbdb2019b654f079bfb", "start_line": 13}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "edit or adapt", "consequences": [], "exceptions": [], "modality": "MUST", "object": "code of conduct", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source musts category; local adoption remains separate"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2f3680e51c628e278812960d1e27bb6c6f03c90977370b5be7335db7d5b281e2"], "rationale": "Conduct-file adaptation combines a must-category entry with concrete should guidance and reporting-contact customization."}]`

## semantic-proposition:da0476f1e8c3aa0f2c2ccd2d8ef02f138b13736ac7ded86b662a5224343e95c4

SPECIALIZED: MAY project participants — allow primary and feature branches and occasional child branches for proposed review improvements

Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 13, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "57aca24220a6454249cea6f64650c000a7ca35898d90b33f10d26bba944e1471", "start_line": 11}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "allow", "consequences": [], "exceptions": [], "modality": "MAY", "object": "primary and feature branches and occasional child branches for proposed review improvements", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:6c3ef4d4f2a71d47ede077ddf887c4424efe90135956cda2983328be7a4c6502", "semantic-proposition:7c3403c3ff73b05121b6b222393c2aad0ac19a89943e21ee95c29dcd1f423dce"], "rationale": "Branch topology allows primary/features and an occasional child for review improvement, while limiting deeper ancestry; prerequisite handling retains its alternatives."}]`

## semantic-proposition:db206dfb22e1be9c7676aed142a3109fd9cc5349e4c63cf69b6bea4acd69d6ce

DISTINCT: SHOULD requester — add other context or screenshots

Retain an independent source-local proposition: requester — SHOULD add other context or screenshots. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "1f48c52f209a971b8e7eae4120144d28fcf8ee38a7778a7b4d8cf1ab356617d2", "end_line": 20, "path": ".github/ISSUE_TEMPLATE/feature_request.md", "repository": "atapas/model-repo", "span_sha256": "5c56004f906c5ae7a2a922578afba2a3fb723073501334131569fb9cb94b35d0", "start_line": 19}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "add", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "other context or screenshots", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/feature_request.md"], "subject": "requester"}}`

Relationships: `[]`

## semantic-proposition:dc9bfc2336a131cde0e7e983980976538713a7f0b78370c4ed1786ca69b7ec16

SPECIALIZED: MUST participants — apply conduct rules within community spaces and official public representation

Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 57, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "da2c36d04f073d150af33f358ccf8875935b431d05bee02d97e48d5b91a2bd0c", "start_line": 53}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "apply", "consequences": [], "exceptions": [], "modality": "MUST", "object": "conduct rules within community spaces and official public representation", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Examples: official email, social account and appointed events"], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:3083e421dbf320a411b5f14de2b54f10d74c2ea5348218fc7f13e44d958f7073", "semantic-proposition:93e50bd54ea4deab1e887ca031aeb14c374e48bb3d69c4776518019cce2c062e"], "rationale": "Conduct applicability includes project/community spaces and official representation; retain differing actor and public-representation examples."}]`

## semantic-proposition:dd05a0a6aead7e7884ee411c22f0efc6e607521342f04d82b6d63366519020be

SPECIALIZED: SHOULD template author — request citation using the supplied CFF 1.2.0 software and preferred article metadata

Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b61bac9eed8e8b770fbf76c91faf923c20fee14d7c6d00f474d8ff78e56c56fb", "end_line": 32, "path": "CITATION.cff", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "b61bac9eed8e8b770fbf76c91faf923c20fee14d7c6d00f474d8ff78e56c56fb", "start_line": 1}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "request", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "citation using the supplied CFF 1.2.0 software and preferred article metadata", "parameters": ["cff-version=1.2.0", "preferred-citation.type=article", "Example software version 1.0.0", "Example release 2021-11-16", "Example article year 2022"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Names and ORCIDs are placeholders; title, version, DOI, date, URL, journal and pagination are example data, not consumer facts"], "scope": ["jlcanovas/gh-best-practices-template", "CITATION.cff"], "subject": "template author"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:55738ad32c5d3fae226f67367b387fe7214f853b30f61256a92999125295b5cd", "semantic-proposition:89247a9d44e58f1a777d247459ea38211fceb282a42a25a31b64fd0b56e0c164"], "rationale": "Optional paper-citation consideration and adapt-or-remove guidance are specialized by CFF example metadata; example authors, identifiers and versions are not consumer facts."}]`

## semantic-proposition:df1d8a163fd5dbbc8effc2e935db58de96ff8ff60dab765456105fcd8548fd7d

SPECIALIZED: MUST maintainers — block merge while a maintainer opposes the pull request

Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "de034656a1636b3fdfb9e4eeb5f68db09c41606da996b6fef98b43152ee67b5e", "end_line": 43, "path": "GOVERNANCE.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "9c09bc935c926af5e082a6880ecbe6b3e4f945c5d885cffdcf7214863ba3e755", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "block", "consequences": [], "exceptions": ["Opposition may be removed after discussion or changes"], "modality": "MUST", "object": "merge while a maintainer opposes the pull request", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "GOVERNANCE.md"], "subject": "maintainers"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:568ac038cf9a6fae9062eebd3e64a96dee4ed560f7f0398b77a9c0d64a4f4b76", "semantic-proposition:a99b77a40359d468b19859c0df0259a4f5b3c9bfc1cab066d3305ea33b05c089", "semantic-proposition:b42003b15c2e3ff4d051bf901e5253dd039f6747c1ed219843519c67705be961"], "rationale": "Merge authority differs: author integration preference, two other developer sign-offs with delegation, two maintainer approvals with >14-day one-approval exception, and an opposition veto. These are scoped policies, not a single universal threshold."}]`

## semantic-proposition:df3f5d7e8f7bc1cba290bb8cda18896d39a797c42d3be8fe1477f37c6b4cc07f

SPECIALIZED: SHOULD participants — respect different viewpoints and experiences

Respect for differing views and experiences overlaps without identical source scope or wording.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "respect", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "different viewpoints and experiences", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:719b64fb50665fb2ac9a31c32a8a99def7fadd770c3f418b12429af5c0fc0930", "semantic-proposition:bcae8bfe4b2dfaf08cb9b284c7e526530b19aa247f98380ecb17a352b4e47af5"], "rationale": "Respect for differing views and experiences overlaps without identical source scope or wording."}]`

## semantic-proposition:e0a92102e1b4669d3d664ac37b86901a6e46b18f874fcc41c2f1a140035e3bea

SPECIALIZED: SHOULD requester — describe alternative solutions or features considered

Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "1f48c52f209a971b8e7eae4120144d28fcf8ee38a7778a7b4d8cf1ab356617d2", "end_line": 17, "path": ".github/ISSUE_TEMPLATE/feature_request.md", "repository": "atapas/model-repo", "span_sha256": "ecb519885028b5144d3cca4d1a2f6e37cbe5bfdbb317f3b6334a04f132b75459", "start_line": 16}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "describe", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "alternative solutions or features considered", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", ".github/ISSUE_TEMPLATE/feature_request.md"], "subject": "requester"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0809500a491391df7e3d569177a86b8f5f5642aaa37a2e7b78bbf912d1913512", "semantic-proposition:d0ad8ce7c2bb71c33fd3619189222f11f52957614f5fc10f51fa5ef8b7bd8727"], "rationale": "Alternatives are requested in PR, proposal and feature prompts; the jlcanovas prompts condition them on alternatives existing."}]`

## semantic-proposition:e365a85130cfb6e48b9ac62e1a6f3c703b26dc1fd2a62e5cf41084093d8c0e97

CONFLICTING: SHOULD repository owner — choose a suitable project license after exploring alternatives

README declares CC BY 4.0 while guidelines describe CC-BY-SA as the starting license. Retain the documented source identity inconsistency; LICENSE.md remains B0 reference-only evidence, and no publication permission is decided.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 92, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "6146af82aa56c593d759e53cad01b60051b1a1d6c0e41774171e58835f27d63e", "start_line": 88}]`

Preserved AST/applicability: `{"ambiguities": ["Conflicts with README and LICENSE.md Attribution 4.0 identity; preserve for C0"], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "choose", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "a suitable project license after exploring alternatives", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source describes CC-BY-SA as starting point"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "CONFLICTING", "counterpart_ids": ["semantic-proposition:7c1b58c56afdbad1aadb30c7cf293a4eeaa1d112f1c95cafb486f328015b0421"], "rationale": "README declares CC BY 4.0 while guidelines describe CC-BY-SA as the starting license. Retain the documented source identity inconsistency; LICENSE.md remains B0 reference-only evidence, and no publication permission is decided."}]`

## semantic-proposition:e5468438ce56320a0cd9535fef610ea89cfc11206f860dcc904922d2e86137bd

DISTINCT: PROHIBITED participants — avoid discriminatory jokes or language

Retain an independent source-local proposition: participants — PROHIBITED avoid discriminatory jokes or language. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "discriminatory jokes or language", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[]`

## semantic-proposition:e953052abf0e062502a47740ddae2690af333729bf85be6d1e8dba5aa0723a8d

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate last matching pattern taking precedence over global owners for JavaScript changes

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate last matching pattern taking precedence over global owners for JavaScript changes. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 17, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "1722f64815200bbc94c13348c99507a90a4a8b33681f8c7be552e8e8279c8c0c", "start_line": 13}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "last matching pattern taking precedence over global owners for JavaScript changes", "parameters": ["*.js", "@js-owner"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:ead9cd2f5bcab669c1da8572ba6e368c1cd9e9a5ac5595e7211d6a59893553c2

SPECIALIZED: SHOULD project participants — consider splitting issues larger than a single pull request

Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 49, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "ee4cc8571265df19ad8e9ae91ba988a359e7426f757f5ea780a15fe8a11d56ea", "start_line": 47}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "consider splitting", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "issues larger than a single pull request", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Advance issues enable feedback, retain intent and track later attempts"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2dafbdaad5c7217c70e7107a6cee140f4f080f15570feec01f8c3b023d3ec431", "semantic-proposition:393eec09bfe975ee68f3c73e9762ecae6621d27c9159c6f525e3c52d97f8fb33", "semantic-proposition:cb6154618defbce295e39c7f0e69a8b8dcd9c2ca76f4a606fed7a7b19fa1044b"], "rationale": "Single-purpose work and bounded review overlap; preserve large-idea exception, approximate few-day advice and reproduction information where possible."}]`

## semantic-proposition:ed744ad262eddb97378e9165e803af16d1a4fc504506a403386e4a79bf6ba234

SPECIALIZED: MUST community leaders — moderate nonconforming contributions and communicate reasons when appropriate

Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "e151c0dedf5e9d7ed354fc2b02e4e65289dfffe3397c2851fcae90254a95da4f", "end_line": 49, "path": "CODE_OF_CONDUCT.md", "repository": "atapas/model-repo", "span_sha256": "8ce250ea4e0d82921b06445448e99e414b7b1f2b17c113616d1ce0449f0b1372", "start_line": 46}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "moderate", "consequences": [], "exceptions": [], "modality": "MUST", "object": "nonconforming contributions and communicate reasons when appropriate", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CODE_OF_CONDUCT.md"], "subject": "community leaders"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:2683ea08aa8b36fe7f5cf5eb1d229a1438a32dca6b55acf134a22fa21d447b6c", "semantic-proposition:345e84c893c49793a31d2f591bb6b2a20804f3972a74cf19f58970c99206c79c", "semantic-proposition:781151aeb26f6aaa2e781d43b6b606ac81986061b1fce5dfbdb9fa6daf4f50d4", "semantic-proposition:a0e5d8e64b6a20002bca5ee9740019c707b8e840198914313ba4999108981d83"], "rationale": "Behavior clarification, corrective action, contribution removal and banning are related but have different actors, modalities and response duties; all are retained."}]`

## semantic-proposition:eecd5c8892f0e437dc966170b5bd5618d79ab99c1b90b4f7ae87a5340c5685b9

SPECIALIZED: SHOULD participants — show empathy for other participants

Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 39, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "9465024e8cb4b47befe0d034c8ece409641cf6fce1fa6e21527a12522c2258d1", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "show", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "empathy for other participants", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:081f31a8ff74dff830d11cca35a51038b92f2fd93832577a55eb755f0a666f01", "semantic-proposition:cc357b938c1a1da5f121260ffced3a6d5f50a118c4c8ed8935510dc496be1767", "semantic-proposition:d265eab3ef6db45e91ef99e5d39138befed6500612f194066ede97023fa3e776"], "rationale": "Empathy is shared conduct intent, with kindness and participant/community wording retained; short, long and contribution versions remain separate."}]`

## semantic-proposition:f0d4e7e90285f95e52ceb9cde4023aef53b1481101730bef23e788f2eac971f1

SPECIALIZED: SHOULD participants — give and accept constructive feedback gracefully

Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 33, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "757bfd5273cefb59917a86fb0b320d907e93e6e917e0f13e3a9f93af8f483334", "start_line": 28}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "give and accept", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "constructive feedback gracefully", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:886502be25fba36356e8b0f1b1d83bb4140778b1f3fc9b8ee0234f9c7aca40cd", "semantic-proposition:a4b3551dfd79150eb9d0189f069800629e6983ee36ffe1c5f9e46937e5075773"], "rationale": "Constructive feedback covers giving, accepting and graceful criticism; retain the distinct actions rather than flattening them."}]`

## semantic-proposition:f2f1083e08f9af5c8af382be6bf92f6fe94b8dafbce9eab53ced3124106ca35a

DISTINCT: SHOULD project participants — checkpoint work through frequent commits and pushes

Retain an independent source-local proposition: project participants — SHOULD checkpoint work through frequent commits and pushes. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 100, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "5133590451fb2163ea1b543b35f68dbdd456fc93eeaa51380f7462e470a67473", "start_line": 96}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "checkpoint", "consequences": ["Remote checkpoints aid collaboration, loss recovery and reversal"], "exceptions": [], "modality": "SHOULD", "object": "work through frequent commits and pushes", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Illustrations: before a coffee break after half an hour or an hour; after finishing part of a feature", "Acceptance and refinement belong to pull requests, not perfect commits"], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[]`

## semantic-proposition:f2f5fe250f654079981c8a39ead77d76a1e2f1461b86ec4c79a76c2e03c5314a

SPECIALIZED: SHOULD repository owner — consider code-owner identification and settings

Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "b3d8e64d45b94dff9323f45fed65f8bff2dff41c478c3f2be6d43e262d3a6c3b", "end_line": 20, "path": "guidelines.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "8ae68fc82a53f064a10f2bfad585b476d13a0020312dc18e92d53d22eee4c8a6", "start_line": 20}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement", "Guidelines assume repository admin or owner permissions"], "semantic_ast": {"action": "consider", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "code-owner identification and settings", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Source shoulds category"], "scope": ["jlcanovas/gh-best-practices-template", "guidelines.md"], "subject": "repository owner"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:53888d0999bc168e78b94ad9f1b47fe98003e10db70a3b13723ed373f4071e50", "semantic-proposition:8e17ff56a50fb9d4449e7fa47ac598e02458af76c13f30aef51d1168d68519ed"], "rationale": "Considering ownership is specialized by definition/checking against platform docs and explicit team write access. Platform truth awaits C4; no settings are changed."}]`

## semantic-proposition:f34830665030f3e50b30d79b205709f05f0c160e030a18a0a95e09707c4a7ac9

REFERENTIAL: DESCRIPTIVE CODEOWNERS example — illustrate docs/* matching immediate children but not deeper nesting

Retain source-local example/reference: CODEOWNERS example — DESCRIPTIVE illustrate docs/* matching immediate children but not deeper nesting. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "5f81d760176abcc6875aaae4a02019d868f1b2e3059b11481c4f0327a2c77225", "end_line": 38, "path": "CODEOWNERS", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "978b6666862421b29b7bdebb69093c565031a74c49ff729779c0d2d482af9348", "start_line": 35}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "illustrate", "consequences": [], "exceptions": [], "modality": "DESCRIPTIVE", "object": "docs/* matching immediate children but not deeper nesting", "parameters": ["docs/*", "docs@example.com"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODEOWNERS"], "subject": "CODEOWNERS example"}}`

Relationships: `[]`

## semantic-proposition:f3ff9668a240b8a5a2c507ae7331dddcf00460aac4a0a5f1caeee2b1868e7dfa

SPECIALIZED: SHOULD project participants — rewrite poor automatically generated commit messages using squash or rebase

Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate.

Source locators: `[{"commit": "801411757531a8880cb315148160fde3079d7227", "content_sha256": "8e3b37ceccf44de1261065078c301dc95e541f990e8740092d6270af32c03e67", "end_line": 106, "path": "README.md", "repository": "tmcw/github-best-practices", "span_sha256": "2a3587fbedca4651809e1bcec9453f28e3bf78959b915869ea368d4ac105f1c4", "start_line": 106}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Long-lived continuously deployed product such as a web application or API", "Author opinion; advice is not platform authority"], "semantic_ast": {"action": "rewrite", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "poor automatically generated commit messages using squash or rebase", "parameters": [], "polarity": "POSITIVE", "preconditions": ["Tools produce unhelpful commit history"], "qualifiers": [], "scope": ["tmcw/github-best-practices", "README.md"], "subject": "project participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:0e8541d6dcccc73b218d9fa055348d33755adc6b153390116a26f2732f394bf5", "semantic-proposition:2c44a979b5cbf683c1aa0624ad537d0bec99c3afb78cf82cf289104c693b1d1e", "semantic-proposition:4be68e7e45e38d45af75c12b417ae771c8560f44988e9b235ceb99b9a056d8f3"], "rationale": "Meaningful commit history and PR explanations coexist with discretionary integration strategy; rewriting poor generated messages is conditional, not a universal squash mandate."}]`

## semantic-proposition:f4dd7a4697ec6b6981ccdc0d2dcae6422b071c2ebae5fa45f11066cbb9363f18

SPECIALIZED: PROHIBITED participants — avoid trolling, derogatory comments and personal or political attacks

Trolling and personal/political attacks overlap; insulting versus derogatory language is retained.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "33cfd16c320b8999276ffbf672cbe7f5c4c73d33eebce4ce09c89940b9a473aa", "end_line": 44, "path": "CODE_OF_CONDUCT.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "68938890c3824c2ba84adb3ec9a101d446a955f3ffebded9d15d5b858421026a", "start_line": 37}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "trolling, derogatory comments and personal or political attacks", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["jlcanovas/gh-best-practices-template", "CODE_OF_CONDUCT.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:7fd5b777fe54d09974108575a3f5300c608adfe87632b10111c7a90e11722cfb", "semantic-proposition:b3ee3b0c477a0685b9b9483f2d091818e0f67a1ce829b7ab85563e113123ec73"], "rationale": "Trolling and personal/political attacks overlap; insulting versus derogatory language is retained."}]`

## semantic-proposition:f6f455e0e3fc3292ffc6dbc8175bee299c35404189d31e8ca24bf086869ac315

REFERENTIAL: MAY README — present and invite unordered placeholder upcoming features and new feature requests

Retain source-local example/reference: README — MAY present and invite unordered placeholder upcoming features and new feature requests. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "cfd165c08d9ef794e79fee309f841657ee2ed01daec8af3637940d5e201845c3", "end_line": 121, "path": "README.md", "repository": "atapas/model-repo", "span_sha256": "4076e5a57b68d18908ad80a176f969c75d2de70207dab2b58ad33f5b1d09c182", "start_line": 107}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "present and invite", "consequences": [], "exceptions": [], "modality": "MAY", "object": "unordered placeholder upcoming features and new feature requests", "parameters": [], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["Feature Request 1 through 11 are placeholders"], "scope": ["atapas/model-repo", "README.md"], "subject": "README"}}`

Relationships: `[]`

## semantic-proposition:fc60ed6cfd4aba5ef66b267df97b0d58650bb9f5e97f1c9369749f2973e37de7

DISTINCT: SHOULD maintainer — document security-supported versions

Retain an independent source-local proposition: maintainer — SHOULD document security-supported versions. No equivalent or superseding proposition is asserted in this batch.

Source locators: `[{"commit": "bf13cd2c7992876da01de065084e8af3e9c7db06", "content_sha256": "ba9643955bfcb04524a6fe5a8c2929b54abc2e67bb3480ce806e742d506e4dc9", "end_line": 13, "path": "SECURITY.md", "repository": "jlcanovas/gh-best-practices-template", "span_sha256": "31671754dfa86cb945b272584aa5fa6f393cbde84c69e8ee290fb4dd0727a29f", "start_line": 5}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Adaptable community template; local project scope, not GES policy", "Placeholders require owner-specific replacement"], "semantic_ast": {"action": "document", "consequences": [], "exceptions": [], "modality": "SHOULD", "object": "security-supported versions", "parameters": ["Examples: supported 5.1.x and 4.0.x; unsupported 5.0.x and <4.0"], "polarity": "POSITIVE", "preconditions": [], "qualifiers": ["No real supported version promise is inferred"], "scope": ["jlcanovas/gh-best-practices-template", "SECURITY.md"], "subject": "maintainer"}}`

Relationships: `[]`

## semantic-proposition:fdfbd6a953c7f288eaf60f400d3baeb2d3c2759b0f3542e3f3a85520306d49f3

SPECIALIZED: PROHIBITED participants — avoid other professionally inappropriate conduct

Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes.

Source locators: `[{"commit": "9aa52517830a0e10043116ff768af8fabeeb4347", "content_sha256": "7be44aa465129dbaef9ff324a07426e097c166ed56fb955d942052a36f2ea687", "end_line": 50, "path": "CONTRIBUTING.md", "repository": "atapas/model-repo", "span_sha256": "45749c5f93e83d820404b02ccb9d3e0b4be93d88fd8e73316c88b4a8cadd2c3e", "start_line": 43}]`

Preserved AST/applicability: `{"ambiguities": [], "applicability": ["Model repository community example; only local source scope", "Presentation/stack/identity examples are not consumer facts"], "semantic_ast": {"action": "avoid", "consequences": [], "exceptions": [], "modality": "PROHIBITED", "object": "other professionally inappropriate conduct", "parameters": [], "polarity": "NEGATIVE", "preconditions": [], "qualifiers": [], "scope": ["atapas/model-repo", "CONTRIBUTING.md"], "subject": "participants"}}`

Relationships: `[{"classification": "SPECIALIZED", "counterpart_ids": ["semantic-proposition:44431fcdd4e33b3ed3478a64653fc2642036df49c0f015bdc9b8b15265043377", "semantic-proposition:9a745252ccc68d81c02ebb8c6053a2df2c57f2b9187e560eaa462dbde6aa05c8"], "rationale": "Professionally inappropriate conduct is a shared catch-all within distinct local conduct scopes."}]`
