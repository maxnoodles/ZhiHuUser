import re
from urllib import parse
a ='https://www.zhihu.com/members/excited-vczh/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=80'

b = re.sub(r'members', '/api/v4/members', a)
b = parse.unquote(b)
print(b)

