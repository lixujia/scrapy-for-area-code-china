# -*- coding: utf-8 -*-
import os
import json
import scrapy
from scrapy import Request


class CpdcSpider(scrapy.Spider):
    save_path = "cpdc_json"
    name = "cpdc"
    allowed_domains = ["cpdc.com.cn"]
    start_urls = (
        'http://www.cpdc.com.cn/web/api.php?op=get_linkage&act=ajax_select&keyid=1&parent_id=0',
    )

    def parse(self, response):
        province_list = json.loads(response.body)

        os.system("mkdir -p {}".format(self.save_path))
        with open("{}/index.json".format(self.save_path), "w") as fp:
            json.dump(province_list, fp, indent=True)
            fp.close()

        for province in province_list:
            sub_path = "{}/{}".format(self.save_path, province["region_id"])
            os.system("mkdir -p {}/cities".format(sub_path))
            with open("{}/index.json".format(sub_path), "w") as fp:
                json.dump(province, fp, indent=True)
                fp.close()

            params = {
                "op": "get_linkage",
                "act": "ajax_select",
                "keyid": "1",
                "parent_id": province["region_id"]
            }
            param_string = "&".join(["{}={}".format(k, v) for k, v in params.items()])
            url = "http://www.cpdc.com.cn/web/api.php?{}".format(param_string)
            print(url)
            yield Request(url, callback=self.parse_city_wrapper(sub_path))

    @staticmethod
    def parse_city_wrapper(relative_path):
        return lambda response: CpdcSpider.parse_city(relative_path, response)

    @staticmethod
    def parse_city(relative_path, response):
        city_list = json.loads(response.body)

        print("relative_path: {}".format(relative_path))
        print("city_list: {}".format(city_list))
        with open("{}/cities/index.json".format(relative_path), "w") as fp:
            json.dump(city_list, fp, indent=True)
            fp.close()

        for city in city_list:
            sub_path = "{}/cities/{}".format(relative_path, city["region_id"])
            os.system("mkdir -p {}/districts".format(sub_path))
            with open("{}/index.json".format(sub_path), "w") as fp:
                json.dump(city, fp, indent=True)
                fp.close()

            params = {
                "op": "get_linkage",
                "act": "ajax_select",
                "keyid": "1",
                "parent_id": city["region_id"]
            }
            param_string = "&".join(["{}={}".format(k, v) for k, v in params.items()])
            url = "http://www.cpdc.com.cn/web/api.php?{}".format(param_string)
            print(url)
            yield Request(url, callback=CpdcSpider.parse_district_wrapper(sub_path))

    @staticmethod
    def parse_district_wrapper(relative_path):
        return lambda response: CpdcSpider.parse_district(relative_path, response)

    @staticmethod
    def parse_district(relative_path, response):
        district_list = json.loads(response.body)

        with open("{}/districts/index.json".format(relative_path), "w") as fp:
            json.dump(district_list, fp, indent=True)
            fp.close()

        for district in district_list:
            sub_path = "{}/districts/{}".format(relative_path, district["region_id"])
            os.system("mkdir -p {}".format(sub_path))
            with open("{}/index.json".format(sub_path), "w") as fp:
                json.dump(district, fp, indent=True)
                fp.close()
