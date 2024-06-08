# CRTO Lab Status

 Posts the latest status of CRTO labs, `running`/`stopped` and remaining `hours` in Discord. 

 ![image](https://github.com/Anon-Exploiter/CRTO-Lab-Status/assets/18597330/b7abd1f9-4daf-4547-be98-a07bbc5fbc62)


### Why?

Due to the lab's limited hours, leaving it running by mistake may exhaust all available time.
https://training.zeropointsecurity.co.uk/courses/red-team-ops#:~:text=Managing%20your%20runtime 

The script should help by notifying the person every 10 minutes about their lab status. 

### Features

Currently, it only contains the following: 
- Fetching the status of labs: `running`/`stopped`
- Fetching the total number of `hours` remaining 
- Posting all that stuff in a `Discord channel` through Webhooks

### How it works?

Trying to login on **snaplabs** through simple requests module was a pain as its using cognito which implements authentication in a shitty way. Easy way to automate was to use selenium and so I did just that. 

The script utilizes `Selenium` with `Chrome (headless)` to first login into the application, opens the course, reads the `status` about the lab if its running or stopped, reads the total `hours remaining` in the lab and posts it all in the specified Discord Channel through Webhooks. 

### How to use?

You can declare the environmental variables in the `config.sh` file, `source` it, and execute the script. 

```bash
source config.sh
python crto.py
```

### How to run this automatically? 

If you haven't noticed, there's Github Actions configured for the project, just fork this repo, create the environmental variables within project settings and the cron should run every 10 minutes posting the output within Discord.

Here's how to configure the environmental variables: 

![image](https://github.com/Anon-Exploiter/CRTO-Lab-Status/assets/18597330/6bc965ec-4010-4bd5-97f6-7bc0dcad07aa)


