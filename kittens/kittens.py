import flickrapi
import random
import os
import urllib
import string
import Image
from django.conf import settings

images_root = "%s/images" % settings.MEDIA_ROOT
owner_blacklist = ['31355686@N00']

def resize_image(image_id, dst_width, dst_height):
    resized_path = "%s/%s/%sx%s.jpg" % (images_root, image_id, dst_width, dst_height)
    if os.path.isfile(resized_path): return True
    img = Image.open('%s/%s/orig.jpg' % (images_root, image_id))
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_ratio = float(dst_width) / float(dst_height)
    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = int(crop_height * dst_ratio)
        x_offset = int(float(src_width - crop_width) / 2)
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = int(crop_width / dst_ratio)
        x_offset = 0
        y_offset = int(float(src_height - crop_height) / 3)

    img = img.crop((x_offset, y_offset, x_offset+crop_width, y_offset+crop_height))
    img = img.resize((int(dst_width), int(dst_height)), Image.ANTIALIAS)
    return img.save(resized_path, 'JPEG', quality=85)

def get_random_image_id():
    dirlist = os.listdir(images_root)
    image_id = False
    while image_id == False:
        try_id = random.choice(dirlist)
        if image_orig_exists(try_id): image_id = try_id
    return image_id

def image_orig_exists(image_id):
    return os.path.isfile("%s/%s/orig.jpg" % (images_root, image_id))

def fetch_new_image():
    flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY)
    photos = flickr.photos_search(
            license='1,2,4,5,7', # attribution
            sort='interestingness-desc',
            content_type='1', # photos
            group_id='10917369@N00', # http://www.flickr.com/groups/cat-portraits/
            media='photos',
            extras='original_format',
            per_page='30',
            page = random.randint(1, 150),
            )
    if photos.attrib['stat'] != 'ok': return False
    for i in xrange(30):
        random_id = random.randint(0, len(photos[0])-1)
        photo = photos[0][random_id]
        if photo.attrib['owner'] in owner_blacklist: continue
        image_id = '%s-%s' % (photo.attrib['owner'], photo.attrib['id'])
        if 'originalformat' in photo.attrib and photo.attrib['originalformat'] == 'jpg' and not image_orig_exists(image_id):
            url = string.Template('http://farm${farm}.staticflickr.com/${server}/${id}_${originalsecret}_o.jpg').safe_substitute(photo.attrib)
            os.mkdir("%s/%s" % (images_root, image_id))
            try:
                dstpath = "%s/%s/orig.jpg" % (images_root, image_id)
                urllib.urlretrieve(url, "%s.tmp" % dstpath)
                os.rename("%s.tmp" % dstpath, dstpath)
                return True
            except IOError, e:
                os.rmdir("%s/%s" % (images_root, image_id))
    return False

