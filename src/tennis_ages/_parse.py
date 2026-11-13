"""Private helpers that parse and clean a Tennis Abstract career JS file.

These work on the file's text, not on the network, so they are what the test
suite covers using the mock files in tests/fixtures/.

Women's files store the opponent's date of birth in column 16; men's files
store the opponent's age (in years) in the same column.
"""
