# How to install AWS Copilot CLI?

## Situation

I want to get started with AWS Copilot. What’s the best way to install it?

## Solution

The easiest way to install AWS Copilot is using [Homebrew][1]. With Homebrew, you can easily install AWS Copilot if you’re running on Mac or Linux. To install the Copilot CLI, follow below instructions:

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

If you’re running on Windows, you need to manually install the CLI. Run the following commands in your terminal to install the Copilot CLI:

```
Invoke-WebRequest -OutFile 'C:\Program Files\copilot.exe' https://github.com/aws/copilot-cli/releases/latest/download/copilot-windows.exe
```

## Conclusion

It’s much easier to use Homebrew to manage Copilot package. If you can’t use Homebrew, you can perform manual installation by following the instructions on [github.com/aws/copilot-cli][2].

[1]: https://brew.sh/
[2]: https://github.com/aws/copilot-cli
