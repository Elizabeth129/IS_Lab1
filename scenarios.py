import abc
import re
from randfacts import getFact


class AbstractScenario(abc.ABC):
    def __init__(self):
        self.finished = False
        self.error_text = None
        self.response = None

    @staticmethod
    def clear_msg(user_msg: str):
        msg = user_msg.lower()
        msg = msg.replace(',', '')
        return msg

    @abc.abstractmethod
    def parse_internal(self, user_msg: str):
        pass

    def parse(self, user_msg: str):
        user_msg = self.clear_msg(user_msg)
        self.parse_internal(user_msg)


class SimpleQuestionScenario(AbstractScenario):
    def parse_internal(self, user_msg: str):
        if '?' not in user_msg:
            self.error_text = "I wanted you to question me something :("
            self.finished = True
            return

        self.response = "And why are you asking?"
        self.finished = True


class WhQuestionScenario(AbstractScenario):
    def parse_internal(self, user_msg: str):
        if '?' not in user_msg:
            self.error_text = "I wanted you to question me something :("
            self.finished = True
            return
        first_word = user_msg.split()[0]
        answers = {
            "why":   "Just because it's necessary!",
            "where": "Far-far away",
            "who":   "I don't know",
            "when":  "Sometime",
            "what":  "What?",
            "which": "Any",
            "whose": "Yours",
            "how":   "Nobody knows",
        }
        self.response = answers.get(first_word)
        self.finished = True
        if self.response is None:
            self.error_text = "I wanted a 'wh' question here"
            return


class WhatIsQuestionScenario(AbstractScenario):
    def parse_internal(self, user_msg: str):
        if re.fullmatch(r"what is .+[?]", user_msg) is None:
            self.error_text = "I wanted you to question me something :("
            self.finished = True
            return
        google_link = f"https://google.com/search?q={user_msg[8:]}".replace(' ', '+')
        self.response = f"You must be very old if you don't know how to use Google. Let me Google it " \
                        f"for you {google_link} "
        self.finished = True


class UniversityScenario(AbstractScenario):
    def parse_internal(self, user_msg: str):
        predefines = [
            [r"(have you (started|finished)|are you writing) your diploma[?]", "It's too early!"],
            [r"when (is|was) the deadline (|.*)[?]", "Yesterday"],
            [r"need i (go to|attend) .*[?]", "However you want, but it's useless"],
            [r"do you want to .*[?]", "And who wants?"]
        ]
        for question in predefines:
            if re.fullmatch(question[0], user_msg) is not None:
                self.response = question[1]
                self.finished = True
                return
        self.error_text = "Expected university scenario"
        self.finished = True


class AnimalsScenario(AbstractScenario):
    def parse_internal(self, user_msg: str):
        predefines = [
            [r"how much does .* eat[?]", "Less than you"],
            [r"how much does .* weigh[?]", "Less than you"],
            [r"do you like .*[?]", "More than you"],
            [r"which animal is the most .*[?]", "You"]
        ]
        for question in predefines:
            if re.fullmatch(question[0], user_msg) is not None:
                self.response = question[1]
                self.finished = True
                return
        self.error_text = "Expected animals scenario"
        self.finished = True


class UnrecognizedScenario(AbstractScenario):
    def parse_internal(self, user_msg):
        self.response = "You are talking some nonsense.\n" \
                        "Here is random fact to make your stupid self feel better: %s" % getFact()
        self.finished = True


possible_scenarios = [UniversityScenario,
                      AnimalsScenario,
                      WhatIsQuestionScenario,
                      WhQuestionScenario,
                      SimpleQuestionScenario]
