import re


class Candidate:
    NUMBER: re.Pattern[str] = re.compile(r"[+-]?\d+(?:\.\d+)?")
    D_QUOTED: re.Pattern[str] = re.compile(r'"([^"]*)"')
    S_QUOTED: re.Pattern[str] = re.compile(r"'([^']*)'")

    @classmethod
    def get_value(cls, prompt: str) -> list[str]:
        res: list[str] = []

        res.extend(Candidate.D_QUOTED.findall(prompt))
        res.extend(Candidate.S_QUOTED.findall(prompt))
        res.extend(Candidate.NUMBER.findall(prompt))
        # res.extend(prompt.split())

        return res
