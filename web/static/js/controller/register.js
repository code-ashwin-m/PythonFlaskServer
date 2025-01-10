(function () {
    'use strict';

    angular.module('myApp').controller('RegisterController', ['$scope', '$location', 'SharedService', function ($scope, $location, SharedService) {
        console.log('RegisterController loaded');
        $scope.isAuthenticated = SharedService.isAuthenticated();
        
        if ($scope.isAuthenticated){
            $location.url('/')
        }

    }]);

}());