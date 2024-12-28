(function () {
    'use strict';

    angular.module('myApp').controller('MainController', ['$scope', '$http', '$location', '$rootScope', 'SharedService', function ($scope, $http, $location, $rootScope, SharedService) {
        const url = 'api/logut';
        console.log('MainController loaded');
        $rootScope.isLogged = SharedService.getToken() !== undefined;
        $scope.userInfo = undefined;

        if (!$rootScope.isLogged){
            $location.url('/login')
        }
        $scope.logout = function () {
            $http({
                method: 'POST',
                url: url,
                withCredentials: true // Enable sending cookies with the request
            }).then(function (response) {
                $scope.response = response.data;
                $rootScope.isLogged = false;
                $location.url('/login')
            }).catch(function (error) {
                $scope.error = error.data
            })
        }
    }]);
}());