(function () {
    'use strict';

    angular.module('myApp').controller('MainController', ['$scope', '$location', 'SharedService', function ($scope, $location, SharedService) {
        console.log('MainController loaded');
        $scope.isAuthenticated = SharedService.isAuthenticated();
        
        $scope.$on('tokenUpdate', listenTokenUpdate)
        function listenTokenUpdate($event){
            $scope.isAuthenticated = SharedService.isAuthenticated();
        }

        $scope.logout = function(){
            SharedService.setToken('');
            $location.url('/login')
        }
    }]);

}());