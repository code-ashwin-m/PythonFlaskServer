(function () {
    'use strict';

    angular.module('myApp').controller('LoginController', ['$scope', '$location', 'SharedService', function ($scope, $location, SharedService) {
        console.log('LoginController loaded');
        $scope.isAuthenticated = SharedService.isAuthenticated();
        
        if ($scope.isAuthenticated){
            $location.url('/')
        }
        
        $scope.login = function(){
            SharedService.setToken('abc');
            $location.url('/')
        }
    }]);

}());