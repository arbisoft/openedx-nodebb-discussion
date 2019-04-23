# Manual to add openedx_nodebb_discusson in your edx platform

Clone this repo into `openedx_nodebb_discussion` folder using the given command

`git clone https://github.com/arbisoft/openedx-nodebb-discussion.git openedx_nodebb_discussion`

---

Copy this folder and place this at the following location in edx codebase

`../edx-platform/openedx/features/`

---

Add `ENABLE_NODEBB_DISCUSSION` flag in the `FEATURES` in the following files


- lms.env.json
- cms.env.json


and set their values to   `true`

```
FEATURES = {
    ...
    "ENABLE_NODEBB_DISCUSSION": true,
}
```
---

Add the following dictionary at the end of `lms.env.json` and `cms.env.json`

```
{
    ...
    ...
    "NODEBB_SETTINGS": {
        "URL": "<YOUR NODEBB URL>",
        "DOMAIN": "<YOUR NODEBB DOMAIN>"
    }
}
```


---
Add the following dictionary at the end of `lms.auth.json` and `cms.auth.json`

```
{
    ...
    ...
    "OPENEDX_NODEBB_DISCUSSION": {
        "DISCUSSION_JWT_SECRET": "<Your secret>",
        "DISCUSSION_JWT_ALGORITHM": "<Your algorithm>",
        "NODEBB_API_TOKEN": "<Your NodeBB Write Api Token>",
    }
}
```
---

Add the following lines at the end of the `lms/envs/aws.py` and `cms/envs/aws.py` files

```
##################### Openedx Nodebb Discussion Secrets ###########
OPENEDX_NODEBB_DISCUSSION = AUTH_TOKENS.get("OPENEDX_NODEBB_DISCUSSION", {})
NODEBB_SETTINGS = ENV_TOKENS.get("NODEBB_SETTINGS", None)
```


**Note:** If you are using edx release `ironwood` then instead of making changes in `aws.py` 
make these changes in `lms/envs/production.py` and `cms/evns/production.py` as `aws.py` file has been 
depricated in `ironwood` edx release.

---

To add `openedx_nodebb_discussion` app into the installed apps add the 
following line in the `INSTALLED_APPS` list present in `lms/common.py` and 
`cms/common.py` file.

```
INSTALLED_APPS = [
    ...
    'openedx.features.openedx_nodebb_discussion',
]
```

---

Append these urls in `lms/urls.py`

```
# add nodebb discussion endpoints
if settings.FEATURES.get('ENABLE_NODEBB_DISCUSSION'):
    urlpatterns += [
        url(
            r'^courses/{}/nodebb'.format(
                settings.COURSE_ID_PATTERN,
            ),
            include('openedx.features.openedx_nodebb_discussion.urls'),
            name='nodebb_discussion_endpoints',
        ),
    ]
```

---

Add a entry point for our discussion tab in the following file
`../edx-platfrom/setup.py`

```
entry_points={
        "openedx.course_tab": [
            "openedx_nodebb_discussion = openedx.features.openedx_nodebb_discussion.plugins:NodeBBTab",
            .....
        ],
}
```

---

After that change the `version number` which is available in the same file for example if it is `0.11` change it to `0.12` and then go to `lms-shell` and your directory path should be like this

`/edx/app/edxapp/edx-platform#`


Here, run the following command 

`pip install -e .`


---

To run migrations run the following commands

```
./manage.py lms makemigrations openedx_nodebb_discussion
./mangae.py lms migrate openedx_nodebb_discussion
```

---

To enable the `NodeBB Discussion` tab in course, you add the "openedx_nodebb_discussion" key to the Advanced Module List
 on the Advanced Settings page of your course from studio.
 