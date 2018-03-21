# -*- encode: utf-8 -*-

import re
import pprint
import requests
import datetime
import uuid
import os
import mimetypes

html = """
<div id="google_image_div" style="overflow:hidden; position:absolute"><script>vu("https://securepubads.g.doubleclick.net/pcs/view?xai\u003dAKAOjsv-_Ea6ix-ZE6iHsOwYmHYgWNJge28I-ZTgLPI36A37eXD_Uxlm7fmfMOLgy8m42V5RC4C1gwmUDMdJXj564YWbhcMC3v99E99EYfXxhhWksXUaISaA5gH8q_3DVmCoyKeCRIQ8uiBdBbIzZh1HLkHEllj53yd7k2fjOLebl4hBA4MEJvx3_nGCNZpX-JcE8unXQWcZ-6cHhi5IoZuUJYEWgKIXQIaUJnWmd3YH6GZg0wOGhUq_rBHJAsTR2stFjuLvnUfLRuHUYlPIrNMCkqEEnyoJvlA\u0026sig\u003dCg0ArKJSzPjL-MK1RSybEAE\u0026adurl\u003d")</script><a id="aw0" target="_blank" href="http://googleads.g.doubleclick.net/pcs/click?xai=AKAOjssMT_PlgVmk4uNnD0CFQBj-jpB6KJIZOjA3U53LGqXOuruHWAy4hdrBikTmTLYHOvewMmMy1LM7udBvWTx86h3uDXsJPGZ8KFeXqBT-U-lwc5ftBJcYEN53GsOUrfX19jJRGvEKEnWLg6vkw2dt828ocbHxTyGWGgpMGx2JtVNVBfLvThxzj_M2_fGpHG6_EPRhmkdYE8jZxCLhdbkRaRWk0VGbPbAY67jfL6PBeqLorhMlV3koIJvIxLcOYk8zVIhLPFNrmbT97c1pC-ozfZN_Jdc&amp;sig=Cg0ArKJSzFWp9cVL5eeN&amp;adurl=http://stackoverflow.com:80/jobs/remote%3Futm_source%3Dwebsite%26utm_medium%3Dbanner%26utm_content%3Dleaderboard_5%26utm_campaign%3Dhouse_ads_ROS_SO&amp;nm=5&amp;nx=96&amp;ny=-17&amp;mb=2" onfocus="ss('aw0')" onmousedown="st('aw0')" onmouseover="ss('aw0')" onclick="ha('aw0')"><img src="https://tpc.googlesyndication.com/pagead/imgad?id=CICAgKCrvPr-WhDYBRhaMggKqqwgRG3EzQ" border="0" width="728" height="90" alt="House Ads Jobs Love Remote Work Day 5 MLB SO 20160819" class="img_ad"></a></div>
<img src="a.jpg" />
<img src="b.jpg" class="b jpg" />
<img src="c.jpg" class="c jpg" >
<img src='d.jpg' class="d jpg" >
<img src='d.jpg' class="d jpg" >
<img src='ef.jpg' class="ef jpg" >
<img src='http://ucenter.51cto.com/images/noavatar_middle.gif' class="ddf jpg" >
<div class="img-box"><img src="//img-ads.csdn.net/2018/201803151802373041.jpg" alt=""></div>
<img class="maxwidth" src="http://ubmcmm.baidustatic.com/media/v1/0f000ji2uInSd4D5jKvI36.jpg" alt="" title="">
"""

pattern = re.compile(r'.*<img.*src=["\'](\S*)["\']\s+')
images = pattern.findall(html)
pp = pprint.PrettyPrinter()
pp.pprint(images)

for img in images:
    new_img = img
    if img.startswith(('http', '//')):
        url = img
        if img.startswith('//'):
            url = 'http:' + img
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
            continue

        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type, False)
        if extension is None:
            extension = '.png'
        elif extension == '.jpe':
            extension = '.jpg'
        print(extension)

        saveDir = 'D:/tmp'
        pathUrl = '/uploads/' + datetime.date.today().strftime('%Y%m%d') + '/';
        if not os.path.exists(saveDir + pathUrl):
            os.mkdir(saveDir + pathUrl)

        pathUrl += uuid.uuid4().__str__() + extension
        new_img = pathUrl
        f = open(saveDir + pathUrl, 'wb')

        for block in response.iter_content(1024):
            if not block:
                break

            f.write(block)

        f.close()

        html = html.replace(img, new_img)

print(html)
