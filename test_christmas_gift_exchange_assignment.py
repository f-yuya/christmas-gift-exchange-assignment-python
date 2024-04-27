import pytest

import christmas_gift_exchange_assignment

type Member = christmas_gift_exchange_assignment.Member


def test_is_valid_pair_正常なペアの場合() -> None:
    result: bool = christmas_gift_exchange_assignment.is_valid_pair((
        {'no': 1, 'name': 'No.1', 'exclusions': []},
        {'no': 2, 'name': 'No.2', 'exclusions': []}))
    assert result == True


def test_is_valid_pair_正常でないペアの場合() -> None:
    result: bool = christmas_gift_exchange_assignment.is_valid_pair((
        {'no': 1, 'name': 'No.1', 'exclusions': [2]},
        {'no': 2, 'name': 'No.2', 'exclusions': []}))
    assert result == False


def test_is_valid_all_pairs_正常なペアの場合() -> None:
    no1: Member = {'no': 1, 'name': 'No.1', 'exclusions': []}
    no2: Member = {'no': 2, 'name': 'No.2', 'exclusions': []}
    no3: Member = {'no': 3, 'name': 'No.3', 'exclusions': []}
    result: bool = christmas_gift_exchange_assignment.is_valid_all_pairs(
        [(no1, no2), (no2, no3), (no3, no1)])
    assert result == True


def test_is_valid_all_pairs_正常でないペアの場合() -> None:
    no1: Member = {'no': 1, 'name': 'No.1', 'exclusions': [2]}
    no2: Member = {'no': 2, 'name': 'No.2', 'exclusions': []}
    no3: Member = {'no': 3, 'name': 'No.3', 'exclusions': []}
    result: bool = christmas_gift_exchange_assignment.is_valid_all_pairs(
        [(no1, no2), (no2, no3), (no3, no1)])
    assert result == False


def test_create_pairs_正常系() -> None:
    no1: Member = {'no': 1, 'name': 'No.1', 'exclusions': []}
    no2: Member = {'no': 2, 'name': 'No.2', 'exclusions': []}
    no3: Member = {'no': 3, 'name': 'No.3', 'exclusions': []}
    result: list[tuple[Member, Member]] = \
        christmas_gift_exchange_assignment.create_pairs([no1, no2, no3])
    excepted: list[tuple[Member, Member]] = [
        (no1, no2), (no2, no3), (no3, no1)]
    assert result == excepted


def test_circular_permutations_正常系() -> None:
    result = list(
        christmas_gift_exchange_assignment.circular_permutations([1, 2, 3, 4]))
    expected: list[list[int]] = [
        [1, 2, 3, 4], [1, 2, 4, 3],
        [1, 3, 2, 4], [1, 3, 4, 2],
        [1, 4, 2, 3], [1, 4, 3, 2]]
    assert result == expected


def test_execute_正常系(capfd: pytest.CaptureFixture[str]) -> None:
    christmas_gift_exchange_assignment.execute([
        {'no': 1, 'name': 'No.1', 'exclusions': [2]},
        {'no': 2, 'name': 'No.2', 'exclusions': []},
        {'no': 3, 'name': 'No.3', 'exclusions': []}
    ])

    standard_output, _ = capfd.readouterr()
    assert standard_output == '''No.1 → No.3
No.3 → No.2
No.2 → No.1
'''


def test_execute_ペアが生成できない場合() -> None:
    with pytest.raises(Exception) as e:
        christmas_gift_exchange_assignment.execute([
            {'no': 1, 'name': 'No.1', 'exclusions': [2]},
            {'no': 2, 'name': 'No.2', 'exclusions': [1]},
            {'no': 3, 'name': 'No.3', 'exclusions': []}
        ])
    assert str(e.value) == 'すべてのパターンを検証しましたが、ペアを生成できません。'
