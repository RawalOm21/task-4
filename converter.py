import asyncio
from flask import Flask, render_template, make_response
from pyppeteer import launch

app = Flask(__name__)

@app.route('/generate-pdf')
def generate_pdf():
    # Render the HTML template
    html_content = render_template('index.html', message="Welcome to the Library API!")

    # Call the async function synchronously
    pdf_bytes = asyncio.run(html_to_pdf(html_content))

    # Create a Flask response with the PDF
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response

async def html_to_pdf(html_content):
    browser = await launch()
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_bytes = await page.pdf({
        'format': 'A4',
        'printBackground': True
    })
    await browser.close()
    return pdf_bytes

if __name__ == '__main__':
    app.run(debug=True)
