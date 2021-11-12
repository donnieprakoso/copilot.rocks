# How to install AWS Copilot CLI?

## Situation

“I want to get started with AWS Copilot. What’s the best way to install it?”

## Solution

The easiest way to install AWS Copilot is using [Homebrew][1]. With Homebrew, you can easily install AWS Copilot by running below command:

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

It’s much easier to use Homebrew to manage Copilot package. If you can’t use Homebrew, you can perform manual installation by following the instructions on [github.com/aws/copilot-cli][2].

[1]: https://brew.sh/
[2]: https://github.com/aws/copilot-cli
