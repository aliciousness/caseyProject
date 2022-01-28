from slack_sdk import WebClient
import pulumi


config = pulumi.Config()

class Casey:
    def __init__(self):
        self.slack = WebClient(token=config.require('SLACK_ACCESS_TOKEN'))
        
    def SLACK(self):
        return self.slack