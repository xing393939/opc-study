### AWS Github Study Guide

#### 资料
1. [AWS SAA-C02 Study Guide](https://github.com/keenanromain/AWS-SAA-C02-Study-Guide)

#### 学习
1. Introduction
2. Identity Access Management (IAM)
  * You cannot nest IAM Groups. IAM 用户组没有层级。
3. Simple Storage Service (S3)
  * 内网ec2访问s3方法1：用NAT Gateway，$0.045/h，$0.045/GB
  * 内网ec2访问s3方法2：用Gateway Endpoint，$0.01/GB
4. CloudFront
  * An Origin Access Identity (OAI) is used for sharing private content via CloudFront
5. Snowball
  * Planes sometimes fly with snowball edges onboard so they can store large amounts of flight data
6. Storage Gateway
  * Cached Volumes differ as they do not store the entire dataset locally like Stored Volumes.
7. Elastic Compute Cloud (EC2)
  * EC2 Not billed if preparing to stop. Billed if preparing to hibernate
8. Elastic Block Store (EBS)
  * The easiest way to move an EC2 instance and a volume to another availability zone is to take a snapshot.
9. Elastic Network Interfaces (ENI)
  * You can attach the ENI to a hot standby instance.
10. Security Groups
  * Security Groups are regional and can span AZs
11. Web Application Firewall (WAF)
  * WAF can either allow the request by serving the requested content or return an HTTP 403 Forbidden status.
12. CloudWatch
  * CloudWatch Alarms Actions can be an Amazon EC2 action, Auto Scaling action, or SNS.
13. CloudTrail
  * By default, CloudTrail Events log files are encrypted using Amazon S3 SSE.
14. Elastic File System (EFS)
  * EFS using the NFSv4 protocol. This makes it required to open up the NFS port for our security group.
15. Amazon FSx for Windows
  * You can use Microsoft Active Directory to authenticate into the file system.
16. Amazon FSx for Lustre
  * FSx Lustre has the ability to store and retrieve data directly on S3 on its own.
17. Relational Database Service (RDS)
  * RDS is not serverless. There is Aurora serverless however which serves a niche purpose.
  * A SQS queue however ensures that writes to the DB do not become lost.
  * Multi-AZ creates a primary DB instance and synchronously replicates the data to a standby instance in a different AZ.
  * Multi-AZ is supported for all DB flavors, Aurora is completely fault-tolerant on its own.
  * Multi-AZ RDS configuration, backups are taken from the standby.
  * If the master DB were to fail, there is no automatic failover. You can manually promote read replicas to be the master.
  * IAM database authentication works with MySQL and PostgreSQL.
  * You can only enable encryption for an Amazon RDS DB instance when you create it. Encrypted instance can't be modified to disable encryption.
18. Aurora
  * Aurora serverless uses for this service are infrequent, intermittent, and unpredictable workloads.
19. DynamoDB
  * DAX does more than just increase read performance by having write through cache. This improves write performance as well.
  * Global Table failover is as simple as redirecting your application’s DynamoDB calls to another AWS region.
  * Replication latency with Global Tables is typically under one second.
20. Redshift
21. ElasticCache
22. Route53
23. Elastic Load Balances (ELB)
24. Auto Scaling
25. Virtual Private Cloud (VPC)
26. Simple Queuing Service (SQS)
27. Simple Workflow Service (SWF)
28. Simple Notification Service (SNS)
29. Kinesis
30. Lambda
31. API Gateway
32. CloudFormation
33. ElasticBeanstalk
34. AWS Organizations
35. Miscellaneous
