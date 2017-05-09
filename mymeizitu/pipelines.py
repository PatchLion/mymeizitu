# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
import os, shutil



class MymeizituPipeline(ImagesPipeline):
    url_to_title = {}

    def get_media_requests(self, item, info):
        for image_url in item['imageurls']:
            url = image_url.strip().lower()
            self.url_to_title[url] = item["title"]
            #print("SSSS->", url, self.url_to_title[url], item['title'])
            if url not in self.url_to_title.keys():
                yield Request(url)

    def file_path(self, request, response=None, info=None):
        url = str(request.url).strip().lower()
        title = self.url_to_title.get(url, None)
        #print("title->>>>>>>>>>>>>>>", title)
        if title:
            newpath = os.path.join(settings["IMAGES_STORE"], title)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            filename = os.path.basename(url)
            newfullpath = os.path.join(newpath, filename)
            #del(self.url_to_title[url])
            print("->>>>>>>Save image to:", newfullpath)
            return newfullpath
        else:
            print("Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", url, " ||| ", self.url_to_title)
            return super().file_path(request,response, info)

    def item_completed(self, results, item, info):
        #print('results---->', results)
        image_paths = [url['path'] for ok, url in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['imageurls'] = image_paths
        for key, value in self.url_to_title:
            if value == item['title']:
                del(self.url_to_title[key])
        return item
