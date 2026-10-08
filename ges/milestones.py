"""Project accepted scope into milestones without changing legacy evidence gates.

These are calculated evidence states, not owner acceptance or the repository's
governed definition of "Verified". Recovery supplies validator results directly;
there is no manifest or boolean override for closing a milestone.
"""
from __future__ import annotations

from .core import digest


GATE_PREREQUISITES = {
    'exhaustive_artifact_accounting': (
        'pinned_git_trees_match', 'review_receipts_valid',
        'independent_omission_audit'),
    'published_content_assurance': (
        'all_bodies_durably_acquired', 'all_source_paths_reconciled',
        'version_include_and_render_assurance'),
    'semantic_extraction': (
        'atomic_claim_fidelity_audit',
        'independent_source_to_claim_omission_audit',
        'claim_document_provenance_validated'),
    'consolidation': (
        'exact_claim_mapping_and_conflict_review',
        'unstructured_claim_denominator_certified',
        'all_structured_occurrences_reconciled'),
    'generalization': ('profiles_parameters_and_templates_reviewed',),
    'operational_completeness': (
        'accepted_policy_exists', 'all_required_bindings_verified'),
    'native_enforcement': (
        'approved_target_inventory',
        'positive_negative_bypass_and_recovery_evidence'),
    'rights_and_publication': (
        'per_file_rights_acceptance', 'authorized_distribution_decision'),
    'estate_rollout': (
        'approved_estate_inventory',
        'fresh_effective_enforcement_and_drift_evidence'),
}

MILESTONE_GATES = {
    'six_source_synthesis': tuple(GATE_PREREQUISITES)[:6],
    'native_pilot_acceptance': ('native_enforcement',),
    'estate_rollout': ('estate_rollout',),
}
RELEASE_MILESTONES = (
    'six_source_synthesis', 'public_release_clearance',
    'native_pilot_acceptance',
)
PUBLICATION_CONDITIONS = (
    'complete_output_inventory', 'use_register_complete',
    'exact_use_clearance', 'authorized_distribution_decision',
)


def evaluate_gate(name: str, completed: int, denominator: int | None,
                  condition: str, prerequisites: dict[str, bool | None]) -> dict:
    """Separate observed incompleteness from absent certification evidence.

    This is the legacy evaluator, retained without changing its contract.
    """
    if type(completed) is not int or completed < 0:
        raise ValueError('Invalid completed count')
    if denominator is not None and (type(denominator) is not int or denominator < completed):
        raise ValueError('Invalid or reduced denominator')
    if (not prerequisites or 'coverage_complete' in prerequisites or
            any(v is not None and type(v) is not bool for v in prerequisites.values())):
        raise ValueError('Gate prerequisites must be explicit boolean/unknown observations')
    coverage = None if denominator is None or denominator == 0 else completed == denominator
    observations = {'coverage_complete': coverage, **prerequisites}
    failed = [key for key, value in observations.items() if value is False]
    unknown = [key for key, value in observations.items() if value is None]
    closed = not failed and not unknown
    return {'gate': name, 'status': 'CLOSED' if closed else 'OPEN',
            'evaluation': 'PROVEN' if closed else ('INCOMPLETE' if failed else 'UNVERIFIED'),
            'completed': completed, 'denominator': denominator,
            'remaining': denominator-completed if denominator is not None else None,
            'closure_condition': condition, 'conditions': observations,
            'incomplete_conditions': failed, 'unverified_conditions': unknown,
            'evidence': 'evidence/recovery-status.json'}


def _validated_gates(gates: list[dict]) -> dict[str, dict]:
    if not isinstance(gates, list):
        raise ValueError('Milestone accounting requires the complete legacy gate array')
    indexed = {}
    for gate in gates:
        if not isinstance(gate, dict) or not isinstance(gate.get('gate'), str):
            raise ValueError('Malformed legacy gate identity')
        name = gate['gate']
        if name not in GATE_PREREQUISITES:
            raise ValueError('Unknown legacy gate identity: ' + name)
        if name in indexed:
            raise ValueError('Duplicate legacy gate identity: ' + name)
        conditions = gate.get('conditions')
        expected_conditions = {'coverage_complete', *GATE_PREREQUISITES[name]}
        if not isinstance(conditions, dict) or set(conditions) != expected_conditions:
            raise ValueError('Missing or unknown conditions for legacy gate: ' + name)
        if any(value is not None and type(value) is not bool
               for value in conditions.values()):
            raise ValueError('Malformed legacy gate observations: ' + name)
        if not isinstance(gate.get('closure_condition'), str) or not gate['closure_condition'].strip():
            raise ValueError('Missing legacy gate closure condition: ' + name)
        if gate.get('remaining') is not None and type(gate['remaining']) is not int:
            raise ValueError('Invalid legacy gate remaining count: ' + name)
        expected = evaluate_gate(
            name, gate.get('completed'), gate.get('denominator'),
            gate['closure_condition'],
            {key: conditions[key] for key in GATE_PREREQUISITES[name]})
        # Canonical JSON distinguishes 0/False and rejects extra claimed fields.
        # Recalculation prevents a supplied status from overruling its evidence.
        if digest(gate) != digest(expected):
            raise ValueError('Inconsistent legacy gate evidence or claimed status: ' + name)
        indexed[name] = gate
    missing = set(GATE_PREREQUISITES) - set(indexed)
    if missing:
        raise ValueError('Missing legacy gate identities: ' + ', '.join(sorted(missing)))
    return indexed


