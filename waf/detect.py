from pathlib import Path
import yaml
from urllib.parse import quote_plus
from logging import getLogger
from typing import Optional
from pydantic import BaseModel
import json

logger = getLogger('waf.detect')


class RulesContent(BaseModel):
    name: Optional[str]
    description: Optional[str]
    body: Optional[list] = None
    header: Optional[list] = None


class OutputRuleContent(BaseModel):
    name: Optional[str]
    description: Optional[str]
    data: Optional[list] = None


def detect_decorator(func):
    def wrapper(self, *args):
        sid = func(self, *args)
        if sid is not None:
            rule = self.rules.get(sid)
            logger.info(f"sid:'{sid}' name:'{rule.name}' description:'{rule.description}'")
            return True

    return wrapper


class Signatures:
    def __init__(self,
                 rules_path="rules",
                 output_rules_path="output_rules"):
        self.rules_path = Path(rules_path)
        self.output_rules_path = Path(output_rules_path)
        self.rules = {}
        self.load_rules()
        self.output_rules = {}
        self.load_output_rules()

    def load_rules(self):
        if self.rules_path.exists():
            for rule in self.rules_path.iterdir():
                with rule.open() as f:
                    for sid, row in yaml.safe_load(f.read()).items():
                        if not row.get('disable'):
                            self.rules[sid] = RulesContent(**row)

    def load_output_rules(self):
        if self.output_rules_path.exists():
            for rule in self.output_rules_path.iterdir():
                with rule.open() as f:
                    for sid, row in yaml.safe_load(f.read()).items():
                        if not row.get('disable'):
                            self.output_rules[sid] = OutputRuleContent(**row)

    @detect_decorator
    def detect(self, request):
        headers = json.dumps({k: v for k, v in request.headers.items()})
        for sid, rule in self.rules.items():
            if request.get_data():
                if rule.body is not None:
                    if all(quote_plus(x).lower() in request.get_data().decode().lower() for x in rule.body):
                        return sid
                    if all(x.lower() in request.get_data().decode().lower() for x in rule.body):
                        return sid
            if rule.header is not None:
                if all(quote_plus(x).lower() in headers.lower() for x in rule.header):
                    return sid
                if all(x.lower() in headers.lower() for x in rule.header):
                    return sid

    def detect_output(self, response):
        for sid, rule in self.output_rules.items():
            if all(x.lower() in str(response.get_data()).lower() for x in rule.data):
                return sid


if __name__ == '__main__':
    detect = Signatures()
    print(detect.rules)
