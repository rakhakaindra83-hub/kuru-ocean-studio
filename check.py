from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((root / 'index.html').as_uri())
    assert page.title() == 'Kuru Studio — Art & Development'
    page.locator('.hero .artwork.visible').wait_for()
    assert page.locator('.hero h1,.hero .panel-copy,.hero .caption,.announcement').count() == 0
    assert page.locator('.hero .artwork').evaluate("el=>getComputedStyle(el).animationName") == 'drift'
    page.locator('.closing').scroll_into_view_if_needed()
    page.locator('.closing.visible').wait_for()
    reduced = browser.new_page(reduced_motion='reduce')
    reduced.goto((root / 'index.html').as_uri())
    assert reduced.locator('.hero .artwork').evaluate("el=>getComputedStyle(el).animationName") == 'none'
    assert reduced.locator('.hero .artwork').evaluate("el=>getComputedStyle(el).opacity") == '1'
    reduced.close()
    for width in (1440, 768, 390, 320):
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
    page.set_viewport_size({'width': 390, 'height': 844})
    page.mouse.move(150, 5)
    page.wait_for_function("document.querySelector('nav').getBoundingClientRect().top > 0")
    page.wait_for_timeout(650)
    page.locator('.menu').click()
    assert page.locator('.menu').get_attribute('aria-expanded') == 'true'
    page.locator('.nav-links a[href="#development"]').click()
    assert page.locator('.menu').get_attribute('aria-expanded') == 'false'
    page.locator('[data-service="Website development"]').click()
    assert page.locator('dialog').evaluate('(d) => d.open')
    assert page.locator('dialog a').count() == 3
    assert page.locator('dialog a').first.get_attribute('href') == 'https://www.instagram.com/favv.vrk/'
    assert page.locator('form').count() == 0
    page.locator('.close').click()
    assert not page.locator('dialog').evaluate('(d) => d.open')
    page.evaluate("document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible')); scrollTo(0,0)")
    page.wait_for_timeout(1000)
    page.screenshot(path=str(root / 'mobile-preview.png'), full_page=True)
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.screenshot(path=str(root / 'desktop-preview.png'), full_page=True)
    assert not errors, errors
    print('PASS: 4 viewport widths, mobile menu, contact dialog, social links; no JavaScript errors.')
    browser.close()

