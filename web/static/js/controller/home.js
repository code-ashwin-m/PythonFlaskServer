(function () {
    'use strict';

    angular.module('myApp').controller('HomeController', ['$scope', '$location', 'SharedService', function ($scope, $location, SharedService) {
        console.log('HomeController loaded');
        $scope.isAuthenticated = SharedService.isAuthenticated();
        if (!$scope.isAuthenticated){
            $location.url('/login')
        }
    }]);

}());