def test_hello_page_uses_base_layout(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.text
    assert "<html" in html
    assert "The app is running on your laptop." in html
    assert "/static/app.css" in html
    assert "/static/htmx.min.js" in html
    assert "fonts.googleapis.com" in html
    assert "Gloock" in html and "Onest" in html
    assert "hx-headers=" in html


def test_static_files_are_served(client):
    css = client.get("/static/app.css")
    assert css.status_code == 200
    assert "--background: #000000" in css.text
    assert "--touch-min" in css.text

    js = client.get("/static/htmx.min.js")
    assert js.status_code == 200
    assert 'version:"2.0.11"' in js.text