def _assessment(conditions: dict[str, bool | None]) -> dict:
    incomplete = [key for key, value in conditions.items() if value is False]
    unverified = [key for key, value in conditions.items() if value is None]
    closed = not incomplete and not unverified
    return {
        'status': 'CLOSED' if closed else 'OPEN',
        'evaluation': 'PROVEN' if closed else ('INCOMPLETE' if incomplete else 'UNVERIFIED'),
        'conditions': conditions,
        'incomplete_conditions': incomplete,
        'unverified_conditions': unverified,
    }


def _publication_milestone(accounting: dict | None) -> dict:
    if accounting is None:
        conditions = {key: None for key in PUBLICATION_CONDITIONS}
        conditions['all_registered_uses_cleared'] = None
        conditions['ges_v0_2_release_scope'] = None
        completed, denominator, accounting_digest = 0, None, None
        release_scope = None
    else:
        # A result has to come from the separate exact-use validator, not the
        # legacy per-artifact rights adapter. Recheck its complete output contract.
        from .publication_use import validate_accounting_result
        validate_accounting_result(accounting)
        conditions = {key: accounting[key] for key in PUBLICATION_CONDITIONS}
        completed, denominator = accounting['completed'], accounting['denominator']
        coverage = None if denominator is None else completed == denominator
        if denominator == 0:
            # An empty register alone is not clearance. This exception requires
            # explicitly reviewed zero use across a nonempty exact output set.
            coverage = True if accounting['zero_use_clearance'] is True else None
        conditions['all_registered_uses_cleared'] = coverage
        release_scope = accounting['release_scope']
        conditions['ges_v0_2_release_scope'] = (
            None if release_scope is None else release_scope == 'GES_V0_2')
        accounting_digest = digest(accounting)
    return {
        **_assessment(conditions),
        'required_gates': [],
        'evidence_inputs': ['publication_use_accounting'],
        'accounting_digest': accounting_digest,
        'release_scope': release_scope,
        'completed': completed,
        'denominator': denominator,
        'legacy_gate_8_is_exact_use_clearance': False,
    }


def milestone_accounting(gates: list[dict], publication: dict | None = None) -> dict:
    """Derive four scoped milestones from complete, internally consistent evidence.

    Callers must obtain publication from ``publication_accounting`` in this
    process, not load a precomputed result as authority. Recovery's CLI accepts
    the underlying manifest, register, receipts and approved policy instead.
    """
    indexed = _validated_gates(gates)
    milestones = {}
    for name in (*RELEASE_MILESTONES, 'estate_rollout'):
        if name == 'public_release_clearance':
            milestones[name] = _publication_milestone(publication)
            continue
        required = MILESTONE_GATES[name]
        conditions = {
            gate_name + '.' + key: indexed[gate_name]['conditions'][key]
            for gate_name in required
            for key in ('coverage_complete', *GATE_PREREQUISITES[gate_name])
        }
        milestones[name] = {
            **_assessment(conditions),
            'required_gates': list(required),
            'evidence_inputs': ['gates.' + gate_name for gate_name in required],
        }
    release_conditions = {
        milestone + '.' + key: value
        for milestone in RELEASE_MILESTONES
        for key, value in milestones[milestone]['conditions'].items()
    }
    return {
        'schema': 'ges.completion-milestones.v1',
        'milestones': milestones,
        'ges_v0_2': {
            **_assessment(release_conditions),
            'required_milestones': list(RELEASE_MILESTONES),
            'estate_rollout_required': False,
        },
        'governance_acceptance_automatically_certified': False,
        'scope': 'Evidence projection only; owner acceptance, human review, merged-main '
                 'verification, and release authorization retain their governance requirements.',
    }
