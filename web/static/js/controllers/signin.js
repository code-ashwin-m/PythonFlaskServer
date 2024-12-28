(function () {
    'use strict';

    angular.module('myApp').controller('SigninController', ['$scope', '$http', function ($scope, $http) {
        $scope.email = "";
        $scope.password = "";
        $scope.error = undefined;
        $scope.response = '';

        const url = 'api/login';

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
                $http.post(url, user).then(
                    function successCallback(response) {
                        $scope.response = response.data;
                    },
                    function errorCallback(error) {
                        $scope.error = error.data.error;
                    }
                );
            }
        };
    }]);
}());