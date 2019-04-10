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
        "URL": "YOUR NODEBB URL",
        "DOMAIN": "YOUR NODEBB DOMAIN",
        "TASK_RETRY_DELAY": "Secs in Integer",
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
        "NODEBB_ADMIN_UID": "<Your NodeBB Admin Uid Must be a Integer>"
    }
}
```
---

Add the following lines in `lms/env/aws.py` and `cms/env/aws.py`

```
##################### Openedx Nodebb Discussion Secrets ###########
OPENEDX_NODEBB_DISCUSSION = AUTH_TOKENS.get("OPENEDX_NODEBB_DISCUSSION", {})
NODEBB_SETTINGS = ENV_TOKENS.get("NODEBB_SETTINGS", None)
```

make sure that you put these lines after the following code portion
    
```
############################## SECURE AUTH ITEMS ###############
# Secret things: passwords, access keys, etc.

with open(CONFIG_ROOT / CONFIG_PREFIX + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

```
    

---

To add `openedx_nodebb_discussion` app into the installed apps add the 
following line in the `INSTALLED_APPS` list present in `lms/common.py` and 
`cms/common.py` file.

```
INSTALLED_APPS = [
    ...
    'openedx.features.openedx_nodebb_discussion.apps.OpenedxNodebbDiscussionConfig',
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

Go to studio using the following url `localhost:18010` 
    
   Add the following line `"openedx_nodebb_discussion"`
   in the `Advanced Module List` of the course in which you want to show `openedx_nodebb_discussion` tab.



 **Note:`Advanced Module List` is available in the `Advanced Settings` of course**