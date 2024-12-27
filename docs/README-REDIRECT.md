```html
<!DOCTYPE html>
<html lang="en" ng-app="myApp">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AngularJS Redirect with Parameters</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular-route.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    nav a {
      margin-right: 10px;
      text-decoration: none;
      color: blue;
    }
  </style>
</head>
<body>

  <h1>AngularJS Redirect with Parameters</h1>

  <div ng-controller="MainController">
    <button ng-click="redirectToPage('about', { id: 123, name: 'John' })">Go to About Page</button>
  </div>

  <div ng-view></div>

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
          template: '<h2>About</h2><p>About Page</p><p>ID: {{ id }}</p><p>Name: {{ name }}</p>',
          controller: 'AboutController'
        })
        .otherwise({
          redirectTo: '/'
        });
    }]);

    // Main Controller
    app.controller('MainController', ['$scope', '$location', function($scope, $location) {
      $scope.redirectToPage = function(route, params) {
        const queryString = Object.keys(params)
          .map(key => `${key}=${encodeURIComponent(params[key])}`)
          .join('&');
        $location.url(`/${route}?${queryString}`);
      };
    }]);

    // About Controller
    app.controller('AboutController', ['$scope', '$location', function($scope, $location) {
      const params = $location.search();
      $scope.id = params.id;
      $scope.name = params.name;
    }]);

    // Home Controller (optional)
    app.controller('HomeController', ['$scope', function($scope) {
      console.log('HomeController loaded');
    }]);
  </script>
</body>
</html>
```
