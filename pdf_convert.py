import markdown
from weasyprint import HTML, CSS

def markdown_to_pdf_weasyprint(md_content, output_pdf="travel_guide.pdf"):
    html_content = markdown.markdown(md_content)
    css = CSS(string="""
        @font-face {
            font-family: 'Noto Color Emoji';
            src: local('Noto Color Emoji'), url(https://github.com/googlefonts/noto-emoji/blob/main/fonts/NotoColorEmoji.ttf?raw=true) format('truetype');
        }

        body {
            font-family: 'Noto Color Emoji', sans-serif;
            font-size: 14px;
            line-height: 1.4; /* Increases margin between lines */
        }

        li {
            margin-bottom: 7px; /* Adds spacing between list items */
        }

        li strong {
            font-size: 15px;
            font-weight: bold; /* Makes list titles bold */
        }
    """)
    HTML(string=html_content).write_pdf(output_pdf, stylesheets=[css])
    return output_pdf