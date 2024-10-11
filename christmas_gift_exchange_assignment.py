import collections
import itertools
import json
import random
import typing


class Member(typing.TypedDict):
    '''
    Member クラス

    Parameters
    ----------
    no:
        No.
    name:
        名前
    execlusions:
        除外する No. のリスト 
    '''
    no: int
    name: str
    exclusions: list[int]


type Pair = tuple[Member, Member]
'''
Pair 型
'''


def is_valid_pair(pair: Pair) -> bool:
    '''
    ペアが正しいか検証します。
    相手が除外の対象になっていない場合は True を、除外の対象の場合は False を返します。

    Parameters
    ----------
    pair:
        ペア（メンバーのタプル）

    Returns
    -------
    ペアが正しいか否か
    '''
    member_from, member_to = pair
    return member_to['no'] not in member_from['exclusions']


def is_valid_all_pairs(pairs: list[Pair]) -> bool:
    '''
    すべてのペアが正しいか検証します。

    Parameters
    ----------
    pairs:
        ペアのリスト

    Returns
    -------
    すべてのペアが正しいか否か
    '''
    return all(map(is_valid_pair, pairs))


def create_pairs(members_from: list[Member]) -> list[Pair]:
    '''
    メンバーのリストからペアのリストを作成します。

    Parameters
    ----------
    members_from:
        メンバーのリスト

    Returns
    -------
    ペアのリスト
    '''
    members_to = collections.deque(members_from)
    members_to.rotate(-1)
    return list(zip(members_from, members_to))


def circular_permutations[T](elements: list[T]) -> typing.Generator[list[T], typing.Any, None]:
    '''
    円順列を作成します。

    Parameters
    ----------
    elements:
        円順列の要素のリスト

    Returns
    -------
    円順列のイテレーター
    '''
    if len(elements) <= 1:
        yield elements
        return

    for permutation in itertools.permutations(elements[1:]):
        yield list((elements[0],) + permutation)


def execute(members: list[Member]) -> None:
    '''
    処理を実行します。

    Raises
    ------
    Exception
        すべてのパターンを検証したが、ペアが生成できない場合に送出する例外
    '''
    for pattern in circular_permutations(members):
        pairs: list[tuple[Member, Member]] = create_pairs(pattern)
        if is_valid_all_pairs(list(pairs)):
            for pair_from, pair_to in pairs:
                print(f'{pair_from['name']} → {pair_to['name']}')
            return

    raise Exception('すべてのパターンを検証しましたが、ペアを生成できません。')


def main() -> None:
    '''
    エントリーポイント
    '''
    with open('./members.json') as file:
        members: list[Member] = json.load(file)
    execute(random.sample(members, len(members)))


if __name__ == '__main__':
    main()
