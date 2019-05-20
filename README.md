# Configuring openedx_edly_discussion in your edx platform through script (short way)
Just navigate to your `lms-shell`
and run the following command in the `edx-platform` directory

```
curl https://raw.githubusercontent.com/edly-io/openedx-edly-discussion/add_configuration_scripts/scripts/integrator.sh | bash
```

After that do the following steps

---

Add `ENABLE_EDLY_DISCUSSION` flag in the `FEATURES` in the following files


- lms.env.json
- cms.env.json


and set their values to   `true`

```
FEATURES = {
    ...
    "ENABLE_EDLY_DISCUSSION": true,
}
```
---

Add the following dictionary at the end of `lms.env.json` and `cms.env.json`

```
{
    ...
    ...
    "EDLY_DISCUSSION_SETTINGS": {
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
    "EDLY_DISCUSSION_SECRETS": {
        "DISCUSSION_JWT_SECRET": "<Your secret>",
        "DISCUSSION_JWT_ALGORITHM": "<Your algorithm>",
        "API_MASTER_TOKEN": "<Your NodeBB Write Api Token>",
    }
}
```
---
After that restart `lms` and `studio`

---
To enable the `Edly Discussion` tab in course, you add the "openedx_edly_discussion" key to the Advanced Module List
 on the Advanced Settings page of your course from studio.





# Configuring openedx_edly_discusson in your edx platform manually

Clone this repo into `openedx_edly_discussion` folder using the given command

`git clone https://github.com/edly-io/openedx-edly-discussion.git openedx_edly_discussion`

---

Copy this folder and place this at the following location in edx codebase

`../edx-platform/openedx/features/`

---

Add `ENABLE_EDLY_DISCUSSION` flag in the `FEATURES` in the following files


- lms.env.json
- cms.env.json


and set their values to   `true`

```
FEATURES = {
    ...
    "ENABLE_EDLY_DISCUSSION": true,
}
```
---

Add the following dictionary at the end of `lms.env.json` and `cms.env.json`

```
{
    ...
    ...
    "EDLY_DISCUSSION_SETTINGS": {
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
    "EDLY_DISCUSSION_SECRETS": {
        "DISCUSSION_JWT_SECRET": "<Your secret>",
        "DISCUSSION_JWT_ALGORITHM": "<Your algorithm>",
        "API_MASTER_TOKEN": "<Your NodeBB Write Api Token>",
    }
}
```
---

Add the following lines at the end of the `lms/envs/aws.py` and `cms/envs/aws.py` files

```
##################### Openedx Edly Discussion Secrets ###########
EDLY_DISCUSSION_SECRETS = AUTH_TOKENS.get("EDLY_DISCUSSION_SECRETS", {})
EDLY_DISCUSSION_SETTINGS = ENV_TOKENS.get("EDLY_DISCUSSION_SETTINGS", None)
```


**Note:** If you are using edx release `ironwood` then instead of making changes in `aws.py` 
make these changes in `lms/envs/production.py` and `cms/evns/production.py` as `aws.py` file has been 
depricated in `ironwood` edx release.

---

To add `openedx_edly_discussion` app into the installed apps add the 
following line in the `INSTALLED_APPS` list present in `lms/common.py` and 
`cms/common.py` file.

```
INSTALLED_APPS = [
    ...
    'openedx.features.openedx_edly_discussion',
]
```

---

Append these urls in `lms/urls.py`

```
# Add edly discussion endpoints
if settings.FEATURES.get('ENABLE_EDLY_DISCUSSION'):
    urlpatterns += [
        url(
            r'^courses/{}/edly'.format(
                settings.COURSE_ID_PATTERN,
            ),
            include('openedx.features.openedx_edly_discussion.urls'),
            name='edly_discussion_endpoints',
        ),
    ]
```

---

Add a entry point for our discussion tab in the following file
`../edx-platfrom/setup.py`

```
entry_points={
        "openedx.course_tab": [
            "openedx_edly_discussion = openedx.features.openedx_edly_discussion.plugins:EdlyTab",
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
./manage.py lms makemigrations openedx_edly_discussion
./mangae.py lms migrate openedx_edly_discussion
```

---

After that restart your `lms` and `studio`

---

To enable the `Edly Discussion` tab in course, you add the "openedx_edly_discussion" key to the Advanced Module List
 on the Advanced Settings page of your course from studio.
