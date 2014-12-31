def assertEqual(a, b, msg=""):
    if a == b:
        return
    else:
        if msg:
            msg = " ({})".format(msg)
        raise AssertionError("{} != {}{}".format(repr(a), repr(b), msg))

def test(entry):
    fn = entry.seltzer
    assertEqual(fn(), "buzz", 1)
    assertEqual(fn(), "buzz", 2)
    assertEqual(fn(), "buzz", 3)
    assertEqual(fn(), "fizz", 4)
    try:
        fn()
        assert false
    except RuntimeError:
        pass
