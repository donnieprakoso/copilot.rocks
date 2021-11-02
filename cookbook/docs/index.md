# Welcome to Copilot.rocks  
  
Building and deploying with container is a solution to the problem of how to get our apps to run reliably in any computing environments — from your laptop to production. Container simplifies the development workflow.   
  
While packaging our app into a container image is relatively easy, it’s not the case when we need to deploy and operate our apps in any computing environment.   
  
Deployment and operating our apps is a different story. It requires us to understand how to use container orchestrator and also what the best practices are. This introduces high learning curve, only to ship our applications.   
  
We need a tool that can help us to build, deploy and operate our applications easily , and that’s AWS Copilot.  
  
## What is AWS Copilot?  
  
As quoted from the official [documentation page][1], “The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications on AWS App Runner, Amazon ECS, and AWS Fargate.”  
  
## How to use this site?  
  
This site is a collection of documented learning from building, deploying and operating applications using AWS Copilot.   
  
The content on this site is structured as a set of (mini) workshop and arranged in a modular manner, so you can move from chapter to chapter easily. You can run the workshop in whichever order you want, depending on your current need.  
  
## What’s the easiest way to install Copilot?  
  
The easiest way to install AWS Copilot is using [Homebrew][2]. With Homebrew, you can easily install AWS Copilot by running below command:  
  
```bash  
brew install aws/tap/copilot-cli  
```  
  
If you need to upgrade Copilot, you can use following command:  
  
```bash  
brew upgrade aws/tap/copilot-cli  
```  
  
And to uninstall Copilot, you can run:  
  
```bash  
brew uninstall aws/tap/copilot-cli  
```  
  
It’s much easier to use Homebrew to manage Copilot package. If you can’t use Homebrew, you can perform manual installation by following the instructions on [github.com/aws/copilot-cli][3].  
  
## Let’s get started  
  
If you’re new to AWS Copilot and containers on AWS, you can visit Getting Started, to get a quick overview.  
  
  
[1]: https://aws.github.io/copilot-cli/  
[2]: https://brew.sh/  
[3]: https://github.com/aws/copilot-cli  
