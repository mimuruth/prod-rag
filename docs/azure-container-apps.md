# Azure Container Apps Overview

Azure Container Apps is a serverless platform for running containerized applications without
managing the underlying infrastructure. Instead of configuring servers, orchestrating
containers, and handling deployment details yourself, Container Apps provides the resources
that keep your applications stable, secure, and scalable, reducing operational overhead and
cost.

## Common uses

- Deploying API endpoints
- Hosting background processing jobs
- Handling event-driven processing
- Running microservices

## Autoscaling

Applications can dynamically scale based on HTTP traffic, event-driven processing, CPU or
memory load, or any KEDA-supported scaler. Most applications can scale to zero; however,
applications that scale on CPU or memory load can't scale to zero.

## Features

- Manage applications with the Azure CLI extension, Azure portal, or ARM templates.
- Enable HTTPS or TCP ingress without managing other Azure infrastructure.
- Build microservices with Dapr and access its rich set of APIs.
- Run jobs on-demand, on a schedule, or based on events.
- Run Azure Functions for event-driven scenarios.
- Run multiple container revisions and split traffic across versions for Blue/Green
  deployments and A/B testing.
- Use internal ingress and DNS-based service discovery for secure internal-only endpoints.
- Run containers from any public or private registry, including Docker Hub and Azure Container
  Registry (ACR).
- Provide an existing virtual network when creating an environment.
- Securely manage secrets directly in your application.
- Monitor logs using Azure Log Analytics.
