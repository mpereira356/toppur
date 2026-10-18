"""Verificação opcional com Playwright e Chrome instalados na máquina."""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


origin = os.environ.get('QA_ORIGIN', 'http://127.0.0.1:3030')
artifacts = Path('.qa')
artifacts.mkdir(exist_ok=True)
failures = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page()
    page.on('pageerror', lambda error: failures.append(str(error)))
    for width in [360, 390, 768, 1440]:
        page.set_viewport_size({'width': width, 'height': 900})
        for route in ['/', '/produtos', '/segmentos', '/sobre', '/contato',
                      '/produtos/gaxetas', '/produtos/acoplamentos']:
            response = page.goto(origin + route)
            assert response.status == 200, (width, route, response.status)
            page.evaluate('document.fonts.ready')
            overflow = page.evaluate('''() => Array.from(document.querySelectorAll('body *'))
                .filter(e => e.getBoundingClientRect().right > innerWidth + 1
                    && getComputedStyle(e).position !== 'fixed'
                    && !e.closest('.filters'))
                .map(e => ({tag:e.tagName, cls:e.className, right:e.getBoundingClientRect().right}))''')
            if page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'):
                failures.append({'width': width, 'route': route, 'overflow': overflow[:8]})
            broken = page.locator('img').evaluate_all('(images) => images.filter(i => i.complete && !i.naturalWidth).map(i => i.src)')
            if broken:
                failures.append({'route': route, 'broken_images': broken})
            if width in [390, 1440] and route in ['/', '/produtos', '/contato']:
                page.screenshot(path=str(artifacts / f'{width}-{route.strip("/") or "inicio"}.png'), full_page=True)

    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(origin)
    page.get_by_role('button', name='Abrir menu').click()
    assert page.locator('#nav').is_visible()
    page.keyboard.press('Escape')
    assert not page.locator('#nav').is_visible()
    page.locator('.faq-list summary').first.click()
    assert page.locator('.faq-list details').first.get_attribute('open') is not None

    page.goto(origin + '/produtos')
    page.get_by_label('Buscar no catálogo').fill('coifas')
    page.get_by_role('button', name='Buscar').click()
    page.wait_for_url('**/produtos?q=coifas&**')
    assert page.locator('.product-card').count() == 1
    page.locator('.product-card').click()
    page.wait_for_url('**/produtos/coifas')
    assert page.locator('h1').inner_text() == 'Coifas'
    page.get_by_role('link', name='Solicitar orçamento desta peça').click()
    page.wait_for_url('**/contato?**')
    assert 'Coifas' in page.get_by_label('Conte sobre sua necessidade').input_value()
    assert page.locator('input[name="csrf_token"]').input_value()

    browser.close()

print(json.dumps({'failures': failures, 'screenshots': str(artifacts)}, ensure_ascii=True, indent=2))
if failures:
    raise SystemExit(1)
