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
            $rootScope.$broadcast('userDataAdded', $scope.userData);
        }).catch(function(error) {
            
        })
    }]);
}());