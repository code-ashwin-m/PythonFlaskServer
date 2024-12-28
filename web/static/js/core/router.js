(function (){
    'use strict';
    
    angular.module('myApp').config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/home.html',
                controller: 'HomeController'
            })
            .when('/register', {
                templateUrl: 'views/signup.html',
                controller: 'SignupController'
            })
            .otherwise({
                redirectTo: '/'
            });
    }]);
}());