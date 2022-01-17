import os,re,slack



client = slack.WebClient(token='xoxb-2895391715429-2911092400561-olwSyFBzi77lNdFYcMimVMAy')
client.chat_postMessage(channel='report-dates', text='This is only a test.')

