# Manual to add openedx_nodebb_discusson in your edx platform

1.  Clone this repo into `openedx_nodebb_discussion` folder using the given command

    `git clone https://github.com/arbisoft/openedx-nodebb-discussion.git openedx_nodebb_discussion`

---

2.  Copy this folder and place this at the following location in edx codebase

    `../edx-platform/openedx/features/`

---

3.  Add `ENABLE_NODEBB_DISCUSSION` flag in the `FEATURES` in the following files


    - lms.env.json
    - cms.env.json


    and set their values to   `true`

```
    FEATURES = {
        ...
        'ENABLE_NODEBB_DISCUSSION': true,
    }
```

---

4.  To add `openedx_nodebb_discussion` app into the installed apps add the 
    following line in the `INSTALLED_APPS` list present in `lms/common.py` file.

```
    INSTALLED_APPS = [
        ...
        'openedx.features.openedx_nodebb_discussion.apps.OpenedxNodebbDiscussionConfig',
    ]
```

---

5.  Append these urls in `lms/urls.py`

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

6.  Add a entery point for our discussion tab in the following file
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

7.  After that change the `version number` which is availabe in the same file for example if it is 
    `0.11` change it to `0.12` and then go to `lms-shell` and your directory path should 
    be like this

    `/edx/app/edxapp/edx-platform#`


    Here, run the following command 

    `pip install -e .`


---

8.  Go to studio using the following url

    `localhost:18010` 

    and add the following line

    `"openedx_nodebb_discussion"`

    in the advacned module list of the course in which you want to show 
    `openedx_nodebb_discussion` tab.



 **Note:`advanced_module_list` is availabe in the `Advanced Settings` of course**