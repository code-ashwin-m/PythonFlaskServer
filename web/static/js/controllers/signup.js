(function () {
    'use strict';

    angular.module('myApp').controller('SignupController', ['$scope', '$http', function ($scope, $http) {
        $scope.name = "";
        $scope.email = "";
        $scope.password = "";
        $scope.student = true;
        $scope.error = undefined;
        $scope.response = '';

        const url = 'api/signup';


        $scope.isUndefined = function (thing) {
            return (typeof thing === "undefined");
        }

        $scope.register = function () {
            $scope.error = undefined;
            let user = {
                name: $scope.name,
                email: $scope.email,
                password: $scope.password,
                student: $scope.student
            }
            console.log(user)
            var errors = [];
            if (user.name == "") {
                errors.push("Name is missing!");
            }
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