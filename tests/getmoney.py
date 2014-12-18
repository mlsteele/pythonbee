def test(entry):
    fn = entry.affluent
    assert fn("get money") == "get paid", "get money must get paid"
    assert fn("get paid") == None, "other inputs must not get paid"
