import requests
from pyquery import PyQuery as pq


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        ## 维持会话，自动处理cookies
        self.session = requests.Session()

    ## 解析出登录所需要的
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = pq(response.text)
        token = selector('input[name="authenticity_token"]').attr('value')
        return token

    def login(self, email, password):
        # print(self.token())
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)

        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)


    ## 详情页面
    def profile(self, html):
        selector = pq(html)
        # print(selector.text())
        name = selector('input[id="user_profile_name"]').attr('value')
        email = selector('select[id="user_profile_email"] option[selected="selected"]').text()
        print(name, email)

if __name__ == "__main__":
        login = Login()
        login.login(email='863163094@qq.com', password='123')
