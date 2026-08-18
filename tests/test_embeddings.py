import math

import pytest

from esm2_fitness.embeddings import pooled_mutant_minus_wt, validate_embedding_pair


def test_pooled_mutant_minus_wt_preserves_embedding_dimension():
    delta = pooled_mutant_minus_wt((1.0, 2.0, 3.0), (1.5, 1.0, 4.0))

    assert delta == pytest.approx((0.5, -1.0, 1.0))
    assert len(delta) == 3


def test_embedding_pair_requires_equal_nonempty_shape():
    with pytest.raises(ValueError, match="dimension"):
        validate_embedding_pair((1.0, 2.0), (1.0,))

    with pytest.raises(ValueError, match="empty"):
        validate_embedding_pair((), ())


def test_embedding_pair_rejects_non_finite_values():
    with pytest.raises(ValueError, match="finite"):
        validate_embedding_pair((1.0, math.nan), (1.0, 2.0))


def test_expected_dimension_is_checked_without_loading_a_model():
    validate_embedding_pair((1.0, 2.0, 3.0), (1.0, 2.0, 4.0), expected_dim=3)

    with pytest.raises(ValueError, match="expected dimension"):
        validate_embedding_pair((1.0, 2.0), (1.0, 2.0), expected_dim=3)
