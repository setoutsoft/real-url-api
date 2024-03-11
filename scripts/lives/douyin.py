# 获取抖音直播的真实流媒体地址，默认最高画质。
# 如果知道该直播间如“6779127643792280332”形式的room_id，则直接传入room_id。
# 如果不知道room_id，可以使用手机上打开直播间后，选择“分享--复制链接”，传入如“https://v.douyin.com/qyRqMp/”形式的分享链接。
#
import requests
import re
from scripts.base import Base


class DouYin(Base):

    _name = '抖音'

    def __init__(self, rid):
        super(Base, self).__init__()
        self.rid = rid

    def get_real_url(self):
        headers = {
            'authority': 'v.douyin.com',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }
        if re.match(r'\d{19}', self.rid):
            room_id = self.rid
        else:
            try:
                url = re.search(r'(https.*)', self.rid).group(1)
                response = requests.head(url, headers=headers)
                url = response.headers['location']
                room_id = re.search(r'\d{19}', url).group(0)
            except Exception as e:
                return '获取RoomID失败，直播间不存在或未开播或参数错误'
        try:
            headers.update(
                {
                    'authority': 'webcast.amemv.com',
                    'cookie': '_tea_utm_cache_1128={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}',
                }
            )
            params = (
                ('type_id', '0'),
                ('live_id', '1'),
                ('room_id', room_id),
                ('app_id', '1128'),
            )
            response = requests.get('https://webcast.amemv.com/webcast/room/reflow/info/', headers=headers, params=params).json()
            rtmp_pull_url = response['data']['room']['stream_url']['rtmp_pull_url']
            hls_pull_url = response['data']['room']['stream_url']['hls_pull_url']
            real_url = [rtmp_pull_url, hls_pull_url]
        except:
            return '直播间不存在或未开播或参数错误'
        return real_url


if __name__ == '__main__':
    r = input('请输入抖音直播间room_id或分享链接：\n')
    print(DouYin(r).get_real_url())
