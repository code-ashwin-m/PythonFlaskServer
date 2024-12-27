Here’s the response converted into GitHub README.md syntax:

# AngularJS Forms with GET and POST Requests

This project demonstrates how to create two forms using AngularJS:  
- **GET Request Form**: Sends a `GET` request to fetch data.  
- **POST Request Form**: Sends a `POST` request to submit data.

---

## Features

- **GET Request Form**:  
  Sends a `GET` request to a public API and fetches data based on user input.  

- **POST Request Form**:  
  Sends a `POST` request to a public API and submits data entered by the user.

- **Response Display**:  
  Displays the server response in a user-friendly format.

---

## Prerequisites

- Basic understanding of HTML, CSS, and AngularJS.
- AngularJS library is required (CDN included in the example).

---

## Code Example

### HTML Code

```html
<!DOCTYPE html>
<html lang="en" ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AngularJS GET and POST Forms</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    form {
      margin-bottom: 20px;
      padding: 15px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    label {
      display: block;
      margin-bottom: 5px;
    }
    input, button {
      margin-bottom: 10px;
    }
    .response {
      margin-top: 20px;
      padding: 10px;
      border: 1px solid #ccc;
      background-color: #f9f9f9;
      border-radius: 5px;
    }
  </style>
</head>
<body ng-controller="FormController">

  <h1>AngularJS GET and POST Forms</h1>

  <!-- GET Request Form -->
  <form ng-submit="submitGetRequest()">
    <h3>GET Request Form</h3>
    <label for="getParam">Enter a parameter:</label>
    <input type="text" id="getParam" ng-model="getParam" placeholder="Enter value" required />
    <button type="submit">Send GET Request</button>
  </form>

  <!-- POST Request Form -->
  <form ng-submit="submitPostRequest()">
    <h3>POST Request Form</h3>
    <label for="postParam">Enter a parameter:</label>
    <input type="text" id="postParam" ng-model="postParam" placeholder="Enter value" required />
    <button type="submit">Send POST Request</button>
  </form>

  <!-- Response Display -->
  <div class="response">
    <h3>Response</h3>
    <pre>{{ response }}</pre>
  </div>

  <script>
    // Define the AngularJS app
    const app = angular.module('myApp', []);

    app.controller('FormController', ['$scope', '$http', function($scope, $http) {
      $scope.getParam = '';
      $scope.postParam = '';
      $scope.response = '';

      // Function to handle GET request
      $scope.submitGetRequest = function() {
        const url = `https://jsonplaceholder.typicode.com/posts/${$scope.getParam}`;
        $http.get(url).then(
          function successCallback(response) {
            $scope.response = response.data;
          },
          function errorCallback(error) {
            $scope.response = 'Error: ' + error.statusText;
          }
        );
      };

      // Function to handle POST request
      $scope.submitPostRequest = function() {
        const url = 'https://jsonplaceholder.typicode.com/posts';
        const data = { param: $scope.postParam };
        $http.post(url, data).then(
          function successCallback(response) {
            $scope.response = response.data;
          },
          function errorCallback(error) {
            $scope.response = 'Error: ' + error.statusText;
          }
        );
      };
    }]);
  </script>
</body>
</html>
```

### How It Works
- GET Request Form:
	•	Accepts a parameter (getParam) from the user.
	•	Sends a GET request to https://jsonplaceholder.typicode.com/posts/{id}.
	•	Displays the response in the “Response” section.
- POST Request Form:
	•	Accepts a parameter (postParam) from the user.
	•	Sends a POST request to https://jsonplaceholder.typicode.com/posts with the entered data.
	•	Displays the response in the “Response” section.
- Response Handling:
	•	Uses AngularJS $http service to handle requests and responses.
	•	Responses are dynamically displayed on the page.

### How to Run
	1.	Save the above code to a file named index.html.
	2.	Open the file in any modern browser.
	3.	Test the GET Request Form by entering a number (e.g., 1) and submitting.
The response will display the data from the JSONPlaceholder API.
	4.	Test the POST Request Form by entering any text and submitting.
The response will display the data sent to the API.

### Example Usage

### GET Request Example:
	•	Input: 1
	•	Response:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit..."
}
```


### POST Request Example:
	•	Input: Hello World
	•	Response:
```json
{
  "param": "Hello World",
  "id": 101
}
```
