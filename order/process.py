# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
import pythainlp
# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #  pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    pdf = pisa.pisaDocument(
                src=BytesIO(html.encode('UTF-8')),
                dest=result,
                encoding='UTF-8'
            )

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None