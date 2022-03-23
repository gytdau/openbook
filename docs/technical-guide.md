## Introduction

The objective of this project is to provide a user-friendly platform for users to read ebooks. Currently, our application reads ebooks from the Project Gutenberg library, which provides free ebooks. The library can be accessed at https://www.gutenberg.org/

Currently, our application is deployed at https://www.libraryathena.com/. It contains around 55,000 books, with plans for more books being added in the future.

Our project consists of the following components:

- Frontend (React.js)
- Database (PostgreSQL)
- Serverless conversion functions (AWS Lambda)
- Heroku

## Design

The basis for our architecture is the microservices architecture. The frontend, database, and lambda functions are all separate services. This separation allows for better scalability and easier development, as each service can be changed and deployed independently of the others.

The front end was built using React.js. It is deployed with Heroku, which is a container-based cloud Platform as a Service (PaaS). Heroku automatically builds and deploys the frontend with each Git commit that is made to the `main` branch of our repository. The frontend runs in a web dyno, a virtual server in the Heroku ecosystem. The frontend is referred to as being deployed when a minified dockerized build is successfully running on a Heroku web dyno.

The database was also built using Heroku Postgres. It runs in a dyno and stores information about our epub files. The Postgres backend is responsible for running queries through its query service, which returns the requested information in a structured data format (JSON in our case). It can also store blobs: large objects that contain binary data such as strings, text and image data. Postgres supports the storage of large amounts of data, so it is able to handle large amounts of data without problems. However, its performance does decrease as the amount of data to be queried increases. The database has a graph function that enables us to query date information.

Docker was used to containerize our React application during development. This helped prevent issues related to missing dependencies and collisions with different versions of dependencies. It was also used to deploy our application to Heroku for testing purposes.

### Testing

Jest, a JavaScript test runner, is used for testing purposes. Tests are stored under the `src/tests/` directory. The tests validate that the components are rendered correctly.

We utilised a number of strategies to ensure that our front end remains stable. Assertions were written to check that the components rendered the data correctly and did not mutate any global state. Fixtures were used to isolate the components and mock the data being passed to them.

## Serverless conversion

As the volume of books to be processed presented numerous scaling challenges, we chose to go with a serverless approach to book conversion. The frontend runs in a single dyno, while the conversion of each book is handled by an AWS Lambda function.

### Process

Each book is converted by first fetching an epub file from Project Gutenberg. Once the epub file is downloaded, the contents are read with our custom-built python epub processor.

The epub processing pipeline was built to guarantee robustness across a wide variety of epub books. It has support for multiple chapter formats, and various nesting scenarios, even where DOM elements are nested in an invalid way. It can also extract images from the epub file and upload them separately.

An epub is actually a zip file that contains a number of other files, such as HTML files, CSS files, and image files. These files are stored in a folder structure. The first step in processing an epub is to unzip the file. The next step is to parse the contents of the `content.opf` file. This file contains metadata about the book, such as the author, title, and language. It also contains a list of the files that make up the book.

The next step is to read each of the files in the `content.opf` file. The files are read one at a time and parsed into a DOM tree. The DOM tree is then traversed to extract the text and images from the file. However, chapters may span multiple files. For this reason, we needed to keep track of the current chapter as we processed the files, merging the DOM trees as required to separate the files into their constituent chapters.

The chapter is then saved as text and stored in our database for future use. The conversion process takes approximately four minutes to complete, depending on the book size.

### AWS Lambda

The lambda functions for our project are implemented using a managed service called AWS Lambda. This service allows you to upload your own code, written in a language of your choice (in our case, python), and handle the deployment and management of that code. Lambda handles the scalability and high availability of the application automatically. In other words, the more traffic we get, the more Lambda instances will be created to handle that traffic.

Lambda currently has a limit of 1000 concurrent executions. In the case of high loads, queueing support comes out-of-the-box. However, the average response time for a Lambda function is around 200ms, which means that this is unlikely to be a problem for our application.

The memory that each lambda invocation utilizes is also worth noting. Memory is directly proportional to the performance of the function being ran, as more memory means better CPU and network performance. However, functions are also proportionally more expensive to how fast they run. In general, we found that 128MB was sufficient for our application, and that the tradeoff to memory sizes was highly proportional and not easily optimizable. Integer values from 128MB to 1536MB are available in 64MB increments.

Lambda also offers a built-in monitoring dashboard that can be used to monitor the performance and errors of your application. The dashboard displays the number of invocations, errors, duration, and throttles for each of your functions.

# Backend

The backend is a Heroku dyno that is a thin wrapper to execute queries on the database and serve data to the front end. It relays information from Amazon RDS, which uses Postgres to store our book data, and S3 for images.

The backend was built using Express.js. Express is a lightweight web application framework that provides a set of features for web and mobile applications. These features include routing, session management, and template engines. ORMs like Sequelize can also be used with Express. However, in our judgement, an ORM was too heavyweight to be necessary for our application, and we opted for interacting with Postgres directly through the `pg` module.
