"""Known invalidated evidence identities cannot regain authority via a policy."""

INVALIDATED_REVIEWERS = frozenset({'automated:semantic-review-v0.2.0'})


def invalidated_reviewer(identity):
    return isinstance(identity, str) and identity in INVALIDATED_REVIEWERS


def validate_authority(document):
    """Reject invalidated identities in every declared authority role list."""
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(key, str) and key.startswith('authorized_'):
                identities = value if isinstance(value, list) else [value]
                if any(invalidated_reviewer(identity) for identity in identities):
                    raise ValueError('Invalidated heuristic identity in authority: ' + key)
            validate_authority(value)
    elif isinstance(document, list):
        for value in document:
            validate_authority(value)
    return document
