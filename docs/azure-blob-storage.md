# Introduction to Azure Blob Storage

Azure Blob Storage is Microsoft's object storage solution for the cloud. Blob Storage is
optimized for storing massive amounts of unstructured data — data that doesn't adhere to a
particular data model or definition, such as text or binary data.

## What Blob Storage is designed for

- Serving images or documents directly to a browser
- Storing files for distributed access
- Streaming video and audio
- Writing to log files
- Storing data for backup and restore, disaster recovery, and archiving
- Storing data for analysis by an on-premises or Azure-hosted service

Clients can access objects over HTTP or HTTPS from anywhere via the Azure Storage REST API,
Azure PowerShell, Azure CLI, or client libraries (.NET, Java, Node.js, Python, Go). Clients can
also connect using SFTP and mount containers using the NFS 3.0 protocol.

## Resources

Blob Storage offers three types of resources: the **storage account**, a **container** in the
account, and a **blob** in a container.

- A **storage account** provides a unique namespace in Azure for your data. For an account
  named `mystorageaccount`, the default Blob Storage endpoint is
  `http://mystorageaccount.blob.core.windows.net`.
- A **container** organizes a set of blobs, similar to a directory. Container names must be a
  valid DNS name, between 3 and 63 characters, start with a letter or number, and contain only
  lowercase letters, numbers, and the dash character.
- A **blob** stores the data itself.

## Blob types

- **Block blobs** store text and binary data, made up of individually managed blocks, and can
  store up to about 190.7 TiB.
- **Append blobs** are optimized for append operations, ideal for scenarios such as logging.
- **Page blobs** store random access files up to 8 TiB and serve as disks for Azure virtual
  machines.
