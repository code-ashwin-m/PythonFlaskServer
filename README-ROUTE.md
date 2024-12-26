# AngularJS Single Page Application (SPA)

This project demonstrates how to create a simple **Single Page Application (SPA)** using **AngularJS** with routing capabilities. The application has three views: **Home**, **About**, and **Contact**, which are dynamically loaded without refreshing the page.

---

## Features

- **Dynamic Routing**: Navigate between pages using AngularJS routing.
- **View Management**: Each route loads its content dynamically into the main view container.
- **Active Link Highlighting**: Highlights the active route in the navigation bar.
- **Minimal JavaScript**: Clean and simple AngularJS code structure.

---

## Prerequisites

To run this project, you need:
- A web browser (preferably modern like Chrome, Edge, or Firefox).
- A basic understanding of AngularJS and HTML.

---

## How It Works

1. **AngularJS and `ngRoute` Module**:  
   - AngularJS is used as the JavaScript framework.  
   - The `ngRoute` module is used to define routes for the SPA.

2. **Dynamic Navigation**:  
   - The navigation bar is implemented using `<a>` tags with `href` attributes pointing to routes like `#!/`, `#!/about`, etc.  

3. **Routing Configuration**:  
   - `$routeProvider` maps routes to their respective templates and controllers.  
   - The `ng-view` directive dynamically loads the content for each route.

4. **View Management**:  
   - Each route is associated with a specific controller and HTML template.  
   - The content for each view is loaded without reloading the page.

---

## Application Structure

```plaintext
index.html   # The main HTML file with AngularJS code
```
### Full Code Example

```html
<!DOCTYPE html>
<html lang="en" ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AngularJS Single Page App</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular-route.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    nav {
      margin-bottom: 20px;
    }
    nav a {
      margin-right: 10px;
      text-decoration: none;
      color: blue;
    }
    nav a.active {
      font-weight: bold;
      text-decoration: underline;
    }
    .view-container {
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
  </style>
</head>
<body>

  <h1>AngularJS Single Page Application</h1>

  <!-- Navigation -->
  <nav>
    <a href="#!/" ng-class="{'active': isActive('/')}" ng-click="setActive('/')">Home</a>
    <a href="#!/about" ng-class="{'active': isActive('/about')}" ng-click="setActive('/about')">About</a>
    <a href="#!/contact" ng-class="{'active': isActive('/contact')}" ng-click="setActive('/contact')">Contact</a>
  </nav>

  <!-- View Container -->
  <div class="view-container" ng-view></div>

  <script>
    // Define the AngularJS application
    const app = angular.module('myApp', ['ngRoute']);

    // Configure routes
    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider
        .when('/', {
          template: '<h2>Home</h2><p>Welcome to the home page!</p>',
          controller: 'HomeController'
        })
        .when('/about', {
          template: '<h2>About</h2><p>This is the about page. Here you can learn more about us.</p>',
          controller: 'AboutController'
        })
        .when('/contact', {
          template: '<h2>Contact</h2><p>Contact us at: contact@example.com</p>',
          controller: 'ContactController'
        })
        .otherwise({
          redirectTo: '/'
        });
    }]);

    // Define controllers
    app.controller('MainController', ['$scope', function($scope) {
      $scope.activeRoute = '/';

      $scope.isActive = function(route) {
        return $scope.activeRoute === route;
      };

      $scope.setActive = function(route) {
        $scope.activeRoute = route;
      };
    }]);

    app.controller('HomeController', ['$scope', function($scope) {
      console.log('HomeController loaded');
    }]);

    app.controller('AboutController', ['$scope', function($scope) {
      console.log('AboutController loaded');
    }]);

    app.controller('ContactController', ['$scope', function($scope) {
      console.log('ContactController loaded');
    }]);
  </script>
</body>
</html>
```

## How to Run
	1.	Save the code as index.html.
	2.	Open the file in your web browser.
	3.	Use the navigation links to switch between Home, About, and Contact pages.
	4.	Observe the dynamic content loading without page refreshes.

