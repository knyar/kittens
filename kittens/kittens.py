import flickrapi
import random
import os
import urllib
import string
import shutil
import Image
from django.conf import settings

orig_fname = 'orig.jpg'
images_root = os.path.join(settings.MEDIA_ROOT, 'images')
owner_blacklist = ['31355686@N00']

def resize_image(image_id, dst_width, dst_height):
    base_path = os.path.join(images_root, image_id)
    resized_path = os.path.join(base_path, '%sx%s.jpg' % (dst_width, dst_height))
    if os.path.isfile(resized_path):
         return True
    img = Image.open(os.path.join(base_path, orig_fname))
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
    while True:
        try_id = random.choice(dirlist)
        if image_orig_exists(try_id):
             return try_id

def image_orig_exists(image_id):
    return os.path.isfile(os.path.join(images_root, image_id, orig_fname))

def fetch_new_image():
    flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY)
    try:
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
    except Exception:
        return False
    if photos.attrib['stat'] != 'ok': return False
    for i in xrange(30):
        random_id = random.randint(0, len(photos[0])-1)
        photo = photos[0][random_id]
        if photo.attrib['owner'] in owner_blacklist: continue
        image_id = '%s-%s' % (photo.attrib['owner'], photo.attrib['id'])
        if 'originalformat' in photo.attrib and photo.attrib['originalformat'] == 'jpg' and not image_orig_exists(image_id):
            url = string.Template('http://farm${farm}.staticflickr.com/${server}/${id}_${originalsecret}_o.jpg').safe_substitute(photo.attrib)
            image_dir = os.path.join(images_root, image_id)

            if not os.path.isdir(image_dir):
                os.mkdir(image_dir)
            try:
                dstpath = os.path.join(images_root, image_id, orig_fname)
                urllib.urlretrieve(url, "%s.tmp" % dstpath)
                os.rename("%s.tmp" % dstpath, dstpath)
                return True
            except IOError, e:
                shutil.rmtree(image_dir)
    return False

