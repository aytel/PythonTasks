def levenstein(str1, str2):
    """
    :return Levenstein distance between str1 and str2.
    """

    n, m = len(str1), len(str2)
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(
                dp[i][j - 1] + 1,
                dp[i - 1][j] + 1,
                dp[i - 1][j - 1] + (str1[i - 1] != str2[j - 1])
            )

    return dp[n][m]


class LazyLoader:
    def __init__(self, filename: str):
        self.filename = filename

    @property
    def content(self) -> dict:
        if hasattr(self, '_content'):
            return self._content
        with open(self.filename, "r", encoding="utf8") as file:
            self._content = json.load(file)
        return self._content
