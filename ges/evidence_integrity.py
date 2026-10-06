"""Known invalidated evidence identities cannot regain authority via a policy."""

INVALIDATED_REVIEWERS = frozenset({'automated:semantic-review-v0.2.0'})


def invalidated_reviewer(identity):
    return isinstance(identity, str) and identity in INVALIDATED_REVIEWERS
