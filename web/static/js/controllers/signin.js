(function () {
    'use strict';

    angular.module('myApp').controller('SigninController', ['$scope', '$http', '$location', '$rootScope', function ($scope, $http, $location, $rootScope) {
        const url = 'api/login';
        $scope.email = "";
        $scope.password = "";
        $scope.error = undefined;
        $scope.response = '';
        
        $scope.isUndefined = function (thing) {
            return (typeof thing === "undefined");
        }

        $scope.signin = function () {
            $scope.error = undefined;
            let user = {
                email: $scope.email,
                password: $scope.password,
            }
            var errors = [];

            if (user.email == undefined || user.email == "") {
                errors.push("Email is missing/invalid!");
            }
            if (user.password == "") {
                errors.push("Password is missing!");
            }
            if (errors.length > 0) {
                $scope.error = "";
                $scope.error += errors.join(", ");
            } else {
                $http({
                    method: 'POST',
                    url: url,
                    data: user,
                    withCredentials: true // Enable sending cookies with the request
                }).then(function(response) {
                    $rootScope.isLogged = true;
                    $location.url('/')
                }).catch(function(error) {
                    $scope.error = error.data.error;
                })
            }
        };
    }]);
}());