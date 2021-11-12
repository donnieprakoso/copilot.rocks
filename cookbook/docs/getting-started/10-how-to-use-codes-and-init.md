# How to use the codes and initialize the Copilot app?

## Situation

I want to run the workshops. How do I get started?

## Solution

Each of the workshop requires you to initialize a Copilot application. To do this, you need to clone the Github repo and initialize the application using `copilot init` command.

The path for the source code and Copilot app name will be provided in each workshop.

## Step-by-step Guide

All source code in this website is located at `codes/` folder which you can find it at the root of the repo. Please refer to the workshop instruction to know which source code path you need to work on.

### Clone Github Repo

To clone the Github repo and get the source code, follow the instructions below:

- Open terminal
- If you’re using SSH, do a Git clone by running this command:

```bash
git clone git@github.com:donnieprakoso/copilot.rocks.git
```

- If you’re using HTTPS, Git clone by running following command:

```bash
git clone https://github.com/donnieprakoso/copilot.rocks.git
```

- Navigate to the `source/` folder and you will find all source code for each workshop

### Initialize Copilot application

All workshops require you to initialize Copilot application. In this example, you will initialize the `hello-copilot/` application

- Open terminal
- Navigate to `codes/hello-copilot/`
- Run `copilot init <WORKSHOP_APP_NAME>` command

You will have similar output as below:

```
✔ Created the infrastructure to manage services and jobs under application hello-copilot..
✔ The directory copilot will hold service manifests for application hello-copilot.
Recommended follow-up action:
    Run `copilot init` to add a new service or job to your application.
```

## Conclusion

While you can use the guided instructions provided by Copilot, most of the workshops require you to define them manually. For an example, with `copilot init` — without the application name — Copilot will guide you to create a new application, define the service name and providing you an option to deploy to specific environment.

It’s advised to follow the manual approach so you have a better understanding on how to define each component with Copilot.
