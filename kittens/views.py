from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
import kittens

def index(request):
    context = {
            'base_url': request.build_absolute_uri('/')[:-1]
        }
    tpl = get_template('index.html')
    html = tpl.render(Context(context))
    return HttpResponse(html)

def fetch_image(request):
    kittens.fetch_new_image()
    # 1x1 gif
    code = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\xf0\x01\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
    return HttpResponse(code, mimetype="image/gif")

def kitten(request, width, height):
    image_id = kittens.get_random_image_id()
    kittens.resize_image(image_id, width, height)
    response = HttpResponseRedirect('//%s/images/%s/%sx%s.jpg' % (settings.MEDIA_URL, image_id, width, height))
    response['Cache-Control'] = 'no-cache'
    return response

