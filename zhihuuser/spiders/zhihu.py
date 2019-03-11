# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from zhihuuser.items import UserItem
import json
import re


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    follows_url = r'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset=0&limit=20'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = r'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset=0&limit=20'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(url=self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(url=self.follows_url.format(user=self.start_user, include=self.follows_query), callback=self.parse_follows)
        yield Request(url=self.followers_url.format(user=self.start_user, include=self.followers_query), callback=self.parse_follows)


    def parse_user(self, response):
        results = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item

        yield Request(url=self.follows_url.format(user=results.get('url_token'), include=self.follows_query), callback=self.parse_follows)
        yield Request(url=self.followers_url.format(user=results.get('url_token'), include=self.followers_query), callback=self.parse_follows)


    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for  result in results.get('data'):
                yield Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            next_page = re.sub(r'members', 'api/v4/members', next_page)
            yield Request(url=next_page, callback=self.parse_follows)
