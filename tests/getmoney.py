def test(affluent):
    assert affluent("get money") == "get paid", "get money must get paid"
    assert affluent("get paid") == None, "other inputs must not get paid"
