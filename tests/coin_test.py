from src.cmds.coin.service import coin


def test_is_coin_can_landed_on_edge():
    n = 0
    m = 100_000_000
    while n < m:
        r = coin()
        if r == "동전이 섰다!":
            assert True
            return
        n += 1

    assert False
