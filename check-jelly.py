from pathlib import Path
from playwright.sync_api import sync_playwright

url = 'https://rakhakaindra83-hub.github.io/kuru-site/'
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.route(url, lambda route: route.fulfill(body='Portfolio navigation verified'))
    page.goto(Path('index.html').resolve().as_uri())
    page.locator('.jelly-link').click()
    assert page.locator('.jelly-link').evaluate("el=>el.classList.contains('departing')")
    assert page.url != url
    page.wait_for_url(url)
    assert 'Portfolio navigation verified' in page.content()
    reduced = browser.new_page(reduced_motion='reduce')
    reduced.route(url, lambda route: route.fulfill(body='Reduced motion navigation verified'))
    reduced.goto(Path('index.html').resolve().as_uri())
    reduced.locator('.jelly-link').focus()
    reduced.keyboard.press('Enter')
    reduced.wait_for_url(url)
    print('PASS: click animates before redirect; keyboard + reduced motion redirect correctly.')
    browser.close()
