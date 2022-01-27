#repsonding function
import slack 
import pulumi

config = pulumi.Config()

access_token = config.require_secret('SLACK_ACCESS_TOKEN')

APP_VERIF_TOKEN = ''

client = slack.WebClient(token=access_token)

client.chat_postMessage(channel='report-dates', text='This is only a test')