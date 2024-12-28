(function () {
    'use strict';

    angular.module('myApp').controller('MainController', ['$scope', '$http', 'TokenService', function ($scope, $http, TokenService) {
        const url = 'api/logut';
        
        $scope.isLogged = TokenService.getToken() !== undefined;
        console.log("isLogged = " + $scope.isLogged);
        $scope.logout = function () {
            $http({
                method: 'POST',
                url: url,
                withCredentials: true // Enable sending cookies with the request
            }).then(function (response) {
                $scope.response = response.data;
                $location.url('/')
            }).catch(function (error) {
                $scope.error = error.data.error;
            })
        }
    }]);
}());