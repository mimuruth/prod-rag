# Azure Functions Overview

Azure Functions is a serverless solution that allows you to build robust apps while using
less code, and with less infrastructure and lower costs. Instead of deploying and maintaining
servers, you use the cloud infrastructure to provide the resources needed to keep applications
running. You focus on the code that matters most, in the most productive language for you.

## Supported languages

Functions supports C#, Java, JavaScript, PowerShell, Python, and Go, or custom handlers for
languages like Rust.

## Hosting options

- **Flex Consumption plan** (recommended): fast event-driven scaling, virtual network
  integration, and pay-as-you-go billing.
- **Premium plan**: always-warm instances for the fastest response times, unlimited execution
  duration, and virtual network integration.
- **Dedicated plan**: run functions in an existing App Service plan with predictable scaling
  and costs.
- **Container Apps**: deploy fully customized containerized function apps alongside
  microservices in Azure Container Apps.
- **Consumption plan**: legacy serverless plan (Windows only); use the Flex Consumption plan
  for new apps.

## Triggers and scenarios

Functions provides event-driven triggers and bindings that connect functions to other services
without extra code. Common scenarios include processing file uploads from Blob Storage,
processing data in real time from event and IoT streams, running AI inference, running
scheduled tasks, building scalable web APIs with HTTP triggers, and creating reliable message
systems using Azure Queue Storage, Service Bus, or Event Hubs.

## Development lifecycle

Code locally, develop and debug with Visual Studio, VS Code, or Maven, deploy via CLI, CI/CD
pipelines, or an IDE, and monitor with built-in Azure Monitor and Application Insights.
