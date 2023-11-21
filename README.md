# Badam Messenger

![Badam Messenger Screenshot](https://github.com/clonerplus/Badam/assets/82161728/c5ce1076-b537-4b6c-b05c-049ec2c41aa6)

## Requirement Explanation

The database should have only one table called "Messages" with the following columns:

- Group ID (number)
- Order (number starting from 1 and unique for each group)
- Sender User ID (number)
- Text (string with a maximum of 3000 characters)
- Time (with millisecond precision)

### Process of inserting a new message

1. The user sends a request to the Producer component, including the group ID, their own ID, and the text.
   - The user can send a message to any group.
   - We trust that the user provides the correct ID.

2. The Producer component sends the above information to Kafka.
   - After that, it gives a confirmation response to the user.

3. Several Consumers receive messages from Kafka and for each message, after assigning appropriate order and time values, they store it in the database.
   - To calculate the order, we should not use any specific feature of the database; instead, we can only retrieve the maximum current order of messages for that group from the database.
   - To complete the above, maintaining the maximum order in memory is not necessary (it should be retrieved only once for each new message), provided that no mistakes occur.
   - To achieve the above, it is essential that messages for each group be processed by a single Consumer.

### Process of receiving the latest messages for a group

1. The user sends a request to the Gateway component, including the group ID.
   - The user can initiate the request route with django/ or flask/ or fastapi/.

2. The Gateway component forwards the request to the appropriate App component.
   - Depending on the user's request, it sends it to the relevant App.
   - Each App should have multiple containers for load balancing between them.

3. The App component retrieves the latest ten messages for that group from the database and returns them.
   - Three different implementations of the App should be done with Django, Flask, and FastAPI, each performing the same task and connecting to the same database.
   - The implementation of the Django App can be part of a Django project with a Consumer.

## Project Steps

### Step 1: Set up without replication

In this step, write the project code and run it using Docker Swarm. It is up to you whether all codes are in one project in Git or under a subgroup.

All services can be run under Docker Swarm, but if you prefer some services, such as Kafka, nginx, and the database, to be non-Dockerized, that's okay.

At this stage, one container for each of the Producer, Consumer, and App microservices is sufficient. Also, place the necessary files for running the programs on Docker Swarm in Git (in the appropriate project of your choice).

### Step 2: Set up with replication

In this stage, each of the Producer, Consumer, and App microservices should have three containers. Pay attention to the Consumer, as messages from each group should only be processed by one Consumer.

### Step 3: Load testing and optimization

Use locust to perform load testing with this scenario:

- 1000 users enter the system within 10 seconds and start making requests
- There are 1,000,000 groups
- Each user randomly selects a group and then requests recent messages from it with a 90% probability
  - (Use the remainder of the user ID divided by 3 to determine whether to send the request to the Django, Flask, or FastAPI app)
- With a 10% probability, the user sends a message containing "Hello from x," where x is the user ID.
