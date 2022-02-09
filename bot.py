from scenarios import possible_scenarios, UnrecognizedScenario


class Bot:
    def __init__(self):
        self.active_scenario = None

    @staticmethod
    def sanity_check(user_msg):
        sentences = [s for s in user_msg.split('.') if s != ""]
        if len(sentences) > 1:
            return "You're talking too much at a time!"
        sentences = [s for s in sentences[0].split('!') if s != ""]
        if len(sentences) > 1:
            return "You're talking too much at a time!"
        sentences = [s for s in sentences[0].split('?') if s != ""]
        if len(sentences) > 1:
            return "You're talking too much at a time!"
        return None

    def process_message(self, user_msg):
        if self.sanity_check(user_msg) is not None:
            return self.sanity_check(user_msg)
        if self.active_scenario is not None:
            if self.active_scenario.finished:
                self.active_scenario = None
            else:
                self.active_scenario.parse(user_msg)
                if self.active_scenario.error_text:
                    return self.active_scenario.error_text
                else:
                    return self.active_scenario.response
        if self.active_scenario is None:
            for scenario_class in possible_scenarios:
                scenario = scenario_class()
                scenario.parse(user_msg)
                self.active_scenario = scenario
                if scenario.error_text is None:
                    return scenario.response

            self.active_scenario = UnrecognizedScenario()
            self.active_scenario.parse(user_msg)
            return self.active_scenario.response
