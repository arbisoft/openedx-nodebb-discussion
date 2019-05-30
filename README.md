# openedx-edly-discussion

It's an open source Django plugin available for Open edX to use NodeBB discussion forum as its own discussion app. This plugin works along with NodeBB plugin i.e. nodebb-plugin-openedx-discussion.

## Features

* Provides a fully functional embed view of NodeBB as course discussions in edX.  
* Synchronization of Open edX with NodeBB to keep the discussion experience seamless. 
  *  Whenever a new user is created in edX application, the same user is also created in NodeBB application and the same goes for the courses i.e. whenever a new course is created, a corresponding category is created in NodeBB application to contain all of the course discussions in one place.
  * It also provide a Django management command to sync existing users and courses of edX with NodeBB.
* Session sharing is handled using JWT authentication.
* User privileges are managed using NodeBB groups.
  *  Course related discussions are only accessible to the enrolled users of the course.

 
## Prerequisites
  * Open edX (hawthorn or later) instance. ([Installation link](https://github.com/edx/devstack))
  * NodeBB (v1.10.x or above) instance. ([Installation link](https://docs.nodebb.org/installing/os/ubuntu/))


## Getting started

### Devstack Setup
You can either use `opendx-devstack` and apply all configurations yourself or you can simple use the pre-configured `openedx-nodebb-devstack`.

  **Using openedx-devstack**
  * Configure your fresh edX devstack instance using [configure edX repo](https://github.com/edly-io/openedx-edly-discussion/wiki/Configure-edX-repo) of openedx_edly_discussion wiki.
  * Generate a master token for API access of NodeBB using this [link](https://github.com/edly-io/openhttps://github.com/edly-io/openedx-edly-discussion/wiki/Configure-openedx_edly_discussionedx-edly-discussion/wiki/Generating-Master-Token).
  * Follow the [Installation guide steps](https://github.com/edly-io/nodebb-plugin-openedx-discussion/blob/master/README.md) of `nodebb-plugin-openedx-discussion` to integrate `nodebb-plugin-openedx-discussion` plugin in your NodeBB instance.

 **Using openedx-nodebb-devstack**
 * Just follow this [link](https://github.com/edly-io/openedx-nodebb-devstack/wiki/Setup-Guide) and you are  done.

### Sync already created users and courses of edX with NodeBB 
Run following shell commands from devstack directory.
```sh
$ make lms-shell
$ ./manage.py lms sync_course_enrollments_with_nodebb
$ exit

$ docker-compose restart lms
```


## Enable Discussion in a Course:
  - Open your desired course from studio
  - Go to the Advance Settings from Settings tab of the Course
  - Add `"openedx_edly_discussion"` to the Advance module list and save it.


## Documentation

[openedx-edly-discussion wiki](https://github.com/edly-io/openedx-edly-discussion/wiki) is the full reference for openedx-edly-discussion plugin, and includes guides for developers.

## Compatibility

openedx-edly-discussion supports:

* Open edX (hawthorn or later)
* NodeBB (v1.10.x or above)
* nodebb-plugin-openedx-discussion (v0.1.0 or newer)
---


## How To Contribute

To contribute, please make a pull request in this repositry on Github: [openedx-edly-discussion](https://github.com/edly-io/openedx-edly-discussion). If you have any question or issue, please feel free to open an issue.


## Contributors

* [Muhammad Zeeshan](https://github.com/zee-pk)
* [Osama Arshad](https://github.com/asamolion)
* [Danial Malik](https://github.com/danialmalik)
* [Hamza Farooq](https://github.com/HamzaIbnFarooq)
* [Muhammad Umar Khan](https://github.com/mumarkhan999)
* [Tehreem Sadat](https://github.com/tehreem-sadat)
* [Hassan Tariq](https://github.com/imhassantariq)
