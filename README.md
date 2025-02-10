# DebugsprAI - The Bug Spray

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

<h2 align="center">
🌟 The Ultimate AI-Powered Debugging Assistant 🌟
</h2>

![](resources/img/debugsprai.svg)

Welcome to **debugsprAI**, where AI meets automation to revolutionize debugging! 🐞🔫

In today's fast-paced development world, AI isn't just assisting—it's solving real problems. From writing code to detecting vulnerabilities, AI is reshaping the way developers work. **DebugsprAI** takes it a step further by automatically fixing bugs directly from GitHub issues, making debugging effortless and efficient.

Imagine this: A developer opens an issue describing a bug. Instead of waiting for manual intervention, **DebugsprAI** jumps in, scans the source code, applies a fix, and submits a pull request—*automatically*.  
No delays, no bottlenecks, just seamless AI-powered debugging.

> Even better when AI is integrated into the review process in the automated manner.

## Table of Content <!-- omit header-->

- [Table of Content ](#table-of-content-)
- [Proof of Concept](#proof-of-concept)
  - [Technology Stacks](#technology-stacks)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [How to Use](#how-to-use)
  - [Subcommand `debug`](#subcommand-debug)
  - [Subcommand `parse`](#subcommand-parse)
- [🎯 Why Choose _DebugsprAI_?](#-why-choose-debugsprai)
- [🚀 Future Enhancements](#-future-enhancements)
- [🤝🏻 Contributing](#-contributing)
- [💡 Have feedback or ideas? Create an issue or reach out!](#-have-feedback-or-ideas-create-an-issue-or-reach-out)
- [🪪 License](#-license)

## Proof of Concept

DebugsprAI is a proof of concept project that demonstrates AI-powered bug fixing. It is built with Python and integrates Google's Gemini LLM, leveraging GitHub Actions to automate the debugging workflow.

The system listens for newly created GitHub issues, analyzes the reported problem, identifies the affected code, and applies intelligent fixes. Here's how it works:

1. **Issue Detection** – When a developer reports a bug on GitHub, DebugsprAI captures the issue.
2. **AI-Powered Analysis** – The AI (Gemini) interprets the issue description, locates the relevant code, and suggests potential fixes.
3. **Automated Code Modification** – Using AI-driven debugging, it adjusts the source code accordingly.
4. **Pull Request Generation** – The fixed code is committed, and a pull request is automatically created for review.
This project explores the potential of AI in software debugging, automating tedious processes to enhance development efficiency. 🔥

### Technology Stacks

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Installation

**DebugsprAI** is a proof of concept project, therefore there is no python package deployed, that can be downloaded via package manager.

In this section we will guide you through the installation process.

### Prerequisites

- Python 3.9+
- Google Gemini Access (The API Key)
  > More LLM will be supported in the future.

### Setup

```bash
# Clone the repository
git clone https://github.com/afri-bit/DebugsprAI.git

# Change directory to the project directory
cd DebugsprAI

# Install project
pip install .

# Setup API Key
export GEMINI_API_KEY=<your_api_key_here>
```

**Optional**

```bash
export GEMINI_MODEL_NAME=gemini-2.0-flash-exp
```

> You can set the model as you required, but the whole setup currently is tested under the `gemini-2.0-flash-exp` model.  
> Unpredicted behaviour may occur, if you take different model.

## How to Use

The **DebugsprAI** application relies on specific user inputs, that is constructed as people normally describe an issue in the github or another repository.  
This application is targeted to run not only for the automation, but also on your local machine. It takes a JSON file with specific format as the main input.

As the first step, let's make sure that the application is installed properly by executing following command

```bash
debugsprai --help
```

If everything is installed correctly you will see following output on your terminal

```bash
Usage: debugsprai [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  debug  _summary_
  parse  Sub command to parse issue markdown file to json format
```

### Subcommand `debug`

This subcommand is the core of the application to debug with help of LLM.

It takes a JSON file as input with following format:

```json
{
  "id": 1,
  "title": "Some Bug",
  "summary": "This bug has something to do with errors",
  "severity_level": "Low (minor issue, doesn't block usage)",
  "programming_language": "python",
  "project_folder": ".",
  "source_folder": "src",
  "test_folder": "tests",
  "system_information": "Linux",
  "actual_behavior": "Actual behaviour is not working as expected",
  "expected_behavior": "The function must be working",
  "logs": "some logs"
}
```

Based on the provided in the JSON file, the request will be sent to LLM and your files in the project will be scanned based on the `programming_language` you choose.

> Currently we only support `python` as proof of concept.

After the process is done, you can see the result under the folder `.airesults`. The LLM will only make the necesssary to the files, that may be related to the description in the issue. The changes will be marked with `AIFIX` comments.

In the folder `.airesults` you will find the folder called `project` where the folder structure will be structured exactly as in your project. The last step you have to do is just copy the whole folder into your project, and you will notice the changes.

> LLM will not change anything unless it is necessary.

### Subcommand `parse`

The command is intended as a helper function to parse a specific style of the markdown file and convert it to JSON file, that is required for `debug` command as input.

Following is the example of the markdown file, that is derived from github issue.

```markdown
### Summary

<Your Summary>

### Severity Level

<Low, Medium, High>

### Programming Language

<python>

### Project Folder

.

### Source Folder

src

### Test Folder

tests

### System Information

Linux

### Actual Behavior

<Describe the current behaviour>

### Expected Behavior

<Describe the expected behaviour>

### Logs

<Put your log information here>
```

## 🎯 Why Choose _DebugsprAI_?

✅ **Saves developer time** - No more manual debugging bottlenecks.\
✅ **Seamless GitHub integration** - Works directly with your existing workflows.\
✅ **AI-powered accuracy** - Smart debugging with minimal false positives.\
✅ **Automated PRs** - Fixes are delivered in a developer-friendly way.

## 🚀 Future Enhancements

We're continuously improving **DebugsprAI** to:

- Support multiple programming languages
- Enhance bug-fixing accuracy with fine-tuned models
- Introduce custom AI training for project-specific debugging

## 🤝🏻 Contributing

Join the revolution in AI-driven debugging! Fork the project, contribute, and help shape the future of **DebugsprAI**.

💡 Have feedback or ideas? Create an issue or reach out!
---

🔗 [GitHub Repository](https://github.com/afri-bit/DebugsprAI) | 🚀 Happy Debugging! 🐞


## 🪪 License

MIT
