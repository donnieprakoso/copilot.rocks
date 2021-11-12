# How to deploy a HTTP API app?

## Situation

I want to create a HTTP based application. I need the application to be publicly accessible. How can I do that with Copilot?

## Solution

Copilot provides you two approaches on building HTTP based applications, using "Request-Driven Web Service” or “Load Balanced Web Service”. This page describes how you can use “Load Balanced Web Service”.

With “Load Balanced Web Service”, you will have Application Load Balancer running as an ingress, and integrated with ECS service running on Fargate.

In this tutorial, you’ll deploy a simple publicly accessible “Hello, World” HTTP app.

## Tutorial Dependencies

This tutorial requires you to complete following workshops:

[How to use the codes and initialize the Copilot app?][1]

## Step-by-step Guide

### Step 1: Source Code and App Initialization

We will use `hello-copilot/` in `codes/` folder for this app.

Once you have the source code, navigate to the `hello-copilot/` folder and initialize the application with “hello-copilot” as the application name.

Please refer to this tutorial — [How to use the codes and initialize the Copilot app?][2]

### Step 2: Code Review

The `hello-copilot/` application is written in Python using Flask framework. You will find the structure as below:

```
hello-copilot/
├── app.py
├── Dockerfile
├── index.html
└── requirements.txt
```

### Step 3: Create Environment

- Open terminal
- Navigate to `hello-copilot/` folder
- Create environment

The first thing we need to create is an environment. To create the environment, run the following command:

```bash
copilot env init --name testing --profile default --default-config
```

This command will create an environment called `testing` with your AWS `default` profile and using `default-config`. The `default-config` flag will create a VPC with two public and two private subnets.

### Step 4: Create service

- Open terminal
- Create the service

In this step you need to create a service with “Load Balanced Web Service” type.

```bash
copilot svc init --name web --dockerfile ./Dockerfile --svc-type “Load Balanced Web Service”
```

This command will create a service called `web` and using the `Dockerfile` resides in the root of `hello-copilot/` folder.

Once the operation is finished, Copilot will create a manifest file with this path `copilot/web/manifest.yml`. This manifest file describes the `web` service as infrastructure-as-code.

### Step 5: Deploy!

To deploy the service into the environment, run the following command:

```bash
copilot svc deploy --name web --env testing
```

This command will deploy the newly initialized `web` service into `testing` environment.

### Step 6: Checking app status

## Conclusion

For “Load Balanced Web Service”, Copilot will provision Application Load Balancer which is running on Layer-7. If your use cases require to run a load balancer on Layer-4, you need to provision Network Load Balancer. At the time of the writing, Copilot doesn’t have this feature. Please refer to this [Github issue][3].

[1]: /getting-started/10-how-to-use-codes-and-init/
[2]: /getting-started/10-how-to-use-codes-and-init/
[3]: https://github.com/aws/copilot-cli/issues/2918
