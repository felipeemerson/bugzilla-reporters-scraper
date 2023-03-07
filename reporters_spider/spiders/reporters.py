import scrapy
import json
import re
import urllib.parse

START_URL = "https://bugzilla.mozilla.org/index.cgi?GoAheadAndLogIn=1"
USERS_FILE_PATH = "<SET THE USERS FILE PATH>"
SAVE_FILE_PATH = "<SET SAVE FILE PATH>"
BUGZILLA_LOGIN = "<SET YOUR BUGZILLA'S EMAIL LOGIN>"
BUGZILLA_PASSWORD = "<SET YOU BUGZILLA'S PASSWORD>"

class ReportersSpider(scrapy.Spider):
    name = "reporters"
    start_urls = [ START_URL ]

    custom_settings = {
        "RANDOMIZE_DOWNLOAD_DELAY": False,
        "DOWNLOAD_DELAY": 60/40.0,
        "CONCURRENT_REQUESTS_PER_IP": 40
    }

    # Create file with empty array
    with open(SAVE_FILE_PATH, 'w') as outfile:
       json.dump([], outfile)

    def parse(self, response):
        self.log('Visited login page: {}'.format(response.url))
        yield scrapy.FormRequest(
            START_URL,
            formdata={"Bugzilla_login": BUGZILLA_LOGIN, "Bugzilla_password": BUGZILLA_PASSWORD},
            callback=self.start_to_requests
        )

    def start_to_requests(self, response):
        # This load the users array from a file, but you can set it directly...
        with open(USERS_FILE_PATH) as users_file:
            users = json.load(users_file)

        emails = [urllib.parse.quote(user) for user in users]

        # Generate the URLs to scrape for each user
        urls = [f'https://bugzilla.mozilla.org/user_profile?login={email}' for email in emails]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_users)

    def parse_users(self, response):
        self.log('Visited page: {}'.format(response.url))

        data = []
        has_permissions = False

        with open(SAVE_FILE_PATH, 'r') as file:
            data = json.load(file)

        user_email = response.xpath('//input[@id="login"]/@value').get()
        
        # first tr value is 14, but init from 1 for caution
        # and exit if tr_value reach 30 maybe user doesnt exist
        tr_value = 1

        while True:
            th = response.xpath(f'//tr[{tr_value}]/th/text()').get()

            if (th == "Permissions"):
                td = response.xpath(f'//tr[{tr_value}]/td/text()').get()

                if ("Can confirm bugs, can edit any bug" in td):
                    has_permissions = True

            if(th == "Bugs filed" or tr_value == 30):
                break

            tr_value += 1
        
        if (tr_value == 30):
            raise CloseSpider(f'User doesn\'t exists at {response.url}')

        user_statistics = {
            'bugs_filed': int(response.xpath(f'//tr[{tr_value}]/td[2]/a/text()').get()),
            'comments_made': int(response.xpath(f'//tr[{tr_value + 1}]/td[2]/text()').get()),
            'assigned_to': int(response.xpath(f'//tr[{tr_value + 2}]/td[2]/a/text()').get()),
            'commented_on': int(response.xpath(f'//tr[{tr_value + 3}]/td[2]/a/text()').get()),
            'qa_contact': int(response.xpath(f'//tr[{tr_value + 4}]/td[2]/a/text()').get()),
            'patches_submitted': int(response.xpath(f'//tr[{tr_value + 5}]/td[2]/text()').get()),
            'patches_reviewed': int(response.xpath(f'//tr[{tr_value + 6}]/td[2]/text()').get()),
            'bugs_poked': int(response.xpath(f'//tr[{tr_value + 7}]/td[2]/text()').get()),
            'has_permissions': has_permissions
        }

        resolved_bugs = response.xpath(f'//tr[{tr_value + 9}]/td[2]/text()').get()
        resolved_bugs = re.findall('\((.*?)\)',resolved_bugs)

        user_statistics['user_email'] = user_email
        user_statistics['bugs_resolved'] = int(resolved_bugs[0])
        user_statistics['bugs_fixed'] = int(resolved_bugs[1])
        user_statistics['bugs_verified'] = int(resolved_bugs[2])
        user_statistics['bugs_invalid'] = int(resolved_bugs[3])

        data.append(user_statistics)

        with open(SAVE_FILE_PATH, 'w') as outfile:
            json.dump(data, outfile)
        self.log('Saved file')