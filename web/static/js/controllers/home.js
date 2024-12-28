(function () {
    'use strict';

    angular.module('myApp').controller('HomeController', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
        const url_user_info = "api/user/info"

        $scope.userData = undefined;
        console.log('HomeController loaded');

        $http({
            method: 'GET',
            url: url_user_info,
            withCredentials: true
        }).then(function(response) {
            $scope.userData = response.data;
            switch (response.data.role) {
                case 1:
                    $scope.userType = "STUDENT"
                    break;
                case 2:
                    $scope.userType = "TEACHER"
                    break;
                default:
                    $scope.userType = "ADMIN"
                    break;
            }
        }).catch(function(error) {
            
        })
    }]);
}());