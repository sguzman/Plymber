import splinter

def cookie():
    with splinter.Browser() as browser:
        browser.visit('https://auth.uber.com/login/?next_url=https%3A%2F%2Fpartners.uber.com')
        browser.fill('textInputValue', 'guzmansalv@gmail.com')

        button = browser.find_by_text('Next')
        button.click()

        browser.fill('password', 'BHigfgEeITMw/3nJw733MD2f6QX0!n')
        button = browser.find_by_text('Next')
        button.click()

        browser.fill('verificationCode', input("Enter Verification code: "))
        button = browser.find_by_text('Verify')
        button.click()

        return browser.cookies.all()