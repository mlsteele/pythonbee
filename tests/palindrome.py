def test(entry):
    fn = entry.palindrome
    assert fn("foo") == False, "foo is not a palindrome"
    assert fn("rewarder redrawer") == True, "'rewarder redrawer' is a palindrome"
