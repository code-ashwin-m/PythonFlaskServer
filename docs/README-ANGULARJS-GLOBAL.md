In AngularJS, sharing a global variable across controllers can be achieved by using a service, factory, or value. Here’s an example using a service, which is a common approach:

Example: Sharing a Global Variable Across Controllers

1. Define the AngularJS App and Service

var app = angular.module('myApp', []);

// Service to store the global variable
app.service('SharedService', function () {
    this.sharedData = {
        value: 'Hello, World!' // Initial value of the global variable
    };
});

2. Define Two Controllers to Access the Shared Variable

// First controller to read and modify the shared variable
app.controller('FirstController', ['$scope', 'SharedService', function ($scope, SharedService) {
    $scope.sharedData = SharedService.sharedData; // Bind to the shared data

    $scope.updateValue = function (newValue) {
        SharedService.sharedData.value = newValue; // Update the shared variable
    };
}]);

// Second controller to access the same shared variable
app.controller('SecondController', ['$scope', 'SharedService', function ($scope, SharedService) {
    $scope.sharedData = SharedService.sharedData; // Bind to the shared data
}]);

3. Define the HTML to Display and Update the Shared Variable

<!DOCTYPE html>
<html ng-app="myApp">
<head>
    <title>AngularJS Shared Variable Example</title>
</head>
<body>
    <div ng-controller="FirstController">
        <h2>First Controller</h2>
        <p>Shared Value: {{ sharedData.value }}</p>
        <input type="text" ng-model="newValue" placeholder="Enter new value">
        <button ng-click="updateValue(newValue)">Update Value</button>
    </div>

    <div ng-controller="SecondController">
        <h2>Second Controller</h2>
        <p>Shared Value: {{ sharedData.value }}</p>
    </div>

    <!-- Include AngularJS -->
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js"></script>
    <!-- Include your app script -->
    <script src="app.js"></script>
</body>
</html>

Explanation:
	1.	SharedService:
	•	Acts as a single source of truth for the shared variable (sharedData).
	•	Any changes made to sharedData in one controller are automatically reflected in the other controller due to AngularJS’s two-way data binding.
	2.	Controllers:
	•	Both controllers inject SharedService to access the shared variable.
	•	They bind SharedService.sharedData to their $scope to enable two-way data binding in the view.
	3.	HTML:
	•	Displays the shared variable’s value and provides an input for updating it.

This approach ensures that the shared data is consistent and synchronized across controllers.
