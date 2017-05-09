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
            #print("SSSS->", url, self.url_to_title[url], item['title'])
            if url not in self.url_to_title.keys():
                self.url_to_title[url] = item["title"]
                yield Request(url)

    def item_completed(self, results, item, info):
        #print('results---->', results)
        image_paths = [x for ok, x in results if ok]
        new_paths = []
        if not image_paths:
            raise DropItem("Item contains no images")
        else:
            for result in image_paths:
                new_paths.append(self.moveImage(result, item["title"]))
        item['imageurls'] = new_paths

        for key in [key for key, value in self.url_to_title.items() if value == item['title']]:
            del (self.url_to_title[key])

        return item

    def moveImage(self, reuslt, title):
        url = reuslt['url']
        root_dir = settings["IMAGES_STORE"]
        old_path = os.path.join(root_dir, reuslt["path"])
        new_path = os.path.join(root_dir, title)
        new_filename = os.path.basename(url)
        new_fullpath = os.path.join(new_path, new_filename)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        shutil.copyfile(old_path, new_fullpath)
        os.remove(old_path)
        return new_fullpath
