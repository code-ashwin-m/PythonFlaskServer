(function (){
    'use strict';
    const app = angular.module('myApp', [
        'ngRoute'
    ]);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/home.html',
                controller: 'HomeController'
            })
            .when('/login', {
                templateUrl: 'views/login.html',
                controller: 'LoginController'
            })
            .when('/register', {
                templateUrl: 'views/register.html',
                controller: 'RegisterController'
            })
            .otherwise({
                redirectTo: '/'
            });
    }]);
}());