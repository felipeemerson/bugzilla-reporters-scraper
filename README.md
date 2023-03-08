<div align="center">

  <h1 align="center">Bugzilla Reporters Scraper</h1>

  <p align="center">
    A scraper that takes a list of Bugzilla reporters (users) emails and gather some data about them.
    </br>
  </p>
</div>

## About
[Bugzilla](https://bugzilla.mozilla.org/) is an open-source bug-tracking system used by Mozilla, Eclipse, etc. This scraper takes a list of Bugzilla users emails and produces a list of JSON objects with statistics related with the bug reporting process of each of those users.

## Pre-requisites
Before run the scraper, you need both [Python](https://www.python.org/downloads/) and [Scrapy](https://docs.scrapy.org/en/latest/intro/install.html) lib installed.

In addition, you need to set some variables at the [`reporters.py`](https://github.com/felipeemerson/bugzilla-reporters-scraper/blob/main/reporters_spider/spiders/reporters.py) file:
- USERS_FILE_PATH: set the path to a file containing a JSON array of users emails
- SAVE_FILE_PATH: set the path to the file that will receive the JSON result (a JSON array with data of each user)
- BUGZILLA_LOGIN: set you Bugzilla's email
- BUGZILLA_PASSWORD: set your Bugzilla's password

## Running

```bash

# Clone this repository
$ git clone https://github.com/felipeemerson/bugzilla-reporters-scraper.git

# Go to project's root folder
$ cd bugzilla-reporters-scraper/

# Run with the scrapy command
$ scrapy crawl reporters
```

## Data result format
Each object in the result will have the properties (more info about each of them in [Bugzilla](https://wiki.mozilla.org/BMO/User_profile_fields)):
- **bugs_filed**: the total number of bugs reported by the user.;
- **comments_made**: the total number of comments that the user has added;
- **assigned_to**: the total number of bugs assigned to a user;
- **commented_on**: the total number of bugs that the user has commented on;
- **qa_contact**: QA-contacts work as part of the QA team to help developers with regression testing, steps to reproduce bugs, and bug verification;
- **patches_submitted**: the number of patches a user has submitted to help fix a bug;
- **patches_reviewed**: shows how many patches a user has reviewed;
- **bugs_poked**: total number of bugs a user has interacted with: filed, commented on, changed status, added whiteboard or keyword tags, changed product or component; anything done to the bug that results in saving changes;
- **has_permissions**: indicates that the user has more permissions than others (may be a developer? Need more investigation...);
- **user_email**: the email of the user;
- **bugs_resolved**: total number of bugs a user has changed from NEW, UNCONFIRMED, or REOPENED to RESOLVED;
- **bugs_fixed**: total number of bugs a user has resolved as FIXED. Only verify FIXED if the bug's resolution can be tied to a specific code checkin in a Mozilla repository;
- **bugs_verified**: total number of resolved bugs that a user has made sure have been resolved correctly;
- **bugs_invalid**: total number of bugs a user has resolved as INVALID; these may be issues that aren't Mozilla bugs, or are features rather than unexpected behavior.

The final result produced by the scraper is like the object below:

```bash
[
  {
    "bugs_filed": 834,
    "comments_made": 6378,
    "assigned_to": 1977,
    "commented_on": 3420,
    "qa_contact": 891,
    "patches_submitted": 2,
    "patches_reviewed": 25,
    "bugs_poked": 4098,
    "has_permissions": true,
    "user_email": "someone@email.com",
    "bugs_resolved": 2476,
    "bugs_fixed": 2142,
    "bugs_verified": 33,
    "bugs_invalid": 34
  },
  { ... },
  .
  .
  .
]
```
