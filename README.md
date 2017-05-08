# CrunchRAT

### Listener Setup
1. From within the `listener` directory, run `pip3 install -r requirements`. This will install all necessary Python libraries.


### Profiles
CrunchRAT allows you to masquerade your implant's traffic via user-created JSON profiles. This functionality is largely based on Cobalt Strike's Malleable C2 functionality (https://www.cobaltstrike.com/help-malleable-c2). CrunchRAT profiles allow you to set HTTP response headers and cookies, which provides granular control over implant traffic. An example profile is included in the "listener/profiles" directory. Refer to the documentation below for an explanation of each supported JSON property:

* **user_agent**: This is the User-Agent that the implant will use for all communications.
* **sleep**: This is the default beacon interval (in seconds).
* **download_implant_to**: This is full file path where the implant will be saved to on the infected system. The infected user **MUST** have write access to this file path.
* **implant_uri**: FILL THIS OUT LATER.
* **beacon_uri**: FILL THIS OUT LATER.
* **update_uri**: FILL THIS OUT LATER.
* **redirect_url**: FILL THIS OUT LATER.
