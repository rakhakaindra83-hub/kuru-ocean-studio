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
    for width in (1440, 768, 390, 320):
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('.menu').click()
    assert page.locator('.menu').get_attribute('aria-expanded') == 'true'
    page.locator('.nav-links a[href="#development"]').click()
    assert page.locator('.menu').get_attribute('aria-expanded') == 'false'
    page.locator('[data-service="Website development"]').click()
    assert page.locator('dialog').evaluate('(d) => d.open')
    assert page.locator('#service').input_value() == 'Website development'
    page.locator('#name').fill('Kuru')
    page.locator('#details').fill('Website portfolio art bertema ocean, responsive.')
    with page.expect_download() as download:
        page.locator('button[type="submit"]').click()
    file = download.value
    file.save_as(root / 'test-brief.txt')
    text = (root / 'test-brief.txt').read_text(encoding='utf-8')
    assert 'Nama: Kuru' in text and 'Website development' in text
    page.locator('.close').click()
    assert not page.locator('dialog').evaluate('(d) => d.open')
    page.evaluate('scrollTo(0,0)')
    page.screenshot(path=str(root / 'mobile-preview.png'), full_page=True)
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.screenshot(path=str(root / 'desktop-preview.png'), full_page=True)
    assert not errors, errors
    print('PASS: 4 viewport widths, mobile menu, dialog, service selection, brief download; no JavaScript errors.')
    browser.close()
    (root / 'test-brief.txt').unlink()
