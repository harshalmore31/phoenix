from seleniumbase import SB

with SB() as sb:
    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "chat-gpt\n")
    sb.click('a:contains("OpenAI")')
    sb.click('a:contains("Try ChatGPT")')
    sb.wait_for_element('textarea[data-id="root"]')
    sb.type('textarea[data-id="root"]', "hii\n")