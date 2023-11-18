# Badam Messenger
<br>
<img width="782" alt="Screenshot 2023-11-19 at 12 38 58 AM" src="https://github.com/clonerplus/Badam/assets/82161728/c5ce1076-b537-4b6c-b05c-049ec2c41aa6">
<br>
**Requirement Explanation**<br>
The database should only have one table called "Messages" with the following columns:<br>
- Group ID (number)<br>
- Order (number starting from 1 and unique for each group)<br>
- Sender User ID (number)<br>
- Text (string with a maximum of 3000 characters)<br>
- Time (with millisecond precision)<br>
<br>
### Process of inserting a new message:<br>
1. The user sends a request to the Producer component, including the group ID, their own ID, and the text.<br>
&emsp;&emsp;a. The user can send a message to any group.<br>
&emsp;&emsp;b. We trust that the user provides the correct ID.<br>
<br>
2. The Producer component sends the above information to Kafka.<br>
&emsp;&emsp;a. After that, it gives a confirmation response to the user.<br>
<br>
3. Several Consumers receive messages from Kafka and for each message, after assigning appropriate order and time values, they store it in the database.<br>
&emsp;&emsp;a. To calculate the order, we should not use any specific feature of the database; instead, we can only retrieve the maximum current order of messages for that group from the database.<br>
&emsp;&emsp;b. To complete the above, maintaining the maximum order in memory is not necessary (it should be retrieved only once for each new message), provided that no mistakes occur.<br>
&emsp;&emsp;c. To achieve the above, it is essential that messages for each group be processed by a single Consumer.<br>
<br>
### Process of receiving the latest messages for a group:<br>
1. The user sends a request to the Gateway component, including the group ID.<br>
&emsp;&emsp;a. The user can initiate the request route with django/ or flask/ or fastapi/.<br><br>
2. The Gateway component forwards the request to the appropriate App component.<br>
&emsp;&emsp;a. Depending on the user's request, it sends it to the relevant App.<br>
&emsp;&emsp;b. Each App should have multiple containers for load balancing between them.<br><br>
3. The App component retrieves the latest ten messages for that group from the database and returns them.<br>
&emsp;&emsp;a. Three different implementations of the App should be done with Django, Flask, and FastAPI, each performing the same task and connecting to the same database.<br>
&emsp;&emsp;b. The implementation of the Django App can be part of a Django project with a Consumer.<br><br>

Project Steps<br>
Step 1: Set up without replication<br>
In this step, write the project code and run it using Docker Swarm. It is up to you whether all codes are in one project in Git or under a subgroup.<br>
All services can be run under Docker Swarm, but if you prefer some services, such as Kafka, nginx, and the database, to be non-Dockerized, that's okay.<br>
At this stage, one container for each of the Producer, Consumer, and App microservices is sufficient. Also, place the necessary files for running the programs on Docker Swarm in Git (in the appropriate project of your choice).<br><br>
Step 2: Set up with replication<br>
In this stage, each of the Producer, Consumer, and App microservices should have three containers. Pay attention to the Consumer, as messages from each group should only be processed by one Consumer.<br><br>
Step 3: Load testing and optimization<br>
Use locust to perform load testing with this scenario:<br>
- 1000 users enter the system within 10 seconds and start making requests<br>
- There are 1,000,000 groups<br>
- Each user randomly selects a group and then requests recent messages from it with a 90% probability<br>
(Use the remainder of the user ID divided by 3 to determine whether to send the request to the Django, Flask, or FastAPI app) and with a 10% probability sends a message containing "Hello from x," where x is the user ID.<br>
The expectation is that the request per second (RPS) and response time (p95) for all APIs are reasonable, for example, more than 100 RPS and less than 1 second response time. Try to achieve an optimal state by adjusting the database index and increasing or decreasing the number of containers.<br>
Also, place the load testing code files in Git (in the appropriate project of your choice).<br>
